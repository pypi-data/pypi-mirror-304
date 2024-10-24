import torch
import torch.nn as nn
import numpy as np
from scipy import signal
import torch.nn.functional as F

class ChannelAttention(nn.Module):
    def __init__(self, num_channels, reduction_ratio=8):
        super(ChannelAttention, self).__init__()
        # Adaptive average and max pooling
        self.avg_pool = nn.AdaptiveAvgPool2d(1)
        self.max_pool = nn.AdaptiveMaxPool2d(1)
        # Shared MLP layers
        self.shared_layer_one = nn.Linear(num_channels, num_channels // reduction_ratio, bias=True)
        self.shared_layer_two = nn.Linear(num_channels // reduction_ratio, num_channels, bias=True)
        # Activation layer
        self.relu = nn.SiLU()
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        b, c, _, _ = x.size()
        # Average pool path
        avg_y = self.avg_pool(x).view(b, c)
        avg_y = self.relu(self.shared_layer_one(avg_y))
        avg_y = self.shared_layer_two(avg_y)
        avg_y = avg_y.view(b, c, 1, 1)
        # Max pool path
        max_y = self.max_pool(x).view(b, c)
        max_y = self.relu(self.shared_layer_one(max_y))
        max_y = self.shared_layer_two(max_y)
        max_y = max_y.view(b, c, 1, 1)
        # Combine and apply sigmoid
        y = self.sigmoid(avg_y + max_y)
        return x * y.expand_as(x)

class ResBlock(nn.Module):
    def __init__(self, in_channels, out_channels, stride=1, kernel_size=3, dropout_rate=0.3):
        super(ResBlock, self).__init__()
        self.conv1 = nn.Conv2d(in_channels, out_channels, kernel_size=kernel_size, stride=stride, padding=kernel_size // 2, bias=False)
        self.bn1 = nn.BatchNorm2d(out_channels)
        self.prelu = nn.SiLU()  # ReLU SiLU Mish LeakyReLU
        self.dropout = nn.Dropout(dropout_rate)
        self.conv2 = nn.Conv2d(out_channels, out_channels, kernel_size=kernel_size, stride=1, padding=kernel_size // 2, bias=False)
        self.bn2 = nn.BatchNorm2d(out_channels)
        self.channel_attention = ChannelAttention(out_channels)  # 注意力机制层
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
        out = self.prelu(out)
        out = self.dropout(out)
        out = self.conv2(out)
        out = self.bn2(out)
        out = self.channel_attention(out) 
        if self.downsample is not None:
            identity = self.downsample(x)        
        out += identity
        out = self.prelu(out)
        return out

class Neural_receiver(nn.Module):
    def __init__(self, subcarriers, timesymbols, streams, num_bits_per_symbol, num_blocks, base_channels, scene, dropout_rate=0.3):
        super(Neural_receiver, self).__init__()
        self.subcarriers = subcarriers
        self.timesymbols = timesymbols
        self.streams = streams
        self.num_blocks = num_blocks
        self.base_channels = base_channels
        self.num_bits_per_symbol = num_bits_per_symbol         
        self.init_conv = nn.Conv2d(4 * streams, base_channels, kernel_size=3, stride=1, padding=1)     
        self.blocks = nn.Sequential()
     
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
        for block_id in range(self.num_blocks):
            in_channels = self.base_channels if block_id == 0 else layer_channels
            layer_channels = self.base_channels + (block_id // 10) * 32
            self.blocks.add_module(
                name=f'resblock_{block_id}',
                module=ResBlock(in_channels, layer_channels, kernel_size =3,dropout_rate=dropout_rate)
            )

        final_channels = self.base_channels + ((self.num_blocks - 1) // 10) * 32
        self.final_conv = nn.Conv2d(final_channels, streams * num_bits_per_symbol, kernel_size=3, stride=1, padding=1)

    def forward(self, y, template_pilot):
        y_weighted = y * self.W
        pilot_weighted = template_pilot * self.V        
        batch_size = y.shape[0]
        y = y.permute(0, 2, 3, 1, 4)
        y = torch.reshape(y, (batch_size, self.timesymbols, self.subcarriers, self.streams * 2))
        template_pilot = template_pilot.permute(0, 2, 3, 1, 4)
        template_pilot = torch.reshape(template_pilot, (batch_size, self.timesymbols, self.subcarriers, self.streams * 2))
        z  = torch.cat([y, template_pilot], dim=-1)
        z = z.permute(0, 3, 1, 2)
        z = self.init_conv(z)        
        z = self.blocks(z)
        z = self.final_conv(z)               
        z = z.permute(0, 2, 3, 1)
        z = torch.reshape(z, (batch_size, self.timesymbols, self.subcarriers, self.streams, self.num_bits_per_symbol))
        z = z.permute(0, 3, 1, 2, 4)
        def complex_division(yy, Z):
            # y and Z are assumed to have dimensions [..., 2] where the last dimension contains real and imaginary parts
            # Extract real and imaginary parts
            y_real, y_imag = y_weighted[..., 0], y_weighted[..., 1]
            Z_real, Z_imag = Z[..., 0], Z[..., 1]       
            # Compute the denominator
            denominator = Z_real**2 + Z_imag**2        
            # Perform complex division
            result_real = (y_real * Z_real + y_imag * Z_imag) / denominator
            result_imag = (y_imag * Z_real - y_real * Z_imag) / denominator        
            # Combine the real and imaginary parts
            result = torch.stack([result_real, result_imag], dim=-1)        
            return result
        corrected_signal = complex_division(y, z)
        combined_data = torch.cat([y_weighted, z, corrected_signal], dim=-1)  # 或者选择其他维度进行组合


        return z
