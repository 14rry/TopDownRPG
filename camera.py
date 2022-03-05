import utilities

class Camera():
    def __init__(self,screen_size):
        self.x = 0
        self.y = 0
        self.max_x = 0
        self.max_y = 0
        self.screen_size = screen_size
        self.lerp_rate = .1

    def change_level(self,level_size):
        self.max_x = 0
        self.max_y = 0
        self.x = 0
        self.y = 0

        if level_size[0] > self.screen_size:
            self.max_x = level_size[0]*2
        if level_size[1] > self.screen_size:
            self.max_y = level_size[1]*2
            

    # take player x,y pos and update camera accordingly
    def update(self,px,py):
        if self.max_x == 0 and self.max_y == 0: # we are in a single screen level, don't move
            return

        # otherwise, move camera with player
        desired_x = 0
        desired_y = 0

        if px > self.screen_size / 2:
            desired_x = min((px-8)*8,self.max_x)

        if py > self.screen_size / 2:
            desired_y = min((py-8)*8,self.max_y)

        self.x = utilities.lerp(self.x,desired_x,self.lerp_rate)
        self.y = utilities.lerp(self.y,desired_y,self.lerp_rate)
