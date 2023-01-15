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
        self.health = 3
        self.takes_player_damage = True
        self.is_attachable = False

        self.invuln_frames = 0
        self.max_invuln_frames = 20

        # for death animation
        self.dead_frames = 0
        self.max_dead_frames = 10

        self.speed = .05

    def take_player_damage(self,damage_amount):
        if self.invuln_frames <= 0:
            self.invuln_frames = self.max_invuln_frames
            self.health -= damage_amount

            if self.health <= 0:
                self.dead_frames = self.max_dead_frames

    def draw(self,x0):
        if self.dead_frames > 0:
            self.dead_frames -= 1

            # draw disapearing animation
            pyxel.rect(
                self.x*8-self.levels.camera.x+x0,
                self.y*8-self.levels.camera.y, 
                self.dead_frames,self.dead_frames,8)

        elif self.invuln_frames % 2 == 0:
            super().draw(x0)
        
    def update(self):

        if not self.alive:
            return

        if self.invuln_frames > 0:
            self.invuln_frames -= 1

        xd = 0
        yd = 0
        # if self.player is not None:
        #     xd = -pyxel.sgn(self.x - self.player.x)*self.speed
        #     yd = -pyxel.sgn(self.y - self.player.y)*self.speed

        # general moveable objects collision check (spikes, walls, pits)
        super().update(xdelta = xd, ydelta = yd)