# 0 - clear floor, 1 - wall, 2 - spikes
collision = [
    [0,1,1,0],
    [0,0,0,0],
    [0,0,1,1],
    [0,0,1,1],
    [1,1,1,0],
    [1,1,1,1],
    [0,0,2,0],
    [1,1,1,1]
]

has_dialog = [
    [0,0,0,0],
    [0,0,1,1],
    [0,0,0,0],
    [0,0,0,0],
    [0,0,0,0],
    [0,0,0,0],
    [0,0,0,0]
]

# special scenery object tiles
ball_tm_index = (3,4)

# other special tiles
wall_highlight = (2,7)
coin = (0,8)
transparent = (1,8)

# list of level indexes that belong to big rooms, with room origin at the start
# at the end of each room list is the room size (x,y)
big_rooms = [
                [[1,3],[1,4],[2,3],[2,4],[16*2,16*2]],
                [[2,2],[3,2],[16*2,16]]
            ]

