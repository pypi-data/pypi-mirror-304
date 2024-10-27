import torch
from einops import rearrange, repeat, reduce, pack, unpack
from torch import nn
from x_transformers import Attention as XAttention, FeedForward
from timm.models._efficientnet_blocks import UniversalInvertedResidual

def pack_one(x, pattern):
    return pack([x], pattern)

def unpack_one(x, ps, pattern):
    return unpack(x, ps, pattern)[0]

class Layer2D(nn.Module):
    def __init__(
        self,
        dim_in,
        dim_out,
        *,
        num_register_tokens=4,
        window_size=8,
        mbconv_expansion_rate=4,
        dropout=0.0,
        dim_head=32,
        heads=None,
    ):
        super().__init__()
        assert num_register_tokens > 0
        self.window_size = window_size

        # Determine number of heads
        if heads is None:
            assert dim_out % dim_head == 0, "dim_out must be divisible by dim_head"
            heads = dim_out // dim_head

        # Register tokens
        self.register_tokens = nn.Parameter(torch.randn(num_register_tokens, dim_out))

        # UIB layer (replacing MBConv)
        self.conv = UniversalInvertedResidual(
            in_chs=dim_in,
            out_chs=dim_out,
            stride=1,  # downsample=False
            exp_ratio=mbconv_expansion_rate,
            drop_path_rate=dropout,
        )

        # Block attention and feedforward using x-transformers
        self.block_attn = XAttention(
            dim=dim_out,
            heads=heads,
            dim_head=dim_head,
            dropout=dropout,
            flash=True,
            one_kv_head=True
        )
        self.block_ff = FeedForward(dim=dim_out, dropout=dropout)

        # Grid attention and feedforward using x-transformers
        self.grid_attn = XAttention(
            dim=dim_out,
            heads=heads,
            dim_head=dim_head,
            dropout=dropout,
            flash=True,
            one_kv_head=True
        )
        self.grid_ff = FeedForward(dim=dim_out, dropout=dropout)

        # LayerNorms (since x-transformers Attention does not include pre/post LayerNorm)
        self.block_attn_norm = nn.LayerNorm(dim_out)
        self.grid_attn_norm = nn.LayerNorm(dim_out)

    def forward(self, x):
        b = x.shape[0]
        w = self.window_size

        # Apply UIB
        x = self.conv(x)

        # Block attention and feedforward with register tokens
        x = rearrange(x, 'b d (x w1) (y w2) -> b (x y) (w1 w2) d', w1=w, w2=w)
        num_windows = x.shape[1]

        # Prepare register tokens
        r = self.register_tokens.unsqueeze(0).unsqueeze(1).expand(b, num_windows, -1, -1)  # (b, num_windows, num_register_tokens, d)
        x = torch.cat([r, x], dim=2)  # Concatenate along sequence dimension

        # Merge batch and window dimensions for processing
        x = x.view(b * num_windows, -1, x.shape[-1])  # (b * num_windows, seq_len, d)

        # Apply LayerNorm
        x = self.block_attn_norm(x)

        # Apply attention
        x = self.block_attn(x) + x

        # Apply feedforward
        x = self.block_ff(x) + x

        # Separate registers and tokens
        r, x = x[:, :self.register_tokens.shape[0], :], x[:, self.register_tokens.shape[0]:, :]

        # Reshape back to original dimensions
        x = x.view(b, -1, w * w, x.shape[-1])  # (b, num_windows, window_area, d)
        x = x.view(b, int(x.shape[1] ** 0.5), int(x.shape[1] ** 0.5), w, w, -1)
        x = rearrange(x, 'b x y w1 w2 d -> b d (x w1) (y w2)')

        # Grid attention and feedforward with register tokens
        x = rearrange(x, 'b d (w1 x) (w2 y) -> b (x y) (w1 w2) d', w1=w, w2=w)
        num_windows = x.shape[1]

        # Average register tokens across windows
        r = r.view(b, -1, self.register_tokens.shape[0], r.shape[-1])  # (b, num_windows, num_register_tokens, d)
        r = r.mean(dim=1, keepdim=True).expand(b, num_windows, -1, -1)  # (b, num_windows, num_register_tokens, d)

        # Concatenate registers and tokens
        x = torch.cat([r, x], dim=2)

        # Merge batch and window dimensions
        x = x.view(b * num_windows, -1, x.shape[-1])

        # Apply LayerNorm
        x = self.grid_attn_norm(x)

        # Apply attention
        x = self.grid_attn(x) + x

        # Apply feedforward
        x = self.grid_ff(x) + x

        # Separate registers and tokens
        _, x = x[:, :self.register_tokens.shape[0], :], x[:, self.register_tokens.shape[0]:, :]

        # Reshape back to image dimensions
        x = x.view(b, -1, w * w, x.shape[-1])
        x = x.view(b, int(x.shape[1] ** 0.5), int(x.shape[1] ** 0.5), w, w, -1)
        x = rearrange(x, 'b x y w1 w2 d -> b d (x w1) (y w2)')

        return x
