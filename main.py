# Imports
import shutil  # For Deleting Files
import time  # For Using Time
from PIL import Image as im
import cv2  # Video Processing Library
from button import Button  # Button Class
from video import Video # Video Class
from athlete import Athlete # Athlete Class
from tip import Tip # Tip Class
from cmu_graphics import *  # CMU Graphics
import os # For the File Explorer


# openpose for pose estimation



# contains app variables
def onAppStart(app):
    # main screen
    setActiveScreen('main')
    app.width = 1470
    app.height = 956
    app.paused = True
    app.stepsPerSecond = 120

    # Video Recording
    app.video_path = "hurdle.mov" # change to custom input
    app.capture = cv2.VideoCapture(app.video_path)
    if not app.capture.isOpened():
        print("error, video")
        exit()
    app.frames = int(app.capture.get(cv2.CAP_PROP_FRAME_COUNT))
    app.fps = app.capture.get(cv2.CAP_PROP_FPS)

    # Video Screen
    app.current_frame = 0
    app.td_time = 0
    app.time = 0
    app.td_times = []
    app.cum_times = []
    app.recording = False
    app.fromwhere = 'library'
    app.instructionbutton = Button('Instructions', 1120, app.height * 0.9-45, 250, 60)
    # app.folder_path = "frames"

    # Videos
    app.buttons = [Button('Library',1120,556,250,80),
                   Button('Athletes',1120,656,250,80),
                   Button('Strategize',1120,756,250,80),
                   Button('Back',1120,app.height*0.1-30,250,60),
                   Button('Video',200,200,250,80),
                   Button('Upload',100,app.height*0.1-30,250,60),
                   Button('Add New',100,app.height*0.1-30,350,60)]
    app.videos = []
    app.videobuttons = []
    app.tx, app.ty = app.width * 0.05, app.height * 0.25
    app.cnt = 0

    # app.videorenames = []


    # File Explorer
    app.curdir = os.getcwd()
    app.files = []
    app.uploaded = False

    # Athletes
    app.athletes = []
    app.athletebuttons = []
    app.setprs = []
    app.editvideos = []
    app.ax, app.ay = app.width * 0.05, app.height * 0.25

    # Text Input
    app.input = ''
    app.activeAthlete = None

    # Strategize
    app.activeVideo = None
    app.timecolors = []
    app.targettimeinput = ''
    app.targettime = None
    # Touchdown charts from https://hurdlesfirstbeta.com/free-articles/training-tips/touchdown-charts/
    # Times were published in The Science of Hurdling by Brent McFarlane, Canadian Track and Field coach who specializes in hurdles
    app.touchdown_times_cum = {12.8 : [2.4,3.4,4.3,5.2,6.2,7.2,8.2,9.2,10.3,11.4,12.8],
                               13.0 : [2.4,3.4,4.4,5.4,6.4,7.4,8.4,9.4,10.5,11.6,13.0],
                               13.2 : [2.5,3.5,4.4,5.4,6.4,7.4,8.5,9.6,10.7,11.8,13.2],
                               13.6 : [2.5,3.6,4.6,5.6,6.6,7.7,8.8,9.9,11.0,12.2,13.6],
                               14.0 : [2.5,3.6,4.6,5.7,6.8,7.9,9.0,10.1,11.2,12.4,14.0],
                               14.4 : [2.6,3.6,4.7,5.8,6.9,8.1,9.3,10.5,11.7,12.9,14.4],
                               14.6 : [2.6,3.7,4.7,5.8,7.0,8.2,9.4,10.6,11.8,13.0,14.6],
                               15.0 : [2.6,3.7,4.9,6.0,7.2,8.3,9.5,10.7,12.0,13.2,15.0],
                               15.5 : [2.7,3.8,5.0,6.2,7.4,8.6,9.8,11.0,12.3,13.6,15.5],
                               16.0 : [2.8,3.9,5.1,6.4,7.6,8.8,10.1,11.3,12.6,14.0,16.0]}
    app.touchdown_times = {}
    buildTDTimes(app)
    app.targettimebutton = Button('targettime',app.width*0.4,app.height*0.21,app.width*0.2,app.height*0.03)
    app.userpredictedtime = None

    ## Tips
    app.start = None
    app.middle = None
    app.end = None


