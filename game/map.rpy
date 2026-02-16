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

    play music "audio/HoliznaCC0-DustyAttic.mp3" volume 0.4 fadein 1.5

    window hide
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
        #sensitive (not quest_attempted["storyteller"])
        focus_mask True
        idle "Map_area1_idle.png"
        hovered Function(play_random_blip)
        #action Jump("quest_storyteller_briefing")
        #action Jump(QUESTS["storyteller"]["label"])
        #action [Hide("mapScreen"), Call(QUESTS["storyteller"]["label"])]
        if quest_attempted.get("storyteller", False):
            action Notify(quest_summaries.get("storyteller", "Storyteller quest completed."))
        else:
            hover "Map_area1.png"
            action Return(QUESTS["storyteller"]["label"])

    #Quest2
    imagebutton:
        #sensitive (not quest_attempted["journalist"])
        focus_mask True
        idle "Map_area2_idle.png"
        hovered Function(play_random_blip)
        #action Jump("quest_journalist_briefing")
        #action Jump(QUESTS["journalist"]["label"])
        #action [Hide("mapScreen"), Call(QUESTS["journalist"]["label"])]
        if quest_attempted.get("journalist", False):
            action Notify(quest_summaries.get("journalist", "Journalist quest completed."))
        else:
            hover "Map_area2.png"
            action Return(QUESTS["journalist"]["label"])
        


    #Quest3
    imagebutton:
        #sensitive (not quest_attempted["artist"])
        focus_mask True
        idle "map_area3_idle.png"
        hovered Function(play_random_blip)
        #action Jump("quest_artresist_briefing")
        #action Jump(QUESTS["artist"]["label"])
        #action [Hide("mapScreen"), Call(QUESTS["artist"]["label"])]
        if quest_attempted.get("artist", False):
            action Notify(quest_summaries.get("artist", "Artist quest completed."))
        else:
            hover "Map_area3.png"
            action Return(QUESTS["artist"]["label"])

    use pc_badge
