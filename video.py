# Kurt Schimmel
# kschimme
# Section L

import cv2
from PIL import Image as im
from cmu_graphics import *

class Video:
    # Stores information for a video
    def __init__(self,path,name):
        self.name = name
        self.path = path
        self.length = None
        self.thumbnail = None
        self.times = []
        self.cum_times = []

    # Checks whether coordinates are within the bounds of a video
    def inVideo(self,x,y):
        return (self.tx <= x <= self.tx + self.w) and (self.ty <= y <= self.ty + self.h)

    def __eq__(self,other):
        return self.path == other.path

    def __repr__(self):
        return f'{self.name}'

    def addTimes(self,td, cum):
        self.times = td
        self.cum_times = cum

    # Finds the Length of a video using the frames an fps
    def findLength(self):
        cap = cv2.VideoCapture(self.path)
        frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        if fps == 0: fps = 1
        secs = frames/fps
        min = int(secs//60)
        sec = secs%60
        if sec < 10:
            sec = '0' + f'{sec:.2f}'
        else:
            sec = f'{sec:.2f}'
        length = f'{min}:{sec}'
        self.length = length

    # Creates a thumbnail for the video
    def setThumbnail(self):
        cap = cv2.VideoCapture(self.path)
        cap.set(cv2.CAP_PROP_POS_FRAMES, 5)
        ret, frame = cap.read()
        if not ret:
            print('unable to read frame')
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_image = im.fromarray(frame)
        self.thumbnail = pil_image

    def rename(self,name):
        self.name = name



