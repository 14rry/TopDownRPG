import pyxel

class Contrail():
    def __init__(self,target):
        self.target = target
        self.trail = []
        self.ages = []
        self.lifetime_frames = 120

        #self.color = 5
        self.color = [1,2,3]

    def update(self):
        new_ages = self.ages
        for idx,val in enumerate(self.ages):
            self.ages[idx] -= 1
            if self.ages[idx] < 0:
                new_ages.pop(idx)
                self.trail.pop(idx)

        self.ages = new_ages

        self.trail.append([self.target.x,self.target.y])
        self.ages.append(self.lifetime_frames)

    def draw(self):
        for idx,pos in enumerate(self.trail):
            color_idx = round((self.ages[idx]/self.lifetime_frames) * (len(self.color)-1))
            #pyxel.pset(pos[0]*8+4,pos[1]*8+4,self.color)
            pyxel.circ(pos[0]*8+4,pos[1]*8+4,2,self.color[color_idx])


