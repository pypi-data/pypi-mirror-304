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

        # 初始化权重
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

        # 初始化卷积层
        self.init_conv = nn.Conv2d(4 * self.streams, self.base_channels, kernel_size=3, padding=1)
        in_channels = self.base_channels
        # 初始化残差块
        self.blocks = nn.Sequential()
        for block_id in range(self.num_blocks):
            in_channels = self.base_channels if block_id == 0 else layer_channels
            layer_channels = self.base_channels + (block_id // 10) * 32
            self.blocks.add_module(
                name=f'resblock_{block_id}',
                module=ResBlock(in_channels, layer_channels, dropout_rate=dropout_rate)
            )
            in_channels = layer_channels
        final_channels = in_channels  # 或特定残差块设计的输出通道数
        # 初始化最终的卷积层
        self.final_conv = nn.Conv2d(final_channels, streams * num_bits_per_symbol, kernel_size=3, padding=1)

    def preprocess(self, y):
        # 数据预处理步骤：将实部和虚部转换为复数形式
        y_complex = torch.complex(y[..., 0], y[..., 1])
        return y_complex

    def forward(self, y, template_pilot):
        # 在模型前向传播中调用预处理
        #y_complex = self.preprocess(y)
        #template_pilot_complex = self.preprocess(template_pilot)
        # 分别应用权重到实部和虚部
        y_real_weighted = y[..., 0] * self.W[..., 0] - y[..., 1] * self.W[..., 1]  # 应用权重到实部
        y_imag_weighted = y[..., 1] * self.W[..., 0] + y[..., 0] * self.W[..., 1]  # 应用权重到虚部
        template_pilot_real_weighted = template_pilot[..., 0] * self.V[..., 0] - template_pilot[..., 1] * self.V[..., 1]  # 应用权重到实部
        template_pilot_imag_weighted = template_pilot[..., 1] * self.V[..., 0] + template_pilot[..., 0] * self.V[..., 1]  # 应用权重到虚部

        # 组合加权后的实部和虚部
        y_weighted = torch.stack([y_real_weighted, y_imag_weighted], dim=-1)  # 最后一个维度是实部和虚部
        template_pilot_weighted = torch.stack([template_pilot_real_weighted, template_pilot_imag_weighted], dim=-1)

        # 现在 y_weighted 包含了加权后的实部和虚部，您可以转换它为复数形式
        y_weighted_complex = torch.complex(y_weighted[..., 0], y_weighted[..., 1])
        template_pilot_weighted_complex = torch.complex(template_pilot_weighted[..., 0], template_pilot_weighted[..., 1])

        # 应用权重
 

        # 调整数据形状以适应卷积层
        batch_size = y.shape[0]
        # 对于加权后的复数信号，调整维度以适应卷积层，确保考虑所有五个维度
        y = torch.view_as_real(y_weighted_complex).permute(0, 4, 1, 2, 3)  # 注意维度顺序
        # 调整维度，合并最后两个维度
        y = y.reshape(y.shape[0], -1, y.shape[2], y.shape[3])

        # 对于加权后的复数导频信号，执行相同的维度调整
        template_pilot = torch.view_as_real(template_pilot_weighted_complex).permute(0, 4, 1, 2, 3)  # 注意维度顺序
        # 调整维度，合并最后两个维度
        template_pilot = template_pilot.reshape(template_pilot.shape[0], -1, template_pilot.shape[2], template_pilot.shape[3])

        # 将接收信号和导频信号合并为模型的输入
        z = torch.cat([y, template_pilot], dim=1)  # 在通道维度上合并

        # 通过神经网络层
        z = self.init_conv(z)
        z = self.blocks(z)
        z = self.final_conv(z)

        # 将输出调整回原始维度
        z = z.permute(0, 2, 3, 1).view(batch_size, self.timesymbols, self.subcarriers, self.streams, self.num_bits_per_symbol)
        
        return z