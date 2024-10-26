import torch
import torch.nn as nn
import numpy as np
import math
from einops import rearrange, repeat
from einops.layers.torch import Rearrange
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class PatchEmbedding(nn.Module):
    def __init__(self, num_patches, patch_dim, emb_size):
        super(PatchEmbedding, self).__init__()
        self.num_patches = num_patches
        self.patch_dim = patch_dim
        self.emb_size = emb_size        
        # 线性层用于patch维度到嵌入维度的转换
        self.linear_proj = nn.Linear(patch_dim, emb_size)        
        # 位置编码
        self.pos_embedding = nn.Parameter(torch.randn(1, num_patches + 1, emb_size))

    def forward(self, x):
        # x: [batch_size, num_antennas, time_symbols, subcarriers, real_imag]
        # 重塑和切分patch
        # 假设x的形状为 [batch_size, 4, 12, 96, 4]
        batch_size = x.shape[0]
        x = x.reshape(batch_size, 4, 12, 96 // 8, 8 * 4)  # 重新组织成patches        
        # 将4个接收天线的数据合并起来，视具体情况可能需要调整
        x = x.reshape(batch_size, 4 * 12 * 12, 32)  # 四个接收天线，每个天线12个时间符号，每个时间符号12个patch
        # 应用线性投影
        x = self.linear_proj(x)  # [batch_size, num_patches, emb_size]
        
        # 添加克隆的位置编码
        x = x + self.pos_embedding[:, :self.num_patches, :]  # 从位置编码中切割出所需的部分
        return x
        
class TransformerEncoderLayer(nn.Module):
    def __init__(self, emb_size, num_heads, ffn_hidden, dropout_rate):
        super().__init__()
        self.attention = nn.MultiheadAttention(emb_size, num_heads, dropout=dropout_rate)
        self.norm1 = nn.LayerNorm(emb_size)
        self.dropout1 = nn.Dropout(dropout_rate)
        self.ffn = nn.Sequential(
            nn.Linear(emb_size, ffn_hidden),
            nn.GELU(),
            nn.Dropout(dropout_rate),
            nn.Linear(ffn_hidden, emb_size),
        )
        self.norm2 = nn.LayerNorm(emb_size)
        self.dropout2 = nn.Dropout(dropout_rate)

    def forward(self, src):
        # Multi-head attention
        src2 = self.norm1(src)
        attn_output, _ = self.attention(src2, src2, src2)
        src = src + self.dropout1(attn_output)
        # Feed-forward network
        src2 = self.norm2(src)
        ffn_output = self.ffn(src2)
        src = src + self.dropout2(ffn_output)
        return src

class Neural_receiver(nn.Module):
    def __init__(self, num_layers, hidden_dim, num_heads, ffn_hidden, num_symbols, subcarriers, streams, num_bits_per_symbol, dropout_rate):
        super().__init__()
        self.streams = streams
        self.num_bits_per_symbol = num_bits_per_symbol
        self.num_symbols = num_symbols
        self.subcarriers = subcarriers
        self.num_patches = 4 * 12 * 12  # 四个接收天线，每个天线12个时间符号，每个时间符号12个patch
        self.patch_dim = 32  # 每个patch包含32个数据点
        self.emb_size = hidden_dim  # 嵌入空间的维度            
        self.patch_embedding = PatchEmbedding(self.num_patches, self.patch_dim, self.emb_size)
        self.ffn_hidden=2048
        self.transformer_layers = nn.ModuleList([
            TransformerEncoderLayer(hidden_dim, num_heads, self.ffn_hidden, dropout_rate) for _ in range(num_layers)
        ])
        self.layer_norm = nn.LayerNorm(hidden_dim)
        self.head = nn.Linear(hidden_dim, 4*6*2)

    def forward(self, y, template_pilot):
        batch_size = y.shape[0]   
        y = torch.cat([y, template_pilot], dim=-1)  # Concatenating pilot signals to the input               
        y = self.patch_embedding(y)  # Apply patch embedding
        # Apply transformer layers
        y = y.permute(1, 0, 2)  # Transformer expects (seq_len, batch_size, embedding_dim)
        for layer in self.transformer_layers:
            y = layer(y)
        y = y.permute(1, 0, 2)  # Convert back to (batch_size, seq_len, embedding_dim)
        # Apply final normalization and classification head
        y = self.layer_norm(y)  # Mean pooling
        y = self.head(y)
        y = y.view(batch_size, self.streams, self.num_symbols, self.subcarriers, self.num_bits_per_symbol)
        return y
