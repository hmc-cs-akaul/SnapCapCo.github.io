from __future__ import division, print_function
import sys
import os
import glob
import re
import random
from pathlib import Path

# Import fast.ai Library
from fastai import *
from fastai.vision import *

# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename



#load model
def load_model(model_path):
    path = Path(model_path)
    classes = ['happy', 'sad','disgustedzip', 'angryzip']
    data2 = ImageDataBunch.single_from_classes(path, classes, ds_tfms=get_transforms(), size=224).normalize(imagenet_stats)
    learn = create_cnn(data2, models.resnet34)
    learn.load('stage-2')
    return learn

def model_predict(img_path, model_path):
    """
       model_predict will return the preprocessed image
    """
    happy = [['I Like It', 'Cardi B', 'I like texts from my exes when they want a second chance'], ['I Like It', 'Cardi B', 'Bad bitch make him nervous'], ['Havana', 'Camila Cabello', 'I knew it when I met him I loved him when I left him'], ['Havana', 'Camila Cabello', "He got me feelin' like"], ['X', 'Nicky Jam', ''], ['X', 'Nicky Jam', ''], ['Moonlight', 'XXXTENTACION', "why you trippin'? Get your mood right"], ['Moonlight', 'XXXTENTACION', "Feel like I'm destined I don't need no Smith & Wesson, no"], ['Mine', 'Bazzi', 'Girl anything I can do just to make you feel alright'], ['Mine', 'Bazzi', "Running circles 'round my mind even when it's rainy all you ever do is shine"], ['Ric Flair Drip (& Metro Boomin)', 'Offset', 'Balenciaga, check my posture, Valentino boots'], ['Ric Flair Drip (& Metro Boomin)', 'Offset', 'Hop in my Bentayga and the seat is a masseuse'], ['Freaky Friday (feat. Chris Brown)', 'Lil Dicky', '*Somehow this shit turned into Freaky Friday'], ['Freaky Friday (feat. Chris Brown)', 'Lil Dicky', 'I am balling on the court, oh my God I can dunk'], ['Believer', 'Imagine Dragons', "Don't you tell me what you think that I can be"], ['Believer', 'Imagine Dragons', 'You made me a believer, believer'], ['Pray For Me (with Kendrick Lamar)', 'The Weeknd', "You know I'll ride again"], ['Pray For Me (with Kendrick Lamar)', 'The Weeknd', 'I fight the world, I fight you, I fight myself'], ['Walk It Talk It', 'Migos', 'Take my shoes and walk a mile'], ['Walk It Talk It', 'Migos', "That's my sauce, where you find it?"], ['Him & I (with Halsey)', 'G-Eazy', "They don't wanna see us make it, they just wanna divide"], ['Him & I (with Halsey)', 'G-Eazy', "Cross my heart, hope to die, To my lover, I'd never lie"], ['Stir Fry', 'Migos', 'Dance with my dogs in the nighttime (wroof)'], ['Stir Fry', 'Migos', "We livin' fast now (fast)"], ['I Like Me Better', 'Lauv', 'To be drunk and in love in New York City'], ['I Like Me Better', 'Lauv', "I like me better when I'm with you"], ['This Is Me', 'Keala Settle', "I am who I'm meant to be, this is me"], ['This Is Me', 'Keala Settle', "And I'm marching on to the beat I drum"], ['Everybody Dies In Their Nightmares', 'XXXTENTACION', "Only time I feel pain, when I'm feelin' love"], ['Everybody Dies In Their Nightmares', 'XXXTENTACION', "Don't go, stay up and don't go"], ['No Brainer', 'DJ Khaled', "You stick out of the crowd, baby, it's a no-brainer"], ['No Brainer', 'DJ Khaled', "Movin' my soul, yeah, you're spiritual"], ["That's What I Like", 'Bruno Mars', "I got a condo in Manhattan / Baby girl, what's happnin'?"], ["That's What I Like", 'Bruno Mars', 'Said you got it if you want it, take my wallet if you want it, now'], ['Paris', 'The Chainsmokers', "Let's show them we are"], ['Paris', 'The Chainsmokers', "We'll get away with everything / Let's show them we are better"], ['Mask Off', 'Future', 'Hit the gas / Bossing my adrenaline'], ['Mask Off', 'Future', '*Fuck it, mask off']]
    sad = [["God's Plan", 'Drake', "I only love my bed and my momma, I'm sorry"], ["God's Plan", 'Drake', "don't start no trouble with me tryna keep it peaceful is a struggle for me"], ['In My Feelings', 'Drake', "Cause I've been goin' off and they don't know when it's stoppin"], ['In My Feelings', 'Drake', "Say you'll never ever leave from beside me 'cause I want you, and I need you and I'm down for you always"], ['Lucid Dreams', 'Juice WRLD', "I still see your shadows in my room can't take back the love that I gave you"], ['Lucid Dreams', 'Juice WRLD', 'I thought you were the one listening to my heart instead of my head'], ['Perfect', 'Ed Sheeran', "I'm dancing in the dark, with you between my arms"], ['Perfect', 'Ed Sheeran', "But darling, just kiss me slow, your heart is all I own and in your eyes you're holding mine"], ['Taste (feat. Offset)', 'Tyga', 'she can get a taste'], ['Taste (feat. Offset)', 'Tyga', "Whole lotta styles, can't even pronounce the name You don't even got no style, see you on my Instagram"], ['Nevermind', 'Dennis Lloyd', 'What if I left and it made no sense'], ['Nevermind', 'Dennis Lloyd', "I ain't gonna fall back down now"], ['Eastside (with Halsey & Khalid)', 'benny blanco', "My love is yours if you're willing to take it give me your heart 'cause I ain't gonna break it"], ['Eastside (with Halsey & Khalid)', 'benny blanco', 'Just take my hand and come with me'], ['Perfect Duet (Ed Sheeran & Beyonc?)', 'Ed Sheeran', 'I found a love for me'], ['Perfect Duet (Ed Sheeran & Beyonc?)', 'Ed Sheeran', 'Now I know I have met an angel in person'], ['1-800-273-8255', 'Logic', 'I wanna feel alive'], ['1-800-273-8255', 'Logic', "I feel like I'm out of my mind\r"], ['Perfect', 'Ed Sheeran', 'Darling, just dive right in and follow my lead'], ['Perfect', 'Ed Sheeran', "We are still kids but we're so in love"], ['Location', 'Khalid', "Let's ride the vibrations"], ['Location', 'Khalid', "I don't need nothing else but you"], ['Solo Dance', 'Martin Jensen', 'Just wanna dance, dance, dance'], ['Solo Dance', 'Martin Jensen', "I'm here to fool around"], ['One Dance', 'Drake', "that's why I need a one dance"], ['One Dance', 'Drake', "Cause if you're down"], ['There for You', 'Martin Garrix', 'Somewhere I lost a piece of me smoking cigarettes on balconies'], ['There for You', 'Martin Garrix', "Love is a road that goes both ways, when your tears roll down your pillow like a river, I'll be there for you"], ['Side To Side', 'Ariana Grande', "Rappers in they feelings cause they feelin' me"], ['Side To Side', 'Ariana Grande', 'Uh, I give zero fucks and I got zero chill in me'], ['Cold Water (feat. Justin Bieber & M1)', 'Major Lazer', 'Everybody gets high sometimes, you know'], ['Cold Water (feat. Justin Bieber & M1)', 'Major Lazer', 'Cause we all get lost sometimes, you know?'], ['Bank Account', '21 Savage', "I pull up in 'Rari's and shit, with choppers and Harley's and shit"]]
    angry = [['rockstar (feat. 21 Savage)', 'Post Malone', 'Man, I feel just like a rockstar'], ['rockstar (feat. 21 Savage)', 'Post Malone', "Your wifey say I'm lookin' like a whole snack"], ['Better Now', 'Post Malone', 'Woulda gave you anything, woulda gave you everything'], ['Better Now', 'Post Malone', "I swear to you, I'll be okay you're only the love of my life"], ['no tears left to cry', 'Ariana Grande', "Ain't got no tears left to cry"], ['no tears left to cry', 'Ariana Grande', "Right now, I'm in a state of mind I wanna be in, like, all the time"], ['Youngblood', '5 Seconds of Summer', 'I give and I give and I give and you take, give and you take'], ['Youngblood', '5 Seconds of Summer', 'Say you want me out of your life'], ['Love Lies (with Normani)', 'Khalid', 'Are you down for the ride?'], ['Love Lies (with Normani)', 'Khalid', "Don't be afraid to tell me if you ain't with it"], ['I Fall Apart', 'Post Malone', "She fooled me twice and it's all my fault"], ['I Fall Apart', 'Post Malone', "Never caught a feelin' this hard harder than the liquor I pour"], ['Never Be the Same', 'Camila Cabello', 'Just one hit of you, I knew I never ever, ever be the same'], ['Never Be the Same', 'Camila Cabello', "I'm a sucker for the way that you move, babe and I could try to run, but it would be useless"], ['Wolves', 'Selena Gomez', "I've been running with the wolves to get to you"], ['Wolves', 'Selena Gomez', 'I wanna feel the way that we did that summer night '], ['changes', 'XXXTENTACION', "You're changing, I can't stand it"], ['changes', 'XXXTENTACION', "My heart can't take this damage And the way I feel, can't stand it"], ['In My Mind', 'Dynoro', "The dreams we have, the love we share This is what we're waiting for"], ['In My Mind', 'Dynoro', 'In my mind, in my head'], ['Thunder', 'Imagine Dragons', 'I was lightning before the thunder'], ['Thunder', 'Imagine Dragons', 'I was dreaming of bigger things'], ['Call Out My Name', 'The Weeknd', "Girl, call out my name, and I'll be on my way"], ['Call Out My Name', 'The Weeknd', 'I made sure I held you close to me'], ['FEFE (feat. Nicki Minaj & Murda Beatz)', '6ix9ine', "Colorful hair, don't care"], ['FEFE (feat. Nicki Minaj & Murda Beatz)', '6ix9ine', 'Eeny, meeny, miny, moe'], ['Fuck Love (feat. Trippie Redd)', 'XXXTENTACION', "Please don't throw your love away, huh"], ['Fuck Love (feat. Trippie Redd)', 'XXXTENTACION', 'Baby, I need you in my life, in my life'], ['Silence', 'Marshmello', "Yeah, I'd rather be a lover than a fighter"], ['Silence', 'Marshmello', "I've been quiet for too long"], ['God is a woman', 'Ariana Grande', "You'll believe God is a woman"], ['God is a woman', 'Ariana Grande', 'So, baby, take my hand, save your soul'], ['Plug Walk', 'Rich The Kid', 'I make money when I talk'], ['Plug Walk', 'Rich The Kid', "It's the plug tryna call me (skrrt, skrrt)"], ['lovely (with Khalid)', 'Billie Eilish', 'Heart made of glass, my mind of stone']]
    disgusted = [['Nice For What', 'Drake', "said you'd be there for me"], ['Nice For What', 'Drake', 'You know dark days, you know hard times'], ['New Rules', 'Dua Lipa', "But my love, he doesn't love me"], ['New Rules', 'Dua Lipa', "don't let him in you'll have to kick him out again"], ['Shape of You', 'Ed Sheeran', 'Your love was handmade for somebody like me'], ['Shape of You', 'Ed Sheeran', 'We push and pull like a magnet do although my heart is falling too'], ['River (feat. Ed Sheeran)', 'Eminem', "I've been a liar, been a thief"], ['River (feat. Ed Sheeran)', 'Eminem', "If all it's gonna cause is pain"], ['Jackie Chan', 'Ti?sto', "She just wanna do it for the 'Gram (you know, you know)"], ['Jackie Chan', 'Ti?sto', '*Now your bitch wanna kick it, Jackie Chan'], ['Finesse (Remix) [feat. Cardi B]', 'Bruno Mars', "We out here drippin' in finesse"], ['Finesse (Remix) [feat. Cardi B]', 'Bruno Mars', "Yeah, we got it goin' on, got it goin' on"], ['Happier', 'Marshmello', 'I want you to be happier, I want you to be happier'], ['Happier', 'Marshmello', 'I want to see you smile'], ['Rise', 'Jonas Blue', "We're gonna ri-ri-ri-ri-rise 'til we fall"], ['Rise', 'Jonas Blue', "They say we're too savage"], ['2002', 'Anne-Marie', 'Oops, I got 99 problems singing bye, bye, bye'], ['2002', 'Anne-Marie', 'Dancing on the hood in the middle of the woods'], ['Let Me Go (with Alesso, Florida Georgia Line & watt)', 'Hailee Steinfeld', 'Someone will love you, let me go'], ['Let Me Go (with Alesso, Florida Georgia Line & watt)', 'Hailee Steinfeld', 'Good on paper, picture perfect'], ['Feel It Still', 'Portugal. The Man', "Ooh woo, I'm a rebel just for kicks, now"], ['Feel It Still', 'Portugal. The Man', "Might've had your fill, but you feel it still"], ['1, 2, 3 (feat. Jason Derulo & De La Ghetto)', 'Sofia Reyes', "If love's the game, let's play a million times"], ['1, 2, 3 (feat. Jason Derulo & De La Ghetto)', 'Sofia Reyes', 'Love how you count it out for me, babe'], ['Shape of You', 'Ed Sheeran', 'Your love was handmade for somebody like me'], ['Shape of You', 'Ed Sheeran', "I'm in love with the shape of you"], ["I'm the One", 'DJ Khaled', "I'm the best yet, and yet, my best is yet to come"], ["I'm the One", 'DJ Khaled', "Yeah, you're lookin' at the truth, the money never lie no"], ['Unforgettable', 'French Montana', '*A fucking good time, never hurt nobody'], ['Unforgettable', 'French Montana', "It's not good enough for me, since I been with you"], ['Attention', 'Charlie Puth', "You've been runnin' round, runnin' round, runnin' round throwin' that dirt all on my name"]]
    classes = ['happy','sad','disgusted','angry']
    learn = load_model(model_path)
    img = open_image(img_path)
    pred_class,pred_idx,outputs = learn.predict(img)
    if classes[pred_idx] == 'disgusted':
        randValue = random.randint(0,len(disgusted))
        caption = 'disgusted! ' + ' Your Caption is: ' +  disgusted[randValue][2] + ' From: ' + disgusted[randValue][0] + ' by: '  + disgusted[randValue][1]
        return caption
    elif classes[pred_idx] == 'angry':
        randValue = random.randint(0,len(angry))
        caption = 'angry! ' + ' Your Caption is: ' +  angry[randValue][2] + ' From: ' + angry[randValue][0] + ' by: '  + angry[randValue][1]
        return caption
    elif classes[pred_idx] == 'sad':
        randValue = random.randint(0,len(sad))
        caption = 'sad! ' + ' Your Caption is: ' +  sad[randValue][2] + ' From: ' + sad[randValue][0] + ' by: '  + sad[randValue][1]
        return caption
    else:
        randValue = random.randint(0,len(happy))
        caption = 'happy! ' + ' Your Caption is: ' +  happy[randValue][2] + ' From: ' + happy[randValue][0] + ' by: '  + happy[randValue][1] 
        return caption

def generate_caption(pred_idx):
    classes = ['happy', 'sad', 'disgusted', 'angry']
    pred_class = classes[pred_idx]
    if pred_class == 'happy':
        return getSongData('~/cs121/app/happysongs.csv')
    if pred_class == 'sad':
        return getSongData('~/cs121/app/sadsongs.csv')
    if pred_class == 'angry':
        return getSongData('~/cs121/app/angrysongs.csv')
    if pred_class == 'disgusted':
        return getSongData('~/cs121/app/disgustedsongs.csv')

def getSongData(fileName):
    with open(fileName, mode='r') as csvFile:
        row_count = sum(1 for row in csvFile)
        randValue = random.randint(0,row_count+1)
        title = csvFile[randValue][0]
        artist = csvFile[randValue][1]
        lyric = csvFile[randValue][2]
        songTuple = (title, artist, lyric)
        return lyric
