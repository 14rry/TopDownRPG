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
        self.levelSize = 16
        self.grid_size = 8


        pyxel.init(self.levelSize*self.grid_size, self.levelSize*self.grid_size+self.grid_size,fps = 60)
        pyxel.load("topdown.pyxres")

        self.startGame()
        
        pyxel.run(self.update, self.draw)
        
    def startGame(self):
        self.player = player.player(4,4)
        
        self.level = [1,1]
        #self.level = levels.levels[1,1]
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
                    self.level = levels.changeLevel(roundX,roundY,self.level[0],self.level[1],self.levelSize)
                    if roundX == self.levelSize:
                        newX = 0
                    elif roundX < 0:
                        newX = self.levelSize - 1
                    if roundY == self.levelSize:
                        newY = 0
                    elif roundY < 0:
                        newY = self.levelSize - 1
                    
                    # TODO: fix AI with new tilemaps
                    # # load AI
                    # self.currentAI = levels.loadAI()

            roundX = self.round_player_pos(newX)
            roundY = self.round_player_pos(newY)
            roundOldX = self.round_player_pos(self.player.x)
            roundOldY = self.round_player_pos(self.player.y)

            # check collision
            tm_pos = self.player_pos_to_tm(roundX,roundY)
            tm_val = pyxel.tilemap(0).pget(tm_pos[0],tm_pos[1])

            tm_pos = self.player_pos_to_tm(roundOldX,roundY)
            tm_val_old_x = pyxel.tilemap(0).pget(tm_pos[0],tm_pos[1])

            tm_pos = self.player_pos_to_tm(roundX,roundOldY)
            tm_val_old_y = pyxel.tilemap(0).pget(tm_pos[0],tm_pos[1])

            if tm_val == (0,0): # clear floor
                self.player.x = newX
                self.player.y = newY
            elif tm_val_old_x == (0,0):
                self.player.y = newY
            elif tm_val_old_y == (0,0):
                self.player.x = newX
            else:
                self.player.vel_y = 0
                self.player.vel_x = 0

            roundX = self.round_player_pos(newX)
            roundY = self.round_player_pos(newY)
            tm_pos = self.player_pos_to_tm(roundX,roundY)
            tm_val = pyxel.tilemap(0).pget(tm_pos[0],tm_pos[1])

            if tm_val == (2,1): # npc
                self.dialogText = dialog.invoke(levels.levelIndex,roundX,roundY) # TODO: need to fix level index with new tilemaps
                self.dialogScreen =  True
                
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
        
        posX = self.grid_size*self.player.x
        posY = self.grid_size*self.player.y
        
        # draw map
        pyxel.bltm(0,0,0,self.level[0]*self.levelSize*self.grid_size,self.level[1]*self.levelSize*self.grid_size,self.grid_size*self.levelSize,self.grid_size*self.levelSize,1)

        # draw ai
        for baddy in self.currentAI:
            baddy.draw_self()
        
        if self.attack:
            #pyxel.image(0.)
            pyxel.rect(self.grid_size*(self.player.x-1),
                       self.grid_size*(self.player.y-1),
                       self.grid_size*3,
                       self.grid_size*3,
                       12)
            # pyxel.rectb(self.grid_size*(self.playerX-1),
            #            self.grid_size*(self.playerY-1),
            #            self.grid_size*(self.playerX+2),
            #            self.grid_size*(self.playerY+2),
            #            gridColor)

        # draw player        
        # pyxel.rect(posX,posY,self.grid_size,self.grid_size,8)
        self.player.draw()
        #pyxel.rectb(posX,posY,9,9,gridColor)
        
        if self.dialogScreen:
            pyxel.rect(5,5,self.levelSize * self.grid_size - 5,self.levelSize * 2 + 5,0)
            pyxel.rectb(5,5,self.levelSize * self.grid_size - 5,self.levelSize * 2 + 5,3)
            for textIndex in range(len(self.dialogText)):
                pyxel.text(self.grid_size,self.grid_size*(textIndex+1),self.dialogText[textIndex],3)
                
        # draw health bar
        xHealth = (self.levelSize - 2*(self.grid_size - self.player.health))*self.grid_size
        pyxel.rect(0,self.levelSize*self.grid_size,xHealth,9,8)
   
    def reset(self):
        levels.reset(levels)
        self.startGame()

    def round_player_pos(self,val):
        return round(val)
        if dir > 0:
            return pyxel.ceil(val)
        else:
            return pyxel.floor(val)

    def player_pos_to_tm(self,x,y):
        return [x + (self.level[0]*self.levelSize),y + (self.level[1]*self.levelSize)]

        
App()