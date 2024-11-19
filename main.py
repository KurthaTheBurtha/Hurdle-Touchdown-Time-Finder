# Necessary Imports
from cmu_graphics import * # CMU Graphics
import cv2 # Video Processing Library
import shutil # For Deleting Files
from PIL import Image # For Processing Images
import os # For Creating and Modifying Files
import time


# contains app variables
def onAppStart(app):
    setActiveScreen('main')
    app.width = 1920
    app.height = 1080
    app.video_path = "hurdle.mov"
    app.capture = cv2.VideoCapture(app.video_path)
    if not app.capture.isOpened():
        print("error, video")
        exit()
    app.frames = int(app.capture.get(cv2.CAP_PROP_FRAME_COUNT))
    app.fps = app.capture.get(cv2.CAP_PROP_FPS)
    app.current_frame = 0
    app.td_time = 0
    app.time = 0
    app.paused = True
    app.folder_path = "frames"
    app.stepsPerSecond = 60
    # clearFolder(app)
    # readFrames(app)
    # testTime(app)


def main_redrawAll(app):
    drawLabel('poo',200,200)


# iterates through the frames
def video_onStep(app):
    if app.paused:
        pass
    else:
        app.current_frame += 1
        if app.current_frame >= app.frames:
            app.current_frame -= 1
    findTime(app)

# controls the key presses in the app
def video_onKeyPress(app,key):
    if key == 'q':
        onClose(app)
    if key == 'p':
        app.paused = not app.paused
    if app.paused:
        if key == 'a':
            app.current_frame -= 1
            if app.current_frame < 0:
                app.current_frame += 1
        elif key == 's':
            app.current_frame += 1
            if app.current_frame >= app.frames:
                app.current_frame -= 1
        elif key == 't':
            if app.td_time == 0:
                app.td_time = findTime(app)
            else:
                findTDTime(app)
        findTime(app)
    else:
        pass

# draws video
def video_redrawAll(app):
    drawFrame(app,getFrame(app))
    drawTimes(app)

#
def findTime(app):
    current_time = app.current_frame/app.fps
    seconds = pythonRound(current_time % 60,2)
    app.time = seconds
    return seconds

def findTDTime(app):
    time = findTime(app) - app.td_time
    app.td_time = time
    return time

def drawTimes(app):
    drawRect(20,10,40,20,fill='gray')
    drawLabel(f'{app.time:.2f}',20,10,fill='white',size = 20)
    drawRect(20,40,40,20,fill='gray')
    drawLabel(f'{app.td_time:.2f}',20,40,fill='white',size = 20)


def getFrame(app):
    app.capture.set(cv2.CAP_PROP_POS_FRAMES,app.current_frame)
    ret, frame = app.capture.read()
    return frame

def drawFrame(app,img):
    drawImage(f"frames/{app.current_frame}.bmp",0,0)
    pass

def testTime(app):
    start = time.time()
    readFrames(app)
    end = rounded(time.time() - start)
    print(end)

def readFrames(app):
    os.makedirs(app.folder_path,exist_ok=True)
    cnt = 0
    for i in range(app.frames):
        app.capture.set(cv2.CAP_PROP_POS_FRAMES,i)
        ret, frame = app.capture.read()
        if not ret:
            break
        cv2.imwrite(os.path.join(app.folder_path,f'{i}.bmp'),frame)
        cnt +=1
        app.frames = cnt

def clearFolder(app):
    folder_path = app.folder_path
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)  # Deletes the folder and all contents
        os.makedirs(folder_path)

def onClose(app):
    clearFolder(app)
    app.capture.release()
    app.quit()


def main():
    runAppWithScreens('main')

main()