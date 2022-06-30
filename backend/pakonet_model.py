from torch import nn
import torch

class PaKoNet(nn.Module) :
    def __init__(self) :
        super(PaKoNet, self).__init__()
        self.VGGNet = nn.Sequential(
            nn.Conv2d(3,64,3, stride = 1, padding = 1),
            nn.ELU(),
            nn.Conv2d(64,64,3, stride = 1, padding = 1),
            nn.ELU(),
            nn.MaxPool2d(kernel_size = 3, stride = 2, padding = 1),
            
            nn.Conv2d(64, 128,3, stride = 1, padding = 1),
            nn.ELU(),
            nn.Conv2d(128, 128,3, stride = 1, padding = 1),
            nn.ELU(),
            nn.MaxPool2d(kernel_size = 3, stride = 2, padding = 1),
            
            nn.Conv2d(128,256, 3, stride = 1, padding = 1),
            nn.ELU(),
            nn.Conv2d(256,256, 3, stride = 1, padding = 1),
            nn.ELU(),
            nn.Conv2d(256,256, 3, stride = 1, padding = 1),
            nn.ELU(),
            nn.MaxPool2d(kernel_size = 3, stride = 2, padding = 1),
            
            nn.Conv2d(256,512, 3, stride = 1, padding = 1),
            nn.ELU(),
            nn.Conv2d(512,512, 3, stride = 1, padding = 1),
            nn.ELU(),
            nn.Conv2d(512,512, 3, stride = 1, padding = 1),
            nn.ELU(),
            nn.MaxPool2d(kernel_size = 3, stride = 2, padding =1),
            
            nn.Conv2d(512,512, 3, stride = 1, padding = 1),
            nn.ELU(),
            nn.Conv2d(512,512, 3, stride = 1, padding = 1),
            nn.ELU(),
            nn.Conv2d(512,512, 3, stride = 1, padding = 1),
            nn.ELU(),
            nn.MaxPool2d(kernel_size = 3, stride = 2, padding =1)
        )
        
        self.bbox_regressor = nn.Sequential(
            nn.Flatten(),
            nn.Linear(in_features = 7*7*512, out_features = 4096),
            nn.ELU(),
            nn.Linear(in_features=4096, out_features = 1024),
            nn.ELU(),
            nn.Linear(in_features=1024, out_features = 64),
            nn.ELU(),
            nn.Linear(in_features=64, out_features = 4),
        )
        
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(in_features = 7*7*512, out_features = 4096),
            nn.ELU(),
            nn.Linear(in_features=4096, out_features = 1024),
            nn.ELU(),
            nn.Linear(in_features=1024, out_features = 64),
            nn.ELU(),
            nn.Linear(in_features=64, out_features = 3),
        )
    
    def forward (self, x ) :
        x = self.VGGNet(x)
        return self.bbox_regressor(x), self.classifier(x)
