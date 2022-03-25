# -*- coding: utf-8 -*-
import pyxel
import moveable_obj

class Ai(moveable_obj.MoveableObj):
    def __init__(self,x,y,levels,sprite):
        super().__init__(x,y,levels,sprite_index = sprite)

        self.x = x
        self.y = y
        self.color = 14
        self.alive = True
        self.size = 9
        self.player = None
        self.health = 10
        self.takes_player_damage = True

        self.speed = .05

    def draw(self):
        super().draw()
        
    def update(self):
        xd = 0
        yd = 0
        if self.player is not None:
            xd = -pyxel.sgn(self.x - self.player.x)*self.speed
            yd = -pyxel.sgn(self.y - self.player.y)*self.speed
        # general moveable objects collision check (spikes, walls, pits)
        super().update(xdelta = xd, ydelta = yd)

    # def draw_self(self):
    #     if not self.alive:
    #         self.size -= 1 # shrink on death
    #     if self.size > 0:
    #         pyxel.rect(self.x*10,
    #                     self.y*10,
    #                     self.size,
    #                     self.size,
    #                     self.color)
            