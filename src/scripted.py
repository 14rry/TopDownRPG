import pyxel
import ai
import tile_lookup

# trigger functions
def add_ground(ground_tile,tm_positions):
    for val in tm_positions:
        pyxel.tilemap(0).pset(val[0],val[1],ground_tile)

class Scripted:
    def __init__(self,levels):
        # types of scripted events
        # eliminate all enemies in level
        self.eliminate_levels = [
            ScriptedLevel([[9,7]],add_ground,[tile_lookup.bridge,[[152,120],[153,120],[154,120],[155,120],[156,120]]]),
            ScriptedLevel([[10, 7], [10, 8], [11, 7], [11, 8]],add_ground,[tile_lookup.dirt,[[160,139],[160,140]]])
            ]
        self.levels = levels

    def update(self):
        for level in self.eliminate_levels:
            if level.triggered: # no need to check levels that have already triggered the event
                continue

            if self.levels.level_index in level.level_index: # current level matches one of the special event levels
                # check if all baddies have been eliminated
                # TODO: exclude good ai like dogs
                num_alive = 0
                for val in self.levels.level_objs:
                    if isinstance(val,ai.Ai):
                        if val.alive:
                            num_alive += 1
                            break

                if num_alive == 0:
                    level.trigger()

class ScriptedLevel:
    def __init__(self,level_index,trigger_fun,trigger_args):
        self.triggered = False
        self.level_index = level_index
        self.trigger_fun = trigger_fun
        self.trigger_args = trigger_args

    def trigger(self):
        if self.triggered:
            return

        self.trigger_fun(*self.trigger_args)

        self.triggered = True

    


