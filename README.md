# SnapCap
## Project Vision
Our web-application adds emotional intelligence and creativity to the caption creation process. We trained a neural network on images of faces to detect emotion from photos. Then we built a program to analyze song metrics in order to classify lyrics into emotion categories. When a user uploads a photo, we use these two analyses to produce a lyric caption that matches their detected mood. 

Our web app can be viewed at: http://ec2-54-183-218-184.us-west-1.compute.amazonaws.com/


## Files
The files are structured in Model-View-Controller style, so that the controller mediates interaction between the model and the view.


### 'View' pages'
* 'index.html'
* 'start.html'
* 'about.html'
* 'howitworks.html'



### 'Model' pages
* predictor.py
* songClassifier.py


### 'Controller' pages
* routes.py

### Misc
* 'style.css'
* 'header.css'
* 'footer.css'
* 'displayResult.css'
* 'index.css'
* 'angrysongs.csv'
* 'neutralsongs.csv'
* 'happysongs.csv'
* 'sadsongs.csv'
* Coding Style Document outlines the standards of style to which our code is held

## Other information
This project was created as a class project for CSCI121 at Harvey Mudd College by AP, AK, AR, KJ, and LC.


