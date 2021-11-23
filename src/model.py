## ----------------------------------------
##   Software Engineering @ NYU
##   Course Project - Tetris Game
##   Ken S. Zhang & Qingyang Li
## ----------------------------------------


import torch
import torch.nn as nn
import torch.nn.functional as F 
from config import NUM_TETRO


class Model(nn.Module):
    def __init__(self, num_class):
        super(Model, self).__init__()
        self.layer1 = nn.Conv2d(1, 64, kernel_size=3, stride=1, padding=1, bias=True)
        self.layer2 = nn.Conv2d(64, 64, kernel_size=3, stride=1, padding=1, bias=True)
        self.layer3 = nn.Conv2d(64, 64, kernel_size=3, stride=1, padding=1, bias=True)
        self.layer4 = nn.Linear(20*10*64, num_class)

    def forward(self, x):
        y = F.relu(self.layer1(x))
        y = F.relu(self.layer2(y))
        y = self.layer3(y)
        y = y.flatten()
        y = self.layer4(y)
        return F.softmax(y, dim=0)
    
if __name__ == '__main__': 
    model = Model(num_class=NUM_TETRO)
    input = torch.rand(size=(1, 1, 20, 10))
    print("Input Size:", input.shape)
    with torch.no_grad():
        out = model(input) 
        print("Output Size:", out.shape)
        print(out)