from flask import Flask
import os
import shutil

if os.path.exists('./uploads/'):
    shutil.rmtree('./uploads')

os.mkdir('./uploads')

UPLOAD_FOLDER = './uploads'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = str(os.environ.get('DB_SK'))

