# -*- coding: utf-8 -*-

import pyxel
import utilities

class Dialog():

    def __init__(self,grid_size):
        self.current_text = ""
        self.dialog_open = False
        self.dialog_on_bottom = True
        self.grid_size = grid_size
        self.invoke_pos = [0,0]

    def update(self,player_x,player_y,level,col_val):
        if self.dialog_open:
            # if pyxel.btnr(pyxel.KEY_Z):
            #     self.dialog_open = False

            if utilities.distance(player_x,player_y,self.invoke_pos[0],self.invoke_pos[1]) > 3:
                self.dialog_open = False

        elif col_val == 4:
            roundX = round(player_x)
            roundY = round(player_y)
            self.invoke(level,roundX,roundY)

    def invoke(self,index,posX,posY):
        self.current_text = self.text_lookup(index,posX,posY)
        self.dialog_open = True
        self.dialog_on_bottom = posY > 8
        self.invoke_pos = [posX,posY]

    # TODO: turn into lookup table instead of if statepements
    def text_lookup(self,index,posX,posY):
        
        if index == [0,0]:
            return ["Welcome to the garden."]
        elif index == [1,1]:
            if [posX,posY] == [12,14]:
                return ["They were relentless.",
                        "I mashed Z for dear life but",
                        "it wasn't enough...",
                        "Maybe you'll have better luck."]
            elif [posX,posY] == [2,2]:
                return ["Go talk to the guy in the", 
                        "room. He's seem some stuff."]

        elif index == [2,0]:
            return ["Some call this the Cave", 
                    "of Fools.",
                    "",
                    "I call it home."]

        elif index == [2,1]:
            if [posX,posY] == [1,3]:
                return ["Get out of my offive!"]

        elif index == [3,0]:
            return ["I'm on a boat!",
            "",
            "(He's not on a boat...)"]

        print("Dialog input:")
        print(index,posX,posY)

        return ["Error: missing dialog"]


    def draw(self,screen_width):
        if self.dialog_open:

            if self.dialog_on_bottom:
                pos_y = 2
            else:
                pos_y = 84

            pyxel.rect(2,pos_y,screen_width - 4, screen_width / 3,0)
            pyxel.rectb(2,pos_y,screen_width - 4, screen_width / 3,3)
            for textIndex in range(len(self.current_text)):
                pyxel.text(6,self.grid_size*(textIndex+1)-2+pos_y,self.current_text[textIndex],3)
                    