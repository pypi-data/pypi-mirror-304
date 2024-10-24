import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.nn import TransformerEncoder, TransformerEncoderLayer
import math

# 设置设备
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Using device:", device)
print(torch.cuda.is_available())
print(torch.cuda.device_count())
print(torch.cuda.current_device())
print(torch.cuda.get_device_name(0))

class SignalNormalization(nn.Module):
    def __init__(self):
        super(SignalNormalization, self).__init__()

    def forward(self, x):
        max_val, _ = torch.max(torch.abs(x).view(x.size(0), -1), dim=1, keepdim=True)
        max_val = max_val.view(x.size(0), 1, 1, 1, 1)
        return x / (max_val + 1e-8)

class SignalTransformer(nn.Module):
    def __init__(self, d_model, nhead, num_encoder_layers, streams, dim_feedforward=2048, dropout=0.1):
        super(SignalTransformer, self).__init__()
        encoder_layers = TransformerEncoderLayer(d_model, nhead, dim_feedforward, dropout).to(device)
        self.transformer_encoder = TransformerEncoder(encoder_layers, num_encoder_layers).to(device)
        self.pos_encoder = PositionalEncoding(d_model, dropout).to(device)
        self.input_proj = nn.Linear(4 * streams, d_model).to(device)

    def forward(self, x):
        x = self.input_proj(x)
        x = self.pos_encoder(x)
        output = self.transformer_encoder(x)
        return output

class PositionalEncoding(nn.Module):
    def __init__(self, d_model, dropout=0.1, max_len=50):
        super(PositionalEncoding, self).__init__()
        self.dropout = nn.Dropout(p=dropout)
        pe = torch.zeros(max_len, d_model).to(device)
        position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1).to(device)
        div_term = torch.exp(torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model)).to(device)
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        pe = pe.unsqueeze(0).transpose(0, 1)
        self.register_buffer('pe', pe)

    def forward(self, x):
        x = x + self.pe[:x.size(0), :]
        return self.dropout(x)

class Neural_receiver(nn.Module):
    def __init__(self, subcarriers, timesymbols, streams, num_bits_per_symbol, num_blocks, base_channels, scene, d_model, nhead, num_encoder_layers, dropout_rate=0.1):
        super(Neural_receiver, self).__init__()
        self.subcarriers = subcarriers
        self.timesymbols = timesymbols
        self.streams = streams
        self.num_blocks = num_blocks
        self.base_channels = base_channels
        self.num_bits_per_symbol = num_bits_per_symbol       
        self.normalization = SignalNormalization().to(device)
        self.signal_transformer = SignalTransformer(d_model, nhead, num_encoder_layers, streams, dropout=dropout_rate).to(device)
        final_output_size = streams * num_bits_per_symbol * timesymbols * subcarriers
        self.output_proj = nn.Linear(d_model * timesymbols * subcarriers, final_output_size).to(device)

        self.register_buffer('W', torch.full((1, 1, timesymbols, subcarriers, 2), 0.9 if scene == 'scene1' else 0.6).to(device))
        self.register_buffer('V', torch.full((1, 1, timesymbols, subcarriers, 2), 0.1 if scene == 'scene1' else 0.0).to(device))

    def forward(self, y, template_pilot):
        y = self.normalization(y.to(device))
        template_pilot = self.normalization(template_pilot.to(device))
        y_weighted = y * self.W
        pilot_weighted = template_pilot * self.V
        batch_size = y.shape[0]
        y = y_weighted.permute(0, 2, 3, 1, 4).reshape(batch_size, self.timesymbols * self.subcarriers, self.streams * 2)
        template_pilot = pilot_weighted.permute(0, 2, 3, 1, 4).reshape(batch_size, self.timesymbols * self.subcarriers, self.streams * 2)
        z = torch.cat([y, template_pilot], dim=-1)
        z = self.signal_transformer(z)
        z = z.reshape(batch_size, -1)
        z = self.output_proj(z)
        z = z.reshape(batch_size, self.streams, self.timesymbols, self.subcarriers, self.num_bits_per_symbol)

        z = z.permute(0, 1, 2, 3, 4)  # 调整维度以匹配目标形状

        return z