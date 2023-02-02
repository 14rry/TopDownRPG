from player_animation import PlayerAnimationState

# 0 - clear floor, 1 - wall, 2 - spikes, 3 - pit, 4 - npc/dialog
collision = [
    [0,1,1,0,0,0,0,0],
    [0,0,4,4,0,0,0,0],
    [0,0,1,1,0,0,0,0],
    [0,0,1,1,0,0,0,0],
    [1,1,1,0,0,0,0,0],
    [1,1,1,1,0,0,0,0],
    [0,0,2,0,0,0,0,0],
    [1,1,1,1,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [3,3,3,0,0,0,0,0],
    [3,3,3,0,0,0,0,0],
    [3,3,3,0,0,0,0,0],
    [1,1,1,1,1,1,0,0],
    [1,1,1,1,1,1,0,0],
    [1,1,1,1,1,1,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [1,1,0,1,0,0,0,0],
    [1,1,0,0,0,0,0,0],
    [1,1,0,0,0,0,0,0],
    [1,1,0,0,0,0,0,0],
    [1,1,1,1,0,0,0,0],
    [1,1,1,1,0,0,0,0],
    [1,1,0,0,0,0,0,0],
]

# special scenery object tiles
ball = (3,4)
ai = [(3,6),(4,6),(5,6)]
tele_ball = [(2,8),(3,9)]

# other special tiles
wall_highlight = (2,7)
coin = (0,8)
transparent = (1,8)

# ANIMATION TABLES

# player sprites (xcoord,ycoord,num_frames (optional))
player_animation = {
    PlayerAnimationState.IDLE: [(1,1,10),(4,1),(1,1,10),(5,1)],
    PlayerAnimationState.IDLE_LEFT: [(0,1,10),(4,0),(0,1,10),(5,0)],
    PlayerAnimationState.IDLE_UP: [(1,2,20),(0,2)],
    PlayerAnimationState.MOVE_UP: [(1,2)],
    PlayerAnimationState.MOVE_LEFT: [(4,2),(0,1),(5,2)],
    PlayerAnimationState.MOVE_DOWN: [(1,1)]
}

ai_animation = {
    PlayerAnimationState.IDLE: [(4,6)],
    PlayerAnimationState.IDLE_LEFT: [(3,6)],
    PlayerAnimationState.IDLE_UP: [(5,6)],
    PlayerAnimationState.MOVE_UP: [(5,6)],
    PlayerAnimationState.MOVE_LEFT: [(3,6)],
    PlayerAnimationState.MOVE_DOWN: [(4,6)]
}

tele_ball_animation = {
    PlayerAnimationState.IDLE: [(2,8,2),(3,9,2)]
}

# list of level indexes that belong to big rooms, with room origin at the start
# at the end of each room list is the room size (x,y)

b_r = [
        [1,3,2,2],
        [2,2,2,1]
    ]

# extend rooms into list of all level indexes programatically
big_rooms = []
for big_room in b_r:

    new_room = []

    new_room_x0 = big_room[0]
    new_room_y0 = big_room[1]

    for i in range(big_room[2]):
        for j in range(big_room[3]):
            new_room.append([new_room_x0,new_room_y0])
            new_room_y0 += 1
        new_room_y0 = big_room[1]
        new_room_x0 += 1

    new_room.append([big_room[2]*16,big_room[3]*16])
    big_rooms.append(new_room)

# big_rooms_og = [
#                 [[1,3],[1,4],[2,3],[2,4],[16*2,16*2]],
#                 [[2,2],[3,2],[16*2,16]]
#             ]

# print(big_rooms)
# print(big_rooms_og)