# draws main screen
def main_redrawAll(app):
    drawImage('assets/bg.png',0,0)
    drawLabel('Hurdle Touchdown Time',80,80,size = 80,font = 'helvetica',align = 'left', fill = 'white')
    drawLabel('Finder',200,160,size = 80,font = 'helvetica',align = 'left', fill = 'white')
    for i in range(3):
        drawButton(app,i)

# draws a button
def drawButton(app,i):
    b = app.buttons[i]
    drawRect(b.tx,b.ty,b.w,b.h,fill = 'white', border = 'black')
    mx,my = b.midpoint()
    drawLabel(b.name,mx,my,font = 'helvetica',size = 20)

def drawHeader(app,title):
    drawRect(0,0,app.width,app.height*0.2,fill='pink',border = 'black')
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
    if key == 'v': # switch to video
        setActiveScreen('video')
    if key == 'a':
        setActiveScreen('athletes')
    if key == 'u':
        setActiveScreen('upload')
        getFiles(app)

# draws the library
def library_redrawAll(app):
    drawHeader(app,'Library')
    drawButton(app,3)
    drawButton(app,5)
    drawVideos(app)
# draws the videos within the library
def drawVideos(app):
    topX = app.width*0.05
    topY = app.height*0.25
    cnt = 0
    for video in app.videos:
        if cnt >= 3:
            cnt = 0
            topX = app.width * 0.05
            topY += iy + app.height * 0.05
        video.thumbnail.thumbnail((app.width*0.8/3,app.width*0.8/3))
        size = video.thumbnail.size
        ix, iy = size
        cmu_image = CMUImage(video.thumbnail)
        drawImage(cmu_image,topX,topY)
        drawLabel(video.name,topX,topY + iy+20,align = 'left',font = 'helvetica')
        drawLabel(video.length,topX + ix,topY+iy+20, align = 'right', font = 'helvetica')
        drawLabel(video.times, topX, topY + iy +30, align = 'left', font = 'helvetica')
        topX += ix + app.width*0.05
        cnt += 1
# controls the mouse clicks within the library
def library_onMousePress(app,x,y):
    if app.buttons[3].inButton(x,y):
        setActiveScreen('main')
    if app.buttons[5].inButton(x,y):
        app.curdir = os.getcwd()
        getFiles(app)
        setActiveScreen('upload')
    for button in app.videobuttons:
        if button.inButton(x,y):
            app.video_path = button.name  # change to custom input
            app.capture = cv2.VideoCapture(app.video_path)
            if not app.capture.isOpened():
                print("error, video")
                exit()
            app.frames = int(app.capture.get(cv2.CAP_PROP_FRAME_COUNT))
            app.fps = app.capture.get(cv2.CAP_PROP_FPS)
            app.current_frame = 0
            app.td_time = 0
            app.time = 0
            app.td_times = []
            app.cum_times = []
            app.recording = False
            app.fromwhere = 'library'
            setActiveScreen('video')
# controls the key presses within the library
def library_onKeyPress(app,key):
    if key == 'q':
        onClose(app)
    if key == 'escape':
        setActiveScreen('main')

def upload_redrawAll(app):
    drawHeader(app, 'Upload')
    drawButton(app, 3)
    if not app.uploaded:
        drawFileExplorer(app)
    else:
        drawSuccess(app)

def upload_onMousePress(app,x,y):
    if app.buttons[3].inButton(x,y) or app.uploaded:
        app.curdir = os.getcwd()
        app.uploaded = False
        setActiveScreen('library')
    if app.uploaded == False:
        for file in app.files:
            if file.inButton(x,y):
                nextdir = app.curdir + '/' + file.name
                if os.path.isdir(nextdir):
                    app.curdir += '/' + file.name
                    getFiles(app)
                elif is_video_file(app.curdir + '/' + file.name):
                    v = Video(app.curdir + '/' + file.name,file.name)
                    if v in app.videos:
                        break
                    v.findLength()
                    v.setThumbnail()
                    app.videos.append(v)
                    app.uploaded = True
                    v.thumbnail.thumbnail((app.width * 0.8 / 3, app.width * 0.8 / 3))
                    size = v.thumbnail.size
                    ix, iy = size
                    app.videobuttons.append(Button(app.curdir + '/' + file.name,app.tx,app.ty,ix,iy))
                    app.tx += ix + app.width * 0.05
                    app.cnt += 1
                    if app.cnt >= 3:
                        app.cnt = 0
                        app.tX = app.width * 0.05
                        app.ty += iy + app.height * 0.05
                break
