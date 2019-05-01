import os
import subprocess
import threading

from flask import Flask

from flask import render_template, redirect, url_for, request, send_from_directory, flash

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    UPLOAD_FOLDER = 'static/'

app = Flask(__name__, static_url_path='')
app.config.from_object(Config)

@app.route('/<filename>')
def get_file(filename):
    return send_from_directory('static',filename)

@app.route('/')
def get_index():
    return get_file('index.html')

def upload_file():
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
        # get the prediction from the model:
        pred_idx=predictor.model_predict(save_to, 'app')
        pred_class=generate_prediction(pred_idx)
        # now get the caption from the DB:
        lyric_caption=generate_caption(pred_idx)
        return render_template('displayResult.html', filename=filename, prediction=pred_class, caption=lyric_caption)

def generate_prediction(pred_idx):
    classes = ['happy', 'sad', 'disgusted', 'angry']
    pred_class = classes[pred_idx]
    return pred_class



# generate caption functions
def generate_caption(pred_idx):
    classes = ['happy', 'sad', 'disgusted', 'angry']
    pred_class = classes[pred_idx]
    if pred_class == 'happy':
        return getSongData('app/csv/happysongs.csv')
    if pred_class == 'sad':
        return getSongData('app/csv/sadsongs.csv')
    if pred_class == 'angry':
        return getSongData('app/csv/angrysongs.csv')
    if pred_class == 'disgusted':
        return getSongData('app/csv/disgustedsongs.csv')

# get caption from database
def getSongData(fileName):
    with open(fileName, mode='r') as csvFile:
        row_count = sum(1 for row in csvFile)
        randValue = random.randint(0,row_count+1)
        title = csvFile[randValue][0]
        artist = csvFile[randValue][1]
        lyric = csvFile[randValue][2]
        songTuple = (title, artist, lyric)
        return lyric

# allowed image types
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['ALLOWED_EXTENSIONS']=ALLOWED_EXTENSIONS

# is file allowed to be uploaded?
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

def load_fastai():
    if os.environ.get("RUNNING_ON_HEROKU"):
        subprocess.run(["pip", "install", "-r", "fastai-requirements.txt"])
    import matplotlib
    matplotlib.use('TkAgg')
    from werkzeug import secure_filename
    from app import predictor
    app.route('/', methods=['POST'])(upload_file)

threading.Thread(target=load_fastai, daemon=True).start()
