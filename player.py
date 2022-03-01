import pyxel
import moveable_obj

class Player(moveable_obj.MoveableObj):
    def __init__(self,x,y,levels):
        super().__init__(x,y,levels)
        #
        # overwrite defaults on inherrited properties
        #
        self.health = 10

        # movement properties
        self.accel = .04
        self.deccel = .1
        self.max_vel = .4
        self.vel_x = 0
        self.vel_y = 0
        self.dir = [0,0]

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
        self.attack_knockback_force = .5
        self.attack_knockback_cooldown = 5

    def move_with_velocity(self,dir_x,dir_y):
        # deacel logic
        if (dir_y == 0 and dir_x == 0):
            if abs(self.vel_y) < .04:
                self.vel_y = 0
            if abs(self.vel_x) < .04:
                self.vel_x = 0

            if self.vel_x > 0:
                self.vel_x -= self.deccel
            elif self.vel_x < 0:
                self.vel_x += self.deccel

            if self.vel_y > 0:
                self.vel_y -= self.deccel
            elif self.vel_y < 0:
                self.vel_y += self.deccel
        else:
            self.vel_x += dir_x * self.accel
            self.vel_y += dir_y * self.accel

        self.vel_x = max(min(self.vel_x,self.max_vel),-self.max_vel)
        self.vel_y = max(min(self.vel_y,self.max_vel),-self.max_vel)

        newX = self.x + self.vel_x
        newY = self.y + self.vel_y

        return [newX,newY]

    def move_without_velocity(self,dir_x,dir_y):
        if pyxel.btnp(pyxel.KEY_X) and self.boost <= 0:
            self.boost = self.top_boost

        newX = self.x + (dir_x*(self.speed+self.boost))
        newY = self.y + (dir_y*(self.speed+self.boost))

        tm_pos = self.levels.player_pos_to_tm(round(newX),round(newY))
        tm_val = pyxel.tilemap(0).pget(tm_pos[0],tm_pos[1])

        [newX,newY] = self.apply_forces(newX,newY,tm_val)

        if self.boost > 0:
            self.boost -= self.boost_decay
            if self.boost < 0:
                self.boost = 0

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
                #newX = min(self.playerX+speed,self.levelSize)
            if pyxel.btn(pyxel.KEY_LEFT):
                dir_x -= 1
                #newX = max(self.playerX-speed,-1)
            if pyxel.btn(pyxel.KEY_UP):
                dir_y -= 1
                #newY = max(self.playerY-speed,-1)
            if pyxel.btn(pyxel.KEY_DOWN):
                dir_y += 1
            
            self.dir = [dir_x,dir_y]
                #newY = min(self.playerY+speed,self.levelSize)

            # account for faster diagonals
            if (dir_y != 0 and dir_x != 0):
                dir_y *= .7
                dir_x *= .7
        else:
            dir_x = self.dir[0]
            dir_y = self.dir[1]
        
        # return self.move_with_velocity(dir_x,dir_y)
        return self.move_without_velocity(dir_x,dir_y)

    def process_attack(self):
        # player attack
        if self.attack:
            if pyxel.frame_count - self.attackFrame > self.attack_cooldown:
                self.attack = False

            # enemy collisions
            # for baddy in self.currentAI:
            #     if baddy.alive:
            #         baddy.checkCollision(roundX,roundY)

        else:
            if pyxel.btnp(pyxel.KEY_Z):
                self.attack = True
                self.attackFrame = pyxel.frame_count

                # attack pushback
                [min_x,min_y,w,h] = self.get_attack_bounds()
                max_x = round((min_x + w - 8)/8)
                max_y = round((min_y + h - 8)/8)
                min_x = round(min_x/8)
                min_y = round(min_y/8)
                cur_x = round(self.x)
                cur_y = round(self.y)
                # pos_check = [
                #     (min_x,cur_y),
                #     (max_x,cur_y),
                #     (cur_x,min_y),
                #     (cur_x,max_y),
                #     (max_x,max_y),
                #     (min_x,min_y),
                #     (min_x,max_y),
                #     (max_x,min_y)] # diagonals case
                # dir_check = [(1,0),(-1,0),(0,1),(0,-1),(-1,-1),(1,1),(1,-1),(-1,1)]
                pos_check = [
                    (min_x,cur_y),
                    (max_x,cur_y),
                    (cur_x,min_y),
                    (cur_x,max_y),
                    ] # TODO: add diagonals case
                dir_check = [(1,0),(-1,0),(0,1),(0,-1)]

                attack_force_x_dir = 0
                attack_force_y_dir = 0

                for idx,vals in enumerate(pos_check):
                    # check map collision
                    if self.levels.check_tile_collision(round(vals[0]),round(vals[1])) == 1:
                        attack_force_x_dir += dir_check[idx][0]
                        attack_force_y_dir += dir_check[idx][1]

                # check scenery collision.. change this to simple box collision check rather than
                #   checking each cardinal direction
                for level_obj in self.levels.level_objs:
                    # BUG: collision box way bigger than it should be for some reason
                    if self.box_collision_detect(min_x,min_y,w,h,level_obj.x,level_obj.y,8,8) == True:
                        print('collide')
                        # calc direction and apply force
                        # this approach is trash
                        # TODO: calculate angle
                        dir_x = 0
                        dir_y = 0
                        if self.x > level_obj.x:
                            dir_x = -1
                        elif self.x < level_obj.x:
                            dir_x = 1

                        if self.y > level_obj.y:
                            dir_y = -1
                        elif self.y < level_obj.y:
                            dir_y = 1

                        level_obj.forces.append(
                            [dir_x*self.attack_knockback_force,
                            dir_y*self.attack_knockback_force,
                            self.attack_knockback_cooldown])

                print(attack_force_x_dir,attack_force_y_dir)

                # TODO: normalize to magnitude of 1

                self.forces.append(
                    [attack_force_x_dir*self.attack_knockback_force,
                    attack_force_y_dir*self.attack_knockback_force,
                    self.attack_knockback_cooldown])

                # TODO: check collision against other moveable_objs

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

        pyxel.blt(self.x*8,self.y*8,0,self.sprite,8,8*self.h_mod,8*self.w_mod,7)

    def draw_attack(self):
        if self.attack:
            [min_x,min_y,w,h] = self.get_attack_bounds()

            pyxel.rect(min_x,
                       min_y,
                       w,
                       h,
                       12)

