import torch
import torch.nn as nn
import numpy as np

class SEBlock(nn.Module):
    def __init__(self, channel, reduction=16):
        super(SEBlock, self).__init__()
        self.avg_pool = nn.AdaptiveAvgPool2d(1)
        self.fc = nn.Sequential(
            nn.Linear(channel, channel // reduction, bias=False),
            nn.ReLU(inplace=True),
            nn.Linear(channel // reduction, channel, bias=False),
            nn.Sigmoid()
        )

    def forward(self, x):
        b, c, _, _ = x.size()
        y = self.avg_pool(x).view(b, c)
        y = self.fc(y).view(b, c, 1, 1)
        return x * y.expand_as(x)

class SpatialAttention(nn.Module):
    def __init__(self, kernel_size=7):
        super(SpatialAttentionBlock, self).__init__()
        self.conv1 = nn.Conv2d(2, 1, kernel_size=kernel_size, padding=kernel_size // 2, bias=False)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        # Compute the spatial attention scores
        avg_out = torch.mean(x, dim=1, keepdim=True)  # Shape: [batch_size, 1, height, width]
        max_out, _ = torch.max(x, dim=1, keepdim=True)  # Shape: [batch_size, 1, height, width]
        x = torch.cat([avg_out, max_out], dim=1)  # Shape: [batch_size, 2, height, width]
        x = self.conv1(x)  # Shape should remain: [batch_size, 1, height, width]
        return self.sigmoid(x)  # Applying sigmoid to scale values between 0 and 1

class ChannelAttention(nn.Module):
    def __init__(self, num_channels, reduction_ratio=16):
        super(ChannelAttention, self).__init__()
        self.avg_pool = nn.AdaptiveAvgPool2d(1)  # Global Average Pooling
        self.fc = nn.Sequential(
            nn.Linear(num_channels, num_channels // reduction_ratio, bias=False),
            nn.ReLU(inplace=True),
            nn.Linear(num_channels // reduction_ratio, num_channels, bias=False),
            nn.Sigmoid()
        )

    def forward(self, x):
        b, c, _, _ = x.size()
        y = self.avg_pool(x).view(b, c)
        y = self.fc(y).view(b, c, 1, 1)
        return x * y.expand_as(x)


class SpatialAttentionBlock(nn.Module):
    def __init__(self, kernel_size=7):
        super(SpatialAttentionBlock, self).__init__()
        assert kernel_size in (3, 7), 'kernel size must be 3 or 7'
        padding = 3 if kernel_size == 7 else 1
        self.conv1 = nn.Conv2d(2, 1, kernel_size, padding=padding, bias=False)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        avg_out = torch.mean(x, dim=1, keepdim=True)
        max_out, _ = torch.max(x, dim=1, keepdim=True)
        x = torch.cat([avg_out, max_out], dim=1)
        x = self.conv1(x)
        return x * self.sigmoid(x)



class ResBlock(nn.Module):
    def __init__(self, in_channels, out_channels, stride=1, kernel_size=3, dropout_rate=0.1):
        super(ResBlock, self).__init__()
        #self.se = SEBlock(out_channels)
        self.conv1 = nn.Conv2d(in_channels, out_channels, kernel_size=kernel_size, stride=stride, padding=kernel_size//2, bias=False)
        self.bn1 = nn.BatchNorm2d(out_channels)
        self.relu = nn.ReLU(inplace=True)
        self.dropout = nn.Dropout(dropout_rate)
        self.conv2 = nn.Conv2d(out_channels, out_channels, kernel_size=kernel_size, stride=1, padding=kernel_size//2, bias=False)
        self.bn2 = nn.BatchNorm2d(out_channels)
        self.spatial_attention = SpatialAttentionBlock()  # Add spatial attention block
        self.channel_attention = ChannelAttention(self.channel_list[0]) 
        if self.channel_list[0] != self.channel_list[1] or stride != 1:
            self.downsample = nn.Sequential(
                nn.Conv2d(self.channel_list[0], self.channel_list[1], kernel_size=1, stride=stride, bias=False),
                nn.BatchNorm2d(self.channel_list[0])
            )
        else:
            self.downsample = None

    def forward(self, x):
        identity = x
        out = self.conv1(x)
        out = self.bn1(out)
        out = self.relu(out)
        out = self.dropout(out)
        out = self.conv2(out)
        out = self.bn2(out)
        out = self.channel_attention(out)  # Apply SEBlock after the last BN
        # Apply spatial attention
        attention = self.spatial_attention(out)  # Generate attention map
        out = out * attention  # Apply attention map
        
        
        if self.downsample is not None:
            identity = self.downsample(x)

        out += identity
        out = self.relu(out)
        return out

class Neural_receiver(nn.Module):
    def __init__(self, subcarriers, timesymbols, streams, num_bits_per_symbol, num_blocks, base_channels, scene, dropout_rate=0.1):
        super(Neural_receiver, self).__init__()
        self.subcarriers = subcarriers
        self.timesymbols = timesymbols
        self.streams = streams
        self.num_blocks = num_blocks
        self.base_channels = base_channels
        self.num_bits_per_symbol = num_bits_per_symbol

        if scene == 'scene1':
            self.register_buffer('W', torch.full((1, 1, timesymbols, subcarriers, 2), np.sqrt(0.9)))
            self.register_buffer('V', torch.full((1, 1, timesymbols, subcarriers, 2), np.sqrt(0.1)))
        elif scene == 'scene2':
            self.register_buffer('W', torch.full((1, 1, timesymbols, subcarriers, 2), np.sqrt(0.6)))  # 修改数据权重以反映幅度比
            self.register_buffer('V', torch.zeros((1, 1, timesymbols, subcarriers, 2)))  # 初始化导频权重为0
            specific_t_V = {1: [0, 4, 8], 2: [1, 5, 9], 3: [2, 6, 10], 4: [3, 7, 11]}
            # 更新导频权重以反映根据功率比调整后的幅度比
            for l in range(streams):
                for t in specific_t_V[l + 1]:
                    self.V[0, 0, t, :, :] = np.sqrt(1.6)  # 使用功率比的平方根作为幅度比

        self.init_conv = nn.Conv2d(4 * self.streams, self.base_channels, kernel_size=3, padding=1)

        self.blocks = nn.Sequential()
        for block_id in range(self.num_blocks):
            in_channels = self.base_channels if block_id == 0 else layer_channels
            layer_channels = self.base_channels + (block_id // 10) * 32
            self.blocks.add_module(
                name=f'resblock_{block_id}',
                module=ResBlock(in_channels, layer_channels, dropout_rate=dropout_rate)
            )

        final_channels = self.base_channels + ((self.num_blocks - 1) // 10) * 32
        self.final_conv = nn.Conv2d(final_channels, streams * num_bits_per_symbol, kernel_size=3, padding=1)

    def forward(self, y, template_pilot):        
        y = y.float()
        template_pilot=template_pilot.float()
        # 假设 rx_signal 是您从文件加载的接收信号张量
        '''
        mean_real = torch.mean(y[..., 0], dim=(0, 1, 2), keepdim=True)
        std_real = torch.std(y[..., 0], dim=(0, 1, 2), keepdim=True)
        mean_imag = torch.mean(y[..., 1], dim=(0, 1, 2), keepdim=True)
        std_imag = torch.std(y[..., 1], dim=(0, 1, 2), keepdim=True)

        # 标准化
        y[..., 0] = (y[..., 0] - mean_real) / (std_real + 1e-6)
        y[..., 1] = (y[..., 1] - mean_imag) / (std_imag + 1e-6)
    '''

        #y = self.data_norm(y)  # Apply normalization
        y_weighted = y * self.W
        pilot_weighted = template_pilot * self.V
        
        batch_size = y.shape[0]
        y = y_weighted.permute(0, 2, 3, 1, 4)
        y = torch.reshape(y, (batch_size, self.timesymbols, self.subcarriers, self.streams * 2))
        template_pilot = pilot_weighted.permute(0, 2, 3,1, 4)
        template_pilot = torch.reshape(template_pilot, (batch_size, self.timesymbols, self.subcarriers, self.streams * 2))

        z = torch.cat([y, template_pilot], dim=-1)
        z = z.permute(0, 3, 1, 2)
        z = self.init_conv(z)
        z = self.blocks(z)
        z = self.final_conv(z)
        z = z.permute(0, 2, 3, 1)
        z = torch.reshape(z, (batch_size, self.timesymbols, self.subcarriers, self.streams, self.num_bits_per_symbol))
        z = z.permute(0, 3, 1, 2, 4)
        return z
