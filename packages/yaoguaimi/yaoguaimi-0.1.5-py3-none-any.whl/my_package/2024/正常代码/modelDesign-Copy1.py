import torch
import torch.nn as nn

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

class Neural_receiver(nn.Module):
    def __init__(self, subcarriers, timesymbols, streams, num_bits_per_symbol, num_blocks, base_channels, scene, dropout_rate=0.1):
        super(Neural_receiver, self).__init__()
        self.subcarriers = subcarriers
        self.timesymbols = timesymbols
        self.streams = streams
        self.num_blocks = num_blocks
        self.base_channels = base_channels
        self.num_bits_per_symbol = num_bits_per_symbol

        # Initialize weights for real and imaginary parts
        self.W_real = torch.full((1, 1, timesymbols, subcarriers), 0.9 if scene == 'scene1' else 0.6)
        self.W_imag = torch.full((1, 1, timesymbols, subcarriers), 0.9 if scene == 'scene1' else 0.6)
        self.V_real = torch.full((1, 1, timesymbols, subcarriers), 0.1 if scene == 'scene1' else 0.0)
        self.V_imag = torch.full((1, 1, timesymbols, subcarriers), 0.1 if scene == 'scene1' else 0.0)

        # Neural network layers for real and imaginary parts
        self.init_conv_real = nn.Conv2d(2 * self.streams, self.base_channels, kernel_size=3, padding=1)
        self.init_conv_imag = nn.Conv2d(2 * self.streams, self.base_channels, kernel_size=3, padding=1)
        self.blocks_real = nn.Sequential()
        self.blocks_imag = nn.Sequential()
        for block_id in range(self.num_blocks):
            self.blocks_real.add_module('resblock_real_{0}'.format(block_id), ResBlock(self.base_channels, self.base_channels, dropout_rate=dropout_rate))
            self.blocks_imag.add_module('resblock_imag_{0}'.format(block_id), ResBlock(self.base_channels, self.base_channels, dropout_rate=dropout_rate))
        self.final_conv_real = nn.Conv2d(self.base_channels, self.streams * self.num_bits_per_symbol, kernel_size=3, padding=1)
        self.final_conv_imag = nn.Conv2d(self.base_channels, self.streams * self.num_bits_per_symbol, kernel_size=3, padding=1)

    def forward(self, y, template_pilot):
        # Move weights to the same device as the input tensors
        device = y.device  # Get the device of the input tensor
        self.W_real = self.W_real.to(device)
        self.W_imag = self.W_imag.to(device)
        self.V_real = self.V_real.to(device)
        self.V_imag = self.V_imag.to(device)
        
        
        # Separate real and imaginary parts
        y_real = y[..., 0] * self.W_real
        y_imag = y[..., 1] * self.W_imag
        pilot_real = template_pilot[..., 0] * self.V_real
        pilot_imag = template_pilot[..., 1] * self.V_imag

        # Reshape for convolutional layers
        batch_size = y.shape[0]
        y_real = y_real.permute(0, 2, 3, 1).reshape(batch_size, self.timesymbols, self.subcarriers, 2 * self.streams)
        y_imag = y_imag.permute(0, 2, 3, 1).reshape(batch_size, self.timesymbols, self.subcarriers, 2 * self.streams)
        pilot_real = pilot_real.permute(0, 2, 3, 1).reshape(batch_size, self.timesymbols, self.subcarriers, 2 * self.streams)
        pilot_imag = pilot_imag.permute(0, 2, 3, 1).reshape(batch_size, self.timesymbols, self.subcarriers, 2 * self.streams)

        # Process real and imaginary parts through separate neural networks
        z_real = torch.cat([y_real, pilot_real], dim=-1)
        z_imag = torch.cat([y_imag, pilot_imag], dim=-1)
        z_real = z_real.permute(0, 3, 1, 2)
        z_imag = z_imag.permute(0, 3, 1, 2)
        z_real = self.init_conv_real(z_real)
        z_imag = self.init_conv_imag(z_imag)
        z_real = self.blocks_real(z_real)
        z_imag = self.blocks_imag(z_imag)
        z_real = self.final_conv_real(z_real)
        z_imag = self.final_conv_imag(z_imag)

        # Combine processed real and imaginary parts
        z = torch.stack([z_real, z_imag], dim=-1)
        z = z.permute(0, 2, 3, 1, 4)

        return z
