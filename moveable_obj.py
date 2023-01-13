
import pyxel
import sound_lookup

class MoveableObj:
    def __init__(self,x,y,levels,sprite_index = (0,0)):

        self.x = x
        self.y = y
        self.levels = levels

        self.takes_player_damage = False

        self.is_attachable = True
        self.attached_to = None
        self.being_thrown = False

        self.level_start_x = self.x
        self.level_start_y = self.y
        
        self.health = 1
        self.alive = True

        self.time_over_pit = 0
        self.max_time_over_pit = 6

        # movement properties
        self.accel = 4
        self.deccel = .1
        self.max_vel = -1
        self.vel_x = 0
        self.vel_y = 0
        self.dir = [0,0]
        self.force_accel = 4

        # for non-velocity movement
        self.speed = .2
        self.top_boost = .5
        self.boost = 0
        self.boost_decay = .1

        # keep track of direction object is facing for drawing purposes
        self.w_mod = 1
        self.h_mod = 1
        self.sprite = 0
        self.sprite_index = sprite_index

        self.forces = [] # [xforce,yforce,cooldown]

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

    def apply_forces_with_velocity(self,newX,newY,tm_val):
        # deaccelerate
        if tm_val != (3,0):
            if self.vel_y != 0:
                if abs(self.vel_y) < .1:
                    self.vel_y = 0
                else:
                    self.vel_y -= self.deccel*pyxel.sgn(self.vel_y)

            if self.vel_x != 0:
                if abs(self.vel_x) < .1:
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
    def update(self,xdelta = 0, ydelta = 0):
        newX = self.x
        newY = self.y
        if self.attached_to != None:
            newX = self.attached_to.x - self.offset[0]
            newY = self.attached_to.y - self.offset[1]

        tm_val = self.get_tilemap_value()

        #[newX,newY] = self.apply_forces(newX,newY,tm_val)
        newX += xdelta
        newY += ydelta
        [newX,newY] = self.apply_forces_with_velocity(newX,newY,tm_val)
        [newX,newY] = self.check_collision(newX,newY)

        if self.being_thrown: # check if we stopped moving aka stopped being thrown
            if self.x == newX and self.y == newY: # not moving
                self.being_thrown = False

        self.x = newX
        self.y = newY

        if self.health <= 0:
            self.alive = False

    def zero_attack_forces_x(self):
        for idx,vals in enumerate(self.forces):
            self.forces[idx][0] = 0

    def zero_attack_forces_y(self):
        for idx,vals in enumerate(self.forces):
            self.forces[idx][1] = 0

    def draw(self):
        if self.alive:

            if self.being_thrown:
                pyxel.circ(
                    self.x*8+4-self.levels.camera.x,
                    self.y*8+4-self.levels.camera.y,
                    12,
                    10)

            pyxel.blt(
                self.x*8-self.levels.camera.x,
                self.y*8-self.levels.camera.y, 
                0, 
                self.sprite_index[0]*8,
                self.sprite_index[1]*8,
                8,8,15)

    def check_collision(self,newX,newY):
        # TODO: rework collision - optimize.. shouldn't need to check tile multile times

        [newX,newY] = self.spike_collision(newX,newY)
        [newX,newY,col_val] = self.wall_collision_check(newX,newY)
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
            print('ow')

        return [newX,newY]

    def pit_collision_check(self,newX,newY,col_val):
        if col_val == 3: # over pit
            self.time_over_pit += 1
            if self.time_over_pit > self.max_time_over_pit:
                self.attached_to = None
                newX = self.level_start_x
                newY = self.level_start_y
                self.health -= 1
                pyxel.play(sound_lookup.sfx_ch,sound_lookup.fall_in_pit)
        else:
            self.time_over_pit = 0

        return [newX,newY]

    def wall_collision_check(self,newX,newY,offset=0):

        x_final = self.x
        y_final = self.y

        roundX = round(newX)
        roundY = round(newY+offset)
        roundOldX = round(self.x)
        roundOldY = round(self.y)

        # check collision on current position
        col_now = self.levels.check_tile_collision(roundX,roundY)

        # collision on old x (allows sliding along walls)
        col_old_x = self.levels.check_tile_collision(roundOldX,roundY)
        
        # collision on old y (allows sliding along walls)
        col_old_y = self.levels.check_tile_collision(roundX,roundOldY)
        final_col_val = col_now
        if col_now != 1: # clear floor
            x_final = newX
            y_final = newY
        elif col_old_x != 1:
            y_final = newY
            self.dir[0] = 0
            self.zero_attack_forces_x()
            final_col_val = col_old_x
        elif col_old_y != 1:
            x_final = newX
            self.dir[1] = 0
            self.zero_attack_forces_y()
            final_col_val = col_old_y
        else:
            self.vel_y = 0
            self.vel_x = 0

        return [x_final,y_final,final_col_val]
    
    def get_tilemap_value(self):
        tm_pos = self.levels.player_pos_to_tm(round(self.x),round(self.y))
        return pyxel.tilemap(0).pget(tm_pos[0],tm_pos[1])



