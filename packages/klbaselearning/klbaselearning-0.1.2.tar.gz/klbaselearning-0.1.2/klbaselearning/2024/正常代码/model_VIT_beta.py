import types
import torch
from torch import nn
from torch import nn, einsum
from einops import rearrange, repeat
from einops.layers.torch import Rearrange

def drop_path(x, drop_prob=0.0, training=False):
    if drop_prob == 0. or not training:
        return x
    keep_prob = 1 - drop_prob
    shape = (x.shape[0],) + (1,) * (x.ndim - 1)
    random_tensor = keep_prob + torch.rand(shape, dtype=x.dtype, device=x.device)
    random_tensor.floor_()
    output = x.div(keep_prob) * random_tensor
    return output


class DropPath(nn.Module):
    def __init__(self, p, **kwargs):
        super().__init__()
        self.p = p

    def forward(self, x):
        x = drop_path(x, self.p, self.training)
        return x

    def extra_repr(self):
        return 'p=%s' % repr(self.p)


class Lambda(nn.Module):
    def __init__(self, lmd):
        super(Lambda, self).__init__()
        if not isinstance(lmd, types.LambdaType):
            raise Exception("'lmd' should be lambda ftn.")
        self.lmd = lmd

    def forward(self, x):
        return self.lmd(x)





class FeedForward(nn.Module):
    def __init__(self, dim_in, hidden_dim, dim_out=None, *, dropout=0.0, f=nn.Linear, activation=nn.ReLU):
        super(FeedForward, self).__init__()
        dim_out = dim_in if dim_out is None else dim_out

        self.net = nn.Sequential(
            f(dim_in, hidden_dim),
            activation(),
            nn.Dropout(dropout) if dropout > 0.0 else nn.Identity(),
            f(hidden_dim, dim_out),
            nn.Dropout(dropout) if dropout > 0.0 else nn.Identity(),
        )

    def forward(self, x):
        x = self.net(x)
        return x


class Attention1d(nn.Module):
    def __init__(self, dim_in, dim_out=None, *, heads=8, dim_head=64, dropout=0.0):
        super(Attention1d, self).__init__()
        inner_dim = heads * dim_head
        dim_out = dim_in if dim_out is None else dim_out

        self.heads = heads
        self.scale = dim_head ** -0.5

        self.to_qkv = nn.Linear(dim_in, inner_dim * 3, bias=False)

        self.to_out = nn.Sequential(
            nn.Linear(inner_dim, dim_out),
            nn.LayerNorm(dim_out),
            nn.Dropout(dropout) if dropout > 0.0 else nn.Identity()
        )

    def forward(self, x, mask=None):
        b, n, _ = x.shape
        qkv = self.to_qkv(x).chunk(3, dim=-1)
        q, k, v = map(lambda t: rearrange(t, 'b n (h d) -> b h n d', h=self.heads), qkv)  # (2, 16, 11, 32)

        dots = einsum('b h i d, b h j d -> b h i j', q, k) * self.scale  # (2, 16, 11, 11)
        dots = dots + mask if mask is not None else dots
        attn = dots.softmax(dim=-1)  # (2, 16, 11, 11)

        out = einsum('b h i j, b h j d -> b h i d', attn, v)  # (2, 16, 11, 32)
        out = rearrange(out, 'b h n d -> b n (h d)')  # (2, 11, 512)
        out = self.to_out(out)  # (2, 11, 512)

        return out, attn


class Transformer(nn.Module):
    def __init__(self, dim_in, dim_out=None, *, heads=8, dim_head=64, dim_mlp=1024, dropout=0.0, sd=0.0,
                 attn=Attention1d, norm=nn.LayerNorm, f=nn.Linear, activation=nn.GELU):
        super(Transformer, self).__init__()
        dim_out = dim_in if dim_out is None else dim_out

        self.shortcut = []
        if dim_in != dim_out:
            self.shortcut.append(norm(dim_in))
            self.shortcut.append(nn.Linear(dim_in, dim_out))
        self.shortcut = nn.Sequential(*self.shortcut)

        self.norm1 = norm(dim_in)
        self.attn = attn(dim_in, dim_out, heads=heads, dim_head=dim_head, dropout=dropout, )
        self.sd1 = DropPath(sd) if sd > 0.0 else nn.Identity()

        self.norm2 = norm(dim_out)
        self.ff = FeedForward(dim_out, dim_mlp, dim_out, dropout=dropout, f=f, activation=activation)
        self.sd2 = DropPath(sd) if sd > 0.0 else nn.Identity()

    def forward(self, x, mask=None):
        skip = self.shortcut(x)
        x = self.norm1(x)
        x, attn = self.attn(x, mask=mask)
        x = self.sd1(x) + skip

        skip = x
        x = self.norm2(x)
        x = self.ff(x)
        x = self.sd2(x) + skip

        return x




