import torch
import torch.nn as nn
import numpy as np
import math
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
        self.pos_embedding = nn.Parameter(torch.randn(1, num_patches, emb_size))
    def forward(self, x):
        # x: [batch_size, num_antennas, time_symbols, subcarriers, real_imag]
        # 重塑和切分patch
        # 假设x的形状为 [batch_size, 4, 12, 96, 2]
        batch_size = x.shape[0]
        x = x.reshape(batch_size, 4, 12, 96//6, 6*6)  # 重新组织成patches  
        # 将4个接收天线的数据合并起来，视具体情况可能需要调整
        x = x.reshape(batch_size, 4 * 12 * 16, 36)  # 四个接收天线，每个天线12个时间符号，每组时间符号6个patch，每个patch有32个数据点（2个时间符号*4个子载波*实部虚部）
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
        self.num_patches = 4 * 12 * 16  # 四个接收天线，每个天线12个时间符号，每个时间符号12个patch
        self.patch_dim = 36 # 每个patch包含16个数据点
        self.emb_size = hidden_dim  # 嵌入空间的维度            
        self.patch_embedding = PatchEmbedding(self.num_patches, self.patch_dim, self.emb_size)
        self.ffn_hidden=ffn_hidden
        self.transformer_layers = nn.ModuleList([
            TransformerEncoderLayer(hidden_dim, num_heads, self.ffn_hidden, dropout_rate) for _ in range(num_layers)
        ])
        self.layer_norm = nn.LayerNorm(hidden_dim)
        self.head = nn.Sequential(
            #nn.Linear(hidden_dim,hidden_dim*2),
           # nn.ReLU(),
           # nn.Linear(hidden_dim*2,hidden_dim),
          #  nn.ReLU(),
            nn.Linear(hidden_dim,6*6)
        )

    def forward(self, y, template_pilot):
        batch_size = y.shape[0]   
        # 导频与数据的功率比信息
        # 更新功率比字典，为每层定义具体的功率比
        def MMSE_channel_estimation(rx_signal, pilot, pilot_positions, noise_variance, power_ratio):
            """
            :param rx_signal: 接收信号张量
            :param pilot: 导频张量
            :param pilot_positions: 导频位置数组
            :param noise_variance: 噪声方差
            :param power_ratio: 导频与数据功率比
            :return: 估计的信道张量
            """
            # 获取张量的形状
            num_samples, num_antennas, num_symbols, num_subcarriers, _ = rx_signal.size()
        
            # 初始化估计的信道张量
            estimated_channel = torch.zeros(num_samples, num_antennas, num_symbols, num_subcarriers, 2)
        
            # 计算每个导频的功率比
            pilot_power = power_ratio / (power_ratio + 1)
            data_power = 1 / (power_ratio + 1)
        
            # 对每一层每个导频位置进行信道估计
            for layer in range(len(pilot_positions)):  # 确保循环通过所有层
                for symbol in pilot_positions[layer]:
                    # 应用MMSE估计
                    for subcarrier in range(num_subcarriers):
                        # 对每个样本和每个接收天线
                        H_hat = (rx_signal[:, :, symbol, subcarrier, :] * pilot_power) / \
                                (pilot_power * pilot_power + noise_variance)
                        estimated_channel[:, :, symbol, subcarrier, :] = H_hat
            
            return estimated_channel
        
        # 定义导频位置和功率比
        pilot_positions = [[0, 4, 8], [1, 5, 9], [2, 6, 10], [3, 7, 11]]
        power_ratio = 1.6 / 0.6  # 导频与数据的功率比
        noise_variance = 0.0316  # 假设噪声方差，需要根据实际情况调整 10DB 0.1 ; 15DB 0.0316; 20DB 0.01; 25DB 0.00316; 30DB:0.001 ; 5DB 0.3162
      #  y = y.to(device)
       # template_pilot = template_pilot.to(device)

        # 执行信道估计
        estimated_channel = MMSE_channel_estimation(y, template_pilot, pilot_positions, noise_variance, power_ratio)
        
        # 现在可以使用estimated_channel进行后续处理
        estimated_channel = estimated_channel.to(device)
        
        y = torch.cat([y,template_pilot,estimated_channel], dim=-1)  # Concatenating pilot signals to the input #template_pilot           
              
        # y = torch.cat([y,noise], dim=-1)  # Concatenating pilot signals to the input               
        y = self.patch_embedding(y)  # Apply patch embedding
        # Apply transformer layers
        y = y.permute(1, 0, 2)  # Transformer expects (seq_len, batch_size, embedding_dim)
        for layer in self.transformer_layers:
            y = layer(y)
        y = y.permute(1, 0, 2)  # Convert back to (batch_size, seq_len, embedding_dim)
        # Apply final normalization and classification head
        #y=self.layer_norm(y)
       # y = self.layer_norm(y)  # 在最后的输出前使用层归一化               
        y = self.head(y)
        y = y.view(batch_size, self.streams, self.num_symbols, self.subcarriers, self.num_bits_per_symbol)
        return y
