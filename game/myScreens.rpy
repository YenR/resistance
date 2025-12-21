label myScreens:

screen mapScreen:
    add "Map.png"

    #Room1
    imagebutton:
        focus_mask True
        idle "map1-trans.png"
        hover "map1.png"
        action Jump("quest_01")

    #Room2
    imagebutton:
        focus_mask True
        idle "map2-trans.png"
        hover "map2.png"
        action Jump("quest_02")

        
    imagebutton:
        focus_mask True
        idle "map3-trans.png"
        hover "map3.png"
        action Jump("quest_03")

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
        
