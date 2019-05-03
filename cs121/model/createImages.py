import csv
import numpy as np
#import pandas as pd
import cv2

w,h = 48,48

with open('fer2013.csv') as csvfile:
    csv_reader = csv.reader(csvfile, delimiter=',')
    line_count = 0

    for row in csv_reader:
        if line_count == 0:
            print(row)
            line_count +=1
        else:
            emotion = row[0]
            
            label = "images/" + str(emotion)+ "/" + str(line_count)+ ".png"
            pixels = map(int, row[1].split())
            pixellist = list(pixels) 
            usage = row[2] 

            pixelsarray = np.asarray(pixellist)
            image = pixelsarray.reshape(w, h) 
            stackedimage = np.dstack((image,) * 3)
            #cv2.imwrite(label, stackedimage)
            # if line_count == 1:
            #     #print(label)
            #     cv2.imwrite("exampleimage.png", stackedimage)
            #     print(image.shape)
            #     print(image)
            if emotion == 1:

                if not image.any():
                    print("empty image data", label)
                cv2.imwrite(label, image)

            line_count+=1
