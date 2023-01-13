import pyxel
import moveable_obj
import utilities
import sound_lookup
import tile_lookup
import ai
from enum import Enum
import player_animation
import input_handler

class Player(moveable_obj.MoveableObj):
    def __init__(self,x,y,levels):
        super().__init__(x,y,levels)
        #
        # overwrite defaults on inherrited properties
        #
        self.input_handler = input_handler.InputHandler()

        self.health = 10
        self.ai_damage = 1 # amount of damage ai inflicts on player collision
        self.ai_pushback = .2
        self.invuln_frames = 0
        self.max_invuln_frames = 20
        self.money = 0

        self.animator = player_animation.PlayerAnimation()

        # movement properties
        self.accel = .025
        #self.deccel = .025
        self.deccel = .2
        self.max_vel = .2
        self.min_vel = .08
        self.move_vel_x = 0
        self.move_vel_y = 0
        self.dir = [0,0]
        self.last_nonzero_dir = [0,0]
        self.vel_magnitude = 0
        self.move_angle = 0
        self.desired_angle = 0

        # for non-velocity movement
        self.speed = .15
        self.top_boost = .5
        self.boost = 0
        self.boost_decay = .1
        
        #
        # not inherrited
        #

        # attack properties
        #self.attack = False
        self.attack_frame = 0
        self.attack_duration = 14
        self.attack_cooldown = 14
        self.attack_cooldown_count = 0
        self.attack_knockback_force = .2 # knockback from wall
        self.attack_knockback_cooldown = 5
        self.attack_object_force = .1 # force against moveable_obj
        self.attack_object_cooldown = 5
        self.wall_pushback_x = 0
        self.wall_pushback_y = 0
        self.attack_damage = 1 # amount of health subtracted from enemy on attack collision (each frame)

        self.z_press = False
        # attract properties
        #self.attract = False

        self.aim_move_penalty = 0.08
        self.aim_debounce_max = 6 # z key must be held down for 5 frames to enter aim state
        self.aim_debounce = 0 
        self.aim_vel_multiplier = 3 # how hard the objects are flung away when aiming

        self.any_attached = False
        self.attach_debounce_max = 6
        self.attach_debounce = 0 # allow player to 'move into' scenery objects and attach
                                # kind of like coyote jump time

        self.state = PlayerState.NORMAL

        self.grapple_dir = [0,0]
        self.grapple_mag = 0
        self.grapple_init_mag = 1
        self.grapple_deccel = 0.01


    def move_with_velocity(self,dir_x,dir_y,tm_val):
        # deacel logic
        if tm_val != (3,0):
            if dir_y == 0:
                if abs(self.move_vel_y) < self.min_vel:
                    self.move_vel_y = 0
                else:
                    self.move_vel_y -= self.deccel*pyxel.sgn(self.move_vel_y)

            if dir_x == 0:
                if abs(self.move_vel_x) < self.min_vel:
                    self.move_vel_x = 0
                else:
                    self.move_vel_x -= self.deccel*pyxel.sgn(self.move_vel_x)

            self.move_vel_x += dir_x * self.accel
            self.move_vel_y += dir_y * self.accel

            self.move_vel_x = max(min(self.move_vel_x,self.max_vel),-self.max_vel)
            self.move_vel_y = max(min(self.move_vel_y,self.max_vel),-self.max_vel)

            # boost
            # self.vel_x += dir_x * self.boost
            # self.vel_y += dir_y * self.boost

            if dir_x != 0 and dir_y != 0:
                self.move_vel_x *= .895
                self.move_vel_y *= .895 # this value depends on max vel... not sure the true math behind this
                # find the value by printing the magnitude (below) and moving diagonal
                # fine tune the value until the diagonal max magnitude is the same as non-diagonal

        # debug print magnitude
        #print(pyxel.sqrt(self.move_vel_x*self.move_vel_x+self.move_vel_y*self.move_vel_y))

        newX = self.x + self.move_vel_x
        newY = self.y + self.move_vel_y

        return [newX,newY]

    def move_without_velocity(self,dir_x,dir_y):
        
        newX = self.x + (dir_x*(self.speed+self.boost))
        newY = self.y + (dir_y*(self.speed+self.boost))

        return [newX,newY]

    def grapple_movement(self,dir_x,dir_y):
        angle = pyxel.atan2(self.grapple_dir[1],self.grapple_dir[0])
        newX = self.x + (self.grapple_mag*pyxel.cos(angle))
        newY = self.y + (self.grapple_mag*pyxel.sin(angle))

        return [newX,newY]

    def move_like_a_car(self,dir_x,dir_y):
        if dir_y < 0: # car accelerating
            self.vel_magnitude += self.accel
            self.vel_magnitude = min(self.vel_magnitude,self.max_vel)
        elif dir_y > 0: # pressing the brake
            self.vel_magnitude -= self.deccel
            self.vel_magnitude = max(self.vel_magnitude,-self.max_vel)
        else: # drifting with no accel or brake
            self.vel_magnitude -= self.deccel/4
            self.vel_magnitude = max(self.vel_magnitude,0)

        self.move_angle = self.move_angle + dir_x*5
        self.move_angle = self.move_angle % 360
        print(self.move_angle)

        newX = self.x + pyxel.cos(self.move_angle)*self.vel_magnitude
        newY = self.y + pyxel.sin(self.move_angle)*self.vel_magnitude

        return [newX,newY]

    def move(self):
        # player movement logic  
        newX = self. x
        newY = self.y
        
        dir_x = 0
        dir_y = 0

        # don't allow change of direction in space
        tm_val = self.get_tilemap_value()

        if tm_val != (3,0):
            if self.input_handler.is_pressed('right'):
                dir_x += 1
            if self.input_handler.is_pressed('left'):
                dir_x -= 1
            if self.input_handler.is_pressed('up'):
                dir_y -= 1
            if self.input_handler.is_pressed('down'):
                dir_y += 1

            # account for faster diagonals
            if (dir_y != 0 and dir_x != 0):
                dir_y *= .7
                dir_x *= .7

            self.dir = [dir_x,dir_y]
            if not (dir_x == 0 and dir_y == 0):
                self.last_nonzero_dir = self.dir

        else:
            dir_x = self.dir[0]
            dir_y = self.dir[1]

        if pyxel.btnp(pyxel.KEY_C) and self.boost <= 0:
            self.boost = self.top_boost
            self.grapple_dir = self.last_nonzero_dir
            self.grapple_mag = self.grapple_init_mag
            pyxel.play(sound_lookup.sfx_ch,sound_lookup.player_dash)

        if self.state == PlayerState.AIMING:
            dir_x = dir_x * self.aim_move_penalty
            dir_y = dir_y * self.aim_move_penalty
        
        if self.grapple_mag != 0:
            [newX,newY] = self.grapple_movement(dir_x,dir_y)
        else:
            [newX,newY] = self.move_without_velocity(dir_x,dir_y)
            #[newX,newY] = self.move_with_velocity(dir_x,dir_y,tm_val)
            #[newX,newY] = self.move_like_a_car(dir_x,dir_y)

        tm_val = self.get_tilemap_value()
        [newX,newY] = self.apply_forces_with_velocity(newX,newY,tm_val)

        if self.boost > 0:
            self.boost -= self.boost_decay
            if self.boost < 0:
                self.boost = 0

        return [newX,newY]
        #return self.move_without_velocity(dir_x,dir_y)

    def check_collision(self, newX, newY):
        # general moveable objects collision check (spikes, walls, pits)
        #[newX2,newY2] = super().check_collision(newX, newY)
        # TODO: rework collision - optimize.. shouldn't need to check tile multile times
        [newX2,newY2] = self.spike_collision(newX,newY)
        [newX2,newY2,col_val] = self.wall_collision_check(newX2,newY2)
        [newX2,newY2] = self.pit_collision_check(newX2,newY2,col_val)

        if (newX2 != newX) or (newY2 != newY): # collided
            self.grapple_mag = 0

        newX = newX2
        newY = newY2

        # other collision checks that only apply to the player (coins)
        tm_pos = self.levels.player_pos_to_tm(round(newX),round(newY))
        tm_val_layer2 = pyxel.tilemap(1).pget(tm_pos[0],tm_pos[1])

        if tm_val_layer2 == tile_lookup.coin: # coin
            self.money += 1
            pyxel.tilemap(1).pset(tm_pos[0],tm_pos[1],tile_lookup.transparent)
            pyxel.play(sound_lookup.sfx_ch,sound_lookup.coin)

        # ai collisions
        if self.invuln_frames <= 0:
            for level_obj in self.levels.level_objs:
                if isinstance(level_obj,ai.Ai) and level_obj.alive:
                    if utilities.box_collision_detect(self.x*8,self.y*8,8,8,level_obj.x*8,level_obj.y*8,8,8) == True:
                        self.health -= self.ai_damage
                        self.invuln_frames = self.max_invuln_frames

                        # player knockback
                        angle = pyxel.atan2(self.y-level_obj.y,self.x-level_obj.x)
                        dir_x = pyxel.cos(angle)
                        dir_y = pyxel.sin(angle)

                        self.forces.append(
                            [dir_x*self.ai_pushback,
                            dir_y*self.ai_pushback,
                            self.attack_object_cooldown])
                
        else:
            self.invuln_frames -= 1

        return [newX,newY,col_val]

    def draw(self):
        self.draw_attack()

        [sprite,lr_flip] = self.animator.get_frame_sprite(self.dir)

        if self.invuln_frames % 2 == 0: # flash on hit
            pyxel.blt((self.x*8)-self.levels.camera.x,self.y*8-self.levels.camera.y,0,sprite[0]*8,sprite[1]*8,8*lr_flip,8,15)

        # draw line showing movement for debugging
        # sx = self.x*8+4-self.levels.camera.x
        # sy = self.y*8+4-self.levels.camera.y
        # pyxel.line(sx,sy,sx+pyxel.cos(self.move_angle)*8,sy+pyxel.sin(self.move_angle)*8, 3)
        
        # draw attack wall push direction
        # sx = self.x*8+4-self.levels.camera.x
        # sy = self.y*8+4-self.levels.camera.y
        # pyxel.line(sx,sy,sx+self.wall_pushback_x*16,sy+self.wall_pushback_y*16,5)

    ##############################################################################
    # ATTACK FUNCTIONS
    ##############################################################################

    def update(self):

        if self.attack_cooldown_count > 0:
            self.attack_cooldown_count -= 1

        if self.state == PlayerState.ATTACKING:
            self.process_attack()

        # continue allow objects to attach during first few frames of attach state
        # similar to coyote time for 2d platformers
        if self.state == PlayerState.ATTACHING:
            if self.attach_debounce < self.attach_debounce_max:
                self.attach_debounce += 1
                self.attract_objects()
            elif self.any_attached == False:
                self.state = PlayerState.NORMAL

        if pyxel.btn(pyxel.KEY_Z):
            if self.state == PlayerState.ATTACHING:
                self.state = PlayerState.AIM_DEBOUNCING
                self.aim_debounce = 0
            elif self.state == PlayerState.AIM_DEBOUNCING:
                self.aim_debounce += 1
                if self.aim_debounce > self.aim_debounce_max:
                    self.state = PlayerState.AIMING
            elif self.state == PlayerState.AIMING:
                self.process_aiming()
            elif (not self.state == PlayerState.ATTACKING
                    and self.z_press == False 
                    and self.attack_cooldown_count == 0):
                self.z_press = True
                self.process_first_attack_frame()
        else:
            self.z_press = False
            if self.state == PlayerState.AIMING or self.state == PlayerState.AIM_DEBOUNCING:
                # deattach everything
                for level_obj in self.levels.level_objs:
                        level_obj.dettach()
                if self.state == PlayerState.AIMING:
                    self.process_aim_release()
                    self.any_attached = False
                else:
                    self.process_first_attack_frame()

        if pyxel.btnp(pyxel.KEY_X):
            if not self.state == PlayerState.ATTACHING: # first time on
                self.state = PlayerState.ATTACHING
                self.attach_debounce = 0
                self.attract_objects()
            else:
                self.de_attract_objects()
                self.state = PlayerState.NORMAL
                self.any_attached = False

    def process_aiming(self):
        dummy = 1

    def process_aim_release(self):
        # apply force to all objects in direction of player movement
        self.attack_scenery_collision(dir = self.last_nonzero_dir,throwing = True)
        self.state = PlayerState.NORMAL

    def draw_attack(self):
        attack_color = -1
        if self.state == PlayerState.ATTACKING: #self.attack:
            attack_color = 12
        elif self.state == PlayerState.ATTACHING:
            if self.attach_debounce < self.attach_debounce_max:
                attack_color = 13
            else:
                attack_color = 11
        elif self.state == PlayerState.AIMING:
            attack_color = 10

        if attack_color >= 0:
            [min_x,min_y,w,h] = self.get_attack_bounds()

            pyxel.rect(min_x-self.levels.camera.x,
                       min_y-self.levels.camera.y,
                       w,
                       h,
                       attack_color)

        if self.state == PlayerState.AIMING:
            # draw aim line (has to be drawn after the rectangle)
            sx = self.x*8+4-self.levels.camera.x
            sy = self.y*8+4-self.levels.camera.y
            pyxel.line(sx,sy,sx+self.last_nonzero_dir[0]*16,sy+self.last_nonzero_dir[1]*16, 3)

    def get_attack_bounds(self):
        min_x = 8*(self.x-1)
        min_y = 8*(self.y-1)
        w = 8*3
        h = 8*3

        return [min_x,min_y,w,h]

    def process_first_attack_frame(self):
        self.state = PlayerState.ATTACKING
        self.attack_frame = pyxel.frame_count # used for cooldown

        # do stuff that only happens on first attack frame
        #self.attack_wall_pushback()
        self.attack_scenery_collision()
        pyxel.play(sound_lookup.sfx_ch, sound_lookup.player_attack)

    def process_attack(self):
        if pyxel.frame_count - self.attack_frame > self.attack_duration:
            self.state = PlayerState.NORMAL
            self.attack_cooldown_count = self.attack_cooldown
        else: # attack not finished, do stuff that happens on every attack frame
            # check scenery and AI collision
            self.attack_scenery_collision()

    def attack_scenery_collision(self,dir = None,throwing = False):
        [min_x,min_y,w,h] = self.get_attack_bounds()
        for level_obj in self.levels.level_objs:
            if level_obj.alive == True:
                if utilities.box_collision_detect(min_x,min_y,w,h,level_obj.x*8,level_obj.y*8,8,8) == True:
                    if level_obj.takes_player_damage == True:
                        level_obj.take_player_damage(self.attack_damage)
                    
                    if dir is None:
                        # calculate angle between player and object and apply force in that direction
                        angle = pyxel.atan2(self.y-level_obj.y,self.x-level_obj.x)
                        dir_x = pyxel.cos(angle)
                        dir_y = pyxel.sin(angle)
                    else:
                        # dir_x = -dir[0]*self.aim_vel_multiplier
                        # dir_y = -dir[1]*self.aim_vel_multiplier
                        dir_x = -pyxel.sgn(dir[0])*self.aim_vel_multiplier
                        dir_y = -pyxel.sgn(dir[1])*self.aim_vel_multiplier
                        
                    level_obj.forces.append(
                        [-dir_x*self.attack_object_force,
                        -dir_y*self.attack_object_force,
                        self.attack_object_cooldown])
                    
                    if not (dir_x == 0 and dir_y == 0): # don't play sound if player let go of aim direction
                        pyxel.play(sound_lookup.sfx_ch, sound_lookup.player_attack_hit_obj)
                        if throwing == True:
                            level_obj.being_thrown = True

    def attack_wall_pushback(self):
        # attack pushback
        [min_x,min_y,w,h] = self.get_attack_bounds()
        max_x = round((min_x + w - 8)/8)
        max_y = round((min_y + h - 8)/8)
        min_x = round(min_x/8)
        min_y = round(min_y/8)
        cur_x = round(self.x)
        cur_y = round(self.y)
        pos_check = [
            (min_x,cur_y),
            (max_x,cur_y),
            (cur_x,min_y),
            (cur_x,max_y),
            (max_x,max_y),
            (min_x,min_y),
            (min_x,max_y),
            (max_x,min_y)] # diagonals case
        dir_check = [(1,0),(-1,0),(0,1),(0,-1),(-1,-1),(1,1),(1,-1),(-1,1)]

        attack_force_x_dir = 0
        attack_force_y_dir = 0

        for idx,vals in enumerate(pos_check):
            # check map collision
            if self.levels.check_tile_collision(round(vals[0]),round(vals[1]),light_up = True) == 1:
                attack_force_x_dir += dir_check[idx][0]
                attack_force_y_dir += dir_check[idx][1]

        if not (attack_force_x_dir == 0 and attack_force_y_dir == 0): # wall collision happened
            force_dir = pyxel.atan2(attack_force_y_dir,attack_force_x_dir)
            self.wall_pushback_x = self.attack_knockback_force*pyxel.cos(force_dir)
            self.wall_pushback_y = self.attack_knockback_force*pyxel.sin(force_dir)
            print('force dir:',force_dir)
            self.forces.append(
                [self.wall_pushback_x,self.wall_pushback_y,
                self.attack_knockback_cooldown+20])
            pyxel.play(2, sound_lookup.player_attack_hit_wall)

    def attract_objects(self):
        # any object within range should follow player movement
        # check scenery collision
        [min_x,min_y,w,h] = self.get_attack_bounds()

        for level_obj in self.levels.level_objs:
            if level_obj.alive == True and level_obj.is_attachable:
                if utilities.box_collision_detect(min_x,min_y,w,h,level_obj.x*8,level_obj.y*8,8,8) == True:
                    level_obj.attach(self)
                    self.any_attached = True

    def de_attract_objects(self):
        for level_obj in self.levels.level_objs:
            level_obj.dettach()

class PlayerState(Enum):
    NORMAL = 1
    ATTACKING = 2
    ATTACHING = 3
    AIMING = 4
    AIM_DEBOUNCING = 5