def upload_onKeyPress(app,key):
    if key == 'q':
        onClose(app)
    if key == 'escape':
        app.curdir = os.getcwd()
        app.uploaded = False
        setActiveScreen('library')
    if key == 'backspace':
        goBack(app)
        getFiles(app)

def goBack(app):
    app.curdir = os.path.dirname(app.curdir)

def drawFileExplorer(app):
    drawLabel(f'{app.curdir}',app.width*0.2,app.height*0.25-20,size = 20, font = 'helvetica', align = 'left')
    drawRect(app.width*0.2,app.height*0.25,app.width*0.6,app.height*0.70,fill=None,border='black')
    for file in app.files:
        drawFile(app,file)
        if os.path.isdir(app.curdir + '/' + file.name):
            drawImage('assets/folder.png',file.tx+2,file.ty)
        elif is_video_file(app.curdir + '/' + file.name):
            drawImage('assets/video.png',file.tx+2,file.ty)

def drawSuccess(app):
    drawLabel('Success!', app.width/2,app.height/2,size = 40, font = 'helvetica', fill = 'lightgreen')
    drawLabel(f'{app.videos[-1].name} was uploaded to library', app.width/2,app.height/2+50,size = 30, font = 'helvetica')

# Checks whether filepath is a video - from ChatGPT
def is_video_file(file_path):
    VIDEO_EXTENSIONS = {".mp4", ".avi", ".mkv", ".mov", ".flv", ".wmv", ".webm"}
    _, extension = os.path.splitext(file_path)  # Extract the file extension
    return extension.lower() in VIDEO_EXTENSIONS

def drawFile(app,button):
    b = button
    drawRect(b.tx,b.ty,b.w,b.h,fill=None,border='black')
    drawLabel(b.name,b.tx + 25,b.ty+9,align = 'left',font = 'helvetica',size = 18)

def getFiles(app):
    files = os.listdir(app.curdir)
    cnt = 0
    app.files = []
    for file in files:
        button = Button(file, app.width * 0.2, app.height * 0.25 + cnt * 20, app.width * 0.6, 20)
        cnt += 1
        app.files.append(button)
    return app.files

# Athletes
def athletes_redrawAll(app):
    drawHeader(app,'Athletes')
    drawButton(app,3)
    drawButton(app,6)
    drawAthletes(app)

def drawAthletes(app):
    topX, topY = app.width * 0.05, app.height * 0.25
    for i in range(len(app.athletes)):
        athlete = app.athletes[i]
        drawRect(topX,topY,app.width*0.9,app.height*0.15,fill=None,border = 'black')
        drawCircle(topX+app.width*0.075,topY + app.height*0.075,50,fill=None,border = 'black')
        drawLabel(athlete.name,topX + app.width * 0.125,topY + app.height * 0.05,size = 20, font = 'helvetica',align = 'left')
        plural = '' if len(athlete.videos) == 1 else 's'
        drawLabel(f'{len(athlete.videos)} video' + plural,topX + app.width * 0.125, topY + app.height * 0.1, size = 20, font = 'helvetica', align = 'left')
        drawLabel(f'{athlete.pr}',topX + app.width * 0.4,topY + app.height * 0.05, size = 20, font = 'helvetica', align = 'right')
        drawAthleteButtons(app,i)
        topY += app.height*0.17

