import pyxel

class Swarm():
    def __init__(self,screen_size):

        self.frame_skips = 0 # num frames to skip between updates.. controls movement speed
        self.frame_count = 0

        self.num = 200
        self.max_pos = screen_size*8 - 1
        self.positions = []
        self.bests = []
        self.overall_best = [0,0]
        self.velocities = []

        self.max_vel = 4

        self.w = .5 # weight
        self.sg = 3 # social coefficient
        self.sp = 1 # cognitive coefficient

        self.color = 3
        self.colors = []
        self.target_color = 10

        x = pyxel.rndi(0,self.max_pos)
        y = pyxel.rndi(0,self.max_pos)
        self.desired_pos = [x,y]

        self.initialize_particles()

    def initialize_particles(self):
        self.positions = []
        self.bests = []
        self.colors = []
        self.velocities = []

        for i in range(self.num):
            self.colors.append(pyxel.rndi(0,15))

            x = pyxel.rndi(0,self.max_pos)
            y = pyxel.rndi(0,self.max_pos)

            self.positions.append([x,y])
            self.bests.append([x,y])

            # update best position
            if i == 0:
                self.overall_best = [x,y]
            else:
                if self.cost([x,y]) < self.cost(self.overall_best):
                    self.overall_best = [x,y]

            # initialize velocity
            #vi ~ U(-|bup-blo|, |bup-blo|)
            vx = pyxel.rndf(-self.max_vel,self.max_vel)
            vy = pyxel.rndf(-self.max_vel,self.max_vel)
            self.velocities.append([vx,vy])

    def draw(self):
        for idx,val in enumerate(self.positions):
            pyxel.pset(val[0],val[1],self.colors[idx])

        pyxel.pset(self.desired_pos[0],self.desired_pos[1],self.target_color)

    def cost(self,pos):
        return pyxel.sqrt((pos[0]-self.desired_pos[0])**2 + (pos[1]-self.desired_pos[1])**2)

    def new_pos(self,pos):
        self.desired_pos = pos
        # update overall and individual best positions
        for i,pos in enumerate(self.positions):
            self.bests[i] = pos
            # update best position
            if i == 0:
                self.overall_best = pos
            else:
                if self.cost(pos) < self.cost(self.overall_best):
                    self.overall_best = pos

    def update(self):
        # TODO: add termination condition
        self.frame_count += 1

        #print(self.desired_pos,self.overall_best,self.cost(self.overall_best))

        if self.frame_count > self.frame_skips:
            self.frame_count = 0

            for idx,pos in enumerate(self.positions):

                # update velocities
                rp = pyxel.rndf(0,1)
                rg = pyxel.rndf(0,1)

                vx = self.velocities[idx][0]
                vy = self.velocities[idx][1]

                vx = self.w * vx + (self.sp*rp*(self.bests[idx][0]-pos[0])) + (self.sg*rg*(self.overall_best[0]-pos[0]))

                rp = pyxel.rndf(0,1)
                rg = pyxel.rndf(0,1)
                vy = self.w * vy + (self.sp*rp*(self.bests[idx][1]-pos[1])) + (self.sg*rg*(self.overall_best[1]-pos[1]))

                self.velocities[idx][0] = min(max(vx,-self.max_vel),self.max_vel)
                self.velocities[idx][1] = min(max(vy,-self.max_vel),self.max_vel)

                # update position
                pos[0] += self.velocities[idx][0]
                pos[1] += self.velocities[idx][1]

                # update best knowns
                if self.cost(pos) < self.cost(self.bests[idx]):
                    self.bests[idx] = pos

                    if self.cost(self.bests[idx]) < self.cost(self.overall_best):
                        self.overall_best = pos

        






