import torch
import torch.nn as nn

class AttentionModule(nn.Module):
    def __init__(self, in_channels):
        super(AttentionModule, self).__init__()
        self.avg_pool = nn.AdaptiveAvgPool2d(1)
        self.fc = nn.Sequential(
            nn.Linear(in_channels, in_channels // 16, bias=False),
            nn.ReLU(inplace=True),
            nn.Linear(in_channels // 16, in_channels, bias=False),
            nn.Sigmoid()
        )

    def forward(self, x):
        b, c, _, _ = x.size()
        y = self.avg_pool(x).view(b, c)
        y = self.fc(y).view(b, c, 1, 1)
        return x * y.expand_as(x)

class ResBlock(nn.Module):
    def __init__(self, in_channels, out_channels, stride=1, kernel_size=3, dropout_rate=0.1):
        super(ResBlock, self).__init__()
        self.conv1 = nn.Conv2d(in_channels, out_channels, kernel_size=kernel_size, stride=stride, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(out_channels)
        self.relu = nn.ReLU(inplace=True)
        self.dropout = nn.Dropout(dropout_rate)
        self.conv2 = nn.Conv2d(out_channels, out_channels, kernel_size=kernel_size, stride=1, padding=1, bias=False)
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
    def __init__(self, subcarriers, timesymbols, streams, num_bits_per_symbol, num_blocks, base_channels, scene, dropout_rate=0.5):
        super(Neural_receiver, self).__init__()
        self.subcarriers = subcarriers
        self.timesymbols = timesymbols
        self.streams = streams
        self.num_blocks = num_blocks
        self.base_channels = base_channels
        self.num_bits_per_symbol = num_bits_per_symbol
        # Initialize the noise reduction (denoising) and attention modules
        self.denoise_module = ResBlock(4 * streams, 4 * streams, kernel_size=3, dropout_rate=dropout_rate)
        self.attention_module = AttentionModule(4 * streams)
        # Scene specific settings
        if scene == 'scene1':
            self.register_buffer('W', torch.full((1, 1, timesymbols, subcarriers, 2), 0.9))
            self.register_buffer('V', torch.full((1, 1, timesymbols, subcarriers, 2), 0.1))
        elif scene == 'scene2':
            self.register_buffer('W', torch.full((1, 1, timesymbols, subcarriers, 2), 0.6))
            self.register_buffer('V', torch.zeros((1, 1, timesymbols, subcarriers, 2)))
            specific_t_V = {1: [0, 4, 8], 2: [1, 5, 9], 3: [2, 6, 10], 4: [3, 7, 11]}
            for l in range(streams):
                for t in specific_t_V[l + 1]:
                    self.V[0, 0, t, :, :] = 1.6

        # Initial convolutional layer
        self.init_conv = nn.Conv2d(4 * self.streams, self.base_channels, kernel_size=3, padding='same')

        # Residual blocks and extra convolutional layers
        self.blocks = nn.Sequential()
        self.blocks = nn.ModuleList()
        for block_id in range(num_blocks):
            in_channels = base_channels if block_id == 0 else base_channels * 2 ** (block_id // 3)
            out_channels = base_channels * 2 ** ((block_id + 1) // 3)
            self.blocks.append(ResBlock(in_channels, out_channels, kernel_size=3, dropout_rate=dropout_rate))


       # Final convolutional layer to produce the output
        final_out_channels = base_channels * 2 ** (num_blocks // 3)
        self.final_conv = nn.Conv2d(final_out_channels, streams * num_bits_per_symbol, kernel_size=3, padding=1)

    def forward(self, y, template_pilot):
        y_weighted = y * self.W
        pilot_weighted = template_pilot * self.V
        batch_size = y.shape[0]
        y = y_weighted.permute(0, 2, 3, 1, 4)
        y = torch.reshape(y, (batch_size, self.timesymbols, self.subcarriers, self.streams * 2))
        template_pilot = pilot_weighted.permute(0, 2, 3, 1, 4)
        template_pilot = torch.reshape(template_pilot, (batch_size, self.timesymbols, self.subcarriers, self.streams * 2))

        z = torch.cat([y, template_pilot], dim=-1).permute(0, 3, 1, 2)
        z = self.denoise_module(z)
        z = self.attention_module(z)
        z = self.init_conv(z)

        for block in self.blocks:
            z = block(z)

        z = self.final_conv(z)
        z = z.permute(0, 2, 3, 1).reshape(batch_size, self.timesymbols, self.subcarriers, self.streams, self.num_bits_per_symbol).permute(0, 3, 1, 2, 4)
        return z
