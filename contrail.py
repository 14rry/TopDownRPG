import pyxel
import utilities

class Contrail():
    def __init__(self,target,camera):
        self.target = target
        self.camera = camera
        self.trail = []
        self.ages = []
        self.lifetime_frames = 120

        #self.color = 5
        self.color = [1,2,3]

        self.intersect_dist = .1
        self.intersect_points = []

    def clear(self):
        self.trail = []
        self.ages = []

    def update(self):
        new_ages = self.ages
        for idx,val in enumerate(self.ages):
            self.ages[idx] -= 1
            if self.ages[idx] < 0:
                for interidx,pos in enumerate(self.intersect_points):
                    if pos == self.trail[idx]:
                        #self.intersect_points.pop(interidx)
                        self.intersect_points = []
                new_ages.pop(idx)
                self.trail.pop(idx)

        self.ages = new_ages

        self.trail.append([self.target.x,self.target.y])
        self.ages.append(self.lifetime_frames)

        self.find_intersects()

    def draw(self):
        for idx,pos in enumerate(self.trail):
            color_idx = round((self.ages[idx]/self.lifetime_frames) * (len(self.color)-1))
            #pyxel.pset(pos[0]*8+4,pos[1]*8+4,self.color)
            pyxel.circ(
                pos[0]*8+4-self.camera.x,
                pos[1]*8+4-self.camera.y,
                2,self.color[color_idx])

        for pos in self.intersect_points:
            pyxel.circ(
                pos[0]*8+4-self.camera.x,
                pos[1]*8+4-self.camera.y,
                4,12)

    def find_intersects(self):
        #self.intersect_points = []
        val = self.trail[-1]
        for idx2,checkval in enumerate(self.trail):
            if utilities.distance(val[0],val[1],checkval[0],checkval[1]) <= self.intersect_dist:
                self.intersect_points.append(checkval)


