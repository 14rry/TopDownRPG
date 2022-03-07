import pyxel
import moveable_obj
import utilities
import sound_lookup
import tile_lookup

class Player(moveable_obj.MoveableObj):
    def __init__(self,x,y,levels):
        super().__init__(x,y,levels)
        #
        # overwrite defaults on inherrited properties
        #
        self.health = 10
        self.money = 0

        # movement properties
        self.accel = .02
        self.deccel = .1
        self.max_vel = .2
        self.vel_x = 0
        self.vel_y = 0
        self.dir = [0,0]
        self.vel_magnitude = 0
        self.move_angle = 0
        self.desired_angle = 0

        # for non-velocity movement
        self.speed = .2
        self.top_boost = .5
        self.boost = 0
        self.boost_decay = .1
        
        #
        # not inherrited
        #

        # attack properties
        self.attack = False
        self.attack_frame = 0
        self.attack_cooldown = 14
        self.attack_knockback_force = .5 # knockback from wall
        self.attack_knockback_cooldown = 5
        self.attack_object_force = .1 # force against moveable_obj
        self.attack_object_cooldown = 5
        self.wall_pushback_x = 0
        self.wall_pushback_y = 0

    def move_with_velocity(self,dir_x,dir_y,tm_val):
        # deacel logic
        if tm_val != (3,0):
            if dir_y == 0:
                if abs(self.vel_y) < .1:
                    self.vel_y = 0
                else:
                    self.vel_y -= self.deccel*pyxel.sgn(self.vel_y)

            if dir_x == 0:
                if abs(self.vel_x) < .1:
                    self.vel_x = 0
                else:
                    self.vel_x -= self.deccel*pyxel.sgn(self.vel_x)

            self.vel_x += dir_x * self.accel
            self.vel_y += dir_y * self.accel

            self.vel_x = max(min(self.vel_x,self.max_vel),-self.max_vel)
            self.vel_y = max(min(self.vel_y,self.max_vel),-self.max_vel)

            self.vel_x += dir_x * self.boost
            self.vel_y += dir_y * self.boost

            if dir_x != 0 and dir_y != 0:
                self.vel_x *= .88
                self.vel_y *= .88 # this value depends on max vel... not sure the true math behind this
                # find the value by printing the magnitude (below) and moving diagonal
                # fine tune the value until the diagonal max magnitude is the same as non-diagonal

        # debug print magnitude
        #print(pyxel.sqrt(self.vel_x*self.vel_x+self.vel_y*self.vel_y))

        newX = self.x + self.vel_x
        newY = self.y + self.vel_y

        return [newX,newY]

    def move_without_velocity(self,dir_x,dir_y):
        
        newX = self.x + (dir_x*(self.speed+self.boost))
        newY = self.y + (dir_y*(self.speed+self.boost))

        return [newX,newY]

    def move_like_a_car(self,dir_x,dir_y):
        if dir_y < 0: # car accelerating
            self.vel_magnitude += self.accel
            self.vel_magnitude = min(self.vel_magnitude,self.max_vel)
            #self.vel_magnitude += dir_y # slow down while turning?
        elif dir_y > 0: # pressing the brake
            self.vel_magnitude -= self.deccel
            self.vel_magnitude = max(self.vel_magnitude,-self.max_vel)
        else: # drifting with no accel or brake
            self.vel_magnitude -= self.deccel/4
            self.vel_magnitude = max(self.vel_magnitude,0)

        self.move_angle = self.move_angle + dir_x*5
        # self.move_angle = utilities.lerp(self.move_angle,self.desired_angle,.1)
        self.move_angle = self.move_angle % 360
        print(self.move_angle)

        newX = self.x + pyxel.cos(self.move_angle)*self.vel_magnitude
        newY = self.y + pyxel.sin(self.move_angle)*self.vel_magnitude

        return [newX,newY]


    def move(self):
        # player movement logic  
        newX = self.x
        newY = self.y
        
        dir_x = 0
        dir_y = 0

        # don't allow change of direction in space
        tm_pos = self.levels.player_pos_to_tm(round(self.x),round(self.y))
        tm_val = pyxel.tilemap(0).pget(tm_pos[0],tm_pos[1])

        if tm_val != (3,0):
            if pyxel.btn(pyxel.KEY_RIGHT):
                dir_x += 1
            if pyxel.btn(pyxel.KEY_LEFT):
                dir_x -= 1
            if pyxel.btn(pyxel.KEY_UP):
                dir_y -= 1
            if pyxel.btn(pyxel.KEY_DOWN):
                dir_y += 1
            
            self.dir = [dir_x,dir_y]

            # account for faster diagonals
            if (dir_y != 0 and dir_x != 0):
                dir_y *= .7
                dir_x *= .7
        else:
            dir_x = self.dir[0]
            dir_y = self.dir[1]

        if pyxel.btnp(pyxel.KEY_X) and self.boost <= 0:
            self.boost = self.top_boost
            pyxel.play(sound_lookup.sfx_ch,sound_lookup.player_dash)
        
        [newX,newY] = self.move_without_velocity(dir_x,dir_y)
        #[newX,newY] = self.move_with_velocity(dir_x,dir_y,tm_val)
        #[newX,newY] = self.move_like_a_car(dir_x,dir_y)

        tm_pos = self.levels.player_pos_to_tm(round(newX),round(newY))
        tm_val = pyxel.tilemap(0).pget(tm_pos[0],tm_pos[1])

        [newX,newY] = self.apply_forces(newX,newY,tm_val)

        if self.boost > 0:
            self.boost -= self.boost_decay
            if self.boost < 0:
                self.boost = 0

        return [newX,newY]
        #return self.move_without_velocity(dir_x,dir_y)

    def process_attack(self):
        if not self.attack and pyxel.btnp(pyxel.KEY_Z):
            self.attack = True
            self.attackFrame = pyxel.frame_count

            # do stuff that only happens on first attack frame
            self.attack_wall_pushback()

            pyxel.play(sound_lookup.sfx_ch, sound_lookup.player_attack)

        
        # player attack
        if self.attack: # attack still alive from a previous frame
            if pyxel.frame_count - self.attackFrame > self.attack_cooldown:
                self.attack = False
            else: # attack not finished, do stuff that happens on every attack frame

                # enemy collisions
                # for baddy in self.currentAI:
                #     if baddy.alive:
                #         baddy.checkCollision(roundX,roundY)

                # check scenery collision
                [min_x,min_y,w,h] = self.get_attack_bounds()

                for level_obj in self.levels.level_objs:
                    if self.box_collision_detect(min_x,min_y,w,h,level_obj.x*8,level_obj.y*8,8,8) == True:
                        # calculate angle between player and object and apply force in that direction
                        angle = pyxel.atan2(self.y-level_obj.y,self.x-level_obj.x)
                        dir_x = pyxel.cos(angle)
                        dir_y = pyxel.sin(angle)

                        level_obj.forces.append(
                            [-dir_x*self.attack_object_force,
                            -dir_y*self.attack_object_force,
                            self.attack_object_cooldown])
                        
                        pyxel.play(sound_lookup.sfx_ch, sound_lookup.player_attack_hit_obj)


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
                self.attack_knockback_cooldown])
            pyxel.play(2, sound_lookup.player_attack_hit_wall)

    def check_collision(self, newX, newY):
        # do checks that only apply to parent and not other moveable objects
        [newX,newY] = super().check_collision(newX, newY)
        roundX = round(newX)
        roundY = round(newY)
        tm_pos = self.levels.player_pos_to_tm(roundX,roundY)
        tm_val = pyxel.tilemap(1).pget(tm_pos[0],tm_pos[1])
        print(tm_val)
        if tm_val == tile_lookup.coin: # coin
            self.money += 1
            pyxel.tilemap(1).pset(tm_pos[0],tm_pos[1],tile_lookup.transparent)
            pyxel.play(sound_lookup.sfx_ch,sound_lookup.coin)

        return [newX,newY]


    def box_collision_detect(self,x1,y1,w1,h1,x2,y2,w2,h2):
        if (x1 < x2 + w2 and
            x1 + w1 > x2 and
            y1 < y2 + h2 and
            h1 + y1 > y2):
            return True
        else:
            return False

    def get_attack_bounds(self):
        min_x = 8*(self.x-1)
        min_y = 8*(self.y-1)
        w = 8*3
        h = 8*3

        return [min_x,min_y,w,h]        

    def draw(self):
        self.draw_attack()

        # selects the up/down sprite and sets direction
        if self.dir[1] == 1:
            self.w_mod = 1
            self.sprite = 8
        elif self.dir[1] == -1:
            self.w_mod = -1
            self.sprite = 8

        # selects the left/right sprite and sets direction
        if self.dir[0] == 1:
            self.sprite = 0
            self.h_mod = -1
        elif self.dir[0] == -1:
            self.sprite = 0
            self.h_mod = 1

        pyxel.blt((self.x*8)-self.levels.camera.x,self.y*8-self.levels.camera.y,0,self.sprite,8,8*self.h_mod,8*self.w_mod,7)

        # draw line showing movement for debugging
        sx = self.x*8+4-self.levels.camera.x
        sy = self.y*8+4-self.levels.camera.y
        pyxel.line(sx,sy,sx+pyxel.cos(self.move_angle)*8,sy+pyxel.sin(self.move_angle)*8, 3)
        
        # draw attack wall push direction
        sx = self.x*8+4-self.levels.camera.x
        sy = self.y*8+4-self.levels.camera.y
        pyxel.line(sx,sy,sx+self.wall_pushback_x*16,sy+self.wall_pushback_y*16,5)


    def draw_attack(self):
        if self.attack:
            [min_x,min_y,w,h] = self.get_attack_bounds()

            pyxel.rect(min_x-self.levels.camera.x,
                       min_y-self.levels.camera.y,
                       w,
                       h,
                       12)