def drawAthletesNoButtons(app):
    topX, topY = app.width * 0.05, app.height * 0.25
    for i in range(len(app.athletes)):
        athlete = app.athletes[i]
        drawRect(topX,topY,app.width*0.9,app.height*0.15,fill=None,border = 'black')
        drawCircle(topX+app.width*0.075,topY + app.height*0.075,50,fill=None,border = 'black')
        drawLabel(athlete.name,topX + app.width * 0.125,topY + app.height * 0.05,size = 20, font = 'helvetica',align = 'left')
        plural = '' if len(athlete.videos) == 1 else 's'
        drawLabel(f'{len(athlete.videos)} video' + plural,topX + app.width * 0.125, topY + app.height * 0.1, size = 20, font = 'helvetica', align = 'left')
        drawLabel(f'{athlete.pr}',topX + app.width * 0.4,topY + app.height * 0.05, size = 20, font = 'helvetica', align = 'right')
        topY += app.height*0.17
def drawAthleteButtons(app,i):
    s = app.setprs[i]
    drawRect(s.tx,s.ty,s.w,s.h,fill = None, border = 'black')
    mx,my = s.midpoint()
    drawLabel(s.name,mx,my,size = 20, font = 'helvetica')
    e = app.editvideos[i]
    drawRect(e.tx,e.ty,e.w,e.h,fill = None, border = 'black')
    mx,my = e.midpoint()
    drawLabel(e.name,mx,my,size = 20, font = 'helvetica')


def athletes_onMousePress(app,x,y):
    if app.buttons[3].inButton(x,y):
        setActiveScreen('main')
    if app.buttons[6].inButton(x,y):
        app.input = ''
        setActiveScreen('athletesAdd')
    for i in range(len(app.setprs)):
        if app.setprs[i].inButton(x,y):
            app.input = ''
            app.activeAthlete = app.athletes[i].name
            setActiveScreen('athletesSetPr')
            return
        if app.editvideos[i].inButton(x,y):
            app.activeAthlete = app.athletes[i].name
            setActiveScreen('athletesEditVideos')
            return
    for i in range(len(app.athletebuttons)):
        if app.athletebuttons[i].inButton(x,y):
            app.activeAthlete = app.athletes[i].name
            setActiveScreen('athletesVideos')

def athletes_onKeyPress(app,key):
    if key == 'q':
        onClose(app)
    if key == 'escape':
        setActiveScreen('main')

def athletesVideos_redrawAll(app):
    drawHeader(app,f'{app.activeAthlete}\'s Videos')
    drawButton(app,3)
    drawAthleteVideos(app)

def drawAthleteVideos(app):
    for i in range(len(app.athletes)):
        if app.athletes[i].name == app.activeAthlete:
            videos = app.athletes[i].videos
    topX = app.width * 0.05
    topY = app.height * 0.25
    cnt = 0
    for video in videos:
        if cnt >= 3:
            cnt = 0
            topX = app.width * 0.05
            topY += iy + app.height * 0.05
        video.thumbnail.thumbnail((app.width * 0.8 / 3, app.width * 0.8 / 3))
        size = video.thumbnail.size
        ix, iy = size
        cmu_image = CMUImage(video.thumbnail)
        drawImage(cmu_image, topX, topY)
        drawLabel(video.name, topX, topY + iy + 20, align='left', font='helvetica')
        drawLabel(video.length, topX + ix, topY + iy + 20, align='right', font='helvetica')
        drawLabel(video.times, topX, topY + iy + 30, align='left', font='helvetica')
        topX += ix + app.width * 0.05
        cnt += 1
def athletesVideos_onMousePress(app,x,y):
    if app.buttons[3].inButton(x,y):
        setActiveScreen('athletes')
    for i in range(len(app.athletes)):
        if app.activeAthlete == app.athletes[i].name:
            buttons = app.athletes[i].videobuttons
            break
    for i in range(len(buttons)):
        if buttons[i].inButton(x,y):
            app.video_path = buttons[i].name  # change to custom input
            app.capture = cv2.VideoCapture(app.video_path)
            if not app.capture.isOpened():
                print("error, video")
                exit()
            app.frames = int(app.capture.get(cv2.CAP_PROP_FRAME_COUNT))
            app.fps = app.capture.get(cv2.CAP_PROP_FPS)
            app.current_frame = 0
            app.td_time = 0
            app.time = 0
            app.td_times = []
            app.cum_times = []
            app.recording = False
            app.fromwhere = 'athletes'
            setActiveScreen('video')

