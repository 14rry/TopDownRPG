
import particles
import input_handler

def init(camera):
    global particle_effects
    particle_effects = particles.Particles(camera)

    global screen_pause_frames
    screen_pause_frames = 0

    global input
    input = input_handler.InputHandler()
