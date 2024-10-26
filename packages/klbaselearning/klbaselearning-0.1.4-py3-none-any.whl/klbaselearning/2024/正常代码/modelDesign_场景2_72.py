import torch
import torch.nn as nn

class ResBlock(nn.Module):
    def __init__(self, channel_list, H, W):
        super(ResBlock, self).__init__()
        # Adjust channel numbers based on input
        self.channel_list = [max(ch, 128) for ch in channel_list]  # Increase to at least 128
        self._conv_1 = nn.Conv2d(self.channel_list[2], self.channel_list[0], kernel_size=3, padding=1)
        self._bn_1 = nn.BatchNorm2d(self.channel_list[0])
        self._conv_2 = nn.Conv2d(self.channel_list[0], self.channel_list[1], kernel_size=3, padding=1)
        self._bn_2 = nn.BatchNorm2d(self.channel_list[1])
        self._relu = nn.ReLU()
        self._dropout = nn.Dropout(0.2)  # Adjusted Dropout rate

    def forward(self, inputs):
        x_ini = inputs
        x = self._bn_1(self._conv_1(x_ini))
        x = self._relu(x)
        x = self._dropout(x)
        x = self._bn_2(self._conv_2(x))
        x = self._relu(x)
        x = self._dropout(x)
        x_ini = x_ini + x
        return x_ini

class Neural_receiver(nn.Module):
    def __init__(self, subcarriers, timesymbols, streams, num_bits_per_symbol, num_blocks=15, channel_list=[128, 128, 128]):
        super(Neural_receiver, self).__init__()
        self.subcarriers = subcarriers
        self.timesymbols = timesymbols
        self.streams = streams
        # Adjust the number of blocks and channels based on the scenario
        self.num_blocks = num_blocks + (4 - streams) * 5  # Increase blocks for more complex scenarios
        self.channel_list = [ch + (subcarriers // 24) * 16 for ch in channel_list]  # Adjust channels based on subcarriers
        self.num_bits_per_symbol = num_bits_per_symbol

        self.blocks = nn.Sequential()
        for block_id in range(self.num_blocks):
            block = ResBlock(channel_list=self.channel_list, H=self.timesymbols, W=self.subcarriers)
            self.blocks.add_module(name='block_{}'.format(block_id), module=block)
        self._conv_1 = nn.Conv2d(4 * self.streams, self.channel_list[2], kernel_size=3, padding=1)
        self._conv_2 = nn.Conv2d(self.channel_list[1], self.streams * self.num_bits_per_symbol, kernel_size=3, padding=1)

    def forward(self, y, template_pilot):
        batch_size = y.shape[0]
        y = y.permute(0, 2, 3, 1, 4)
        y = torch.reshape(y, (batch_size, self.timesymbols, self.subcarriers, self.streams * 2))
        template_pilot = template_pilot.permute(0, 2, 3, 1, 4)
        template_pilot = torch.reshape(template_pilot, (batch_size, self.timesymbols, self.subcarriers, self.streams * 2))

        z = torch.cat([y, template_pilot], dim=-1)
        z = z.permute(0, 3, 1, 2)
        z = self._conv_1(z)
        z = self.blocks(z)
        z = self._conv_2(z)
        z = z.permute(0, 2, 3, 1)
        z = torch.reshape(z, (batch_size, self.timesymbols, self.subcarriers, self.streams, self.num_bits_per_symbol))
        z = z.permute(0, 3, 1, 2, 4)
        return z
