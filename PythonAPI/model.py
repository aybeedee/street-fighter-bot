import torch
from torch import nn

class Model1(nn.Module):
    def __init__(self):
        super(Model1, self).__init__()

        self.layer1 = nn.Linear(25, 30)
        self.a1 = nn.LeakyReLU()
        self.layer2 = nn.Linear(30, 30)
        self.a2 = nn.Sigmoid()
        self.layer3 = nn.Linear(30, 1)

    def forward(self, x):

        x = self.layer1(x)
        x = self.a1(x)
        x = self.layer2(x)
        x = self.a2(x)
        x = self.layer3(x)
        x = torch.sigmoid(x)
    
        return x
    
class Model2(nn.Module):
    def __init__(self):
        super(Model2, self).__init__()

        self.layer1 = nn.Linear(25, 20)
        self.a1 = nn.LeakyReLU()
        self.layer2 = nn.Linear(20, 1)

    def forward(self, x):

        x = self.layer1(x)
        x = self.a1(x)
        x = self.layer2(x)
        x = torch.sigmoid(x)
    
        return x
    
class Model3(nn.Module):
    def __init__(self):
        super(Model3, self).__init__()

        self.layer1 = nn.Linear(24, 20)
        self.a1 = nn.LeakyReLU()
        self.layer2 = nn.Linear(20, 1)

    def forward(self, x):

        x = self.layer1(x)
        x = self.a1(x)
        x = self.layer2(x)
        x = torch.sigmoid(x)
    
        return x
    
class Model4(nn.Module):
    def __init__(self):
        super(Model4, self).__init__()

        self.layer1 = nn.Linear(24, 30)
        self.a1 = nn.LeakyReLU()
        self.layer2 = nn.Linear(30, 30)
        self.a2 = nn.Sigmoid()
        self.layer3 = nn.Linear(30, 1)

    def forward(self, x):

        x = self.layer1(x)
        x = self.a1(x)
        x = self.layer2(x)
        x = self.a2(x)
        x = self.layer3(x)
        x = torch.sigmoid(x)
    
        return x