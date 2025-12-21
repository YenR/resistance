label myScreens:

screen mapScreen:
    add "Map_.png"

    #Room1
    imagebutton:
        focus_mask True
        idle "Map_area1_idle.png"
        hover "Map_area1.png"
        action Jump("quest_01")

    #Room2
    imagebutton:
        focus_mask True
        idle "Map_area2_idle.png"
        hover "Map_area2.png"
        action Jump("quest_02")

        

    #Room3
    #imagebutton:
    #    if wing_strength >= 2:
    #        focus_mask True
    #        idle "map room 3 idle.png"
    #        hover "map room 3 hover.png"
    #        action Jump("room3")
    #    else:
    #        idle "map room empty.png"
    #        hover "map room empty.png"
        
