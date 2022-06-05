from data_class import LBData
import numpy as np
import pandas as pd
import torch
from torch.utils.data import Dataset
from torch.utils.data import DataLoader
import matplotlib.pyplot as plt
from torch import nn
from torchvision import transforms

# Setting Field
image_size = (224,224)

dc_data = LBData()

class CustomDataset(Dataset) :
    def __init__(self, data) :
        
        data_list, bbox_list, category_list = [],[],[]
        self.x_mean, self.x_std = [], []
        
        for i in range (data.get_len()) :
            if(dc_data.get_admission(i)) :
                data.resize_image(i, image_size)
                processed_image = data.get_image(i)
                processed_image = transforms.ToTensor()(data.get_image(i))
                data_list.append(processed_image)
                bbox_list.append(torch.Tensor(dc_data.get_bbox(i)))
                category_list.append(self.category_mapping(dc_data.get_class(i)))
        
        self.x = torch.stack(data_list)
        
        for i in range( 3 ) : #by channel / normalization
            self.x_mean.append(self.x[:][i][:][:].mean())
            self.x_std.append(self.x[:][i][:][:].std())
            self.x[:][i][:][:] -= self.x_mean[i]
            self.x[:][i][:][:] /= self.x_std[i]
        
        self.bbox = torch.stack(bbox_list)
        self.category = torch.stack(category_list)
        
    def category_mapping(self, category) :
        one_hot_category = torch.zeros(3);
        if(category == 'over') :
            one_hot_category[1] = 1;
        elif(category == 'under') :
            one_hot_category[2] = 1;
        else :
            one_hot_category[0] = 1;
        return one_hot_category;
    
    def __getitem__(self, idx) :
        return self.x[idx], self.bbox[idx], self.category_mapping(self.category[idx]);
    
    def __len__(self) :
        return len(self.x)
    
    
bs = 5;
bn_params = 10;

train_dataset = CustomDataset(dc_data)
train_dataloader = DataLoader(train_dataset, batch_size = bs , shuffle = True)

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
    
    def forward (self, x ) :
        x = self.VGGNet(x)
        return self.bbox_regressor(x)

def train(dataloader, model, loss_fn, optimizer) :
    size = len(dataloader.dataset)
    train_loss, cnt = 0, 0
    for batch, (X, bbox, category), in enumerate(dataloader):
        pred = model.forward(X)
        ans =  np.concatenate([bbox], axis=1).tolist()
        
        loss =loss_fn(pred, torch.Tensor(ans))
        train_loss += loss;
        cnt+=1;
        train_loss_log.append(loss.detach().item());
        
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        scheduler.step()
        
        
        if(batch%2==0) :
            loss, current = loss.item(), batch * len(X)
            print(f"loss: {loss:>7f} [{current:>5d}/{size:>5d}] / current lr : {scheduler.get_last_lr()}")
    
    train_loss /= cnt;
    print(f"average loss: {train_loss:>7f}")
    
            
def test(dataloader, model, loss_fn) :
    size = len(dataloader.dataset)
    num_batches = len(dataloader)
    model.eval()
    val_loss, correct =0, 0
    with torch.no_grad():
        for X, bbox, category in dataloader:
            
            pred = model.forward(X)
            ans =  np.concatenate([bbox, category], axis=1).tolist()
            
    val_loss /= num_batches
    correct /= size
    accuracy_log.append(100*correct);
    print(f"val Error : \n Accuracy: { (100*correct) : >0.1f}% Avg loss : {val_loss :>8f}\n")


model = PaKoNet()
loss_fn = nn.MSELoss()

optimizer = torch.optim.Adam(model.parameters(), lr =1e-4)
scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=len(train_dataloader)*50, gamma=0.1)

epochs= 150

train_loss_log = []
accuracy_log = []


for t in range(epochs) :
    print(f"Epoch {t+1}\n-------------------------------------")
    train(train_dataloader, model, loss_fn, optimizer)
    #test(train_dataloader, model, loss_fn)
    
print("Done!")

fig, ax = plt.subplots()
plt.xlabel('step')

ax.plot(train_loss_log)
ax.set_ylabel("loss")
ax2 = ax.twinx()
#ax2.plot(np.linspace(1,bs*epochs,len(accuracy_log)), accuracy_log, color="red", marker="o")
ax2.set_ylabel("accuracy")
plt.savefig("naive.jpg")
plt.show()

from PIL import Image, ImageDraw
from torchvision.transforms import ToTensor, ToPILImage

def test_image(dataloader, model, loss_fn) :
    size = len(dataloader.dataset)
    num_batches = len(dataloader)
    model.eval()
    val_loss, correct =0, 0
    with torch.no_grad():
        for X, bbox, category in dataloader:
            
            pred = model.forward(X).squeeze()
            ans =  np.concatenate([bbox], axis=1).tolist()[0]
            
            img = ToPILImage()(X.squeeze())
            
            draw = ImageDraw.Draw(img)
            draw.rectangle((pred[0]*img.size[0], pred[1]*img.size[1], pred[2]*img.size[0], pred[3] * img.size[1]), outline=(0,255,0), width = 1)
            draw.rectangle((ans[0]*img.size[0], ans[1]*img.size[1], ans[2]*img.size[0], ans[3] * img.size[1]), outline=(255,0,0), width = 1)
            display(img)
            
            print ('pred : ' , pred ,'\n\nans : ', ans)
            print(np.shape(pred), np.shape(torch.Tensor(ans)))
            loss_test = nn.MSELoss()
            print (f'loss : {loss_test(pred,torch.Tensor(ans)) : >8f}')
            
    val_loss /= num_batches
    correct /= size
    accuracy_log.append(100*correct);
    print(f"val Error : \n Accuracy: { (100*correct) : >0.1f}% Avg loss : {val_loss :>8f}\n")
    
val_dataloader = DataLoader(train_dataset, batch_size = 1 , shuffle = True)
test_image(val_dataloader, model, loss_fn)