from enum import Enum
from player import Player
import tile_lookup

class PlayerAnimation():
    def __init__(self):
        self.state = PlayerAnimationState.IDLE
        self.frame = 0
        self.sub_frame = 0
        self.max_sub_frame = 6 # number of frames to repeat.. controls animation speed
        self.left_right_flip = 1

        self.animation_table = []
        self.update_animation_table()
        self.sprite = self.update_sprite()

    # main function, returns player sprite for given animation frame
    # gets called each time player is drawn
    def get_frame_sprite(self,dir):
        self.update_direction(dir)
        self.update_sprite()

        return [self.sprite,self.left_right_flip]

    def update_sprite(self):
        self.sub_frame += 1
        if self.sub_frame > self.max_sub_frame:
            self.sub_frame = 0
            self.frame += 1
            if self.frame > self.max_frame:
                self.frame = 0

        self.sprite = self.animation_table[self.frame]

    def update_direction(self,dir):
        prev_state = self.state

        if dir[0] == 0 and dir[1] == 0: # not moving
            if self.state == PlayerAnimationState.MOVE_LEFT:
                self.state = PlayerAnimationState.IDLE_LEFT
            elif self.state == PlayerAnimationState.MOVE_DOWN:
                self.state = PlayerAnimationState.IDLE

        else: # moving
            # selects the up/down sprite and sets direction
            if dir[1] == 1:
                self.state = PlayerAnimationState.MOVE_DOWN
            elif dir[1] == -1:
                self.state = PlayerAnimationState.MOVE_UP

            # selects the left/right sprite and sets direction
            if dir[0] == 1:
                self.state = PlayerAnimationState.MOVE_LEFT # not a typo, right is the same as left just flipped
                self.left_right_flip = -1
            elif dir[0] == -1:
                self.state = PlayerAnimationState.MOVE_LEFT
                self.left_right_flip = 1

        if prev_state != self.state: # state changed, updated animation tables
            self.update_animation_table()

    def update_animation_table(self):
        self.animation_table = tile_lookup.player[self.state]
        self.max_frame = len(self.animation_table) - 1
        self.frame = 0
        self.sub_frame = 0

class PlayerAnimationState(Enum):
    IDLE = 1
    MOVE_LEFT = 2
    MOVE_RIGHT = 3
    MOVE_UP = 4
    MOVE_DOWN = 5
    IDLE_LEFT = 6