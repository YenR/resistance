# ==============================================================================
# CHARACTER STATS SCREEN
# ==============================================================================

screen char_stats():
    modal True
    tag menu
    #add "#1a1a1aee"
    add "Character_sheet.png"

    # --- SAFETY CHECK: CRASH PROTECTION ---
    if pc is None:
        vbox:
            align (0.5, 0.5)
            spacing 20
            
            text "No Character Selected Yet" color "#000" size 40 xalign 0.5
            text "Please start the a mission and choose a profile first." color "#222" size 20 xalign 0.5
            
            null height 20
            
            textbutton "Close":
                action Hide("char_stats") # Hide instead of Return bc we called it using show()
                xalign 0.5
                padding (40, 15)
                background "#444"

    # --- NORMAL SCREEN (Only runs if pc exists) ---
    # else:
    #     vbox:
    #         align (0.55, 0.5)
    #         xsize 1000
    #         ysize 800
    #         #padding (50, 50)
            
    #         vbox:
    #             spacing 20
                
    #             null height 40
    #             label "IDENTITY & STATUS" xalign 0.5 text_size 50 #text_font "fonts/BeachmanScript.ttf"
    #             label "[pc.codename]" xalign 0.5 text_size 80 text_color "#000" text_font "fonts/BeachmanScript.ttf"
                
    #             #null height 20
                
    #             hbox:
    #                 spacing 80 

    #                 null width 15
                    
    #                 # --- COLUMN 1: IDENTITY & DISABILITY ---
    #                 vbox:
                    
    #                     xsize 400
                        
    #                     add pc.portrait size (360, 200) #xalign 0.5

    #                     null height 25

    #                     #label "Profile" text_size 40 text_color "#000"
                        
    #                     text "Origin: [pc.origin]" color "#222"
    #                     text "Ethnicity: [pc.race]" color "#222"
    #                     text "Skin: [pc.skin_tone]" color "#222"
    #                     text "Gender: [pc.gender]" color "#222"
                        
    #                     if pc.disability == "None":
    #                         text "Disability: None" color "#888"
    #                     else:
    #                         text "Disability: [pc.disability]" color "#ffaa00"

    #                     null height 20
                        
    #                     $ friction = pc.get_profile_friction()
    #                     frame:
    #                         background "#330000"
    #                         padding (10, 10)
    #                         text "Systemic Friction: +[friction]" color "#ff6666" size 28


    #                 # --- COLUMN 2: SKILLS & LANGUAGES ---
    #                 vbox:
    #                     xsize 450
    #                     #label "Competencies" text_size 40 text_color "#000"
                        
    #                     label "{size=24}Languages{/size}" text_color "#333"
    #                     for lang, known in pc.languages.items():
    #                         if known:
    #                             text "✓ [lang]" color "#0d830d"
    #                         else:
    #                             text "✘ [lang]" color "#555" 
                        
    #                     null height 15
                        
    #                     label "{size=24}Skills{/size}" text_color "#333"
    #                     for skill, has_skill in pc.skills.items():
    #                         if has_skill:
    #                             text "• [skill]" color "#0d830d"
    #                         else:
    #                             text "• [skill]" color "#444"


    #                     null height 15

    #                     #label "Resources" text_size 30 text_color "#000"

    #                     vbox:
    #                         text "Economic Capital ([pc.economic_capital]%)" size 20 color "#333"
    #                         bar:
    #                             value pc.economic_capital 
    #                             range 100 
    #                             ysize 20
    #                             xsize 300 
    #                             right_bar Solid("#333333")
    #                             left_bar Solid("#f1c40f")

    #                     vbox:
    #                         text "Social Network ([pc.social_capital]%)" size 20 color "#333"
    #                         bar:
    #                             value pc.social_capital 
    #                             range 100 
    #                             ysize 20
    #                             xsize 300 
    #                             right_bar Solid("#333333")
    #                             left_bar Solid("#3498db")

    #                     vbox:
    #                         text "Immigration Security ([pc.immigration_status]%)" size 20 color "#333"
    #                         bar:
    #                             value pc.immigration_status 
    #                             range 100 
    #                             ysize 20
    #                             xsize 300 
    #                             right_bar Solid("#333333")
    #                             left_bar Solid("#2ecc71")
                
    #             null height 10
                
    #             textbutton "Close":
    #                 xalign 0.5
    #                 action Hide("char_stats") # Hide instead of Return bc we called it using show()
    #                 padding (50, 20)
    #                 text_size 30
    #                 background "#444"
        

    else:
        vbox:
            align (0.6, 0.55)
            xsize 1000
            ysize 800

            vbox:
                spacing 20

                null height 40
                #label "STATUS" xalign 0.5 text_size 50
                label "The [pc.archetype]" xalign 0.45 text_size 100 text_color "#000" text_font "fonts/BeachmanScript.ttf"

                hbox:
                    spacing 80
                    null width 15

                    vbox:
                        xsize 400
                        add pc.portrait size (490, 350)
                        null height 10

                        # text "[pc.codename]" color "#222"
                        # null height 10

                        $ friction = pc.get_profile_friction()
                        # frame:
                        #     background "#330000"
                        #     padding (10, 10)
                        #     text "Systemic Friction: +[friction]" color "#ff6666" size 28

                    vbox:
                        xsize 450

                        label "{size=24}Access{/size}" text_color "#333"
                        text "📄 Papers: [pc.papers]/2" color "#222"
                        text "🗣️ Language: [pc.language]/2" color "#222"
                        text "🏛️ Affiliation: [pc.affiliation]/2" color "#222"
                        text "💰 Savings: [pc.savings]/2" color "#222"

                        null height 15
                        label "{size=24}Strengths{/size}" text_color "#333"
                        for s in pc.strengths:
                            text "• [s]" color "#222"

                null height 10

                textbutton "Close":
                    xalign 0.45
                    action Hide("char_stats")
                    padding (50, 20)
                    text_size 30
                    background "#dab1a7"


