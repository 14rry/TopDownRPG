import pyxel

class InputHandler:
    def __init__(self):
        self.up = pyxel.KEY_I
        self.down = pyxel.KEY_K
        self.left = pyxel.KEY_J
        self.right = pyxel.KEY_L

        self.up2 = pyxel.KEY_RIGHT
        self.down2 = pyxel.KEY_DOWN
        self.left2 = pyxel.KEY_LEFT
        self.right2 = pyxel.KEY_RIGHT

        self.key_map = {
            'up':[pyxel.KEY_I,pyxel.KEY_UP],
            'down':[pyxel.KEY_K,pyxel.KEY_DOWN],
            'left':[pyxel.KEY_J,pyxel.KEY_LEFT],
            'right':[pyxel.KEY_L,pyxel.KEY_RIGHT]
        }

    def is_pressed(self,key_val):
        if key_val not in self.key_map:
            print('Input Handler Error: undefined key')
            return False
        
        return any([pyxel.btn(key) for key in self.key_map[key_val]]) 
