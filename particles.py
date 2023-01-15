import pyxel
from enum import Enum
import math

class Particles:
    def __init__(self,camera):
        self.active_effects = []
        self.camera = camera

    def add(self,new_effect):
        self.active_effects.append(new_effect)

    def update(self):
        still_alive = []
        for val in self.active_effects:
            num_alive = val.update()

            if num_alive > 0:
                still_alive.append(val)

        self.active_effects = still_alive

    def draw(self,x0):
        for val in self.active_effects:
            val.draw(x0,self.camera.x,self.camera.y)

    def destroy_all(self):
        self.active_effects = []

class ParticleEffect:
    def __init__(self,x,y):
        self.type = ParticleEffectType.RADIAL
        self.x = x
        self.y = y
        self.speed = .1
        self.r = .1
        self.num_pts = 8
        self.lifetime = 600

        self.pts = []

        for i in range(self.num_pts):

            dir = 2*(i/self.num_pts)*math.pi
            xdir = math.cos(dir)
            ydir = math.sin(dir)

            self.pts.append(Particle(
                self.x,
                self.y,
                xdir,
                ydir,
                self.lifetime,
                self.speed
            ))

    def update(self):
        still_alive = []
        for pt in self.pts:
            pt.life -= 1

            if pt.life > 0:

                pt.x += pt.speed*pt.xdir
                pt.y += pt.speed*pt.ydir

                still_alive.append(pt)

        self.pts = still_alive

        return len(self.pts)

    def draw(self,x0,camx,camy):
        for pt in self.pts:
            pyxel.circ(
                pt.x*8-camx+x0,
                pt.y*8-camy,
                2,
                3
                )
                
class Particle:
    def __init__(self,x,y,xdir,ydir,life,speed):
        self.x = x
        self.y = y
        self.xdir = xdir
        self.ydir = ydir
        self.life = life
        self.speed = speed

class ParticleEffectType(Enum):
    RADIAL = 1