import ai
import pyxel
import tile_lookup
import moveable_obj
import camera
import tele_ball
import config
import doggy

class LevelHandler:
    def __init__(self,lvl_idx=[1,1]):
        self.level_index = lvl_idx # controls starting level
        self.level_size = [16,16]
        self.screen_size = 16
        self.grid_size = 8

        self.level_collision = [ [0] * self.level_size[0] for _ in range(self.level_size[1])]

        self.max_x = 3
        self.max_y = 1

        self.level_objs = []
        self.update_level_objs()

        self.camera = camera.Camera(self.screen_size)

    def clean_up_scenery(self):
        new_lvl_objs = []
        # delete any unattached scenery and write it back into the tilemap
        for lvl_obj in self.level_objs:
            if lvl_obj.attached_to == None and lvl_obj.alive == True:
                tm_pos = self.player_pos_to_tm(round(lvl_obj.x),round(lvl_obj.y))
                pyxel.tilemap(1).pset(tm_pos[0],tm_pos[1],lvl_obj.sprite_index)
            else:
                if isinstance(lvl_obj.attached_to,doggy.Doggy):
                    tm_pos = self.player_pos_to_tm(round(lvl_obj.x),round(lvl_obj.y))
                    pyxel.tilemap(1).pset(tm_pos[0]+1,tm_pos[1]+1,lvl_obj.sprite_index) # offset x pos by 1 to avoid overwriting doggy.. clunky solution
                else:
                    new_lvl_objs.append(lvl_obj)

        return new_lvl_objs

    def change_level(self,new_level,level_offset):
        self.level_objs = self.clean_up_scenery()
        
        self.level_index = [self.level_index[0] + level_offset[0] + new_level[0], 
            self.level_index[1] + level_offset[1] + new_level[1]]

        # handle multi-screen levels
        player_offset = [0,0]

        is_big_room = False
        self.level_size = [16,16] # default one screen size
        for big_room in tile_lookup.big_rooms:
            if is_big_room:
                break
            for idx,room in enumerate(big_room[:-1]):
                if self.level_index == room:
                    is_big_room = True
                    self.level_size = big_room[-1]
                    if idx > 0: # not the origin room
                        self.level_index = big_room[0] # set level index to origin room
                        player_offset = [(room[0]-big_room[0][0])*16,(room[1]-big_room[0][1])*16]
                    break

        print("level:",self.level_index)

        self.camera.change_level(self.level_size,player_offset,new_level)
        self.update_level_objs()
        config.particle_effects.destroy_all()
            
        return player_offset

    # also updates collision matrix
    def update_level_objs(self):
        self.level_collision = [ [0] * self.level_size[1] for _ in range(self.level_size[0])]

        # build list of active scenery, ai, etc. based on presence of certain special tiles
        for i in range(self.level_size[0]):
            for j in range(self.level_size[1]):
                tm_pos = self.player_pos_to_tm(i,j)
                tm_val = pyxel.tilemap(1).pget(tm_pos[0],tm_pos[1])
                is_obj = False
                if tm_val == tile_lookup.ball:
                    self.level_objs.append(moveable_obj.MoveableObj(i,j,self,tm_val))
                    is_obj = True
                elif tm_val in tile_lookup.ai:
                    self.level_objs.append(ai.Ai(i,j,self,tm_val))
                    is_obj = True
                elif tm_val in tile_lookup.tele_ball:
                    self.level_objs.append(tele_ball.TeleBall(i,j,self,tm_val))
                    is_obj = True
                elif tm_val == tile_lookup.doggy:
                    self.level_objs.append(doggy.Doggy(i,j,self,tm_val))
                    is_obj = True

                if is_obj == True:
                    pyxel.tilemap(1).pset(tm_pos[0],tm_pos[1],(1,8)) # (1,8) is transparent tile on layer 2

                # build wall matrix for pathfiding
                tm_val = pyxel.tilemap(0).pget(tm_pos[0],tm_pos[1])

                try:    
                    if tile_lookup.collision[tm_val[1]][tm_val[0]] == 1:
                        self.level_collision[i][j] = 1
                except (ValueError, IndexError):
                    continue


    def check_for_change(self,roundX,roundY,newX,newY):
        new_level = [0,0]
        level_did_change = False

        if roundX >= self.level_size[0]:
            new_level = [1,0]
            level_offset = [pyxel.floor((newX-1)/16),pyxel.floor(newY/16)] # accounts for the possibility of being on a different level in big rooms (i.e. if player moves to the right in a big room, the true 'level' index could be 2,3 instead of 1,3)
            newX = 0
            level_offset2 = [0,pyxel.floor(newY/16)] # accounts for the possibility of being on a different level in big rooms (i.e. if player moves to the right in a big room, the true 'level' index could be 2,3 instead of 1,3)
        elif roundX < 0:
            new_level = [-1,0]
            level_offset = [pyxel.floor((newX+1)/16),pyxel.floor(newY/16)]
            newX = self.screen_size - 1
            level_offset2 = [0,pyxel.floor(newY/16)]

        if roundY >= self.level_size[1]:
            new_level = [0,1]
            level_offset = [pyxel.floor(newX/16),pyxel.floor((newY-1)/16)]
            newY = 0
            level_offset2 = [pyxel.floor((newX)/16),0]

        elif roundY < 0:
            new_level = [0,-1]
            level_offset = [pyxel.floor(newX/16),pyxel.floor((newY+1)/16)]
            newY = self.screen_size - 1
            level_offset2 = [pyxel.floor((newX)/16),0]

        if not new_level == [0,0]:
            player_offset = self.change_level(new_level,level_offset)

            newX += player_offset[0] - level_offset2[0]*16
            newY += player_offset[1] - level_offset2[1]*16

            level_did_change = True

        return [newX,newY,level_did_change]

    # returns 1 if wall, 0 if floor, -1 if error
    def check_tile_collision(self,roundX,roundY,light_up = False):

        # try:    
        #     return self.level_collision[roundX][roundY]
        # except (ValueError, IndexError):

        # fall back to tm value .. this happens when changing level
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

    def draw(self,x0):

        # base layer
        pyxel.bltm(x0,0,0,
            self.camera.x+self.level_index[0]*self.screen_size*self.grid_size,
            self.camera.y+self.level_index[1]*self.screen_size*self.grid_size,
            self.grid_size*self.screen_size,
            self.grid_size*self.screen_size,
            8)

        # second layer sprites w/ transparency i.e. coins
        pyxel.bltm(x0,0,1,
            self.camera.x+self.level_index[0]*self.screen_size*self.grid_size,
            self.camera.y+self.level_index[1]*self.screen_size*self.grid_size,
            self.grid_size*self.screen_size,
            self.grid_size*self.screen_size,
            8)