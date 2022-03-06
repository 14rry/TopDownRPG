import ai
import pyxel
import tile_lookup
import moveable_obj
import camera

class LevelHandler:
    def __init__(self):
        self.level_index = [1,1] # controls starting level
        self.level_size = [16,16]
        self.screen_size = 16
        self.grid_size = 8

        # emptyAI = [ai.ai(0,0,False)]

        # level_ai = np.array([[emptyAI,emptyAI,emptyAI,emptyAI],
        #                     [level1_ai,emptyAI,emptyAI,emptyAI]])

        self.max_x = 3
        self.max_y = 1

        self.level_objs = []

        self.camera = camera.Camera(self.screen_size)

    def change_level(self,new_level,level_offset):

        self.level_index = [self.level_index[0] + level_offset[0] + new_level[0], 
            self.level_index[1] + level_offset[1] + new_level[1]]

        # handle multi-screen levels
        player_offset = [0,0]
        if self.level_index == [1,3] or self.level_index == [2,3]: # need to account for all cases... this could get annoying
            self.level_size = [16*2,16*2]
            if self.level_index == [2,3]: # account for being able to enter into another level index which is shared in the big room
                self.level_index = [1,3]
                player_offset = [16,0]
        elif self.level_index == [2,2] or self.level_index == [3,2]:
            self.level_size = [16*2,16]
            if self.level_index == [3,2]:
                self.level_index = [2,2]
                player_offset = [16,0]
        else:
            self.level_size = [16,16]
            player_offset = [0,0]

        print("level:",self.level_index)


        self.camera.change_level(self.level_size,player_offset)

        # build list of active scenery, ai, etc. based on presence of certain special tiles
        pyxel.load("topdown.pyxres") # TODO: this is a bad workaround for resetting tilemap after changing for scenery..

        self.level_objs = []
        for i in range(self.level_size[0]):
            for j in range(self.level_size[1]):
                tm_pos = self.player_pos_to_tm(i,j)
                tm_val = pyxel.tilemap(0).pget(tm_pos[0],tm_pos[1])
                if tm_val == tile_lookup.ball_tm_index:
                    self.level_objs.append(moveable_obj.MoveableObj(i,j,self,tm_val))
                    # replace ball tile with floor
                    pyxel.tilemap(0).pset(tm_pos[0],tm_pos[1],(0,0)) # (0,0) is floor
            
        return player_offset

    # def loadAI():
    #     return level_ai[levelIndex[0],levelIndex[1]]
        #return level1_ai
    
    def reset(self):
        self.level_index = [1,1]
        # level1_ai = [ai.ai(), ai.ai(10,10)]

        # self.level_ai = np.array([[emptyAI,emptyAI,emptyAI,emptyAI],
        #                  [level1_ai,emptyAI,emptyAI,emptyAI]])

    def check_for_change(self,roundX,roundY,newX,newY):
        if (roundX == self.level_size[0] or 
            roundY == self.level_size[1] or
            roundX < 0 or
            roundY < 0):
                new_level = [0,0]
                if roundX == self.level_size[0]:
                    new_level = [1,0]
                    level_offset = [pyxel.floor((newX-1)/16),pyxel.floor(newY/16)] # accounts for the possibility of being on a different level in big rooms (i.e. if player moves to the right in a big room, the true 'level' index could be 2,3 instead of 1,3)
                    #level_offset = [0,pyxel.floor(newY/16)] # accounts for the possibility of being on a different level in big rooms (i.e. if player moves to the right in a big room, the true 'level' index could be 2,3 instead of 1,3)
                    newX = 0
                elif roundX < 0:
                    new_level = [-1,0]
                    level_offset = [pyxel.floor((newX+1)/16),pyxel.floor(newY/16)]
                    newX = self.screen_size - 1
                if roundY == self.level_size[1]:
                    new_level = [0,1]
                    level_offset = [pyxel.floor(newX/16),pyxel.floor((newY-1)/16)]
                    newY = 0
                elif roundY < 0:
                    new_level = [0,-1]
                    level_offset = [pyxel.floor(newX/16),pyxel.floor((newY+1)/16)]
                    newY = self.screen_size - 1


                player_offset = self.change_level(new_level,level_offset)

                print('lvl off:',level_offset)
                newX += player_offset[0] - level_offset[0]*16
                newY += player_offset[1] - level_offset[1]*16

                print(newX,newY)
                
                # TODO: fix AI with new tilemaps
                # # load AI
                # self.currentAI = levels.loadAI()

        return [newX,newY]

    # returns 1 if wall, 0 if floor, -1 if error
    def check_tile_collision(self,roundX,roundY):
        tm_pos = self.player_pos_to_tm(roundX,roundY)
        tm_val = pyxel.tilemap(0).pget(tm_pos[0],tm_pos[1])
        #print(len(tile_lookup.collision[0]),len(tile_lookup.collision))
        if tm_val[0] >= len(tile_lookup.collision[0]) or tm_val[1] >= len(tile_lookup.collision):
            print('check_tile_collision lookup error out of bounds, tm_val:')
            print(tm_val)
            return -1
        else:
            return tile_lookup.collision[tm_val[1]][tm_val[0]]

    def player_pos_to_tm(self,x,y):
        return [x + (self.level_index[0]*self.screen_size),y + (self.level_index[1]*self.screen_size)]

    def draw(self):
        pyxel.bltm(0,0,0,
            self.camera.x+self.level_index[0]*self.screen_size*self.grid_size,
            self.camera.y+self.level_index[1]*self.screen_size*self.grid_size,
            self.grid_size*self.screen_size,
            self.grid_size*self.screen_size,
            15)
