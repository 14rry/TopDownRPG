import ai
from enum import Enum
import tile_lookup
import utilities
import moveable_obj

class Doggy(ai.Ai):
    def __init__(self,x,y,levels,sprite):
        super().__init__(x,y,levels,sprite)

        self.dog_state = DoggyState.IDLE
        self.known_balls = []
        self.target_ball = None
        self.can_be_thrown = False
        self.ball_min_distance = .9
        self.wait_frames = 60 # how long to wait after retrieving

        self.player_damage = 0

        self.frame_count = 0
        self.update_frame_rate = 20

        self.invincible = True

        print('Ruff!')

    def take_player_damage(self,damage_amount):
        return

    def find_ball(self):
        min_ball_distance = 9999
        for obj in self.levels.level_objs:
            if obj.sprite_index == tile_lookup.ball:
                self.known_balls.append(obj)
                ball_distance = utilities.distance(self.x,self.y,obj.x,obj.y)
                if ball_distance < min_ball_distance:
                    self.target_ball = obj

    def target(self,x,y,next_state):
        if utilities.distance(self.x,self.y,x,y) < self.ball_min_distance:
            self.move_dir = [0,0]
            self.dog_state = next_state
        else:
            if abs(x - self.x) > 1:
                if x > self.x:
                    self.move_dir[0] = 1
                else:
                    self.move_dir[0] = -1
            if abs(y - self.y) > 1:
                if y > self.y:
                    self.move_dir[1] = 1
                else:
                    self.move_dir[1] = -1

    def update(self):
        self.frame_count += 1

        if self.dog_state == DoggyState.WAITING:
            xd = 0
            yd = 0
            if self.frame_count > self.wait_frames:
                self.frame_count = 0
                self.dog_state = DoggyState.IDLE
        else:
            if self.frame_count > self.update_frame_rate:
                self.frame_count = 0

                if self.dog_state == DoggyState.RETRIEVING:
                    if utilities.distance(self.x,self.y,self.target_ball.x,self.target_ball.y) > self.ball_min_distance: # ball got taken away, go fetch it again
                        self.dog_state = DoggyState.FETCHING
                    else:
                        self.target(self.player.x,self.player.y,DoggyState.WAITING)
                else:
                    self.find_ball()

                    if self.target_ball is not None:
                        self.target(self.target_ball.x,self.target_ball.y,DoggyState.RETRIEVING)

                        if self.dog_state == DoggyState.RETRIEVING:
                            self.target_ball.attach(self)

                        #self.get_dir_to_ball()

            xd = self.move_dir[0]*self.speed
            yd = self.move_dir[1]*self.speed

        # general moveable objects collision check (spikes, walls, pits)
        moveable_obj.MoveableObj.update(self,xdelta = xd, ydelta = yd)

class DoggyState(Enum):
    IDLE = 1
    FOLLOWING_PLAYER = 2
    FETCHING = 3
    RETRIEVING = 4
    WAITING = 5