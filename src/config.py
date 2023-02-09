
import particles

def init(camera):
    global particle_effects
    particle_effects = particles.Particles(camera)

    global screen_pause_frames
    screen_pause_frames = 0
