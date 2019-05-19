# -*- coding: utf-8 -*-

class ai:
    def __init__(self, x=4, y=4, alive = True):
        self.x = x
        self.y = y
        self.color = 14
        self.alive = alive
        
    def checkCollision(self,x,y):
        xMin = x - 1
        xMax = x + 1
        yMin = y - 1
        yMax = y + 1
        
        if (self.x >= xMin and self.x <= xMax
            and self.y >= yMin and self.y <= yMax):
            self.alive = False
            