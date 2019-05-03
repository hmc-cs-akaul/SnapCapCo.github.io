# Ali and Anisha
import csv

with open('songDatabase.csv') as csvfile:
    csvReader = csv.reader(csvfile, delimiter=',')
    lineCount = 0
    happy, sad, angry, neutral = [], [], [], []

    for row in csvReader:
        if lineCount < 2:
            lineCount += 1
        else:
            songName = row[1]
            artist = row[2]
            danceability = float(row[3])
            energy = int(row[3])
            key = int(row[5])
            loudness = row[6]
            mode = int(row[7])
            valence = float(row[12])
            tempo = float(row[13])
            emotion= ""
            lyric1 = row[16]
            lyric2 = row[17]

            lineCount += 1

            #check for keys corresponding to emotions
            if key == 2 and mode == 1 or key == 9 and mode == 1:
                emotion = "happy"
            elif key == 3 and mode == 0:
                emotion = "neutral"
            elif key == 6 and mode == 0:
                emotion = "sad"
            elif key == 11 and mode == 1:
                emotion = "angry"
            # if key does not directly match, do further analysis
            else:
                # more negative song
                if valence <= 0.4:
                    if tempo <= 105:
                        emotion = "sad"
                    else:
                        emotion = "angry"
                # more positive song
                elif valence > 0.6:
                    if tempo <= 119:
                        emotion = "neutral"
                    elif tempo > 119:
                        emotion = "happy"

            songInfo1 = [songName, artist, lyric1]
            songInfo2 = [songName, artist, lyric2]
            if(emotion == "happy"):
                happy.append(songInfo1)
                happy.append(songInfo2)
            elif(emotion == "angry"):
                angry.append(songInfo1)
                angry.append(songInfo2)
            elif(emotion == "sad"):
                sad.append(songInfo1)
                sad.append(songInfo2)
            elif(emotion == "disgust"):
                disgust.append(songInfo1)
                disgust.append(songInfo2)
            

with open('happysongs.csv', mode='w') as csvfile:
    database = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for row in happy:
        database.writerow(row)

with open('angrysongs.csv', mode='w') as csvfile:
    database = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for row in angry:
        database.writerow(row)

with open('sadsongs.csv', mode='w') as csvfile:
    database = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for row in sad:
        database.writerow(row)

with open('neutralsongs.csv', mode='w') as csvfile:
    database = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for row in neutral:
        database.writerow(row)


