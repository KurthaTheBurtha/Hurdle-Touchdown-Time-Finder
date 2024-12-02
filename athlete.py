class Athlete:
    def __int__(self,name):
        self.name = name
        self.videos = []
        self.pr = None

    def addVideo(self,video):
        if video not in self.videos:
            self.videos.append(video)