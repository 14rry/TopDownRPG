# -*- coding: utf-8 -*-
"""
Created on Fri Aug 10 22:43:07 2018

@author: larry
"""

import pyxel
import numpy as np

import levels
import dialog

class App:
    def __init__(self):
        self.levelSize = 20

        pyxel.init(self.levelSize*10, self.levelSize*10+10)
        
        self.startGame()
        
        pyxel.run(self.update, self.draw)
        
    def startGame(self):
        self.playerX = 4
        self.playerY = 17
        self.playerHealth = 10
        
        self.level = levels.levels[1,1]
        
        self.currentAI = levels.loadAI()
        
        self.attack = False
        self.attackFrame = 0
        
        self.dialogScreen = False
        self.dialogText = [""]

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        if pyxel.btnp(pyxel.KEY_R):
            self.reset()
            
            
#        def btnp(self, key, hold=0, period=0):
#        press_frame = self._key_state.get(key, 0)
#
#        return (press_frame == self._module.frame_count
#                or press_frame > 0 and period > 0 and
#                (self._module.frame_count - press_frame - hold) % period == 0)
#            
        if self.dialogScreen:
            if pyxel.btnr(pyxel.KEY_Z):
                self.dialogScreen = False
        else:
            # check enemy collision
            for baddy in self.currentAI:
                if (baddy.alive and 
                    baddy.x == self.playerX and
                    baddy.y == self.playerY):
                    self.playerHealth -= 1
            
            
            # player movement logic  
            hold = 2
            repeat = 2
            newX = self.playerX
            newY = self.playerY
            
            attackCooldown = 4
            
            if pyxel.btnp(pyxel.KEY_RIGHT,hold,repeat):
                newX = min(self.playerX+1,self.levelSize)
            if pyxel.btnp(pyxel.KEY_LEFT,hold,repeat):
                newX = max(self.playerX-1,-1)
            if pyxel.btnp(pyxel.KEY_UP,hold,repeat):
                newY = max(self.playerY-1,-1)
            if pyxel.btnp(pyxel.KEY_DOWN,hold,repeat):
                newY = min(self.playerY+1,self.levelSize)
          
#            xVec = -1 * pyxel.btnp(pyxel.KEY_LEFT) + pyxel.btnp(pyxel.KEY_RIGHT)
#            yVec = -1 * pyxel.btnp(pyxel.KEY_UP) + pyxel.btnp(pyxel.KEY_DOWN)
#            
#            newX = max(min(self.playerX+xVec,self.levelSize),-1)
#            newY = max(min(self.playerY+yVec,self.levelSize),-1)
            
            
    
            # check if we need to change levels
            if (newX == self.levelSize or 
                newY == self.levelSize or
                newX < 0 or
                newY < 0):
                    self.level = levels.changeLevel(newX,newY,self.levelSize)
                    if newX == self.levelSize:
                        newX = 0
                    elif newX < 0:
                        newX = self.levelSize - 1
                    if newY == self.levelSize:
                        newY = 0
                    elif newY < 0:
                        newY = self.levelSize - 1
                        
                    # load AI
                    self.currentAI = levels.loadAI()

            # check collision
            if self.level[newY,newX] == 1: # clear floor
                self.playerX = newX
                self.playerY = newY
            elif self.level[newY,newX] == 3: # npc
                self.dialogText = dialog.invoke(levels.levelIndex,newX,newY)
                self.dialogScreen =  True      
                
            # player attack
            if self.attack:
                if pyxel.frame_count - self.attackFrame > attackCooldown:
                    self.attack = False
                for baddy in self.currentAI:
                    if baddy.alive:
                        baddy.checkCollision(self.playerX,self.playerY)
            else:
                if pyxel.btnp(pyxel.KEY_Z):
                    self.attack = True
                    self.attackFrame = pyxel.frame_count

        
    def draw(self):
        pyxel.pal(1, 7) # background color
        gridColor = 6
        
        pyxel.cls(6)

        
        posX = 10*self.playerX;
        posY = 10*self.playerY;
        
        # draw map
        for i in range(self.levelSize):
            for j in range(self.levelSize):
                pyxel.rect(10*i,10*j,(10*i)+9,(10*j)+9,self.level[j,i])
                pyxel.rectb(10*i,10*j,(10*i)+9,(10*j)+9,gridColor)
        
        # draw ai
        for baddy in self.currentAI:
            if baddy.alive:
                pyxel.rect(baddy.x*10,
                           baddy.y*10,
                           (baddy.x*10)+9,
                           (baddy.y*10)+9,
                           baddy.color)

        
        if self.attack:
            pyxel.rect(10*(self.playerX-1),
                       10*(self.playerY-1),
                       10*(self.playerX+2),
                       10*(self.playerY+2),
                       12)
            pyxel.rectb(10*(self.playerX-1),
                       10*(self.playerY-1),
                       10*(self.playerX+2),
                       10*(self.playerY+2),
                       gridColor)
        # draw player        
        pyxel.rect(posX,posY,posX+9,posY+9,8)
        pyxel.rectb(posX,posY,posX+9,posY+9,gridColor)
        
        if self.dialogScreen:
            pyxel.rect(5,5,self.levelSize * 10 - 5,self.levelSize * 2 + 5,0)
            pyxel.rectb(5,5,self.levelSize * 10 - 5,self.levelSize * 2 + 5,3)
            for textIndex in range(len(self.dialogText)):
                pyxel.text(10,10*(textIndex+1),self.dialogText[textIndex],3)
                
        # draw health bar
        xHealth = (self.levelSize - 2*(10 - self.playerHealth))*10
        pyxel.rect(0,self.levelSize*10,xHealth,(self.levelSize*10) + 9,8)
   
    def reset(self):
        levels.reset(levels)
        self.startGame()
        
App()