def athletesVideos_onKeyPress(app,key):
    if key == 'escape':
        setActiveScreen('athletes')
def athletesAdd_redrawAll(app):
    drawHeader(app,'Add Athlete')
    drawButton(app,3)
    drawInput(app,'Athlete\'s name')

def drawInput(app,name):
    drawLabel(f'Please enter the {name}:',app.width/2,app.height*0.4,font = 'helvetica',size = 40)
    drawLabel(app.input,app.width/2,app.height * 0.5, font = 'helvetica', size = 40)

def athletesAdd_onKeyPress(app,key):
    if key == 'escape':
        setActiveScreen('athletes')
    elif key == 'backspace':
        app.input = app.input[:-1]
    elif key == 'space':
        app.input += ' '
    elif key == 'enter':
        app.athletes.append(Athlete(app.input))
        b = Button('Set PR',app.ax + app.width * 0.7,app.ay+app.height * 0.05,app.width*0.15,app.height*0.05)
        b.assignAthlete(app.input)
        app.setprs.append(b)
        b = Button('Edit Videos',app.ax + app.width * 0.5,app.ay+app.height * 0.05,app.width*0.15,app.height*0.05)
        b.assignAthlete(app.input)
        app.editvideos.append(b)
        b = Button(app.input,app.ax,app.ay,app.width*0.9,app.height*0.15)
        b.assignAthlete(app.input)
        app.athletebuttons.append(b)
        app.ay += app.height * 0.17
        setActiveScreen('athletes')
    else:
        app.input += key
def athletesAdd_onMousePress(app,x,y):
    if app.buttons[3].inButton(x,y):
        setActiveScreen('main')
def athletesSetPr_redrawAll(app):
    drawHeader(app,'Set PR')
    drawButton(app,3)
    drawInput(app,'PR')
def athletesSetPr_onMousePress(app,x,y):
    if app.buttons[3].inButton(x, y):
        setActiveScreen('athletes')
def athletesSetPr_onKeyPress(app,key):
    if key == 'escape':
        setActiveScreen('athletes')
    elif key == 'backspace':
        app.input = app.input[:-1]
    elif key == 'enter':
        if not app.input.replace('.','',1).isdigit():
            app.input = ''
        else:
            for i in range(len(app.athletes)):
                if app.activeAthlete == app.athletes[i].name:
                    app.athletes[i].setPr(app.input)
                    break
            setActiveScreen('athletes')
    elif key in '1234567890.':
        app.input += key
def athletesEditVideos_redrawAll(app):
    drawHeader(app,'Edit Videos')
    drawButton(app,3)
    drawVideos(app)

def athletesEditVideos_onMousePress(app,x,y):
    if app.buttons[3].inButton(x, y):
        setActiveScreen('athletes')
    for j in range(len(app.videobuttons)):
        if app.videobuttons[j].inButton(x,y):
            i = findAthlete(app,app.activeAthlete)
            b = app.videobuttons[len(app.athletes[i].videos)].copy()
            b.rename(app.videobuttons[j].name)
            app.athletes[i].addVideo(app.videos[j],b)
            setActiveScreen('athletes')

def athletesEditVideos_onKeyPress(app,key):
    if key == 'escape':
        setActiveScreen('athletes')

def findAthlete(app,athlete):
    for i in range(len(app.athletes)):
        if app.athletes[i].name == athlete:
            return i
    return -1

# Pick Athlete to strategize
def strategize_redrawAll(app):
    drawHeader(app,'Strategize')
    drawButton(app,3)
    drawAthletesNoButtons(app)
def strategize_onMousePress(app,x,y):
    if app.buttons[3].inButton(x,y):
        setActiveScreen('main')
    for i in range(len(app.athletebuttons)):
        if app.athletebuttons[i].inButton(x,y):
            app.activeAthlete = app.athletes[i].name
            setActiveScreen('strategizeVideo')

