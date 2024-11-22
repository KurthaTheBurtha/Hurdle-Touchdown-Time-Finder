class Button():
    def __init__(self,name,tx,ty,w,h):
        self.name = name
        self.tx = tx
        self.ty = ty
        self.w = w
        self.h = h

    def inButton(self,x,y):
        return (self.tx <= x <= self.tx + self.w) and (self.ty <= y <= self.ty + self.h)
    
    def midpoint(self):
        return (self.tx+self.w/2,self.ty+self.h/2)