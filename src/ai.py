# -*- coding: utf-8 -*-
import pyxel
import moveable_obj
import random
import tile_lookup
import player_animation

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
        self.is_attachable = False
        self.player_damage = 1

        self.invuln_frames = 0
        self.max_invuln_frames = 20

        # for death animation
        self.dead_frames = 0
        self.max_dead_frames = 10

        self.speed = .05

        # movement
        self.max_decision_cooldown = 60
        self.decision_cooldown = pyxel.rndi(0,60)
        self.move_dir = [0,0]
        self.deccel = .037
        self.min_vel = .038

        self.animator = player_animation.PlayerAnimation(tile_lookup.ai_animation)
        self.lr_flip = 1

    def take_player_damage(self,damage_amount):
        if self.invuln_frames <= 0:
            self.invuln_frames = self.max_invuln_frames
            self.health -= damage_amount
            self.move_dir = [0,0] # stop moving

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
            super().draw(x0,self.lr_flip)
        
    def update(self):

        if not self.alive:
            return

        if self.invuln_frames <= 0:
            self.movement_update()

        xd = 0
        yd = 0
        # if self.player is not None:
        #     xd = -pyxel.sgn(self.x - self.player.x)*self.speed
        #     yd = -pyxel.sgn(self.y - self.player.y)*self.speed

        xd = self.move_dir[0]*self.speed
        yd = self.move_dir[1]*self.speed

        # general moveable objects collision check (spikes, walls, pits)
        super().update(xdelta = xd, ydelta = yd)

        [self.sprite_index,self.lr_flip] = self.animator.get_frame_sprite(self.move_dir)


    def movement_update(self):
        self.decision_cooldown -= 1
        if self.decision_cooldown < 0:
            self.decision_cooldown = self.max_decision_cooldown

            # self.new_dir_with_diagonals()
            self.new_dir_cardinals_only()

    def new_dir_with_diagonals(self):
        self.move_dir = [random.randint(-1,1),random.randint(-1,1)]

    def new_dir_cardinals_only(self):
        r = random.randint(0,3)
        if r == 0:
            self.move_dir = [-1,0]
        elif r == 1:
            self.move_dir = [1,0]
        elif r == 2:
            self.move_dir = [0,1]
        elif r == 3:
            self.move_dir = [0,-1]