# ==============================================================================
# CHOICES PROBABILITY %
# ==============================================================================

screen risk_assessment_menu_2options(pc, prompt, option1, option1tt, option2, option2tt, option3=Null, option3tt=Null):
    modal True
    
    # Calculate odds for display
    #$ odds1 = calculate_outcome_odds(pc, option1_type)
    #$ odds2 = calculate_outcome_odds(pc, option2_type)
    #$ odds3 = calculate_outcome_odds(pc, option3_type)

    frame:
        xalign 0.5
        yalign 0.5
        padding (40, 40)

        vbox:
            spacing 20
            text prompt size 30 xalign 0.5 bold True
            
            # OPTION 1
            button:
                action Return(option1)
                xfill True
                padding (20, 20)
                hbox:
                    text option1
                
                # TOOLTIP LOGIC
                tooltip option1tt
                background "#333" hover_background "#555"

            # OPTION 2
            button:
                action Return(option2)
                xfill True
                padding (20, 20)
                hbox:
                    text option2

                tooltip option2tt
                background "#333" hover_background "#555"

            if option3 != Null:
                button:
                    action Return(option3)
                    xfill True
                    padding (20, 20)
                    hbox:
                        text option3

                    tooltip option3tt
                    background "#333" hover_background "#555"

                
    # THE TOOLTIP DISPLAY AREA
    # This box displays the text defined in the button's "tooltip" property
    # $ tooltip = GetTooltip()
    # if tooltip:
    #     frame:
    #         xalign 0.9
    #         yalign 0.5
    #         xmaximum 300
    #         padding (20, 20)
    #         background "#000000cc"
    #         text "[tooltip]" color "#fff" size 22
        


    $ tooltip = GetTooltip()
    if tooltip:
        frame:
            xpos 0.7
            ypos 0.45
            xmaximum 500
            padding (25, 25)
            background "#000000dd"

            vbox:
                spacing 10
                text "Risk Analysis" size 20 bold True color "#aaa"
                text "[tooltip]" color "#fff" size 20

# ==============================================================================================================
# STATS BUTTON
# ==============================================================================================================

