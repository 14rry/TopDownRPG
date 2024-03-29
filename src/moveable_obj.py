
import pyxel
import utilities
import sound_lookup
import ai
import particles
import config
import tile_lookup

class MoveableObj:
    def __init__(self,x,y,levels,sprite_index = (0,0)):

        self.x = x
        self.y = y
        self.levels = levels

        self.takes_player_damage = False

        self.is_attachable = True
        self.attached_to = None
        self.being_thrown = False
        self.can_be_thrown = True

        self.level_start_x = self.x
        self.level_start_y = self.y
        
        self.health = 1
        self.alive = True
        self.invincible = False

        self.time_over_pit = 0
        self.max_time_over_pit = 6
        self.pit_damage = 0

        # movement properties
        self.accel = 4
        #self.deccel = .1
        self.max_vel = -1
        #self.min_vel = .09
        self.vel_x = 0
        self.vel_y = 0
        self.dir = [0,0]
        self.force_accel = 4

        self.deccel = .05
        self.min_vel = .051

        # for non-velocity movement
        self.speed = .2
        self.top_boost = .5
        self.boost = 0
        self.boost_decay = .1

        # keep track of direction object is facing for drawing purposes
        self.sprite = 0
        self.sprite_index = sprite_index

        self.forces = [] # [xforce,yforce,cooldown]

        self.invuln_frames = 0
        self.max_invuln_frames = 20

        self.collision_value = tile_lookup.collision[sprite_index[1]][sprite_index[0]]

    def attach(self,attachment_obj):
        self.attached_to = attachment_obj
        self.offset = [attachment_obj.x - self.x, attachment_obj.y - self.y]

    def dettach(self):
        self.attached_to = None

    # step through list of external forces on object and move object accordingly
    def apply_forces(self,newX,newY,tm_val):
        for idx,vals in enumerate(self.forces):
            if self.forces[idx][2] > 0 or tm_val == (3,0): # space
                newX += vals[0]
                newY += vals[1]

            if tm_val != (3,0):
                self.forces[idx][2] -= 1
            
            if self.forces[idx][2] <= -2 or (vals[0] == 0 and vals[1] == 0): # going down to -2 gives wiggle room for space
                self.forces.pop(idx)

        return [newX,newY]

    def take_player_damage(self,dontcare):
        if self.invuln_frames <= 0:
            self.invuln_frames = self.max_invuln_frames

    def apply_forces_with_velocity(self,newX,newY,tm_val):
        # deaccelerate
        if tm_val != (3,0):
            if self.vel_y != 0:
                if abs(self.vel_y) < self.min_vel:
                    self.vel_y = 0
                else:
                    self.vel_y -= self.deccel*pyxel.sgn(self.vel_y)

            if self.vel_x != 0:
                if abs(self.vel_x) < self.min_vel:
                    self.vel_x = 0
                else:
                    self.vel_x -= self.deccel*pyxel.sgn(self.vel_x)
        
        for idx,vals in enumerate(self.forces):
            self.vel_x += vals[0]*self.force_accel
            self.vel_y += vals[1]*self.force_accel

            self.forces.pop(idx)

        newX += self.vel_x
        newY += self.vel_y

        return [newX,newY]

    # called from main.py on each moveable object in a level
    def update(self,xdelta = 0, ydelta = 0, avoids_pits = False):
        if self.invuln_frames > 0:
            self.invuln_frames -= 1

        newX = self.x
        newY = self.y
        if self.attached_to != None:
            newX = self.attached_to.x - self.offset[0]
            newY = self.attached_to.y - self.offset[1]

        tm_val = self.get_tilemap_value()

        #[newX,newY] = self.apply_forces(newX,newY,tm_val)
        newX += xdelta
        newY += ydelta
        [newX_2,newY_2] = self.apply_forces_with_velocity(newX,newY,tm_val)

        if newX_2 != newX or newY_2 != newY: # external force affected movement, allow falling in pits
            avoids_pits = False

        newX = newX_2
        newY = newY_2

        [newX,newY] = self.check_collision(newX,newY,avoids_pits)

        if self.being_thrown: # check if we stopped moving aka stopped being thrown
            if self.x == newX and self.y == newY: # not moving
                self.being_thrown = False
            else:
                self.level_obj_collision_check()

        self.x = newX
        self.y = newY

        if self.health <= 0 and self.alive:
            self.alive = False
            config.particle_effects.add(particles.ParticleEffect(self.x,self.y))

    def zero_attack_forces_x(self):
        for idx,vals in enumerate(self.forces):
            self.forces[idx][0] = 0

    def zero_attack_forces_y(self):
        for idx,vals in enumerate(self.forces):
            self.forces[idx][1] = 0

    def draw(self,x0,lr_flip=1):
        if self.alive:

            if self.being_thrown:
                pyxel.circ(
                    self.x*8+4-self.levels.camera.x+x0,
                    self.y*8+4-self.levels.camera.y,
                    12,
                    10)

            pyxel.blt(
                self.x*8-self.levels.camera.x+x0,
                self.y*8-self.levels.camera.y, 
                0, 
                self.sprite_index[0]*8,
                self.sprite_index[1]*8,
                8*lr_flip,8,8)

    def check_collision(self,newX,newY,avoids_pits = False):
        # TODO: rework collision - optimize.. shouldn't need to check tile multile times

        [newX,newY] = self.spike_collision(newX,newY)
        [newX,newY,col_val] = self.wall_collision_check(newX,newY,avoids_pits=avoids_pits,obj=self)
        [newX,newY] = self.pit_collision_check(newX,newY,col_val)

        return [newX,newY]

    def spike_collision(self,newX,newY):
        # check collision on current position
        # check each edge
        col_now = 0
        pos_check_offset = [[-1,-1],[-1,0],[-1,1],[0,1],[1,1],[1,0],[1,-1],[0,-1]]
        for offset in pos_check_offset:
            test_x = round(newX+(offset[0]*.4))
            test_y = round(newY+(offset[1]*.4))
            col_now = self.levels.check_tile_collision(test_x,test_y)

            if col_now == 2:
                print(test_x,test_y,newY,offset[1])
                break

        if col_now == 2:
            self.health -= 1
            newX = self.level_start_x
            newY = self.level_start_y

        return [newX,newY]

    def pit_collision_check(self,newX,newY,col_val):
        if self.being_thrown:
            return [newX,newY] # throwing over pit, skip check

        if col_val == 3: # over pit
            print('test')
            self.time_over_pit += 1
            if self.time_over_pit > self.max_time_over_pit:
                self.attached_to = None
                newX = self.level_start_x
                newY = self.level_start_y
                self.health -= self.pit_damage
                sound_lookup.sfx_queue.insert(0,sound_lookup.fall_in_pit)

                if self.health <= 0:
                    self.alive = False
                    config.particle_effects.add(particles.ParticleEffect(self.x,self.y))

        else:
            self.time_over_pit = 0

        return [newX,newY]

    def wall_collision_check(self,newX,newY,offset=0,avoids_pits = False,obj=None):

        x_final = self.x
        y_final = self.y

        roundX = round(newX)
        roundY = round(newY+offset)
        roundOldX = round(self.x)
        roundOldY = round(self.y)

        # check collision on current position
        col_now = self.levels.check_tile_collision_multilayer(roundX,roundY,obj=obj)

        # collision on old x (allows sliding along walls)
        col_old_x = self.levels.check_tile_collision_multilayer(roundOldX,roundY,obj=obj)
        
        # collision on old y (allows sliding along walls)
        col_old_y = self.levels.check_tile_collision_multilayer(roundX,roundOldY,obj=obj)
        final_col_val = col_now[0]
        if not self.is_wall(col_now,avoids_pits): # clear floor
            x_final = newX
            y_final = newY
        elif not self.is_wall(col_old_x,avoids_pits):
            y_final = newY
            self.dir[0] = 0
            self.zero_attack_forces_x()
            final_col_val = col_old_x[0]
        elif not self.is_wall(col_old_y,avoids_pits):
            x_final = newX
            self.dir[1] = 0
            self.zero_attack_forces_y()
            final_col_val = col_old_y[0]
        else:
            self.vel_y = 0
            self.vel_x = 0

        return [x_final,y_final,final_col_val]

    def is_wall(self,col_val,avoids_pits):
        is_wall = False
        for val in col_val:
            is_wall = val == 1 or (avoids_pits and val == 3)
            if is_wall: 
                return True

        return False

    def level_obj_collision_check(self):
        for level_obj in self.levels.level_objs:
            if isinstance(level_obj,ai.Ai) and level_obj.alive and not level_obj.invincible:
                if utilities.box_collision_detect(self.x*8,self.y*8,8,8,level_obj.x*8,level_obj.y*8,8,8) == True:
                    level_obj.health -= 99
    
    def get_tilemap_value(self):
        tm_pos = self.levels.player_pos_to_tm(round(self.x),round(self.y))
        return pyxel.tilemap(0).pget(tm_pos[0],tm_pos[1])



