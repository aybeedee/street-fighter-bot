import torch
from torch import nn

class Model(nn.Module):
    def __init__(self):
        super(Model, self).__init__()

        self.layer1 = nn.Linear(24, 30)
        self.a1 = nn.ReLU()
        self.layer2 = nn.Linear(30, 15)
        self.a2 = nn.ReLU()
        self.layer3 = nn.Linear(15, 10)
        self.a3 = nn.Sigmoid()
        self.layer4 = nn.Linear(10, 2)

        
    def forward(self, x):
        x = self.layer1(x)
        x = self.a1(x)
        x = self.layer2(x)
        x = self.a2(x)
        x = self.layer3(x)
        x = self.a3(x)
        x = self.layer4(x)

        return x
    
rKeyModel = torch.load("models/B.pt")
rKeyModel.eval()

print("speed test")

input_features = [
	35,
	1,
	0,
	176,
	158,
	192,
	3,
	124,
	192,
	0,
	0,
	0,
	0,
	0,
	0,
	0,
	0,
	0,
	0,
	0,
	0,
	0,
    0,
    -34
]
input_tensor = torch.tensor([input_features]).float()
onePred = rKeyModel(input_tensor)
_, predicted = torch.max(onePred.data, 1)
print(predicted)