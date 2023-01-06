from enum import Enum
import tile_lookup

class PlayerAnimation():
    def __init__(self):
        self.state = PlayerAnimationState.IDLE
        self.frame = 0
        self.sub_frame = 0
        self.max_sub_frame = 6 # number of frames to repeat.. controls animation speed
        self.repeat = 0
        self.max_repeat = 0
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
            self.repeat += 1
            if self.repeat > self.max_repeat:
                self.repeat = 0
                self.frame += 1
                if self.frame > self.max_frame: # step to next sprite in animation
                    self.frame = 0

        temp = self.animation_table[self.frame]

        # defining num repitions is optional.. here's how we handle it
        if len(temp) == 2:
            self.max_repeat = 0
            self.sprite = temp
        else:
            self.max_repeat = temp[2]
            self.sprite = (temp[0],temp[1])

    def update_direction(self,dir):
        prev_state = self.state

        if dir[0] == 0 and dir[1] == 0: # not moving
            if self.state == PlayerAnimationState.MOVE_LEFT:
                self.state = PlayerAnimationState.IDLE_LEFT
            elif self.state == PlayerAnimationState.MOVE_DOWN:
                self.state = PlayerAnimationState.IDLE
            elif self.state == PlayerAnimationState.MOVE_UP:
                self.state = PlayerAnimationState.IDLE_UP

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
    IDLE_UP = 7