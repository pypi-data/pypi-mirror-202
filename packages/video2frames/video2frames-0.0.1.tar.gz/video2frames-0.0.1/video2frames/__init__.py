import os
import cv2
from frame_split import directory
from frame_split import vidcap
from frame_split import frameRate

count = 1

def getFrame(sec):
    vidcap.set(cv2.CAP_PROP_POS_MSEC,sec*1000)
    hasFrames, image = vidcap.read()
    if hasFrames:
        cv2.imwrite(os.path.join(directory, "image"+str(count)+".jpg"), image)        # save frame as JPG file
    return hasFrames
