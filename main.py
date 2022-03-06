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
import tile_lookup

class App:
    def __init__(self):
        self.levelSize = 16
        self.grid_size = 8

        pyxel.init(self.levelSize*self.grid_size,self.levelSize*self.grid_size+self.grid_size,fps = 60)
        
        pyxel.load("topdown.pyxres")

        self.startGame()
        
        pyxel.run(self.update, self.draw)
        
    def startGame(self):
        self.levels = levels.LevelHandler()
        self.player = player.Player(4,4,self.levels)
        self.levels.level_index = [1,2] # starting level
        
        #self.currentAI = levels.loadAI()
        
        self.dialogScreen = False
        self.dialogText = [""]

        self.attack = False
        self.attack_frame = 0

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        if pyxel.btnp(pyxel.KEY_R):
            self.reset()
            
        if self.dialogScreen:
            if pyxel.btnr(pyxel.KEY_Z):
                self.dialogScreen = False

        # check enemy collision
        # for baddy in self.currentAI:
        #     if (baddy.alive and 
        #         baddy.x == self.player.x and
        #         baddy.y == self.player.y):
        #         self.playerHealth -= 1
        
        [newX,newY] = self.player.move()

        roundX = self.round_player_pos(newX)
        roundY = self.round_player_pos(newY)
        
        # check if we need to change levels
        [newX,newY] = self.levels.check_for_change(roundX,roundY,newX,newY)
        [newX,newY] = self.player.check_collision(newX,newY)
        self.player.x = newX
        self.player.y = newY

        #print(newX,newY)

        roundX = self.round_player_pos(newX)
        roundY = self.round_player_pos(newY)
        tm_pos = self.levels.player_pos_to_tm(roundX,roundY)
        tm_val = pyxel.tilemap(0).pget(tm_pos[0],tm_pos[1])

        if tm_val == (2,1): # npc
            self.dialogText = dialog.invoke(self.levels.level_index,roundX,roundY)
            self.dialogScreen =  True

        for level_obj in self.levels.level_objs:
            level_obj.update()

        self.levels.camera.update(self.player.x,self.player.y)
            
        self.player.process_attack()

        
    def draw(self):        
        pyxel.cls(6)
        
        # draw map
        self.levels.draw()

        # draw ai
        # for baddy in self.currentAI:
        #     baddy.draw_self()

        # draw player        
        self.player.draw()
        
        if self.dialogScreen:
            pyxel.rect(5,5,self.levelSize * self.grid_size - 5,self.levelSize * 2 + 5,0)
            pyxel.rectb(5,5,self.levelSize * self.grid_size - 5,self.levelSize * 2 + 5,3)
            for textIndex in range(len(self.dialogText)):
                pyxel.text(self.grid_size,self.grid_size*(textIndex+1),self.dialogText[textIndex],3)

        # draw level objects
        for val in self.levels.level_objs:
            val.draw()
                
        # draw health bar
        xHealth = (self.levelSize - 2*(self.grid_size - self.player.health))*self.grid_size
        pyxel.rect(0,self.levelSize*self.grid_size,xHealth,9,8)
   
    def reset(self):
        self.levels.reset()
        self.startGame()

    def round_player_pos(self,val):
        return round(val)
        if dir > 0:
            return pyxel.ceil(val)
        else:
            return pyxel.floor(val)
        
App()