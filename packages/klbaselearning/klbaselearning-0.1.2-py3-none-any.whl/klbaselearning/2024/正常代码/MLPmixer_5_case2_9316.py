import torch
import torch.nn as nn
from functools import partial
import numpy as np
from functools import partial
import math

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
class DropPath(nn.Module):
    """Drop paths (Stochastic Depth) per sample."""
    def __init__(self, drop_prob=None):
        super().__init__()
        self.drop_prob = drop_prob

    def forward(self, x):
        return drop_path(x, self.drop_prob, self.training)

def drop_path(x, drop_prob: float = 0., training: bool = False):
    """Drop paths (Stochastic Depth) per sample (when applied in main path of residual blocks)."""
    if drop_prob == 0. or not training:
        return x
    keep_prob = 1 - drop_prob
    # work with diff dim tensors, not just 2D ConvNets
    shape = (x.shape[0],) + (1,) * (x.ndim - 1)
    random_tensor = keep_prob + torch.rand(shape, dtype=x.dtype, device=x.device)
    random_tensor.floor_()  # binarize
    output = x.div(keep_prob) * random_tensor
    return output

class MLPMixerLayer(nn.Module):
    def __init__(self, num_patches, hidden_dim, tokens_mlp_dim, channels_mlp_dim,dropout_rate=0,drop_path_rate=0.25):
        super().__init__()
        self.norm1 = nn.LayerNorm(hidden_dim)
        self.token_mixing = nn.Sequential(
            nn.Linear(num_patches, tokens_mlp_dim),
            nn.GELU(),
            nn.Dropout(dropout_rate),  # Add dropout here
            nn.Linear(tokens_mlp_dim, num_patches),
        )

        self.norm2 = nn.LayerNorm(hidden_dim)
        self.channel_mixing = nn.Sequential(
            nn.Linear(hidden_dim, channels_mlp_dim),
            nn.GELU(),
            nn.Dropout(dropout_rate),  # Add dropout here
            nn.Linear(channels_mlp_dim, hidden_dim),
        )

        self.drop_path = DropPath(drop_path_rate) if drop_path_rate > 0 else nn.Identity()

    def forward(self, x):
        # Apply LayerNorm before token mixing
        y = self.norm1(x)
        # Token mixing (patch mixing)
        y = y.permute(0, 2, 1)  # Swap the 'hidden_dim' and 'num_patches' dimensions
        y = self.token_mixing(y)
        y = y.permute(0, 2, 1)  # Swap back after token mixing
        x = x + self.drop_path(y)  # DropPath 应用于残差连接
        # Apply LayerNorm before channel mixing      
        y = self.norm2(x)
        # Channel mixing
        y = self.channel_mixing(y)
        x = x + self.drop_path(y)  # 再次应用
        return x


        
