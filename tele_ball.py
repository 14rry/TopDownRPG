# -*- coding: utf-8 -*-
import pyxel
import moveable_obj

class TeleBall(moveable_obj.MoveableObj):
    def __init__(self,x,y,levels,sprite):
        super().__init__(x,y,levels,sprite_index = sprite)

        self.x = x
        self.y = y
        self.color = 14
        self.alive = True
        self.size = 9
        self.player = None

        self.moving = False
        
    def update(self):
        # general moveable objects collision check (spikes, walls, pits)
        prev_x = self.x
        prev_y = self.y
        super().update()

        if self.attached_to is None:
            if self.x != prev_x or self.y != prev_y:
                self.moving = True
            elif self.moving == True: # stopped moving, teleport player to position
                self.player.x = self.x
                self.player.y = self.y
                self.player.attack_frame = -1 # stop the player attack, which otherwise interferes with the teleportation
                self.moving = False

        

            