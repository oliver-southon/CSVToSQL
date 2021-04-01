from app import app
from flask import Flask, render_template, flash, request, redirect, url_for
import os
from werkzeug.utils import secure_filename
from create_db import *
from file_read_backwards import FileReadBackwards
import urllib.request

ALLOWED_EXTENSIONS = set(['csv'])

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def upload_form():
    return render_template('upload.html')

@app.route('/', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('File uploaded successfully.')
            filepath = (str('uploads/' + filename))
            makeDB(filepath)
            # with FileReadBackwards('dump.sql') as f:
            #     b_lines = [ row for row in f]

            with open(sql_name, 'r') as f:
                content = f.read()
 
            return render_template("upload.html", content=content)
        else:
            flash('Only CSV files are allowed')
            return redirect(request.url)
    # return render_template('test.html', b_lines=b_lines)



if __name__ == "__main__":
    
    app.run()