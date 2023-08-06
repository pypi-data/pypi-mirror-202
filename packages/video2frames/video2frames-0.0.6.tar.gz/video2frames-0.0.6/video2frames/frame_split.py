import cv2
import os
import argparse

# parser = argparse.ArgumentParser()
# parser.add_argument('-fps', '--frameRate', required = False, type = int, help = "Number of frames inbetween image capture")
# parser.add_argument('-vid', '--videoPath', required = False, type = str, help = "Path of video")
# args = parser.parse_args()
# frameRate = args.frameRate
# videoPath = args.videoPath

sec = 0
count = 1
frameRate = 5
videoPath = ('videos/video2.mp4')

vidcap = cv2.VideoCapture(videoPath)

directory = 'capture'
if not os.path.exists(directory):
    os.makedirs(directory)

def getFrame(sec):
    vidcap.set(cv2.CAP_PROP_POS_MSEC,sec*1000)
    hasFrames, image = vidcap.read()
    if hasFrames:
        cv2.imwrite(os.path.join(directory, "image"+str(count)+".jpg"), image)        # save frame as JPG file
    return hasFrames

success = getFrame(sec)
while success:
    count = count + 1
    sec = sec + frameRate
    sec = round(sec, 2)
    success = getFrame(sec)

print('Frames split successfully')