screen stats_button_overlay():
    zorder 100
    frame:
        background None
        align (0.98, 0.02) 
        
        textbutton "STATS":

            sensitive (pc is not None)
            
            action Show("char_stats")
            
            # 2. Colors for different states:
            text_color "#ffffff"             # Normal (White)
            text_hover_color "#cccccc"       # Hover (Light Grey)
            text_insensitive_color "#444444" # Disabled/No Character (Dark Grey)


# ------------------------------------------------------------------
# UI Transforms (reusable)
# ------------------------------------------------------------------

transform bg_fade_in(t=0.25):
    alpha 0.0
    linear t alpha 1.0

transform panel_pop_in(t=0.25, dy=30):
    alpha 0.0
    yoffset dy
    linear t alpha 1.0 yoffset 0

transform card_hover_zoom():
    on idle:
        linear 0.12 zoom 1.0
    on hover:
        linear 0.12 zoom 1.03

# ==============================================================================
# CHARACTER SELECT SCREEN
# ==============================================================================

screen character_select(char_candidates):
    modal True
    add "#000" at bg_fade_in()

    vbox at panel_pop_in():
        align (0.5, 0.5)
        spacing 24

        text "Choose who will resist today." xalign 0.5 size 52 bold True color "#fff"

        hbox:
            align (0.5, 0.5)
            spacing 40

            for char in char_candidates:

                button at card_hover_zoom():
                    xsize 420
                    ysize 460
                    background "#222"
                    hover_background "#333"
                    padding (20, 20)

                    hovered Function(play_random_blip)

                    action [SetVariable("pc", char), Pause(0.08), Return()]

                    vbox:
                        spacing 10

                        text "[char.codename]" xalign 0.5 size 30 bold True color "#fff"
                        add char.portrait size (380, 220) xalign 0.5

                        null height 10

                        text "Strengths" size 22 color "#aaa" bold True
                        for s in char.strengths:
                            text "• [s]" size 18 color "#ddd"

                        # null height 10

                        # text "Gameplay" size 22 color "#aaa" bold True
                        # for g in char.gameplay:
                        #     text "• [g]" size 18 color "#ddd"

                        # text "Stats" size 22 color "#aaa" bold True
                        # text "📄 Papers: [char.papers]/2   🗣️ Language: [char.language]/2" size 18 color "#ddd"
                        # text "🏛️ Affiliation: [char.affiliation]/2   💰 Savings: [char.savings]/2" size 18 color "#ddd"
                        # text "👁️ Visibility: [char.visibility]/100" size 18 color "#ddd"
                        # #text "🫠 Energy: [char.energy]/100   👁️ Visibility: [char.visibility]/100" size 18 color "#ddd"
                        # null height 10
                        # text "Starting condition:" size 18 color "#999"
                        # text "{i}🕯️ [char.starting_condition]{/i}" size 18 color "#bbb"


# ======================================================================
# CHARACTER REVEAL SCREEN (after selection)
# ======================================================================

screen character_reveal(pc):
    modal True
    add "#000"

    frame:
        xalign 0.5
        yalign 0.5
        xsize 500
        background "#222"
        padding (40, 40)

        vbox:
            spacing 18

            text "FILE SUMMARY" xalign 0.5 size 48 bold True color "#fff"
            text "[pc.codename]" xalign 0.5 size 32 bold True color "#fff"

            null height 10
            text "Starting condition:" size 20 color "#999"
            text "{i}🕯️ [pc.starting_condition]{/i}" size 22 color "#bbb"

            null height 20
            text "Stats" size 26 color "#aaa" bold True
            text "📄 Papers: [pc.papers]/2   🗣️ Language: [pc.language]/2" size 22 color "#ddd"
            text "🏛️ Affiliation: [pc.affiliation]/2   💰 Savings: [pc.savings]/2" size 22 color "#ddd"
            #text "👁️ Visibility: [pc.visibility]/100" size 22 color "#ddd"

            null height 28
            textbutton "Continue" xalign 0.5 action Return()


