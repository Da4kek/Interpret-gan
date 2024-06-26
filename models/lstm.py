import numpy as np
import torch.backends.cudnn as cudnn
import torch.optim
import torch.nn.functional as F
import torch.nn as nn
from torch.autograd import Variable
from torchvision import transforms, datasets
import sys
import os
import random
import math
import time
import torch
torch.utils.backcompat.broadcast_warning.enabled = True
cudnn.benchmark = True


class Model(nn.Module):

    def __init__(self, input_size=128, lstm_size=128, lstm_layers=1, output_size=128):
        # Call parent
        super().__init__()
        # Define parameters
        self.input_size = input_size
        self.lstm_size = lstm_size
        self.lstm_layers = lstm_layers
        self.output_size = output_size

        # Define internal modules
        self.lstm = nn.LSTM(input_size, lstm_size,
                            num_layers=lstm_layers, batch_first=True)
        self.output = nn.Linear(lstm_size, output_size)
        self.classifier = nn.Linear(output_size, 40)

    def forward(self, x):
        # Prepare LSTM initiale state
        batch_size = x.size(0)
        lstm_init = (torch.zeros(self.lstm_layers, batch_size, self.lstm_size),
                     torch.zeros(self.lstm_layers, batch_size, self.lstm_size))
        if x.is_cuda:
            lstm_init = (lstm_init[0].cuda(), lstm_init[0].cuda())
        lstm_init = (Variable(lstm_init[0], volatile=x.volatile), Variable(
            lstm_init[1], volatile=x.volatile))

        # Forward LSTM and get final state
        x = self.lstm(x, lstm_init)[0][:, -1, :]

        # Forward output
        x = F.relu(self.output(x))
        x = self.classifier((x))
        return x
