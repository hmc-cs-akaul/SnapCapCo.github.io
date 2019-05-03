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
            pred_array = [pred_class] + getSongData(pred_class)
            pred_emotion = pred_array[0]
            pred_caption = pred_array[1]
            pred_song = pred_array[2]
            pred_artist = pred_array[3]
            return render_template('displayResult.html', filename=filename, prediction=pred_emotion, caption=pred_caption, song=pred_song, artist=pred_artist)
    return render_template('index.html')

def generate_caption(pred_class):
    if pred_class == 'happy':
        return getSongData('/home/ubuntu/cs121/app/databases/happysongs.csv')
    if pred_class == 'sad':
        return getSongData('/home/ubuntu/cs121/app/databases/sadsongs.csv')
    if pred_class == 'angry':
       return getSongData('/home/ubuntu/cs121/app/databases/angrysongs.csv')
    if pred_class == 'neutral':
       return getSongData('/home/ubuntu/cs121/app/databases/neutralsongs.csv')

def getSongData(fileName):
    with open(fileName, mode='r') as csvFile:
        return fileName
        reader = csv.reader(csvFile, delimiter=',')
        csvlist = [r for r in reader]
        row_count = len(csvlist)
        
        randValue = random.randint(0,row_count+1)
        title = csvlist[randValue][0]
        artist = csvlist[randValue][1]
        lyric = csvlist[randValue][2]
        songArray = [lyric] + [title] + [artist]
        return songArray

# allowed image types
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
app.config['ALLOWED_EXTENSIONS']=ALLOWED_EXTENSIONS

# is file allowed to be uploaded?
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']
