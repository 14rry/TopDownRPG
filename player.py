import pyxel

class player:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        
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

        # for non-velocity movement
        self.speed = .2

        self.top_boost = .5
        self.boost = 0
        self.boost_decay = .1

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
            #newY = min(self.playerY+speed,self.levelSize)

        # account for faster diagonals
        if (dir_y != 0 and dir_x != 0):
            dir_y *= .7
            dir_x *= .7
        
        # [newX,newY] = self.move_with_velocity(dir_x,dir_y)
        [newX,newY] = self.move_without_velocity(dir_x,dir_y)


        return [newX,newY]
        