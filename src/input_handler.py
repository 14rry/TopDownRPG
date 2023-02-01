import pyxel

class InputHandler:
    def __init__(self):
        

        self.key_map = {
            'up':[pyxel.KEY_I,pyxel.KEY_UP,pyxel.GAMEPAD1_BUTTON_DPAD_UP],
            'down':[pyxel.KEY_K,pyxel.KEY_DOWN,pyxel.GAMEPAD1_BUTTON_DPAD_DOWN],
            'left':[pyxel.KEY_J,pyxel.KEY_LEFT,pyxel.GAMEPAD1_BUTTON_DPAD_LEFT,pyxel.GAMEPAD1_AXIS_LEFTX],
            'right':[pyxel.KEY_L,pyxel.KEY_RIGHT,pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT],
            'attach':[pyxel.KEY_Z,pyxel.GAMEPAD1_BUTTON_A],
            'attack':[pyxel.KEY_X,pyxel.GAMEPAD1_BUTTON_B],
            'sprint':[pyxel.KEY_C,pyxel.GAMEPAD1_BUTTON_X]
        }

    def is_pressed(self,key_val):
        if key_val not in self.key_map:
            print('Input Handler Error: undefined key')
            return False
        
        return any([pyxel.btn(key) for key in self.key_map[key_val]])

    def btnp(self,key_val):
        if key_val not in self.key_map:
            print('Input Handler Error: undefined key')
            return False
        
        return any([pyxel.btnp(key) for key in self.key_map[key_val]])