# screen character_select(char_candidates):
#     modal True
    
#     # Background
#     add "#000000"

#     vbox:
#         align (0.5, 0.5)
#         spacing 30
        
#         label "SELECT YOUR PROFILE" xalign 0.5 text_size 60 text_bold True

#         hbox:
#             align (0.5, 0.5)
#             spacing 40
            
#             for char in char_candidates:
                
#                 button:
#                     # Size of the "Card"
#                     xsize 400
#                     ysize 750
#                     background "#222"
#                     hover_background "#333"
                    
#                     padding (20, 20) 
                    
#                     # ACTION: Select character and return
#                     action [SetVariable("pc", char), Return()]
                    
#                     vbox:
#                         spacing 10
                        
#                         # 1. CODENAME & IMAGE
#                         text "[char.codename]" xalign 0.5 size 30 bold True color "#fff"
                        
#                         #add Solid(char.placeholder_color) size (360, 200) xalign 0.5
#                         add char.portrait size (360, 200) xalign 0.5

#                         null height 20
                        
#                         # 2. IMMUTABLE STATS
#                         label "Background" text_size 24 text_color "#aaa"
#                         text "Origin: [char.origin]" size 18
#                         text "Race: [char.race]" size 18
#                         text "Gender: [char.gender]" size 18
                        
#                         if char.disability != "None":
#                             text "Disability: [char.disability]" size 18 color "#ffaa00"
#                         else:
#                             text "Disability: None" size 18 color "#666"

#                         null height 10

#                         # 3. SKILLS & LANGUAGE
#                         label "Known Skills" text_size 24 text_color "#aaa"
                        
#                         # Languages
#                         hbox:
#                             spacing 10
#                             if char.languages["English"]:
#                                 text "ENG" color "#8f8" size 20 bold True
#                             else:
#                                 text "ENG" color "#444" size 20
                            
#                             if char.languages["Local Language"]:
#                                 text "LOC" color "#8f8" size 20 bold True
#                             else:
#                                 text "LOC" color "#444" size 20
                        
#                         # Skills
#                         vbox:
#                             for skill, has_skill in char.skills.items():
#                                 if has_skill:
#                                     text "• [skill]" size 16 color "#ddd"
                        
#                         null height 20
                        
                        # 4. MYSTERY WARNING
                        #text "<i>Resources & Status unknown...</i>" xalign 0.5 color "#555" size 16

# ==============================================================================
# RISK ASSESSMENT MENU / CHOICES PROBABILITY %
# ==============================================================================

screen risk_assessment_menu(pc, prompt, option1_name, option1_type, option2_name, option2_type, option3_name, option3_type):
    modal True
    
    # Calculate odds for display
    $ odds1 = calculate_outcome_odds(pc, option1_type)
    $ odds2 = calculate_outcome_odds(pc, option2_type)
    $ odds3 = calculate_outcome_odds(pc, option3_type)

    frame:
        xalign 0.5
        yalign 0.5
        padding (40, 40)
        vbox:
            spacing 20
            text prompt size 30 xalign 0.5 bold True
            
            # OPTION 1
            button:
                action Return(option1_type)
                xfill True
                padding (20, 20)
                hbox:
                    text option1_name
                    # This text only shows on hover (simple version) or always shows.
                    # Let's show a "Risk" label.
                
                # TOOLTIP LOGIC
                tooltip "PROJECTIONS:\nSuccess: {}%\nComplication: {}%\nFailure: {}%".format(odds1['good'], odds1['mixed'], odds1['bad'])
                background "#333" hover_background "#555"

            # OPTION 2
            button:
                action Return(option2_type)
                xfill True
                padding (20, 20)
                text option2_name
                tooltip "PROJECTIONS:\nSuccess: {}%\nComplication: {}%\nFailure: {}%".format(odds2['good'], odds2['mixed'], odds2['bad'])
                background "#333" hover_background "#555"

            # OPTION 3
            button:
                action Return(option3_type)
                xfill True
                padding (20, 20)
                text option3_name
                tooltip "PROJECTIONS:\nSuccess: {}%\nComplication: {}%\nFailure: {}%".format(odds3['good'], odds3['mixed'], odds3['bad'])
                background "#333" hover_background "#555"
                
    # THE TOOLTIP DISPLAY AREA
    # This box displays the text defined in the button's "tooltip" property
    $ tooltip = GetTooltip()
    if tooltip:
        frame:
            xalign 0.9
            yalign 0.5
            xmaximum 300
            padding (20, 20)
            background "#000000cc"
            text "[tooltip]" color "#fff" size 22
        
