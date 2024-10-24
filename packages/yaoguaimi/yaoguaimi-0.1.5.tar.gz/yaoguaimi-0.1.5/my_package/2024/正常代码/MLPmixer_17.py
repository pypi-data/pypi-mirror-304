import torch
import torch.nn as nn
from functools import partial
import numpy as np
from functools import partial
import math

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


class MLPMixerLayer(nn.Module):
    def __init__(self, num_patches, hidden_dim, tokens_mlp_dim, channels_mlp_dim,dropout_rate):
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


    def forward(self, x):
        # Apply LayerNorm before token mixing
        y = self.norm1(x)
        # Token mixing (patch mixing)
        y = y.permute(0, 2, 1)  # Swap the 'hidden_dim' and 'num_patches' dimensions
        y = self.token_mixing(y)
        y = y.permute(0, 2, 1)  # Swap back after token mixing
        x = x + y # DropPath 应用于残差连接
        # Apply LayerNorm before channel mixing      
        y = self.norm2(x)
        # Channel mixing
        y = self.channel_mixing(y)
        x = x + y  # 再次应用
        return x


        
class Neural_receiver(nn.Module):
    def __init__(self, num_patches, num_layers, hidden_dim, tokens_mlp_dim, channels_mlp_dim, num_symbols, subcarriers, streams, num_bits_per_symbol,dropout_rate):
        super().__init__()
        self.streams = streams
        self.num_bits_per_symbol = num_bits_per_symbol
        self.num_symbols = num_symbols
        self.subcarriers = subcarriers
        self.num_patches = num_symbols*subcarriers
        self.patch_embedding = nn.Sequential(
            nn.Linear(4*self.streams, hidden_dim),
        )

        self.mixer_layers = nn.ModuleList([
            MLPMixerLayer(num_patches, hidden_dim, tokens_mlp_dim, channels_mlp_dim,dropout_rate) for _ in range(num_layers)
        ])
        self.layer_norm = nn.LayerNorm(hidden_dim)
        self.head = nn.Sequential(
            nn.Dropout(0),  # Add dropout here before the final linear layer
            nn.Linear(hidden_dim,4*6)
        )

    def forward(self, y, template_pilot):
        batch_size = y.shape[0]
        y = torch.cat([y,template_pilot], dim=-1)  # Concatenating pilot signals to the input #template_pilot     
        y = y.view(batch_size, self.num_patches, -1)  # Reshaping into patches
        y = self.patch_embedding(y)  # Apply patch embedding)    
        # Apply mixer layers
        for layer in self.mixer_layers:
            y = layer(y)
        # Apply final normalization and classification head
        #y = self.layer_norm(y)
        y = self.head(y)
        y = y.view(batch_size,  self.streams, self.num_symbols,self.subcarriers ,self.num_bits_per_symbol)
        return y
