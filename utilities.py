import pyxel

def lerp(v0, v1, t):
    return (1 - t) * v0 + t * v1

def box_collision_detect(x1,y1,w1,h1,x2,y2,w2,h2):
        if (x1 < x2 + w2 and
            x1 + w1 > x2 and
            y1 < y2 + h2 and
            h1 + y1 > y2):
            return True
        else:
            return False

def distance(x1,y1,x2,y2):
    return pyxel.sqrt((x1-x2)**2 + (y1-y2)**2)
