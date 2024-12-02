class Athlete:
    def __init__(self,name):
        self.name = name
        self.videos = []
        self.pr = 'No PR set'

    def addVideo(self,video):
        if video not in self.videos:
            self.videos.append(video)

    def setPr(self,pr):
        self.pr = pr