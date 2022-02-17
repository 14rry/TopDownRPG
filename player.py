import pyxel

class player:
    def __init__(self,x,y,levels):
        self.x = x
        self.y = y
        self.levels = levels
        
        self.health = 10
        
        # attack properties
        self.attack = False
        self.attack_frame = 0

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

        # keep track of direction player is facing for drawing purposes
        self.w_mod = 1
        self.h_mod = 1
        self.sprite = 0

        # attack stuff
        self.attack = False
        self.attack_cooldown = 14

        self.forces = []

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

        # apply forces
        for idx,vals in enumerate(self.forces):
            print(idx,vals)
            newX += vals[0]
            newY += vals[1]

            self.forces[idx][2] -= 1
            if self.forces[idx][2] <= 0:
                self.forces.pop(idx)

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

        # account for faster diagonals .. for some reason this makes it jitter?
        if (dir_y != 0 and dir_x != 0):
            dir_y *= .7
            dir_x *= .7
        
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

                # map collisions
                [min_x,min_y,w,h] = self.get_attack_bounds()
                pos_check = [(min_x/8,self.y),((min_x+w-8)/8,self.y),(self.x,min_y/8),(self.x,(min_y+h-8)/8)]
                dir_check = [(1,0),(-1,0),(0,1),(0,-1)]
                #pos_check = [(self.x,min_y/8)]

                for idx,vals in enumerate(pos_check):
                    # need access to level info here...
                    tm_pos = self.levels.player_pos_to_tm(round(vals[0]),round(vals[1]))
                    tm_val = pyxel.tilemap(0).pget(tm_pos[0],tm_pos[1])

                    if tm_val == (1,0):
                        self.forces.append([dir_check[idx][0]*.4,dir_check[idx][1]*.4,5])

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

