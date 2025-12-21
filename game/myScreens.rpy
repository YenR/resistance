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
        

## char stats screen

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
    else:
        vbox:
            align (0.55, 0.5)
            xsize 1000
            ysize 800
            #padding (50, 50)
            
            vbox:
                spacing 20
                
                null height 40
                label "IDENTITY & STATUS" xalign 0.5 text_size 50 #text_font "fonts/BeachmanScript.ttf"
                label "[pc.codename]" xalign 0.5 text_size 80 text_color "#000" text_font "fonts/BeachmanScript.ttf"
                
                #null height 20
                
                hbox:
                    spacing 80 

                    null width 15
                    
                    # --- COLUMN 1: IDENTITY & DISABILITY ---
                    vbox:
                    
                        xsize 400
                        
                        add pc.portrait size (360, 200) #xalign 0.5

                        null height 25

                        #label "Profile" text_size 40 text_color "#000"
                        
                        text "Origin: [pc.origin]" color "#222"
                        text "Ethnicity: [pc.race]" color "#222"
                        text "Skin: [pc.skin_tone]" color "#222"
                        text "Gender: [pc.gender]" color "#222"
                        
                        if pc.disability == "None":
                            text "Disability: None" color "#888"
                        else:
                            text "Disability: [pc.disability]" color "#ffaa00"

                        null height 20
                        
                        $ friction = pc.get_profile_friction()
                        frame:
                            background "#330000"
                            padding (10, 10)
                            text "Systemic Friction: +[friction]" color "#ff6666" size 28


                    # --- COLUMN 2: SKILLS & LANGUAGES ---
                    vbox:
                        xsize 450
                        #label "Competencies" text_size 40 text_color "#000"
                        
                        label "{size=24}Languages{/size}" text_color "#333"
                        for lang, known in pc.languages.items():
                            if known:
                                text "✓ [lang]" color "#0d830d"
                            else:
                                text "✘ [lang]" color "#555" 
                        
                        null height 15
                        
                        label "{size=24}Skills{/size}" text_color "#333"
                        for skill, has_skill in pc.skills.items():
                            if has_skill:
                                text "• [skill]" color "#0d830d"
                            else:
                                text "• [skill]" color "#444"


                        null height 15

                        #label "Resources" text_size 30 text_color "#000"

                        vbox:
                            text "Economic Capital ([pc.economic_capital]%)" size 20 color "#333"
                            bar:
                                value pc.economic_capital 
                                range 100 
                                ysize 20
                                xsize 300 
                                right_bar Solid("#333333")
                                left_bar Solid("#f1c40f")

                        vbox:
                            text "Social Network ([pc.social_capital]%)" size 20 color "#333"
                            bar:
                                value pc.social_capital 
                                range 100 
                                ysize 20
                                xsize 300 
                                right_bar Solid("#333333")
                                left_bar Solid("#3498db")

                        vbox:
                            text "Immigration Security ([pc.immigration_status]%)" size 20 color "#333"
                            bar:
                                value pc.immigration_status 
                                range 100 
                                ysize 20
                                xsize 300 
                                right_bar Solid("#333333")
                                left_bar Solid("#2ecc71")
                
                null height 10
                
                textbutton "Close":
                    xalign 0.5
                    action Hide("char_stats") # Hide instead of Return bc we called it using show()
                    padding (50, 20)
                    text_size 30
                    background "#444"
