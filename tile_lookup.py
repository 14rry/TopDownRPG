from player_animation import PlayerAnimationState

# 0 - clear floor, 1 - wall, 2 - spikes, 3 - pit
collision = [
    [0,1,1,0],
    [0,0,0,0],
    [0,0,1,1],
    [0,0,1,1],
    [1,1,1,0],
    [1,1,1,1],
    [0,0,2,0],
    [1,1,1,1],
    [0,0,0,0],
    [3,3,3,0],
    [3,3,3,0],
    [3,3,3,0]
]

has_dialog = [
    [0,0,0,0],
    [0,0,1,1],
    [0,0,0,0],
    [0,0,0,0],
    [0,0,0,0],
    [0,0,0,0],
    [0,0,0,0],
    [0,0,0,0],
    [0,0,0,0],
    [0,0,0,0],
    [0,0,0,0],
    [0,0,0,0]
]

# special scenery object tiles
ball = (3,4)
ai = (3,6)
tele_ball = (2,8)

# other special tiles
wall_highlight = (2,7)
coin = (0,8)
transparent = (1,8)

# player sprites
player_forward = [(1,1)]
player_backward = [(1,2)]
player_left = [(0,1)]
player_move_left = [(4,2),(0,1),(5,2)]

player = {
    PlayerAnimationState.IDLE: [(1,1)],
    PlayerAnimationState.IDLE_LEFT: [(0,1)],
    PlayerAnimationState.MOVE_UP: [(1,2)],
    PlayerAnimationState.MOVE_LEFT: [(4,2),(0,1),(5,2)],
    PlayerAnimationState.MOVE_DOWN: [(1,1)]
}

# list of level indexes that belong to big rooms, with room origin at the start
# at the end of each room list is the room size (x,y)
big_rooms = [
                [[1,3],[1,4],[2,3],[2,4],[16*2,16*2]],
                [[2,2],[3,2],[16*2,16]]
            ]

