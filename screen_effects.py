import pyxel
class ScreenEffects:
    def __init__(self):
        self.screen_size = 16
        self.grid_size = 8

        self.clip_percent = 0
        self.fade_rate = 0.03

    def fade_in(self):
        if self.clip_percent > 0.5:
            pyxel.clip()
            self.clip_percent = 0
            return True

        middle = self.screen_size * self.grid_size / 2
        xy = middle - self.clip_percent * self.screen_size * self.grid_size
        wh = self.clip_percent * self.screen_size * self.grid_size * 2
        pyxel.clip(xy, xy, wh, wh)

        self.clip_percent += self.fade_rate

        return False