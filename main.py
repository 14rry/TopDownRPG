# -*- coding: utf-8 -*-
"""
Created on Fri Aug 10 22:43:07 2018

@author: larry
"""

import pyxel
import numpy as np

import levels
import dialog
import player

class App:
    def __init__(self):
        self.levelSize = 20

        pyxel.init(self.levelSize*10, self.levelSize*10+10,fps = 60)
        
        self.startGame()
        
        pyxel.run(self.update, self.draw)
        
    def startGame(self):
        self.player = player.player(4,17)
        
        self.level = levels.levels[1,1]
        self.currentAI = levels.loadAI()
        
        self.dialogScreen = False
        self.dialogText = [""]

        self.attack = False
        self.attack_frame = 0

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
                    baddy.x == self.player.x and
                    baddy.y == self.player.y):
                    self.playerHealth -= 1
            
            [newX,newY] = self.player.move()

            newX = max(min(newX,self.levelSize),-1)
            newY = max(min(newY,self.levelSize),-1)
            
            roundX = self.round_player_pos(newX)
            roundY = self.round_player_pos(newY)
            
            # check if we need to change levels
            if (roundX == self.levelSize or 
                roundY == self.levelSize or
                roundX < 0 or
                roundY < 0):
                    self.level = levels.changeLevel(roundX,roundY,self.levelSize)
                    if roundX == self.levelSize:
                        newX = 0
                    elif roundX < 0:
                        newX = self.levelSize - 1
                    if roundY == self.levelSize:
                        newY = 0
                    elif roundY < 0:
                        newY = self.levelSize - 1
                        
                    # load AI
                    self.currentAI = levels.loadAI()

            roundX = self.round_player_pos(newX)
            roundY = self.round_player_pos(newY)

            # check collision
            if self.level[roundY,roundX] == 1: # clear floor
                self.player.x = newX
                self.player.y = newY
            elif self.level[roundY,roundX] == 3: # npc
                self.dialogText = dialog.invoke(levels.levelIndex,roundX,roundY)
                self.dialogScreen =  True
            else:
                self.player.vel_y = 0
                self.player.vel_x = 0
                
            # player attack
            attackCooldown = 14
            if self.attack:
                if pyxel.frame_count - self.attackFrame > attackCooldown:
                    self.attack = False
                for baddy in self.currentAI:
                    if baddy.alive:
                        baddy.checkCollision(roundX,roundY)
            else:
                if pyxel.btnp(pyxel.KEY_Z):
                    self.attack = True
                    self.attackFrame = pyxel.frame_count

        
    def draw(self):
        pyxel.pal(1, 7) # background color
        gridColor = 6
        
        pyxel.cls(6)
        
        posX = 10*self.player.x
        posY = 10*self.player.y
        
        # draw map
        for i in range(self.levelSize):
            for j in range(self.levelSize):
                pyxel.rect(10*i,10*j,10,10,self.level[j,i])
                #pyxel.rectb(10*i,10*j,10,10,gridColor)
        
        # draw ai
        for baddy in self.currentAI:
            baddy.draw_self()
        
        if self.attack:
            pyxel.rect(10*(self.player.x-1),
                       10*(self.player.y-1),
                       29,
                       29,
                       12)
            # pyxel.rectb(10*(self.playerX-1),
            #            10*(self.playerY-1),
            #            10*(self.playerX+2),
            #            10*(self.playerY+2),
            #            gridColor)
        # draw player        
        pyxel.rect(posX,posY,9,9,8)
        #pyxel.rectb(posX,posY,9,9,gridColor)
        
        if self.dialogScreen:
            pyxel.rect(5,5,self.levelSize * 10 - 5,self.levelSize * 2 + 5,0)
            pyxel.rectb(5,5,self.levelSize * 10 - 5,self.levelSize * 2 + 5,3)
            for textIndex in range(len(self.dialogText)):
                pyxel.text(10,10*(textIndex+1),self.dialogText[textIndex],3)
                
        # draw health bar
        xHealth = (self.levelSize - 2*(10 - self.player.health))*10
        pyxel.rect(0,self.levelSize*10,xHealth,9,8)
   
    def reset(self):
        levels.reset(levels)
        self.startGame()

    def round_player_pos(self,val):
        return round(val)
        if dir > 0:
            return pyxel.ceil(val)
        else:
            return pyxel.floor(val)

        
App()