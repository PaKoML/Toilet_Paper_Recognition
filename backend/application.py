from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
app = Flask(__name__)

@app.route('/upload')
def upload_file():
    return render_template('file_upload.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file_get() :
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))
        return 'file upload successfully'
    
if __name__ == '__main__' : 
    app.run(host = '0.0.0.0')