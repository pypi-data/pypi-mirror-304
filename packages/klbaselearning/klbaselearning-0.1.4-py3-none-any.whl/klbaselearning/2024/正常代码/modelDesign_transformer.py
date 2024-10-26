#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import torch
import torch.nn as nn
from torch.nn import TransformerEncoder, TransformerEncoderLayer

class PositionalEncoding(nn.Module):
    def __init__(self, d_model, dropout=0.1, max_len=500):
        super(PositionalEncoding, self).__init__()
        self.dropout = nn.Dropout(p=dropout)

        position = torch.arange(max_len).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2) * -(math.log(10000.0) / d_model))
        pe = torch.zeros(max_len, 1, d_model)
        pe[:, 0, 0::2] = torch.sin(position * div_term)
        pe[:, 0, 1::2] = torch.cos(position * div_term)
        self.register_buffer('pe', pe)

    def forward(self, x):
        x = x + self.pe[:x.size(0)]
        return self.dropout(x)

class NeuralReceiver(nn.Module):
    def __init__(self, subcarriers, timesymbols, streams, num_bits_per_symbol, num_blocks, base_channels, nhead, nhid, nlayers, dropout=0.5):
        super(NeuralReceiver, self).__init__()
        self.model_type = 'Transformer'
        self.src_mask = None
        self.pos_encoder = PositionalEncoding(nhid, dropout)
        encoder_layers = TransformerEncoderLayer(nhid, nhead, nhid, dropout)
        self.transformer_encoder = TransformerEncoder(encoder_layers, nlayers)
        self.encoder = nn.Linear(subcarriers * streams * 2, nhid)
        self.decoder = nn.Linear(nhid, subcarriers * streams * num_bits_per_symbol)
        self.init_conv = nn.Conv2d(4 * streams, base_channels, kernel_size=3, padding=1)
        self.final_conv = nn.Conv2d(base_channels, streams * num_bits_per_symbol, kernel_size=3, padding=1)
        self.nhid = nhid
        self.num_blocks = num_blocks

    def forward(self, y, template_pilot):
        batch_size = y.shape[0]
        y = y.permute(0, 2, 3, 1, 4).reshape(batch_size, self.timesymbols, self.subcarriers, self.streams * 2)
        template_pilot = template_pilot.permute(0, 2, 3, 1, 4).reshape(batch_size, self.timesymbols, self.subcarriers, self.streams * 2)
        src = torch.cat([y, template_pilot], dim=-1).permute(0, 3, 1, 2).reshape(batch_size, -1, self.nhid)
        src = self.encoder(src)
        src = self.pos_encoder(src)
        output = self.transformer_encoder(src, self.src_mask)
        output = self.decoder(output)
        output = output.view(batch_size, self.timesymbols, self.subcarriers, self.streams, self.num_bits_per_symbol)
        return output.permute(0, 3, 1, 2, 4)

# 实例化模型
model = NeuralReceiver(subcarriers=624, timesymbols=12, streams=2, num_bits_per_symbol=4, num_blocks=6, base_channels=64, nhead=8, nhid=200, nlayers=3, dropout=0.5)