def strategize_onKeyPress(app,key):
    if key == 'q':
        onClose(app)
    if key == 'escape':
        setActiveScreen('main')

# Video Selection to Strategize
def strategizeVideo_redrawAll(app):
    drawHeader(app,'Select Video')
    drawButton(app,3)
    drawAthleteVideos(app)

def strategizeVideo_onKeyPress(app,key):
    if key == 'escape':
        setActiveScreen('strategize')

def strategizeVideo_onMousePress(app,x,y):
    if app.buttons[3].inButton(x,y):
        setActiveScreen('strategize')
    for i in range(len(app.athletes)):
        if app.activeAthlete == app.athletes[i].name:
            buttons = app.athletes[i].videobuttons
            break
    for i in range(len(buttons)):
        if buttons[i].inButton(x, y):
            j = findAthlete(app,app.activeAthlete)
            app.activeVideo = app.athletes[j].videos[i]
            findColors(app)
            predictTDTimes(app)
            makeTips(app)
            setActiveScreen('times')

# Finds the Appropriate Colors based on Split Times
def findColors(app):
    times = app.activeVideo.times
    if times == []: return
    times = [float(times[i]) for i in range(len(times))]
    colors = ['black']
    fastest = max(times[1:])
    slowest = min(times[1:])
    for i in range(1,len(times)):
        if fastest == slowest:
            colors.append('black')
        elif times[i] == fastest:
            colors.append('green')
        elif times[i] == slowest:
            colors.append('red')
        else:
            colors.append('black')
    app.timecolors = colors

# Analyzes Times for a single video
def times_redrawAll(app):
    drawHeader(app,str(app.activeVideo))
    drawButton(app,3)
    drawTimeAnalysis(app)
    drawTargetTimeInput(app)
    drawPredictionTimes(app)
    if app.targettime != None:
        drawTargetTimes(app)
    if app.start != None:
        drawTip(app,app.start,app.height * 0.65)
    if app.middle != None:
        drawTip(app,app.middle,app.height * 0.75)
    if app.end != None:
        drawTip(app,app.end,app.height * 0.85)

def drawTip(app,tip,height):
    drawLabel(f'{tip.note}',app.width * 0.5, height, size = 30, font = 'helvetica',fill = tip.color)
    drawLabel(f'{tip.tip}',app.width * 0.5, height + app.height *0.05, size = 30, font = 'helvetica',fill = tip.color)
def drawTargetTimeInput(app):
    drawLabel(f"Input Time Here: {app.targettimeinput}",app.width*0.5, app.height*0.225,font = 'helvetica', size = 20)

def drawPredictionTimes(app):
    drawLabel(f'Your predicted time: {app.userpredictedtime}', app.width * 0.50, app.height *0.40, size=30, font='helvetica')
    for i in range(len(app.touchdown_times[app.userpredictedtime])):
        drawLabel(app.touchdown_times[app.userpredictedtime][i], app.width * 0.05 + (i) * (app.width * 0.9 / 10),
                  app.height * 0.45, size=40, font='helvetica')

def drawTargetTimes(app):
    drawLabel(f'Splits for this time: {app.targettime}',app.width * 0.50,app.height * 0.50, size=30, font='helvetica')
    for i in range(len(app.touchdown_times[app.targettime])):
        drawLabel(app.touchdown_times[app.targettime][i],app.width * 0.05 + (i) * (app.width*0.9/10),app.height * 0.55,size = 40, font = 'helvetica')

# draws the splits from a video
def drawTimeAnalysis(app):
    # drawRect(app.width*0.05, app.height*0.3,app.width*0.9,app.height*0.1,fill=None,border='black')
    for i in range(len(app.activeVideo.times)):
        drawLabel(app.activeVideo.times[i],app.width*0.05 + i * (app.width*0.9/10), app.height*0.35,size = 40, font = 'helvetica',fill = app.timecolors[i])

def times_onMousePress(app,x,y):
    if app.buttons[3].inButton(x,y):
        setActiveScreen('strategizeVideo')

