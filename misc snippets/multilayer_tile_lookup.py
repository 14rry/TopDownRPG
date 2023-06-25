
## Multilayer tile lookup

# levels:
def check_tile_collision_multilayer(self,roundX,roundY,light_up = False,layer=0):

    # try:    
    #     return self.level_collision[roundX][roundY]
    # except (ValueError, IndexError):

    # fall back to tm value .. this happens when changing level
    tm_pos = self.player_pos_to_tm(roundX,roundY)
    tm_vals = [pyxel.tilemap(0).pget(tm_pos[0],tm_pos[1]), pyxel.tilemap(1).pget(tm_pos[0],tm_pos[1])]
    #print(len(tile_lookup.collision[0]),len(tile_lookup.collision))

    col_vals = []
    for tm_val in tm_vals:
        if tm_val[0] >= len(tile_lookup.collision[0]) or tm_val[1] >= len(tile_lookup.collision):
            print('check_tile_collision lookup error out of bounds, tm_val:')
            print(tm_val)
            col_vals.append(-1)
        else:
            tile_coll = tile_lookup.collision[tm_val[1]][tm_val[0]]
            if tile_coll == 1 and light_up:
                pyxel.tilemap(0).pset(tm_pos[0],tm_pos[1],tile_lookup.wall_highlight)
            col_vals.append(tile_coll)

    return col_vals


# moveable obj:

def is_wall(self,col_val,avoids_pits):
    is_wall = False
    for val in col_val:
        is_wall = val == 1 or (avoids_pits and val == 3)
        if is_wall: 
            return True

    return False





elif level_obj.collision_value == 1: # level object has wall collision
    if utilities.box_collision_detect(self.x*8,self.y*8,8,8,level_obj.x*8,level_obj.y*8,8,8):
        newX = self.x
        newY = self.y