# Kurt Schimmel
# kschimme
# Section L

import copy
class Button():
    def __init__(self,name,tx,ty,w,h):
        self.name = name
        self.tx = tx
        self.ty = ty
        self.w = w
        self.h = h
        self.athlete = None

    def __repr__(self):
        return f'{self.name}'

    def inButton(self,x,y):
        return (self.tx <= x <= self.tx + self.w) and (self.ty <= y <= self.ty + self.h)
    
    def midpoint(self):
        return (self.tx+self.w/2,self.ty+self.h/2)

    def assignAthlete(self,athlete):
        self.athlete = athlete

    def rename(self,name):
        self.name = name

    def copy(self):
        return copy.deepcopy(self)