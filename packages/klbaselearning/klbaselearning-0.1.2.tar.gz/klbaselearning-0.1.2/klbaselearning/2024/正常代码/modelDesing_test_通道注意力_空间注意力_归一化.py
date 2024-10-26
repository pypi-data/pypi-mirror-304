import torch
import torch.nn as nn

class ChannelAttention(nn.Module):
    def __init__(self, num_channels):
        super(ChannelAttention, self).__init__()
        self.gap = nn.AdaptiveAvgPool2d(1)  # 全局平均池化，减少空间维度
        self.gmp = nn.AdaptiveMaxPool2d(1)  # 全局最大池化
        # 使用两个不同的池化层可以捕获不同的特征

        # 用一个较简单的方式来实现通道缩放，避免复杂的变换，以确保不会引入额外的错误
        self.fc = nn.Sequential(
            nn.Conv2d(num_channels, num_channels // 16, 1, bias=False),  # 降维
            nn.ReLU(),
            nn.Conv2d(num_channels // 16, num_channels, 1, bias=False),  # 升维
        )
        self.sigmoid = nn.Sigmoid()  # 使用Sigmoid来确保输出权重在0到1之间

    def forward(self, x):
        avg_out = self.gap(x)  # 应用全局平均池化
        max_out = self.gmp(x)  # 应用全局最大池化
        out = self.fc(avg_out) + self.fc(max_out)  # 对两种池化结果应用相同的变换并相加
        return x * self.sigmoid(out)  # 应用Sigmoid激活并与原始输入相乘进行缩放

class SpatialAttention(nn.Module):
    def __init__(self, kernel_size=7):
        super(SpatialAttention, self).__init__()
        self.conv1 = nn.Conv2d(2, 1, kernel_size, padding=(kernel_size - 1) // 2, bias=False)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        avg_out = torch.mean(x, dim=1, keepdim=True)  # 对每个通道计算平均值
        max_out, _ = torch.max(x, dim=1, keepdim=True)  # 对每个通道计算最大值
        combined = torch.cat([avg_out, max_out], dim=1)  # 将平均值和最大值在通道维度合并
        attention = self.conv1(combined)  # 通过卷积层生成空间注意力图
        attention = self.sigmoid(attention)  # 使用Sigmoid函数激活
        # 使用广播机制将注意力图扩展到所有通道
        return x * attention.expand_as(x)

        
class ResBlock(nn.Module):
    def __init__(self, in_channels, out_channels, stride=1, kernel_size=3, dropout_rate=0.3):
        super(ResBlock, self).__init__()
        self.conv1 = nn.Conv2d(in_channels, out_channels, kernel_size=kernel_size, stride=stride, padding=kernel_size//2, bias=False)
        self.bn1 = nn.BatchNorm2d(out_channels)
        self.relu = nn.ReLU(inplace=True)
        self.dropout = nn.Dropout(dropout_rate)
        self.conv2 = nn.Conv2d(out_channels, out_channels, kernel_size=kernel_size, stride=1, padding=kernel_size//2, bias=False)
        self.bn2 = nn.BatchNorm2d(out_channels)

        if in_channels != out_channels or stride != 1:
            self.downsample = nn.Sequential(
                nn.Conv2d(in_channels, out_channels, kernel_size=1, stride=stride, bias=False),
                nn.BatchNorm2d(out_channels)
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
        if self.downsample is not None:
            identity = self.downsample(x)
        out += identity
        out = self.relu(out)
        return out

class SignalNormalization(nn.Module):
    def __init__(self):
        super(SignalNormalization, self).__init__()

    def forward(self, x):
        # Batch normalization across the complex signal (real and imaginary separately)
        real, imag = x[..., 0], x[..., 1]
        # Standardize each independently
        real = (real - real.mean()) / (real.std() + 1e-8)
        imag = (imag - imag.mean()) / (imag.std() + 1e-8)
        # Combine and return
        return torch.stack((real, imag), -1)

class Neural_receiver(nn.Module):
    def __init__(self, subcarriers, timesymbols, streams, num_bits_per_symbol, num_blocks, base_channels, scene, dropout_rate=0.3):
        super(Neural_receiver, self).__init__()
        self.subcarriers = subcarriers
        self.timesymbols = timesymbols
        self.streams = streams
        self.num_blocks = num_blocks
        self.base_channels = base_channels
        self.num_bits_per_symbol = num_bits_per_symbol

        # Initialize the normalization layer
        self.normalization = SignalNormalization()

        # Initialize attention layers
        self.channel_attention = ChannelAttention(num_channels=base_channels)
        self.spatial_attention = SpatialAttention(kernel_size=7)

        # Scene-dependent weights initialization
        if scene == 'scene1':
            self.register_buffer('W', torch.full((1, 1, timesymbols, subcarriers, 2), 0.9))
            self.register_buffer('V', torch.full((1, 1, timesymbols, subcarriers, 2), 0.1))
        elif scene == 'scene2':
            self.register_buffer('W', torch.full((1, 1, timesymbols, subcarriers, 2), 0.6))
            self.register_buffer('V', torch.zeros((1, 1, timesymbols, subcarriers, 2)))

        # Initial convolution
        self.init_conv = nn.Conv2d(4 * self.streams, self.base_channels, kernel_size=3, padding=1)

        # Residual blocks
        self.blocks = nn.Sequential()
        for block_id in range(self.num_blocks):
            in_channels = self.base_channels if block_id == 0 else layer_channels
            layer_channels = self.base_channels + (block_id // 10) * 32
            self.blocks.add_module(
                name=f'resblock_{block_id}',
                module=ResBlock(in_channels, layer_channels, dropout_rate=dropout_rate)
            )

        # Final convolution
        final_channels = self.base_channels + ((self.num_blocks - 1) // 10) * 32
        self.final_conv = nn.Conv2d(final_channels, streams * num_bits_per_symbol, kernel_size=3, padding=1)


    def forward(self, y, template_pilot):
        # Apply normalization
        y = self.normalization(y)
        template_pilot = self.normalization(template_pilot)

        # Apply scene-dependent weights
        y_weighted = y * self.W
        pilot_weighted = template_pilot * self.V

        # Reshape and concatenate
        batch_size = y.shape[0]
        y = y_weighted.permute(0, 2, 3, 1, 4).reshape(batch_size, self.timesymbols, self.subcarriers, self.streams * 2)
        template_pilot = pilot_weighted.permute(0, 2, 3, 1, 4).reshape(batch_size, self.timesymbols, self.subcarriers, self.streams * 2)
        z = torch.cat([y, template_pilot], dim=-1).permute(0, 3, 1, 2)
        # Process through the network
        z = self.init_conv(z)
        #print("After init_conv:", z.shape)  # Debugging: Print shape after initial convolution
        z = self.channel_attention(z)  # Apply channel attention after initial convolution
        #print("After channel_attention:", z.shape) 
        z = self.blocks(z)
        #print("After blocks:", z.shape)
        z = self.spatial_attention(z)  # Apply spatial attention after residual blocks
        z = self.final_conv(z)
       # print("After final_conv:", z.shape)
        z = z.permute(0, 2, 3, 1).reshape(batch_size, self.timesymbols, self.subcarriers, self.streams, self.num_bits_per_symbol)
        return z.permute(0, 3, 1, 2, 4)