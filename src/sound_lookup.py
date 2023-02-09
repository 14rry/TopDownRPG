import pyxel

# sound lookup
sfx_ch = 3
player_attack = 63
player_attack_hit_wall = 62
player_attack_hit_obj = 61
player_attack_hit_ai = 55 # TODO
player_dash = 60
player_footstep = 58
coin = 62
fall_in_pit = 59
ai_destroy = 57
player_take_damage = 56

footstep_freq = 4 # play new footstep every 4 frames while walking

note_lookup = ['C2','E-2','F2','F#2','G2','B-2']
#note_lookup = ['C3','E-4','F4','F#4','G4','B-4']

sfx_queue = []
sfx_cooldown = 0
sfx_max_cooldown = 10

def update():
    if len(sfx_queue) > 0:
        pyxel.play(sfx_ch,sfx_queue.pop())