class PatchEmbdding(nn.Module):
    def __init__(self, spectra_size, patch_size, dim_out, channel=1):
        super(PatchEmbdding, self).__init__()
        if not spectra_size % patch_size == 0:
            raise Exception('Spectra dimensions must be divisible by the patch size!')
        patch_dim = channel * patch_size
        self.patch_embedding = nn.Sequential(
            Rearrange('b c (d p) -> b d (p c)', p=patch_size), #16 384 16
            nn.LayerNorm(patch_dim),
            nn.Linear(patch_dim, dim_out),
        )

    def forward(self, x):
        x = self.patch_embedding(x)
        return x


class CLSToken(nn.Module):
    def __init__(self, dim):
        super(CLSToken, self).__init__()
        self.cls_token = nn.Parameter(torch.randn(1, 1, dim) * 0.02)

    def forward(self, x):
        b, n, _ = x.shape
        cls_tokens = repeat(self.cls_token, '() n d -> b n d', b=b)
        x = torch.cat((cls_tokens, x), dim=1)
        return x


class AbsPosEmbedding(nn.Module):
    def __init__(self, spectra_size, patch_size, dim, stride=None, cls=True):
        super(AbsPosEmbedding, self).__init__()
        if not spectra_size % patch_size == 0:
            raise Exception('Spectra dimensions must be divisible by the patch size!')
        stride = patch_size if stride is None else stride
        output_size = self._conv_output_size(spectra_size, patch_size, stride)
        num_patches = output_size * 1
        self.pos_embedding = nn.Parameter(torch.randn(1, num_patches + int(cls), dim) * 0.02)

    def forward(self, x):
        x = x + self.pos_embedding
        return x

    @staticmethod
    def _conv_output_size(spectra_size, kernel_size, stride, padding=0):
        return int(((spectra_size - kernel_size + (2 * padding)) / stride) + 1)


class ViT(nn.Module):
    def __init__(self, spectra_size, patch_size, num_classes, dim, depth, heads, dim_mlp, channel=2, dim_head=16,
                 dropout=0.0, emb_dropout=0.0, sd=0.0, embedding=None, classifier=None, name='vit', **block_kwargs):
        super(ViT, self).__init__()
        self.name = name
        self.embedding = nn.Sequential(
            PatchEmbdding(spectra_size=spectra_size, patch_size=patch_size, dim_out=dim, channel=channel),
            CLSToken(dim=dim),
            AbsPosEmbedding(spectra_size=spectra_size, patch_size=patch_size, dim=dim, cls=True),
            nn.Dropout(emb_dropout) if emb_dropout > 0.0 else nn.Identity(),
        ) if embedding is None else embedding

        self.transformers = []
        for i in range(depth):
            self.transformers.append(
                Transformer(dim, heads=heads, dim_head=dim_head, dim_mlp=dim_mlp, dropout=dropout,
                            sd=(sd * i / (depth - 1)))
            )
        self.transformers = nn.Sequential(*self.transformers)

        self.classifier = nn.Sequential(
            # Lambda(lambda x: x[:, 0]),
            nn.Linear(dim, num_classes),
            nn.LayerNorm(num_classes)

        ) if classifier is None else classifier

    def forward(self, x):
        # x = x.unsqueeze(1)
        x = self.embedding(x)
        x = self.transformers(x)
        x = x[:, 0]
        x = self.classifier(x)

        return x


out_features_dim = 96


class Neural_receiver(nn.Module):
    def __init__(self,subcarriers, timesymbols, streams, num_bits_per_symbol):
        super(Neural_receiver, self).__init__()
        self.subcarriers = subcarriers
        self.timesymbols = timesymbols
        self.streams = streams
        self.num_bits_per_symbol = num_bits_per_symbol
        self.conv1 = nn.Conv2d(self.subcarriers, out_features_dim, kernel_size=2, padding='same')
        self.mlp = ViT(spectra_size=out_features_dim * 96, patch_size=96, num_classes=self.streams*self.timesymbols*self.subcarriers*self.num_bits_per_symbol,
                       dim=256, depth=10, heads=4, dim_mlp=512, channel=2, dim_head=32)

    def forward(self, x, pilot):
        batch_size = x.shape[0]
        y = torch.cat((x, pilot), dim=-1)  # (16 624 12 8) (16 96 12 16)
        # 256 个数，16接收天线*2（导频/数据）*2（实数/虚数）
        # x = x.reshape(batch_size, 256, 16,2,2)
        y = torch.reshape(y, (batch_size, 2, -1)) #16 192 96 #16 96 624

        out = self.mlp(y)
        out = out.view(batch_size,self.streams, self.timesymbols, self.subcarriers, self.num_bits_per_symbol)        # out = super().forward(x)
        # out = torch.reshape(out (batch_size, self.streams, self.timesymbols, self.subcarriers, self.num_bits_per_symbol))
        return out

if __name__ == '__main__':
    y = torch.randn(16, 4, 12, 96, 2)
    template_pilot = torch.randn(16, 4, 12, 96, 2)  # 不再需要此参数，已更改模型结构
    model = Neural_receiver(96, 12, 4, 6)
    # y = torch.randn(16, 2, 12, 624, 2)
    # template_pilot = torch.randn(16, 2, 12, 624, 2)
    # model = Neural_receiver(624, 12, 2, 4)
    out = model(y, template_pilot)
    print(out.shape)