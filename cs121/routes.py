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
        # run prediction
        try:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                save_to=(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                file.save(save_to)
            
                #load in emotion detection model, load result into pred_class
                pred_class=predictor.model_predict(save_to, '/home/ubuntu/cs121/app')
            
                #create array of generated info
                pred_array = getSongData(pred_class)
                pred_emotion = pred_array[0]
                pred_caption = pred_array[1]
                pred_song = pred_array[2]
                pred_artist = pred_array[3]
            
                #send generated info to displayResult
                return render_template('displayResult.html', filename=filename, 
                                       prediction=pred_emotion, caption=pred_caption, 
                                       song=pred_song, artist=pred_artist)
            # if entry is too large, reload page
            except:
                return render_template('index.html')
    return render_template('index.html')

#get song data from matching song database csv
def generate_caption(pred_class):
    if pred_class == 'happy':
        return getSongData('/home/ubuntu/cs121/app/databases/happysongs.csv')
    if pred_class == 'sad':
        return getSongData('/home/ubuntu/cs121/app/databases/sadsongs.csv')
    if pred_class == 'angry':
       return getSongData('/home/ubuntu/cs121/app/databases/angrysongs.csv')
    if pred_class == 'neutral':
       return getSongData('/home/ubuntu/cs121/app/databases/neutralsongs.csv')

#parse appropriate song database, return array of generated info
def getSongData(fileName):
    with open(fileName, mode='r') as csvFile:
        reader = csv.reader(csvFile, delimiter=',')
        csvlist = [r for r in reader]
        row_count = len(csvlist)
        
        #generate random value in range of number of songs in database
        randValue = random.randint(0,row_count+1)
        
        #pull random row from database and store info
        title = csvlist[randValue][0]
        artist = csvlist[randValue][1]
        lyric = csvlist[randValue][2]
        
        #create and return array of generated caption info
        songArray = [lyric, title, artist]
        return songArray

# allowed image types
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
app.config['ALLOWED_EXTENSIONS']=ALLOWED_EXTENSIONS

# is file allowed to be uploaded?
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']
