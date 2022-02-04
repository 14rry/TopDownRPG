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
        self.player_vel_x = 0
        self.player_vel_y = 0
        
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
            newX = self.playerX
            newY = self.playerY
            
            attackCooldown = 4

            dir_x = 0
            dir_y = 0
            if pyxel.btn(pyxel.KEY_RIGHT):
                dir_x += 1
                #newX = min(self.playerX+speed,self.levelSize)
            if pyxel.btn(pyxel.KEY_LEFT):
                dir_x -= 1
                #newX = max(self.playerX-speed,-1)
            if pyxel.btn(pyxel.KEY_UP):
                dir_y -= 1
                #newY = max(self.playerY-speed,-1)
            if pyxel.btn(pyxel.KEY_DOWN):
                dir_y += 1
                #newY = min(self.playerY+speed,self.levelSize)

            # account for faster diagonals
            if (dir_y != 0 and dir_x != 0):
                dir_y *= .7
                dir_x *= .7
            
            accel = .3
            deccel = .1
            max_vel = .4

            # deacel logic

            # if (dir_y == 0 and dir_x == 0):
            #     if abs(self.player_vel_y) < .04:
            #         self.player_vel_y = 0
            #     if abs(self.player_vel_x) < .04:
            #         self.player_vel_x = 0

            #     if self.player_vel_x > 0:
            #         self.player_vel_x -= deccel
            #     elif self.player_vel_x < 0:
            #         self.player_vel_x += deccel

                # if self.player_vel_y > 0:
                #     self.player_vel_y -= deccel
                # elif self.player_vel_y < 0:
                #     self.player_vel_y += deccel

            #else:
            #     self.player_vel_x += dir_x * accel
            #     self.player_vel_y += dir_y * accel

            # self.player_vel_x = max(min(self.player_vel_x,max_vel),-max_vel)
            # self.player_vel_y = max(min(self.player_vel_y,max_vel),-max_vel)

            # newX = self.playerX + self.player_vel_x
            # newY = self.playerY + self.player_vel_y

            newX = self.playerX + (dir_x*accel)
            newY = self.playerY + (dir_y*accel)
          
#            xVec = -1 * pyxel.btnp(pyxel.KEY_LEFT) + pyxel.btnp(pyxel.KEY_RIGHT)
#            yVec = -1 * pyxel.btnp(pyxel.KEY_UP) + pyxel.btnp(pyxel.KEY_DOWN)
#            
            newX = max(min(newX,self.levelSize),-1)
            newY = max(min(newY,self.levelSize),-1)

            roundX = self.round_player_pos(dir_x,newX)
            roundY = self.round_player_pos(dir_y,newY)
            
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

            roundX = self.round_player_pos(dir_x,newX)
            roundY = self.round_player_pos(dir_y,newY)

            # check collision
            if self.level[roundY,roundX] == 1: # clear floor
                self.playerX = newX
                self.playerY = newY
            elif self.level[roundY,roundX] == 3: # npc
                self.dialogText = dialog.invoke(levels.levelIndex,roundX,roundY)
                self.dialogScreen =  True
            else:
                self.player_vel_y = 0
                self.player_vel_x = 0
                
            # player attack
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
        
        posX = 10*self.playerX;
        posY = 10*self.playerY;
        
        # draw map
        for i in range(self.levelSize):
            for j in range(self.levelSize):
                pyxel.rect(10*i,10*j,9,9,self.level[j,i])
                pyxel.rectb(10*i,10*j,9,9,gridColor)
        
        # draw ai
        for baddy in self.currentAI:
            baddy.draw_self()
        
        if self.attack:
            pyxel.rect(10*(self.playerX-1),
                       10*(self.playerY-1),
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
        pyxel.rectb(posX,posY,9,9,gridColor)
        
        if self.dialogScreen:
            pyxel.rect(5,5,self.levelSize * 10 - 5,self.levelSize * 2 + 5,0)
            pyxel.rectb(5,5,self.levelSize * 10 - 5,self.levelSize * 2 + 5,3)
            for textIndex in range(len(self.dialogText)):
                pyxel.text(10,10*(textIndex+1),self.dialogText[textIndex],3)
                
        # draw health bar
        xHealth = (self.levelSize - 2*(10 - self.playerHealth))*10
        pyxel.rect(0,self.levelSize*10,xHealth,9,8)
   
    def reset(self):
        levels.reset(levels)
        self.startGame()

    def round_player_pos(self,dir,val):
        if dir > 0:
            return pyxel.ceil(val)
        else:
            return pyxel.floor(val)

        
App()