import labelbox
import requests
import io
import PIL
import numpy as np
import pandas as pd
from pprint import pprint
from PIL import Image, ImageDraw

class Data:
    def __init__(self):
        print("initializing...")
        
        # endtime must be set
        end_time = "2022-05-19"
        
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
        
    
    def get_admission(self, idx):
        if(len(self.labels[idx]['Reviews'])==0 or self.labels[idx]['Reviews'][0]['score']!=1 ):
            return False;
        else :
            return True;
    
    def load_image(self):
        # load image 
        for i in range (len(self.labels)) :
            
            if(i % 10 == 0) :
                print(f"loading images ... {i}/{len(self.labels)} done.")
            response = requests.get(self.labels[i]['Labeled Data'])
            image_bytes = io.BytesIO(response.content)

            self.img.append(PIL.Image.open(image_bytes))
    
    def get_image(self, idx):
        return self.img[idx];
    
    def get_class(self, idx):
        return self.labels[idx]['Label']['classifications'][0]['answer']['title']
    
    def get_bbox(self, idx):
        top = self.labels[idx]['Label']['objects'][0]['bbox']['top']
        left = self.labels[idx]['Label']['objects'][0]['bbox']['left']
        bottom = top + self.labels[idx]['Label']['objects'][0]['bbox']['height']
        right = left + self.labels[idx]['Label']['objects'][0]['bbox']['width']
        
        top /= self.img[idx].size[1]
        bottom /= self.img[idx].size[1]
        left /= self.img[idx].size[0]
        right /= self.img[idx].size[0]
        
        self.bbox[idx] = [left, top, right, bottom]
        return self.bbox[idx];
    
    def resize_image(self, idx, x_size, y_size, option = 0) :
        self.img[idx] = self.img[idx].resize((x_size, y_size), 0);
        return self.img[idx];
        
    def test(self):
        pass;