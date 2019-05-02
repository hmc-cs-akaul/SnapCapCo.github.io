from flask import render_template, redirect, url_for, request, send_from_directory, flash
from app import app
import os
from werkzeug import secure_filename
from app import predictor
import csv

@app.route('/<filename>')
def get_file(filename):
    return send_from_directory('templates',filename)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            save_to=(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file.save(save_to)
            pred_class=predictor.model_predict(save_to, '/home/ubuntu/cs121/app')
            lyric_caption = generate_caption(pred_class)
            # lyric_caption = "caption here" 
            return render_template('displayResult.html', filename=filename, prediction=pred_class, caption=lyric_caption)
    return render_template('index.html')


def generate_caption(pred_class):
    # classes = ['happy', 'sad', 'disgusted', 'angry']
    # pred_class = classes[pred_idx]
    if pred_class == 'happy':
       # return "happy caption"
        return getSongData('/home/ubuntu/cs121/app/happysongs.csv')
    if pred_class == 'sad':
       # return "sad caption"
        return getSongData('/home/ubuntu/cs121/app/sadsongs.csv')
    if pred_class == 'angry':
        return "angry caption"
       # return getSongData('/home/ubuntu/cs121/app/angrysongs.csv')
    if pred_class == 'disgusted':
        return "disgusted caption"
       # return getSongData('/home/ubuntu/cs121/app/disgustedsongs.csv')
    else:
        return "could not find database to grab caption"

def getSongData(fileName):
    with open(fileName, mode='r') as csvFile:
        return fileName
        reader = csv.reader(csvFile, delimiter=',')
        for r in reader:
            return r[0]
        #return "created reader obj"
        # row_count = sum(1 for row in reader)
       # csvlist = list(reader)
        csvlist = [r for r in reader]
        return "made list"
        row_count = len(csvlist)
        
        return "made row_count"
        randValue = random.randint(0,row_count+1)
        title = csvlist[randValue][0]
        artist = csvlist[randValue][1]
        lyric = csvlist[randValue][2]
        songTuple = (title, artist, lyric)
        return lyric

# allowed image types
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
app.config['ALLOWED_EXTENSIONS']=ALLOWED_EXTENSIONS

# is file allowed to be uploaded?
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']
