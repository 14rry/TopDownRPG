import utilities

class Camera():
    def __init__(self,screen_size):
        self.x = 0
        self.y = 0
        self.max_x = 0
        self.max_y = 0
        self.screen_size = screen_size
        self.lerp_rate = .1
        self.grid_size = 8

    # offset is [x,y] for where the 'far left' position should be
    def change_level(self,level_size,player_offset):
        self.max_x = 0
        self.max_y = 0
        self.x = player_offset[0]*self.grid_size
        self.y = player_offset[1]*self.grid_size

        offset = [0,0]

        if level_size[0] > self.screen_size:
            self.max_x = level_size[0]*4 - offset[0]
        if level_size[1] > self.screen_size:
            self.max_y = level_size[1]*4 - offset[1]

        print(self.max_x)
            

    # take player x,y pos and update camera accordingly
    def update(self,px,py):
        if self.max_x == 0 and self.max_y == 0: # we are in a single screen level, don't move
            return

        # otherwise, move camera with player
        desired_x = 0
        desired_y = 0

        if px > self.screen_size/2:
            desired_x = min((px-self.grid_size)*self.grid_size,self.max_x)

        if py > self.screen_size/2:
            desired_y = min((py-self.grid_size)*self.grid_size,self.max_y)

        self.x = utilities.lerp(self.x,desired_x,self.lerp_rate)
        self.y = utilities.lerp(self.y,desired_y,self.lerp_rate)

        # print(self.x,self.y)
