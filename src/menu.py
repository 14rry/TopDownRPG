from enum import Enum
import pyxel
import sound_lookup
import config

class MenuState(Enum):
    CLOSED = 0
    SETTINGS = 1

menu_state = MenuState.CLOSED
settings_menu_text = ['Settings','Music','SFX']

padding = 12
col1 = 3
col2 = 11

cursor_pos = 0
max_cursor_pos = 0

def update():
    if config.input.btnp('menu'):
        global menu_state
        if menu_state == MenuState.SETTINGS:
            menu_state = MenuState.CLOSED
        else:
            menu_state = MenuState.SETTINGS

    if menu_state != MenuState.CLOSED:
        global cursor_pos
        dir = config.input.get_directional_input_btnp()

        if dir[1] == 1:
            cursor_pos = min(cursor_pos+1,max_cursor_pos)
            print(cursor_pos,max_cursor_pos)
        elif dir[1] == -1:
            cursor_pos = max(cursor_pos-1,0)

        update_menu_x(dir[0],cursor_pos)

def update_menu_x(dir,cursor_pos):
    if dir == 0:
        return

    if menu_state == MenuState.SETTINGS:
        current_str = settings_menu_text[cursor_pos+1]

        if current_str == 'Music':
            sound_lookup.set_music_volume(sound_lookup.music_volume+dir)
        elif current_str == 'SFX':
            sound_lookup.set_sfx_volume(sound_lookup.sfx_volume+dir)



def draw():
    if menu_state == MenuState.SETTINGS:
        pyxel.rect(10,10,100,100,col1)
        draw_menu_text(settings_menu_text,cursor_pos)

def draw_menu_text(txt_str,cursor_pos):

    global max_cursor_pos
    max_cursor_pos = len(txt_str)-2

    x = padding
    y = padding
    for val in txt_str:

        if y//padding == cursor_pos + 2:
            pyxel.text(x-padding/2,y,'>',col2)

        if menu_state == MenuState.SETTINGS and x > padding:
            val = append_sound_levels(val)

        pyxel.text(x,y,val,col2)

        if x == padding:
            x += padding

        y += padding

def append_sound_levels(current_str):
    if current_str == 'Music':
        current_str += " "
        volume = sound_lookup.music_volume
    elif current_str == 'SFX':
        current_str += "   "
        volume = sound_lookup.sfx_volume
    else:
        raise ValueError('Menu str doesnt music or sfx.')


    for i in range(7):
        if i < volume:
            current_str += "+"
        else:
            current_str += "-"

    return current_str






