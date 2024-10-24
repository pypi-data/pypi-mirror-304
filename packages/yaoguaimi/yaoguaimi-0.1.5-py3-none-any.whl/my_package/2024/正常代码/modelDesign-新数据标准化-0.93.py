import torch
import torch.nn as nn


class SignalNormalization2(nn.Module):
    def __init__(self):
        super(SignalNormalization2, self).__init__()

    def forward(self, x):
        # 计算每个样本的最大值
        max_val, _ = torch.max(torch.abs(x).view(x.size(0), -1), dim=1, keepdim=True)
        max_val = max_val.view(x.size(0), 1, 1, 1, 1)
        return x / (max_val + 1e-8)  # 加上小量避免除以零
class ComplexDenoisingAutoencoder2(nn.Module):
    def __init__(self, input_channels, features=64):
        super(ComplexDenoisingAutoencoder2, self).__init__()
        # 确保这里的input_channels与x_real和x_imag的通道数相匹配
        self.denoiser_real = nn.Sequential(
            nn.Conv2d(input_channels, 64, kernel_size=3, padding=1),  # input_channels应该是1
            nn.ReLU(),
            nn.Conv2d(64, input_channels, kernel_size=3, padding=1)  # 这里保持input_channels不变
        )
        self.denoiser_imag = nn.Sequential(
            nn.Conv2d(input_channels, 64, kernel_size=3, padding=1),  # 同上
            nn.ReLU(),
            nn.Conv2d(64, input_channels, kernel_size=3, padding=1)  # 同上
        )

    def forward(self, x):
        batch_size, layers, symbols, subcarriers, _ = x.size()
        # 以下代码没有变化
        x_real = x[..., 0].view(batch_size * layers, 1, symbols, subcarriers)  # 确保这里的1对应input_channels
        x_imag = x[..., 1].view(batch_size * layers, 1, symbols, subcarriers)  # 同上

        # 对实部和虚部进行去噪
        denoised_real = self.denoiser_real(x_real).view(batch_size, layers, symbols, subcarriers)
        denoised_imag = self.denoiser_imag(x_imag).view(batch_size, layers, symbols, subcarriers)

        # 合并去噪后的实部和虚部
        denoised = torch.stack((denoised_real, denoised_imag), dim=-1)

        return denoised



########################去噪模块单通道################################
class DenoisingAutoencoder(nn.Module):   
    def __init__(self, input_channels, output_channels):
        super(DenoisingAutoencoder, self).__init__()
        self.encoder = nn.Sequential(
            nn.Conv2d(input_channels, 16, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(16, 32, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2)
        )
        self.decoder = nn.Sequential(
            nn.ConvTranspose2d(32, 16, kernel_size=2, stride=2),
            nn.ReLU(),
            nn.ConvTranspose2d(16, output_channels, kernel_size=2, stride=2),
            nn.Sigmoid()  # 或者根据您的数据范围使用其他激活函数
        )

    def forward(self, x):
        encoded = self.encoder(x)
        decoded = self.decoder(encoded)
        return decoded

#######################去噪模块复数通道################################

class ComplexDenoisingAutoencoder(nn.Module):
    def __init__(self):
        super(ComplexDenoisingAutoencoder, self).__init__()
        # Encoder
        self.encoder = nn.Sequential(
            nn.Conv2d(2, 8, kernel_size=3, padding=1),  # Assume input is [B, 2, H, W]
            nn.ReLU(),
            nn.MaxPool2d(2),  # Reduce size
            # More layers as needed
        )
        # Decoder
        self.decoder = nn.Sequential(
            nn.ConvTranspose2d(8, 2, kernel_size=2, stride=2),
            nn.ReLU(),
            # More layers as needed
        )

    def forward(self, x):
        # Combine real and imaginary parts into channel dimension
        x_combined = x.view(x.size(0), 2, -1, x.size(3))  # [B, 2, H, W]
        encoded = self.encoder(x_combined)
        decoded = self.decoder(encoded)
        # Split back into real and imaginary parts
        decoded = decoded.view(x.size(0), x.size(1), x.size(2), x.size(3), 2)  # [B, Layers, Symbols, Subcarriers, 2]
        return decoded



########################通道注意力################################
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


########################空间注意力################################
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



########################残差################################
class ResBlock(nn.Module):
    def __init__(self, in_channels, out_channels, stride=1, kernel_size=3, dropout_rate=0.1):
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

########################数据标准化################################

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


########################主程序################################

class Neural_receiver(nn.Module):
    def __init__(self, subcarriers, timesymbols, streams, num_bits_per_symbol, num_blocks, base_channels, scene, dropout_rate=0.1):
        super(Neural_receiver, self).__init__()
        self.subcarriers = subcarriers
        self.timesymbols = timesymbols
        self.streams = streams
        self.num_blocks = num_blocks
        self.base_channels = base_channels
        self.num_bits_per_symbol = num_bits_per_symbol
        self.normalization2 = SignalNormalization2()
        self.denoise2 = ComplexDenoisingAutoencoder2(input_channels=1)  # 假设实部和虚部被拼接
        # Initialize the normalization layer
        self.normalization = SignalNormalization()
        self.denoise = ComplexDenoisingAutoencoder()  # 根据需要调整通道数
        #self.denoise2 = DenoisingAutoencoder(input_channels=4, output_channels=4)

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

        
        y = self.normalization2(y)
        template_pilot = self.normalization2(template_pilot)

        #y = self.denoise2(y)
        #template_pilot = self.denoise2(template_pilot)        
        
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
        #z = self.channel_attention(z)  # Apply channel attention after initial convolution
        #print("After channel_attention:", z.shape) 
        z = self.blocks(z)
        #print("After blocks:", z.shape)
        #z = self.spatial_attention(z)  # Apply spatial attention after residual blocks
        z = self.final_conv(z)
       # print("After final_conv:", z.shape)
        z = z.permute(0, 2, 3, 1).reshape(batch_size, self.timesymbols, self.subcarriers, self.streams, self.num_bits_per_symbol)
        return z.permute(0, 3, 1, 2, 4)