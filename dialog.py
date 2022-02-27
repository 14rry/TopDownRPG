# -*- coding: utf-8 -*-
# TODO: turn into lookup table instead of if statepements
def invoke(index,posX,posY):
    print("Dialog input:")
    print(index,posX,posY)
    if index == [0,0]:
        return ["Welcome to the garden."]
    elif index == [1,1]:
        if [posX,posY] == [12,14]:
            return ["They were relentless.",
                    "I mashed Z for dear life but",
                    "it wasn't enough...",
                    "Maybe you'll have better luck."]
        elif [posX,posY] == [2,2]:
            return ["Go talk to the guy in the room.", 
                    "He's seem some stuff."]

    elif index == [2,0]:
        return ["Some call this the Cave", 
                "of Fools.",
                "",
                "I call it home."]

    elif index == [2,1]:
        if [posX,posY] == [1,3]:
            return ["Get out of my offive!"]

    elif index == [3,0]:
        return ["I'm on a boat!",
        "",
        "(He's not on a boat...)"]

    return ["Error: missing dialog"]