# ==============================================================================
# DICE ROLL SCREEN
# ==============================================================================

screen dice_roll(final_value, outcome): 
    modal True
    zorder 100
    
    # Screen variables to track the animation state
    default rolls_left = 20
    default current_display = 0
    default is_finished = False

    frame:
        align (0.5, 0.5)
        padding (60, 60) # Increased padding slightly for looks
        background "#000000cc"
        
        vbox:
            spacing 20
            xalign 0.5
            
            text "Rolling..." xalign 0.5 size 40
            
            # Show the flickering number OR the final result
            text "[current_display]" size 100 color "#fff" xalign 0.5

            if is_finished:
                # Display the Outcome Text based on the result passed from python
                if outcome == "good":
                    text "SUCCESS" color "#00ff00" xalign 0.5 size 60 bold True
                elif outcome == "mixed":
                    text "COMPLICATION" color "#ffaa00" xalign 0.5 size 60 bold True
                else:
                    text "FAILURE" color "#ff0000" xalign 0.5 size 60 bold True
                
                null height 20

                # Returns True (success) or False (fail) to the game script
                textbutton "Continue":
                    xalign 0.5
                    padding (40, 15)
                    background "#444"
                    hover_background "#666"
                    text_size 30
                    action Return(True)

    # THE ANIMATION LOGIC
    if not is_finished:
        timer 0.05 repeat True action If(
            rolls_left > 0, 
            # If still rolling:
            [SetScreenVariable("rolls_left", rolls_left - 1), SetScreenVariable("current_display", renpy.random.randint(1, 99))],
            # If done rolling:
            [SetScreenVariable("is_finished", True), SetScreenVariable("current_display", final_value)]
        )

# ==============================================================================
#  SCREEN QUEST SUMMARY 
# ==============================================================================

screen quest_summary(title="Quest Complete", body=""):
    modal True

    frame:
        xalign 0.5
        yalign 0.5
        padding (30, 25)

        vbox:
            spacing 12

            text title size 40
            if body:
                text body

            null height 10

            text "Seeds of change planted: [seeds_of_change] ([signed(seeds_of_change - quest_start_seeds)])"
            #text "Suspicion 👁️: [suspicion] ([signed(suspicion - quest_start_suspicion)])"
            #text "Storyteller Influence 📻: [storyteller_influence] ([signed(storyteller_influence - quest_start_influence)])"

            null height 18

            if quest_failed:
                textbutton "Main Menu 🏠" action MainMenu(confirm=False)
            else:
                textbutton "Back to map 🗺️" action Return()

# ------------------------------------------------------------------
# PC Badge (Map HUD)
# ------------------------------------------------------------------

screen pc_badge():
    if pc:

        frame:
            xalign 0.98   # right side
            yalign 0.05   # top-ish
            background "#222c"
            padding (14, 14)

            vbox:
                spacing 8

                text "[pc.codename]" size 26 bold True color "#fff"

                add pc.portrait size (240, 140)
                text "Seeds of change: [seeds_of_change]" size 18 color "#ddd"
                # text "📄 [pc.papers]/2   🗣 [pc.language]/2" size 18 color "#ddd"
                # text "🏛 [pc.affiliation]/2   💰 [pc.savings]/2" size 18 color "#ddd"
                #text "👁 [pc.visibility]/100" size 18 color "#ddd"

                # if pc.starting_condition:
                #     text "{i}🕯️ [pc.starting_condition]{/i}" size 16 color "#bbb"
