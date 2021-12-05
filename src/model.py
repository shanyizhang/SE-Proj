## ----------------------------------------
##   Software Engineering @ NYU
##   Course Project - Tetris Game
##   Ken S. Zhang & Qingyang Li
## ----------------------------------------


from numpy.lib.arraypad import pad
import torch.nn as nn
import torch.nn.functional as F 
import numpy as np
from config import ROW, COLUMN
from tetro import L


class CNNModel(nn.Module):
    def __init__(self, num_class):
        """
        Init the CNN Model
        Input: Number of types of tetromino
        Output: None
        """
        super(CNNModel, self).__init__()
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
        

class DeterministicModel(object):
    def __init__(self, num_class):
        self.num_class = num_class
        self.length = 4

    def predict(self, x, crop=True):
        if crop:
            bottom_index = 0
            for _ in range(len(x)):
                if np.any(x[_]):
                    bottom_index = _
                    break
            if bottom_index >= ROW - (self.length-1):
                bottom_index = ROW - self.length
            bottom = x[bottom_index:bottom_index+self.length]
        else:
            bottom = x
        padded_bottom = list()
        for i in range(self.length):
            line = bottom[i]
            padded_line = np.append([1.,], line)
            padded_line = np.append(padded_line, [1.,])
            padded_bottom.append(padded_line)
        padded_bottom.append([1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.])
        padded_bottom = np.array(padded_bottom) # 5 x 12
        exclude = list()
        try:
            for i in range(self.length):
                for j in range(COLUMN+1):
                    if i != self.length-1 and j > 0 and j < COLUMN-1:
                        # Detect T
                        if padded_bottom[i][j] + padded_bottom[i][j+1] + padded_bottom[i][j+2] + padded_bottom[i+1][j+1] == 0 and \
                            padded_bottom[i+1][j] + padded_bottom[i+1][j+2] == 2:
                            exclude.append(6)         
                    if i < self.length and j > 0 and j < COLUMN-1:
                        # Detect J & L
                        if padded_bottom[i][j] + padded_bottom[i][j+1] + padded_bottom[i][j+2] == 0 and \
                            padded_bottom[i+1][j] + padded_bottom[i+1][j+1] + padded_bottom[i+1][j+2] == 3 and \
                            padded_bottom[i][j-1] + padded_bottom[i][j+3] > 0:
                            exclude.append(4)
                            exclude.append(5)
                    if i == 0 and j > 1 and j < COLUMN+1:
                        # Detect I
                        if padded_bottom[i][j] + padded_bottom[i+1][j] + padded_bottom[i+2][j] + padded_bottom[i+3][j] == 0:
                            exclude.append(2)                    
                    if i != self.length-1 and j > 0 and j < COLUMN:
                        # Detect O
                        if padded_bottom[i][j] + padded_bottom[i][j+1] + padded_bottom[i+1][j] + padded_bottom[i+1][j+1] == 0 and \
                            padded_bottom[i][j-1] + padded_bottom[i+1][j-1] + padded_bottom[i][j+2] + padded_bottom[i+1][j+2] == 4:
                            exclude.append(3)     
        except Exception as _:
            return  np.unique(exclude)
        return np.unique(exclude)

    