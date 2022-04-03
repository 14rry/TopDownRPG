import pyxel

class MoveableObj:
    def __init__(self,x,y,levels,sprite_index = (0,0)):

        self.x = x
        self.y = y
        self.levels = levels
        
        self.health = 10

        # movement properties
        self.accel = .04
        self.deccel = .1
        self.max_vel = -1
        self.vel_x = 0
        self.vel_y = 0
        self.dir = [0,0]

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

    # step through list of external forces on object and move object accordingly
    def apply_forces(self,newX,newY,tm_val):
        for idx,vals in enumerate(self.forces):
            print(idx,vals)
            if self.forces[idx][2] > 0 or tm_val == (3,0): # space
                newX += vals[0]
                newY += vals[1]

            if tm_val != (3,0):
                self.forces[idx][2] -= 1
            else:
                print('space!')
                print(self.forces[idx][2])

            if self.forces[idx][2] <= -2 or (vals[0] == 0 and vals[1] == 0): # going down to -2 gives wiggle room for space
                self.forces.pop(idx)

        return [newX,newY]

    # called from main.py on each moveable object in a level
    def update(self):
        tm_val = self.get_tilemap_value()

        [newX,newY] = self.apply_forces(self.x,self.y,tm_val)
        [self.x,self.y] = self.check_collision(newX,newY)

    def zero_attack_forces_x(self):
        for idx,vals in enumerate(self.forces):
            self.forces[idx][0] = 0

    def zero_attack_forces_y(self):
        for idx,vals in enumerate(self.forces):
            self.forces[idx][1] = 0

    def draw(self):
        pyxel.blt(self.x*8, self.y*8, 0, self.sprite_index[0]*8, self.sprite_index[1]*8,8,8,15)

    def check_collision(self,newX,newY):

        x_final = self.x
        y_final = self.y

         # level collision
        roundX = round(newX)
        roundY = round(newY)
        roundOldX = round(self.x)
        roundOldY = round(self.y)

        # check collision on current position
        col_now = self.levels.check_tile_collision(roundX,roundY)

        # collision on old x (allows sliding along walls)
        col_old_x = self.levels.check_tile_collision(roundOldX,roundY)
        
        # collision on old y (allows sliding along walls)
        col_old_y = self.levels.check_tile_collision(roundX,roundOldY)
        
        if col_now == 0: # clear floor
            x_final = newX
            y_final = newY
        elif col_old_x == 0:
            y_final = newY
            self.dir[0] = 0
            self.zero_attack_forces_x()
        elif col_old_y == 0:
            x_final = newX
            self.dir[1] = 0
            self.zero_attack_forces_y()
        else:
            self.vel_y = 0
            self.vel_x = 0

        return [x_final,y_final]
    
    def get_tilemap_value(self):
        tm_pos = self.levels.player_pos_to_tm(round(self.x),round(self.y))
        return pyxel.tilemap(0).pget(tm_pos[0],tm_pos[1])