def times_onKeyPress(app,key):
    if key == 'escape':
        setActiveScreen('strategizeVideo')
    elif key in '1234567890.':
        app.targettimeinput += key
    elif key == 'backspace':
        app.targettimeinput = app.targettimeinput[:-1]
    elif key == 'space':
        app.targettimeinput += ' '
    elif key == 'enter':
        if not app.targettimeinput.replace('.','',1).isdigit():
            app.targettimeinput = ''
        else:
            app.targettime = float(app.targettimeinput)
            times = sorted([time for time in app.touchdown_times])[::-1]
            for time in times:
                if app.targettime >= time:
                    app.targettime = time
                    break
def predictTDTimes(app):
    athletecumtimes = app.activeVideo.cum_times
    splitnumber = len(athletecumtimes) - 1
    totalusertime = athletecumtimes[splitnumber]
    timesplit = {}
    for time in app.touchdown_times_cum:
        timesplit[time] = app.touchdown_times_cum[time][splitnumber]
    diffs = {}
    for time in timesplit:
        diffs[time] = abs(totalusertime - timesplit[time])
    times = sorted([diffs[time] for time in diffs])
    for time in diffs:
        if diffs[time] == times[0]:
            app.userpredictedtime = time

def makeTips(app):
    times = [float(time) for time in app.activeVideo.times]
    predictedtimes = app.touchdown_times[app.userpredictedtime]
    diff = []
    for i in range(len(times)):
        diff.append(predictedtimes[i] - times[i])
    if len(times) >= 3:
        tip = Tip('start')
        predstart = diff[0] + diff[1] + diff[2]
        if predstart < -0.1:
            tip.note = 'Your start is slower than expected'
            tip.tip = 'Work on getting out of the blocks'
            tip.color = 'red'
        else:
            tip.note = 'Your start is on pace for a good race'
            tip.tip = 'Keep it up!'
            tip.color = 'green'
        app.start = tip
    if len(times) >= 1:
        tip = Tip('middle')
        predmid = 0
        for i in range(3,7):
            predmid += diff[i]
            if i >= len(times):
                break
        if predmid < -0.1:
            tip.note = 'The middle of your race is slower than expected.'
            tip.tip = 'Work on consistency over the hurdles'
            tip.color = 'red'
        else:
            tip.note = 'The middle of your race is great!'
            tip.tip = 'Keep going!'
            tip.color = 'green'
        app.middle = tip
    if len(times) > -0.1:
        tip = Tip('end')
        predend = 0
        for i in range(7,len(times)):
            predend += diff[i]
        if predend < 0:
            tip.note = 'The end of your race is slower than expected.'
            tip.tip = 'Work on sprint and hurdle endurance'
            tip.color = 'red'
        else:
            tip.note = 'The end of your race is fantastic'
            tip.tip = 'You are awesome!'
            tip.color = 'green'
        app.end = tip


# Video


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
    if key == 'escape':
        if app.fromwhere == 'library':
            setActiveScreen('library')
        else:
            setActiveScreen('athletesVideos')
    if key == 't':
        if app.td_time == 0:
            app.td_time = findTime(app)
        else:
            findTDTime(app)
        app.recording = not app.recording
    if key == 'backspace':
        if len(app.td_times) > 0:
            app.td_times.pop()
            app.cum_times.pop()
    if key == 'r':
        app.current_frame = 0
        app.td_times = []
        app.cum_times = []
    if key == 'v':
        for i in range(len(app.videos)):
            if app.videos[i].path == app.video_path:
                app.videos[i].addTimes(app.td_times,app.cum_times)
                break
    if app.paused:
        if key == 'a':
            app.current_frame -= 1
            if app.current_frame < 0:
                app.current_frame += 1
        elif key == 's':
            app.current_frame += 1
            if app.current_frame >= app.frames:
                app.current_frame -= 1
        findTime(app)

def video_onMousePress(app,x,y):
    if app.buttons[3].inButton(x,y):
        if app.fromwhere == 'library':
            setActiveScreen('library')
        else:
            setActiveScreen('athletesVideos')
    if app.instructionbutton.inButton(x,y):
        setActiveScreen('instructions')

