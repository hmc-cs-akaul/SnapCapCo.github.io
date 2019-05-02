# Ali and Anisha
import csv

with open('miniSongDatabase.csv') as csvfile:
    csvReader = csv.reader(csvfile, delimiter=',')
    lineCount = 0
    songDatabase = []

    for row in csvReader:
        if lineCount == 0:
            print(f'Column names are {", ".join(row)}')
            lineCount += 1
        else:
            songName = row[1]
            artist = row[2]
            danceability = float(row[3])
            energy = float(row[4])
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
                emotion = "fear"
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
                    elif tempo > 105 and tempo <= 133:
                        emotion = "disgust"
                    else:
                        emotion = "angry"
                # more positive song
                elif valence > 0.4 and valence < 0.6:
                    if tempo <= 105:
                        emotion = "fear"
                    elif tempo < 105 and tempo <= 133:
                        emotion = "neutral"
                    else:
                        emotion = "surprise"
                elif valence > 0.6:
                    if tempo <= 119:
                        emotion = "neutral"
                    elif tempo > 119:
                        emotion = "happy"

            print(songName , " was written by " , artist
            , " and has a danceability of: " , danceability
            , ", an energy of: " , energy , ", a key of: " ,
            key , ", a loudness of: " , loudness ,  ", a mode of: "
            , mode , ", a valence of: " , valence, ", a tempo of: "
            , str(tempo), " and has been categorized as ", emotion, "\n")

            songInfo = [emotion, songName, artist, lyric1, lyric2]
            songDatabase.append(songInfo)

with open('emotionDatabase.csv', mode='w') as csvfile:
    database = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for row in songDatabase:
        database.writerow(row)


    print(f'Processed {line_count} lines.')
