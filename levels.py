import ai
import pyxel
import tile_lookup
import moveable_obj
import camera

class LevelHandler:
    def __init__(self,lvl_idx=[1,1]):
        self.level_index = lvl_idx # controls starting level
        self.level_size = [16,16]
        self.screen_size = 16
        self.grid_size = 8

        # emptyAI = [ai.ai(0,0,False)]

        # level_ai = np.array([[emptyAI,emptyAI,emptyAI,emptyAI],
        #                     [level1_ai,emptyAI,emptyAI,emptyAI]])

        self.max_x = 3
        self.max_y = 1

        self.level_objs = []
        self.update_level_objs()

        self.camera = camera.Camera(self.screen_size)

    def clean_up_scenery(self):
        new_lvl_objs = []
        # delete any unattached scenery and write it back into the tilemap
        for lvl_obj in self.level_objs:
            print(lvl_obj.attached_to)
            if lvl_obj.attached_to == None:
                tm_pos = self.player_pos_to_tm(round(lvl_obj.x),round(lvl_obj.y))
                pyxel.tilemap(0).pset(tm_pos[0],tm_pos[1],lvl_obj.sprite_index)
            else:
                new_lvl_objs.append(lvl_obj)
                #print('bye:',tm_pos,lvl_obj.sprite_index)

        return new_lvl_objs

    def change_level(self,new_level,level_offset):
        self.level_objs = self.clean_up_scenery()

        self.level_index = [self.level_index[0] + level_offset[0] + new_level[0], 
            self.level_index[1] + level_offset[1] + new_level[1]]

        # handle multi-screen levels
        player_offset = [0,0]

        is_big_room = False
        for big_rooms in tile_lookup.big_rooms:
            if is_big_room:
                break
            for idx,room in enumerate(big_rooms[:-2]):
                print(room)
                if self.level_index == room:
                    is_big_room = True
                    self.level_size = big_rooms[-1]
                    if idx > 0: # not the origin room
                        self.level_index = big_rooms[0] # set level index to origin room
                        player_offset = [(room[0]-big_rooms[0][0])*16,(room[1]-big_rooms[0][1])*16]
                    break

        if not is_big_room:
            self.level_size = [16,16]

        print("level:",self.level_index)

        self.camera.change_level(self.level_size,player_offset)
        self.update_level_objs()
            
        return player_offset

    # def loadAI():
    #     return level_ai[levelIndex[0],levelIndex[1]]
        #return level1_ai

    def update_level_objs(self):
        # build list of active scenery, ai, etc. based on presence of certain special tiles
        for i in range(self.level_size[0]):
            for j in range(self.level_size[1]):
                tm_pos = self.player_pos_to_tm(i,j)
                tm_val = pyxel.tilemap(0).pget(tm_pos[0],tm_pos[1])
                if tm_val == tile_lookup.ball:
                    self.level_objs.append(moveable_obj.MoveableObj(i,j,self,tm_val))
                    # replace ball tile with floor
                    pyxel.tilemap(0).pset(tm_pos[0],tm_pos[1],(0,0)) # (0,0) is floor
                elif tm_val == tile_lookup.ai:
                    print('hi')
                    self.level_objs.append(ai.Ai(i,j,self,tm_val))
                    pyxel.tilemap(0).pset(tm_pos[0],tm_pos[1],(0,0)) # (0,0) is floor

    def check_for_change(self,roundX,roundY,newX,newY):
        level_did_change = False
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
                level_did_change = True
                # TODO: fix AI with new tilemaps
                # # load AI
                # self.currentAI = levels.loadAI()

        return [newX,newY,level_did_change]

    # returns 1 if wall, 0 if floor, -1 if error
    def check_tile_collision(self,roundX,roundY,light_up = False):
        tm_pos = self.player_pos_to_tm(roundX,roundY)
        tm_val = pyxel.tilemap(0).pget(tm_pos[0],tm_pos[1])
        #print(len(tile_lookup.collision[0]),len(tile_lookup.collision))
        if tm_val[0] >= len(tile_lookup.collision[0]) or tm_val[1] >= len(tile_lookup.collision):
            print('check_tile_collision lookup error out of bounds, tm_val:')
            print(tm_val)
            return -1
        else:
            tile_coll = tile_lookup.collision[tm_val[1]][tm_val[0]]
            if tile_coll == 1 and light_up:
                pyxel.tilemap(0).pset(tm_pos[0],tm_pos[1],tile_lookup.wall_highlight)
            return tile_coll

    def player_pos_to_tm(self,x,y):
        return [x + (self.level_index[0]*self.screen_size),y + (self.level_index[1]*self.screen_size)]

    def draw(self):
        # base layer
        pyxel.bltm(0,0,0,
            self.camera.x+self.level_index[0]*self.screen_size*self.grid_size,
            self.camera.y+self.level_index[1]*self.screen_size*self.grid_size,
            self.grid_size*self.screen_size,
            self.grid_size*self.screen_size,
            15)

        # second layer sprites w/ transparency i.e. coins
        pyxel.bltm(0,0,1,
            self.camera.x+self.level_index[0]*self.screen_size*self.grid_size,
            self.camera.y+self.level_index[1]*self.screen_size*self.grid_size,
            self.grid_size*self.screen_size,
            self.grid_size*self.screen_size,
            15)