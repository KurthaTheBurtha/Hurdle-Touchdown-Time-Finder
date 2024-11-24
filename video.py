import cv2
from PIL import Image as im
from cmu_graphics import *

class Video:
    def __init__(self,name,path):
        self.name = name
        self.path = path
        self.length = None
        self.thumbnail = None

    def validatePath(self):
        pass

    def __repr__(self):
        return f'Video: {self.name}, Path: {self.path}, Length: {self.length}, Thumbnail: {self.thumbnail}'
    def findLength(self):
        cap = cv2.VideoCapture(self.path)
        frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        secs = frames/fps
        min = secs//60
        sec = secs%60
        length = f'{min}:{'0' + str(sec) if sec < 10 else sec}'
        self.length = length

    def setThumbnail(self):
        cap = cv2.VideoCapture(self.path)
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        ret, frame = cap.read()
        if not ret:
            print('unable to read frame')
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_image = im.fromarray(frame)
        cmu_image = CMUImage(pil_image)
        self.thumbnail = cmu_image



