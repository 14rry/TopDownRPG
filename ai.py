# -*- coding: utf-8 -*-
import pyxel

class ai:
    def __init__(self, x=4, y=4, alive = True):
        self.x = x
        self.y = y
        self.color = 14
        self.alive = alive
        self.size = 9
        
    # check if the player's attack hits the enemy.. should probably be moved    
    def checkCollision(self,x,y):
        xMin = x - 1
        xMax = x + 1
        yMin = y - 1
        yMax = y + 1
        
        if (self.x >= xMin and self.x <= xMax
            and self.y >= yMin and self.y <= yMax):
            self.alive = False

    def draw_self(self):
        if not self.alive:
            self.size -= 1 # shrink on death
        if self.size > 0:
            pyxel.rect(self.x*10,
                        self.y*10,
                        self.size,
                        self.size,
                        self.color)
            