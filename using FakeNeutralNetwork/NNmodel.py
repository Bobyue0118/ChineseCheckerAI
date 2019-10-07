import pdb

import sys
import os

import random
import numpy as np
from collections import deque
import torch
from torch.autograd import Variable
import torch.nn as nn


class StateNet(nn.Module):
    def __init__(self,):
        super(StateNet,self).__init__()
        #input [4, 3, 10, 10] [B, S, H, W]
        self.conv1 = nn.Sequential(
            nn.Conv2d(in_channels=3, out_channels=12, kernel_size=4, stride=2, padding=1),
            nn.ReLU(inplace=True)
        )  # torch.Size([4, 12, 5, 5])
        self.conv2 = nn.Sequential(
            nn.Conv2d(in_channels=12, out_channels=6, kernel_size=4, stride=1, padding=0),
            nn.ReLU(inplace=True)
        )  # torch.Size([4, 6, 2, 2])

        self.fc1 = nn.Sequential(
            nn.Linear(24,12),
            nn.ReLU()
        )
        self.out = nn.Linear(12,1)

    def forward(self, x):
        x = self.conv1(x)
        x = self.conv2(x)
        x = x.view(x.size(0),-1)
        x = self.fc1(x)
        return self.out(x)
