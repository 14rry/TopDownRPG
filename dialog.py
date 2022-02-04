# -*- coding: utf-8 -*-

def invoke(index,posX,posY):
    if index == [1,1]:
        if [posX,posY] == [14,18]:
            return ["They were relentless.",
                    "I mashed Z for dear life but it wasn't enough...",
                    "Maybe you'll have better luck."]
        elif [posX,posY] == [2,4]:
            return ["Go talk to the guy in the room.", 
                    "He's seem some stuff."]

    return ["Error: missing dialog"]