class Neural_receiver(nn.Module):
    def __init__(self, num_patches, num_layers, hidden_dim, tokens_mlp_dim, channels_mlp_dim, num_symbols, subcarriers, streams, num_bits_per_symbol,dropout_rate=0):
        super().__init__()
        self.streams = streams
        self.num_bits_per_symbol = num_bits_per_symbol
        self.num_symbols = num_symbols
        self.subcarriers = subcarriers
        self.num_patches = num_symbols * subcarriers
        self.patch_embedding = nn.Sequential(
            nn.Linear(streams * 6, hidden_dim),
            nn.Dropout(0)  # Add dropout here
        )
        self.mixer_layers = nn.ModuleList([
            MLPMixerLayer(num_patches, hidden_dim, tokens_mlp_dim, channels_mlp_dim) for _ in range(num_layers)
        ])
        self.layer_norm = nn.LayerNorm(hidden_dim)
        self.head = nn.Sequential(
            nn.Dropout(0),  # Add dropout here before the final linear layer
            nn.Linear(hidden_dim, streams * num_bits_per_symbol)
        )

    def forward(self, y, template_pilot):
        batch_size = y.shape[0]
        samples = y.shape[0]
        ###########################STD标准化#############################
        #y_mean = y.mean(dim=(0, 2, 3), keepdim=True)  # 对样本、符号和子载波的维度求均值
        #y_std = y.std(dim=(0, 2, 3), keepdim=True)    # 对样本、符号和子载波的维度求标准差
        #y_normalized = (y - y_mean) / (y_std + 1e-6)  # 防止除以零
        # 标准化导频 P
        #P_mean = template_pilot.mean(dim=(0, 2, 3), keepdim=True)  # 对符号和子载波的维度求均值
        #P_std = template_pilot.std(dim=(0, 2, 3), keepdim=True)    # 对符号和子载波的维度求标准差
        #P_normalized = (template_pilot - P_mean) / (P_std + 1e-6)  # 防止除以零
        ###########################除以最大值标准化#############################
       # y_max_abs = y.abs().max(dim=0, keepdim=True)[0].max(dim=1, keepdim=True)[0].max(dim=1, keepdim=True)[0]  # Fix applied here
       # y_normalized = y / (y_max_abs + 1e-6)  # 避免除以零
       # p_max_abs = template_pilot.abs().max(dim=0, keepdim=True)[0].max(dim=1, keepdim=True)[0].max(dim=1, keepdim=True)[0]  # Fix applied here
      #  p_normalized = template_pilot / (p_max_abs + 1e-6)  # 避免除以零
        ###############################功率归一化#############################
        # 假定 y 是你的信号张量，形状为 [20000, 4, 12, 96, 2]
        #y_complex = torch.view_as_complex(y)  # 将最后一个维度转换为复数
        #signal_power = torch.mean(torch.abs(y_complex)**2, dim=[1, 2, 3], keepdim=True)  # 计算每个样本的功率        
        #target_power = 1.0  # 假定你希望每个样本的平均功率是 1
        #normalization_factor = torch.sqrt(signal_power / target_power)  # 计算归一化因子
        #y_normalized = y_complex / normalization_factor  # 应用归一化
        #y_normalized = torch.view_as_real(y_normalized)  # 如果需要，转换回实部和虚部表示

        # 假定 P_expanded 是扩展后的导频信号，形状为 [20000, 4, 12, 96, 2]
        #P_expanded_complex = torch.view_as_complex(template_pilot)  # 转换为复数形式
        # 计算每个样本的导频功率
       #P_expanded_power = torch.mean(torch.abs(P_expanded_complex)**2, dim=(1, 2, 3), keepdim=True)  # 对所有维度求平均功率，除了批次维度        
        # 计算归一化因子
        #normalization_factor = torch.sqrt(P_expanded_power / target_power)       
        # 应用功率归一化
        #P_expanded_normalized_complex = P_expanded_complex / normalization_factor  # 应用归一化       
        # 转换回实部和虚部表示
       # P_expanded_normalized = torch.view_as_real(P_expanded_normalized_complex)
        # 先计算每个样本的均值，并进行中心化
        # 假定 rx_signal 是你的接收信号张量，形状为 [20000, 4, 12, 96, 2]
        # 假定 pilot 是你的导频信号张量，形状为 [20000, 4, 12, 96, 2]
        # 将最后一个维度（实部和虚部）转换为复数

 ##########################################功率归一化2###########################################      
        # 设置目标功率
        #target_power = 1.0  # 例如，我们将目标功率设置为1        
        # 假定 rx_signal 和 pilot 是你的接收信号和导频信号张量，形状为 [20000, 4, 12, 96, 2]        
        # 将最后一个维度（实部和虚部）转换为复数
        #rx_signal_complex = torch.view_as_complex(y)
        #pilot_complex = torch.view_as_complex(template_pilot)      
        # 对接收信号进行中心化
        #rx_signal_mean = torch.mean(rx_signal_complex, dim=[1, 2, 3], keepdim=True)
        #rx_signal_centered = rx_signal_complex - rx_signal_mean       
        # 对导频信号进行中心化
        #pilot_mean = torch.mean(pilot_complex, dim=[1, 2, 3], keepdim=True)
        #pilot_centered = pilot_complex - pilot_mean        
        # 计算接收信号的归一化因子，并应用归一化
        #rx_signal_power = torch.mean(torch.abs(rx_signal_centered)**2, dim=[1, 2, 3], keepdim=True)
        #normalization_factor_rx = torch.sqrt(rx_signal_power / target_power)  # 注意这里的除法，我们将信号功率除以目标功率
        #rx_signal_normalized = rx_signal_centered / (normalization_factor_rx + 1e-6)  # 防止除以零
        #rx_signal_normalized = torch.view_as_real(rx_signal_normalized)  # 转换回实部和虚部表示      
        # 计算导频信号的归一化因子，并应用归一化
        #pilot_power = torch.mean(torch.abs(pilot_centered)**2, dim=[1, 2, 3], keepdim=True)
        #normalization_factor_pilot = torch.sqrt(pilot_power / target_power)  # 同样将信号功率除以目标功率
        #pilot_normalized = pilot_centered / (normalization_factor_pilot + 1e-6)  # 防止除以零
        #pilot_normalized = torch.view_as_real(pilot_normalized)  # 转换回实部和虚部表示
        # 对y进行归一化处理

 ##########################################功率归一化3###########################################      
        
        # 假定 rx_signal 和 pilot 是你的接收信号和导频信号张量，形状为 [batch_size, channels, height, width, 2]
        
        # 将最后一个维度（实部和虚部）转换为复数
        rx_signal_complex = torch.view_as_complex(y)
        pilot_complex = torch.view_as_complex(template_pilot)
        
        # 计算整个批次的平均功率
        rx_signal_power = torch.mean(torch.abs(rx_signal_complex) ** 2)
        pilot_power = torch.mean(torch.abs(pilot_complex) ** 2)
        
        # 设置目标功率
        target_power = 1.0  # 例如，我们将目标功率设置为1
        
        # 计算归一化因子
        normalization_factor_rx = torch.sqrt(rx_signal_power / target_power)
        normalization_factor_pilot = torch.sqrt(pilot_power / target_power)
        
        # 应用功率归一化
        rx_signal_normalized_complex = rx_signal_complex / (normalization_factor_rx + 1e-6)  # 防止除以零
        pilot_normalized_complex = pilot_complex / (normalization_factor_pilot + 1e-6)  # 防止除以零
        
        # 转换回实部和虚部表示
        rx_signal_normalized = torch.view_as_real(rx_signal_normalized_complex)
        pilot_normalized = torch.view_as_real(pilot_normalized_complex)
                     
        
       # y_max_abs = y.abs().max()  # 获取y中所有元素的最大绝对值
        #y_normalized = y / (y_max_abs + 1e-6)  # 对整个批次的数据进行归一化
        
        # 对template_pilot进行归一化处理
        #p_max_abs = template_pilot.abs().max()  # 获取template_pilot中所有元素的最大绝对值
        #p_normalized = template_pilot / (p_max_abs + 1e-6)  # 对整个批次的数据进行归一化
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
        noise_variance = 0.1  # 假设噪声方差，需要根据实际情况调整
        y = y.to(device)
        template_pilot = template_pilot.to(device)

        # 执行信道估计
        estimated_channel = MMSE_channel_estimation(y, template_pilot, pilot_positions, noise_variance, power_ratio)
        
        # 现在可以使用estimated_channel进行后续处理
        estimated_channel = estimated_channel.to(device)

        
        y = torch.cat([y,template_pilot,estimated_channel], dim=-1)  # Concatenating pilot signals to the input #template_pilot     
        y = y.view(batch_size, self.num_patches, -1)  # Reshaping into patches
        y = self.patch_embedding(y)  # Apply patch embedding
        # Apply mixer layers
        for layer in self.mixer_layers:
            y = layer(y)
        # Apply final normalization and classification head
        y = self.layer_norm(y)
        y = self.head(y)
        y = y.view(batch_size,  self.streams, self.num_symbols,self.subcarriers ,self.num_bits_per_symbol)
        return y
