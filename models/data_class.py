import labelbox
import requests
import io
import PIL
import numpy as np
import pandas as pd
from pprint import pprint
from PIL import Image, ImageDraw

class LBData:
    def __init__(self):
        
        # setting field
        end_time = "2022-05-24"
        #####
        
        print("initializing...")
        
        # load project data
        LB_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiJjbDM3M2ExYjdtb214MDg4eGN0dHM4eGFiIiwib3JnYW5pemF0aW9uSWQiOiJjbDM3M2ExYXZtb213MDg4eGZjb2EwYW05IiwiYXBpS2V5SWQiOiJjbDNjYWd2dnAxZmJ1MDc4dmFtcTdiOTV1Iiwic2VjcmV0IjoiNWMyMGM3ZmQxYWVkYTQ1NDBlNmMxODJiZjE5YzVhZWMiLCJpYXQiOjE2NTI5MjA5NzEsImV4cCI6MjI4NDA3Mjk3MX0.Z3EZFFbUvRLzSAWfL_VnOqZvU4ozVX3wm2M2rC5MofQ"
        lb = labelbox.Client(api_key=LB_API_KEY)

        project = lb.get_project('cl373dszln9yt06b84hf92ozm')
        self.labels = project.export_labels(download = True, start="2022-05-13", end=end_time)
        
        self.img = [];
        print("loading images...");
        self.load_image();
        print("loading images done !")
        
        self.bbox = ['n/a' for i in range (len(self.labels))]
        
        print("Loading bounding boxes... ")
        for i in range (self.get_len()) :
            if(self.get_admission(i)) : 
                self.load_bbox(i);
        print("Loading bounding boxes done !")
            
        
        
    
    def get_admission(self, idx):
        if(len(self.labels[idx]['Reviews'])==0 or self.labels[idx]['Reviews'][0]['score']!=1 or self.labels[idx]['Skipped']):
            return False;
        else :
            #print(idx , 'has admission')
            return True;
    
    def load_image(self):
        # load image 
        for i in range (self.get_len()) :
            
            if(i % 20  == 0) :
                print(f"loading images ... {i}/{len(self.labels)} done.")
            
            response = requests.get(self.labels[i]['Labeled Data'])
            image_bytes = io.BytesIO(response.content)

            self.img.append(PIL.Image.open(image_bytes))
            
    
    def get_image(self, idx):
        return self.img[idx];
    
    def get_class(self, idx):
        return self.labels[idx]['Label']['classifications'][0]['answer']['title']
    
    def load_bbox(self, idx):
        x0 = self.labels[idx]['Label']['objects'][0]['bbox']['left']
        y0 = self.labels[idx]['Label']['objects'][0]['bbox']['top']
        x1 = x0 + self.labels[idx]['Label']['objects'][0]['bbox']['width']
        y1 = y0 + self.labels[idx]['Label']['objects'][0]['bbox']['height']
        
        x0 /= self.img[idx].size[0]
        x1 /= self.img[idx].size[0]
        y0 /= self.img[idx].size[1]
        y1 /= self.img[idx].size[1]
        
        self.bbox[idx] = [x0, y0, x1, y1]
        return self.bbox[idx];
    
    def get_bbox(self, idx):
        return self.bbox[idx];
    
    def resize_image(self, idx, size_to, option = 0) :
        #print(f'current idx : {idx}')
        self.img[idx] = self.img[idx].resize(size_to, 0);
        return self.img[idx];
        
    def get_len(self) :
        return len(self.labels);
    
    def test(self,idx): # for debugging
        print (self.labels[idx])
        
    def draw_image(self, idx) : # for debugging
        bbox = self.get_bbox(idx)
        img = self.get_image(idx)
        draw = ImageDraw.Draw(img)
        draw.rectangle((bbox[0]*img.size[0], bbox[1]*img.size[1], bbox[2]*img.size[0], bbox[3] * img.size[1]), outline=(0,255,0), width = 1)
        display(img)