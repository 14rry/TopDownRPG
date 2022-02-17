import ai
import pyxel

class level_handler:
    def __init__(self):
        self.level_index = [1,1]
        self.level_size = 16
        self.grid_size = 8
        # emptyAI = [ai.ai(0,0,False)]

        # level_ai = np.array([[emptyAI,emptyAI,emptyAI,emptyAI],
        #                     [level1_ai,emptyAI,emptyAI,emptyAI]])

        self.max_x = 3
        self.max_y = 1

    def changeLevel(self,x,y,size):
        current_level_x = self.level_index[0]
        current_level_y = self.level_index[1]
        if x == size:
            current_level_x = min(current_level_x+1,self.max_x)
        elif x < 0:
            current_level_x = max(current_level_x-1,0)
            
        if y == size:
            current_level_y = min(current_level_y + 1,self.max_y)
        elif y < 0:
            current_level_y = max(current_level_x - 1,0)

        self.level_index = [current_level_x, current_level_y]
            
        return [current_level_x,current_level_y]

    # def loadAI():
    #     return level_ai[levelIndex[0],levelIndex[1]]
        #return level1_ai
    
    def reset(self):
        self.level_index = [1,1]
        # level1_ai = [ai.ai(), ai.ai(10,10)]

        # self.level_ai = np.array([[emptyAI,emptyAI,emptyAI,emptyAI],
        #                  [level1_ai,emptyAI,emptyAI,emptyAI]])

    def player_pos_to_tm(self,x,y):
        return [x + (self.level_index[0]*self.level_size),y + (self.level_index[1]*self.level_size)]

    def draw(self):
        pyxel.bltm(0,0,0,self.level_index[0]*self.level_size*self.grid_size,self.level_index[1]*self.level_size*self.grid_size,self.grid_size*self.level_size,self.grid_size*self.level_size,1)