def video_redrawAll(app):
    drawFrame(app,getFrame(app))
    drawTimes(app)
    drawButton(app,3)
    b = app.instructionbutton
    drawRect(b.tx, b.ty, b.w, b.h, fill='white', border='black')
    mx, my = b.midpoint()
    drawLabel(b.name, mx, my, font='helvetica', size=20)

# draws the times on screen
def drawTimes(app):
    drawRect(app.width/2-60,app.height*0.92,120,40,fill='white',border = 'black')
    drawLabel(f'{app.time:.2f}',app.width/2,app.height*0.92+20,fill='black',size = 20)
    drawRect(app.width/2-60,app.height*0.1-20,120,40,fill='white',border = 'black')
    td_time = app.time - app.td_time if app.td_time != 0 else app.td_time
    drawLabel(f'{td_time:.2f}', app.width / 2, app.height * 0.1, fill='black', size = 20)
    if app.recording:
        drawCircle(app.width/2+35,app.height*0.1,8,fill='red')
    for i in range(len(app.td_times)):
        boxh = int(app.height/11)
        # time
        drawRect(0,0+boxh*i,boxh,boxh,fill='white',border = 'black')
        drawLabel(f'{app.td_times[i]}',(boxh//2),(boxh//2)+boxh*i,fill='black',size = 20)
        # label
        drawRect(boxh,0+boxh*i,20,boxh,fill='white',border='black')
        drawLabel(f'{i}',boxh+10,boxh//2 + boxh*i,fill = 'black',size = 20)
        # cumulative time
        drawRect(boxh+20,0+boxh*i,boxh,boxh,fill='white',border='black')
        drawLabel(f'{app.cum_times[i]:.2f}',boxh+20 + boxh//2,boxh//2+boxh*i,fill='black',size=20)

def instructions_redrawAll(app):
    drawHeader(app,'Instructions')
    drawButton(app,3)
    drawInstructions(app)

def drawInstructions(app):
    drawLabel('Use \'t\' to start/recording splits',app.width*0.5, app.height*0.3,font = 'helvetica', size = 30)
    drawLabel('Use \'p\' to pause/unpause the video',app.width*0.5, app.height*0.4,font = 'helvetica', size = 30)
    drawLabel('Use \'a\' and \'s\' to go back and forwards a frame',app.width*0.5, app.height*0.5,font = 'helvetica', size = 30)
    drawLabel('Use \'v\' to save the current splits to the video',app.width*0.5, app.height*0.6,font = 'helvetica', size = 30)
    drawLabel('Use \'r\' to restart the video',app.width*0.5, app.height*0.7,font = 'helvetica', size = 30)
    drawLabel('Use \'backspace\' to delete the most recent split',app.width*0.5, app.height*0.8,font = 'helvetica', size = 30)

def instructions_onMousePress(app,x,y):
    if app.buttons[3].inButton(x,y):
        setActiveScreen('video')

def instructions_onKeyPress(app,key):
    if key == 'escape':
        setActiveScreen('video')

## other methods ##

# builds the not cumulative target touchdown times
def buildTDTimes(app):
    for targettime in app.touchdown_times_cum:
        times = app.touchdown_times_cum[targettime]
        result = [times[0]]
        for i in range(1,len(times)):
            result.append(pythonRound(times[i]-times[i-1],2))
        app.touchdown_times[targettime] = result

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
    if len(app.cum_times) == 0:
        app.cum_times.append(time)
    else:
        app.cum_times.append(app.cum_times[-1]+time)
    app.td_time = 0
    return time


# gets the current frame of the video
def getFrame(app):
    app.capture.set(cv2.CAP_PROP_POS_FRAMES, app.current_frame)
    ret, frame = app.capture.read()
    if not ret:
        return
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    pil_image = im.fromarray(frame)
    cmu_image = CMUImage(pil_image)
    return cmu_image

# draws the current frame
def drawFrame(app,img):
    if img == None: return
    drawImage(img,0,0)

def onClose(app):
    # clearFolder(app)
    app.capture.release()
    app.quit()


def main():
    runAppWithScreens('main')

main()