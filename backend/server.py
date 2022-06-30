import os
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import numpy as np
import cv2
import torch
from torchvision import transforms
from torchvision.transforms import ToTensor, ToPILImage
from IPython.display import display 
from PIL import Image, ImageDraw

from pakonet_model import PaKoNet

UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif', 'pt'}
MEMORY_ROUTE = './memory/'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

model = PaKoNet()
model.load_state_dict(torch.load("tissue_model.pt"))
model.eval()
print(model)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def transform_image(in_image) :
    input_transforms = [
        transforms.Resize((224,224)),
        transforms.ToTensor(),
        transforms.Normalize([0.5234, 0.9585, 0.6256],[0.1797, 0.1135, 0.2118])
    ]
    my_transforms = transforms.Compose(input_transforms)
    image = Image.open(in_image)
    timg = my_transforms(image)
    print('before unsqueeze : ', np.shape(timg))
    timg = timg.unsqueeze(dim=0)
    print('after unsqueeze : ', np.shape(timg))
    return timg
    
def get_prediction(input_tensor) :
    bbox, category = model.forward(input_tensor)
    return bbox, category;
    
@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['file']
        
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        if not allowed_file(file.filename) :
            return 'only Jpeg type files are allowed'
        
        if file and allowed_file(file.filename):
            input_tensor = transform_image(file)
            print(np.shape(input_tensor))
            bbox, category = get_prediction(input_tensor)
            bbox = bbox[0]
            category = category[0]
            
            print(bbox, category)
            #file_type = type(file)
            #print(file_type, file.filename)
            #filename = secure_filename(file.filename)
            #file.save(os.path.join(MEMORY_ROUTE, secure_filename(file.filename)))
            
            #input_tensor = transform_image(file)
            img = transforms.ToTensor()(Image.open(file))
            img = ToPILImage()(img.squeeze())
            draw = ImageDraw.Draw(img)
            print(bbox, img.size)
            draw.rectangle((bbox[0]*img.size[0], bbox[1]*img.size[1], bbox[2]*img.size[0], bbox[3] * img.size[1]), outline=(0,255,0), width = 1)
            img.save(os.path.join('./static/','result.jpg'))
            flash(category[0].item());
            return result_show();
    return 

@app.route('/result')
def result_show():
    return render_template('result_show.html')

@app.route('/')
def index():
    return render_template('file_upload.html')


if __name__ == '__main__' :
    app.secret_key = 'temp'
    app.run(host = '0.0.0.0', debug = True)