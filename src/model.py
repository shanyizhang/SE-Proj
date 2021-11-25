## ----------------------------------------
##   Software Engineering @ NYU
##   Course Project - Tetris Game
##   Ken S. Zhang & Qingyang Li
## ----------------------------------------


import torch.nn as nn
import torch.nn.functional as F 


class Model(nn.Module):
    def __init__(self, num_class):
        """
        Init the CNN Model
        Input: Number of types of tetromino
        Output: None
        """
        super(Model, self).__init__()
        self.layer1 = nn.Conv2d(1, 64, kernel_size=3, stride=1, padding=1, bias=True)
        self.layer2 = nn.Conv2d(64, 64, kernel_size=3, stride=1, padding=1, bias=True)
        self.layer3 = nn.Conv2d(64, 64, kernel_size=3, stride=1, padding=1, bias=True)
        self.layer4 = nn.Linear(20*10*64, num_class)

    def forward(self, x):
        """
        Implement the forward propagation 
        Input: Input feature
        Output: Prediction
        """
        y = F.relu(self.layer1(x))
        y = F.relu(self.layer2(y))
        y = self.layer3(y)
        y = y.flatten()
        y = self.layer4(y)
        return F.softmax(y, dim=0)
        