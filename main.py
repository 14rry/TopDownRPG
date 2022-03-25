# -*- coding: utf-8 -*-
"""
Created on Fri Aug 10 22:43:07 2018

@author: larry
"""

import pyxel
import levels
import dialog
import player
import ai
import tele_ball
import swarm
import contrail

class App:
    def __init__(self):
        self.levelSize = 16
        self.grid_size = 8
        self.playing_music = False

        pyxel.init(self.levelSize*self.grid_size,self.levelSize*self.grid_size+self.grid_size,fps = 60)
        pyxel.load("topdown.pyxres")
        self.startGame()
        pyxel.run(self.update, self.draw)
        
    def startGame(self):
        self.levels = levels.LevelHandler([1,2])
        self.player = player.Player(1,1,self.levels)
        #self.swarm = swarm.Swarm(self.levelSize)
        self.contrail = contrail.Contrail(self.player,self.levels.camera)

        # assign player to AI and tele ball
        for lvl_obj in self.levels.level_objs:
            if isinstance(lvl_obj,ai.Ai) or isinstance(lvl_obj,tele_ball.TeleBall):
                lvl_obj.player = self.player
                
        self.dialogScreen = False
        self.dialogText = [""]

        #pyxel.playm(1,0,True)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        if pyxel.btnp(pyxel.KEY_R):
            self.reset()
        if pyxel.btnp(pyxel.KEY_M):
            if self.playing_music:
                pyxel.stop()
                self.playing_music = False
            else:
                pyxel.playm(1,0,True)
                self.playing_music = True
            
        if self.dialogScreen:
            if pyxel.btnr(pyxel.KEY_Z):
                self.dialogScreen = False
        
        [newX,newY] = self.player.move()

        # check if we need to change levels
        [newX,newY,did_change] = self.levels.check_for_change(round(newX),round(newY),newX,newY)            
        [newX,newY] = self.player.check_collision(newX,newY)
        self.player.x = newX
        self.player.y = newY

        if did_change:
            self.player.level_start_x = newX
            self.player.level_start_y = newY
            self.player.grapple_mag = 0

            # assign player to AI
            for lvl_obj in self.levels.level_objs:
                if isinstance(lvl_obj,ai.Ai) or isinstance(lvl_obj,tele_ball.TeleBall):
                    lvl_obj.player = self.player

            self.contrail.clear()

        # check if we need to run dialog
        roundX = round(newX)
        roundY = round(newY)
        tm_val = self.player.get_tilemap_value()
        
        if tm_val == (2,1): # npc
            self.dialogText = dialog.invoke(self.levels.level_index,roundX,roundY)
            self.dialogScreen =  True

        # update non-player objects in the current level
        for level_obj in self.levels.level_objs:
            level_obj.update()

        self.levels.camera.update(self.player.x,self.player.y)
            
        self.player.update()
        # self.swarm.new_pos([self.player.x*8,self.player.y*8])
        # self.swarm.update()
        self.contrail.update()
        
    def draw(self):        
        pyxel.cls(6)
        
        # draw map
        self.levels.draw()

        # draw player        
        self.contrail.draw()
        self.player.draw()

        # draw level objects
        for val in self.levels.level_objs:
            val.draw()
        
        if self.dialogScreen:
            pyxel.rect(5,5,self.levelSize * self.grid_size - 5,self.levelSize * 2 + 5,0)
            pyxel.rectb(5,5,self.levelSize * self.grid_size - 5,self.levelSize * 2 + 5,3)
            for textIndex in range(len(self.dialogText)):
                pyxel.text(self.grid_size,self.grid_size*(textIndex+1),self.dialogText[textIndex],3)
                
        # draw health bar
        xHealth = self.player.health*self.grid_size*self.levelSize/10
        pyxel.rect(0,self.levelSize*self.grid_size,xHealth,9,8)

        pyxel.text(0,self.levelSize*self.grid_size,str(self.player.health),3)

        # self.swarm.draw()
   
    def reset(self):
        self.levels.clean_up_scenery()
        self.startGame()
        
App()