# Kurt Schimmel
# kschimme
# Section L

class Athlete:
    # Holds information for an Athlete
    def __init__(self,name):
        self.name = name
        self.videos = []
        self.videobuttons = []
        self.pr = 'No PR set'

    def addVideo(self,video,button):
        if video not in self.videos:
            self.videos.append(video)
            self.videobuttons.append(button)

    def setPr(self,pr):
        self.pr = pr