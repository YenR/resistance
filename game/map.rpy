# label map:
#     #screen black
#     scene black 
#     with fade

#     call screen mapScreen

#     $ chosen_label = _return

#     if chosen_label:
#         $ renpy.notify("Selected: " + str(chosen_label))
#         call expression chosen_label

#     jump map


label map:

    # ✅ If all quests attempted, end the run
    if all(quest_attempted.get(k, False) for k in QUESTS.keys()):
        jump run_end

    scene black
    with fade

    call screen mapScreen

    $ chosen_label = _return

    if chosen_label:
        $ chosen_key = None
        python:
            for k, v in QUESTS.items():
                if v["label"] == chosen_label:
                    chosen_key = k
                    break

        if chosen_key and quest_attempted.get(chosen_key, False):
            $ renpy.notify("Not again. Not in this run. 🕯️")
        else:
            if chosen_key:
                $ quest_attempted[chosen_key] = True

            call expression chosen_label

            # ✅ After finishing a quest, check again
            if all(quest_attempted.get(k, False) for k in QUESTS.keys()):
                jump run_end

    jump map



# ==============================================================================
# MAP SCREEN
# ==============================================================================


screen mapScreen:
    add "Map_3.png"

    #Quest1
    imagebutton:
        sensitive (not quest_attempted["storyteller"])
        focus_mask True
        idle "Map_area1_idle.png"
        hover "Map_area1.png"
        #action Jump("quest_storyteller_briefing")
        #action Jump(QUESTS["storyteller"]["label"])
        #action [Hide("mapScreen"), Call(QUESTS["storyteller"]["label"])]
        action Return(QUESTS["storyteller"]["label"])

    #Quest2
    imagebutton:
        sensitive (not quest_attempted["journalist"])
        focus_mask True
        idle "Map_area2_idle.png"
        hover "Map_area2.png"
        #action Jump("quest_journalist_briefing")
        #action Jump(QUESTS["journalist"]["label"])
        #action [Hide("mapScreen"), Call(QUESTS["journalist"]["label"])]
        action Return(QUESTS["journalist"]["label"])
        


    #Quest3
    imagebutton:
        sensitive (not quest_attempted["artist"])
        focus_mask True
        idle "map_area3_idle.png"
        hover "map_area3.png"
        #action Jump("quest_artresist_briefing")
        #action Jump(QUESTS["artist"]["label"])
        #action [Hide("mapScreen"), Call(QUESTS["artist"]["label"])]
        action Return(QUESTS["artist"]["label"])

    use pc_badge
