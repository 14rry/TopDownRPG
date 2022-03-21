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

        self.speed = .05

    def draw(self):
        if self.alive:
            super().draw()
        
    def update(self):
        # general moveable objects collision check (spikes, walls, pits)
        super().update()
        if self.health <= 0:
            self.alive = False

        if self.player is not None:
            self.x += -pyxel.sgn(self.x - self.player.x)*self.speed
            self.y += -pyxel.sgn(self.y - self.player.y)*self.speed

    # def draw_self(self):
    #     if not self.alive:
    #         self.size -= 1 # shrink on death
    #     if self.size > 0:
    #         pyxel.rect(self.x*10,
    #                     self.y*10,
    #                     self.size,
    #                     self.size,
    #                     self.color)
            