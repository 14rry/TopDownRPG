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
# import swarm
import contrail
import screen_effects
from enum import Enum
import config

enable_bg = False

class App:
    def __init__(self):
        self.playing_music = False

        self.screen_effects = screen_effects.ScreenEffects()

        # level size = 16 * 8 = 128x128
        # with background, 224x128

        self.levelSize = 16
        self.grid_size = 8
        self.sidebar_width = 0 #12 # in num tiles

        self.screen_width = self.levelSize*self.grid_size + self.sidebar_width*self.grid_size

        if enable_bg:

            self.window_width = 224
            self.game_draw_start = self.window_width/2 - self.screen_width/2
        else:
            self.window_width = self.screen_width
            self.game_draw_start = 0

        pyxel.init(
            self.window_width,
            self.levelSize*self.grid_size,
            fps = 60)

        pyxel.load("resources/topdown.pyxres")
        pyxel.image(1).load(0,0,'resources/gamewindow.png')

        self.startGame()
        pyxel.run(self.update, self.draw)

    def startGame(self):
        self.state = AppState.INTRO
        self.levels = levels.LevelHandler([1,1])
        self.player = player.Player(1,1,self.levels)
        # self.swarm = swarm.Swarm(self.levelSize)
        self.contrail = contrail.Contrail(self.player,self.levels.camera)
        self.dialog = dialog.Dialog(self.grid_size)

        # assign player to AI and tele ball
        for lvl_obj in self.levels.level_objs:
            if isinstance(lvl_obj,ai.Ai) or isinstance(lvl_obj,tele_ball.TeleBall):
                lvl_obj.player = self.player

        #pyxel.playm(1,0,True)

        config.init(self.levels.camera)

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

        if self.state == AppState.INTRO:
            done = self.screen_effects.fade_in()

            if done:
                self.state = AppState.RUNNING

        if self.state == AppState.RUNNING:
                      
            [newX,newY] = self.player.move()

            # check if we need to change levels
            [newX,newY,did_change] = self.levels.check_for_change(round(newX),round(newY),newX,newY)            
            [newX,newY,col_val] = self.player.check_collision(newX,newY)
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
            self.dialog.update(newX,newY,self.levels.level_index,col_val)
            # if self.dialogScreen:
            #     if pyxel.btnr(pyxel.KEY_Z):
            #         self.dialogScreen = False

            # roundX = round(newX)
            # roundY = round(newY)
            # tm_val = self.player.get_tilemap_value()
            
            # if tm_val == (2,1): # npc
            #     dialog.invoke(self.levels.level_index,roundX,roundY)

            # update non-player objects in the current level
            for level_obj in self.levels.level_objs:
                level_obj.update()

            self.levels.camera.update(self.player.x,self.player.y)
                
            self.player.update()
            # self.swarm.new_pos([self.player.x*8,self.player.y*8])
            # self.swarm.update()
            self.contrail.update()

            config.particle_effects.update()
        
    def draw(self):        
        pyxel.cls(1)

        if enable_bg:
            pyxel.blt(0,0,1,0,0,224,128) # draw background
        
        # draw map
        self.levels.draw(self.game_draw_start)

        # draw player        
        self.contrail.draw(self.game_draw_start)
        self.player.draw(self.game_draw_start)

        # draw level objects
        for val in self.levels.level_objs:
            val.draw(self.game_draw_start)
        
        self.dialog.draw(self.screen_width)

        # draw health bar
        # xHealth = self.player.health*self.grid_size*self.levelSize/10
        # pyxel.rect(self.game_draw_start,self.levelSize*self.grid_size,xHealth,9,8)
        # pyxel.text(self.game_draw_start,self.levelSize*self.grid_size,str(self.player.health),3)

        # self.swarm.draw()

        config.particle_effects.draw(self.game_draw_start)
   
    def reset(self):
        self.levels.clean_up_scenery()
        pyxel.load("resources/topdown.pyxres")
        self.startGame()

class AppState(Enum):
    INTRO = 0
    RUNNING = 1
        
App()