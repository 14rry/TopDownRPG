import ai
import pyxel
import tile_lookup
import moveable_obj

class LevelHandler:
    def __init__(self):
        self.level_index = [1,1] # controls starting level
        self.level_size = 16
        self.grid_size = 8
        # emptyAI = [ai.ai(0,0,False)]

        # level_ai = np.array([[emptyAI,emptyAI,emptyAI,emptyAI],
        #                     [level1_ai,emptyAI,emptyAI,emptyAI]])

        self.max_x = 3
        self.max_y = 1

        self.level_objs = []

    def change_level(self,x,y,size):
        current_level_x = self.level_index[0]
        current_level_y = self.level_index[1]
        if x == size:
            current_level_x = current_level_x+1
        elif x < 0:
            current_level_x = current_level_x-1
            
        if y == size:
            current_level_y = current_level_y + 1
        elif y < 0:
            current_level_y = current_level_y - 1

        self.level_index = [current_level_x, current_level_y]

        print("level:",self.level_index)

        # build list of active scenery, ai, etc. based on presence of certain special tiles
        pyxel.load("topdown.pyxres") # bad workaround for resetting tilemap after changing for scenery..

        self.level_objs = []
        for i in range(16):
            for j in range(16):
                tm_pos = self.player_pos_to_tm(i,j)
                tm_val = pyxel.tilemap(0).pget(tm_pos[0],tm_pos[1])
                if tm_val == tile_lookup.ball_tm_index:
                    self.level_objs.append(moveable_obj.MoveableObj(i,j,self,tm_val))
                    # replace ball tile with floor
                    pyxel.tilemap(0).pset(tm_pos[0],tm_pos[1],(0,0)) # (0,0) is floor
            
        return [current_level_x,current_level_y]

    # def loadAI():
    #     return level_ai[levelIndex[0],levelIndex[1]]
        #return level1_ai
    
    def reset(self):
        self.level_index = [1,1]
        # level1_ai = [ai.ai(), ai.ai(10,10)]

        # self.level_ai = np.array([[emptyAI,emptyAI,emptyAI,emptyAI],
        #                  [level1_ai,emptyAI,emptyAI,emptyAI]])

    def check_for_change(self,roundX,roundY,newX,newY):
        if (roundX == self.level_size or 
            roundY == self.level_size or
            roundX < 0 or
            roundY < 0):
                self.change_level(roundX,roundY,self.level_size)
                if roundX == self.level_size:
                    newX = 0
                elif roundX < 0:
                    newX = self.level_size - 1
                if roundY == self.level_size:
                    newY = 0
                elif roundY < 0:
                    newY = self.level_size - 1
                
                # TODO: fix AI with new tilemaps
                # # load AI
                # self.currentAI = levels.loadAI()

        return [newX,newY]

    def check_tile_collision(self,roundX,roundY):
        tm_pos = self.player_pos_to_tm(roundX,roundY)
        tm_val = pyxel.tilemap(0).pget(tm_pos[0],tm_pos[1])
        return tile_lookup.collision[tm_val[1]][tm_val[0]]

    def player_pos_to_tm(self,x,y):
        return [x + (self.level_index[0]*self.level_size),y + (self.level_index[1]*self.level_size)]

    def draw(self):
        pyxel.bltm(0,0,0,self.level_index[0]*self.level_size*self.grid_size,self.level_index[1]*self.level_size*self.grid_size,self.grid_size*self.level_size,self.grid_size*self.level_size)
