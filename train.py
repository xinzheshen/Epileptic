import torch
from model import DCNN

x = torch.randn(10, 1, 1280, 23)
y = DCNN()(x)
print(y.size())