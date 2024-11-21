# Imports
from cmu_graphics import * # CMU Graphics
import cv2 # Video Processing Library
import shutil # For Deleting Files
from PIL import Image # For Processing Images
import os # For Creating and Modifying Files
import time # For Using Time
from button import Button # Button Class

# openpose for pose estimation



# contains app variables
def onAppStart(app):
    setActiveScreen('main')
    app.width = 1470
    app.height = 956
    app.paused = True

    app.video_path = "hurdle.mov" # change to custom input
    app.capture = cv2.VideoCapture(app.video_path)
    if not app.capture.isOpened():
        print("error, video")
        exit()
    app.frames = int(app.capture.get(cv2.CAP_PROP_FRAME_COUNT))
    app.fps = app.capture.get(cv2.CAP_PROP_FPS)

    app.current_frame = 0
    app.td_time = 0
    app.time = 0
    app.folder_path = "frames"
    app.stepsPerSecond = 120
    app.td_times = []

    app.buttons = [Button('Library',1120,756,250,80),
                   Button('Athletes',1120,656,250,80),
                   Button('Strategize',1120,556,250,80),
                   Button('Back',1120,app.height*0.1-40,250,80),
                   Button('Video',200,200,250,80)]

# draws main screen
def main_redrawAll(app):
    drawImage('bg.png',0,0)
    drawLabel('Hurdle Touchdown Time',80,80,size = 80,font = 'helvetica',align = 'left', fill = 'white')
    drawLabel('Finder',200,160,size = 80,font = 'helvetica',align = 'left', fill = 'white')
    for i in range(3):
        drawButton(app,i)
    # main_drawButtons(app)

# draws a button
def drawButton(app,i):
    b = app.buttons[i]
    drawRect(b.tx,b.ty,b.w,b.h,fill = 'white', border = 'black')
    mx,my = b.midpoint()
    drawLabel(b.name,mx,my,font = 'helvetica',size = 20)

def drawHeader(app,title):
    drawRect(0,0,app.width,app.height*0.2,fill='red',border = 'black')
    drawLabel(title,app.width/2,app.height*0.1,fill='black',font = 'helvetica',size = 80)

# switches to appropriate screens when buttons are pressed
def main_onMousePress(app,x,y):
    for i in range(3):
        b = app.buttons[i]
        if b.inButton(x,y):
            setActiveScreen(b.name.lower())

# controls the main screen
def main_onKeyPress(app,key):
    if key == 'q':
        onClose(app)

# Library
def library_redrawAll(app):
    drawHeader(app,'Library')
    drawButton(app,3)
    drawButton(app,4)

def library_onMousePress(app,x,y):
    if app.buttons[3].inButton(x,y):
        setActiveScreen('main')
    if app.buttons[4].inButton(x,y):
        setActiveScreen('video')

# Athletes
def athletes_redrawAll(app):
    drawHeader(app,'Athletes')
    drawButton(app,3)

def athletes_onMousePress(app,x,y):
    if app.buttons[3].inButton(x,y):
        setActiveScreen('main')

# Strategize
def strategize_redrawAll(app):
    drawHeader(app,'Strategize')
    drawButton(app,3)

def strategize_onMousePress(app,x,y):
    if app.buttons[3].inButton(x,y):
        setActiveScreen('main')

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
        elif key == 'backspace':
            if len(app.td_times) > 0:
                app.td_times.pop()
        findTime(app)
    else:
        pass

# draws video
def video_redrawAll(app):
    drawFrame(app,getFrame(app))
    drawTimes(app)

## other methods ##

# finds the current time in the video using the current frame and the fps
def findTime(app):
    current_time = app.current_frame/app.fps
    seconds = pythonRound(current_time % 60,2)
    app.time = seconds
    return seconds

# finds the current touchdown time split
def findTDTime(app):
    time = findTime(app) - app.td_time
    app.td_time = time
    app.td_times.append(f'{time:.2f}')
    app.td_time = 0
    return time

# draws the times
def drawTimes(app):
    drawRect(20,0,40,20,fill='gray')
    drawLabel(f'{app.time:.2f}',20,10,fill='white',size = 20, align = 'left')
    drawRect(20,30,40,20,fill='gray')
    drawLabel(f'{app.td_time:.2f}',20,40,fill='white',size = 20, align = 'left')
    if len(app.td_times) > 0:
        for i in range(len(app.td_times)):
            drawRect(20+ 50 * i,60,40,20,fill='gray')
            drawLabel(f'{app.td_times[i]}',20 + 50 * i,70,fill='white',size = 20, align = 'left')
            

# gets the current frame of the video
def getFrame(app):
    app.capture.set(cv2.CAP_PROP_POS_FRAMES,app.current_frame)
    ret, frame = app.capture.read()
    if not ret:
        print('unable to read frame')
    cv2.imwrite('frame.jpg',frame)
    # cv2.imshow('Frame',frame)
    return frame

# draws the current frame
def drawFrame(app,img):
    drawImage('frame.jpg',0,0)
    
# tests how long it takes to readFrames
def testTime(app):
    start = time.time()
    readFrames(app)
    end = rounded(time.time() - start)
    print(end)

#reads all frames in the video
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

# deletes frames from the 'frames' folder
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