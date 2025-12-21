# ==============================================================================
# DEFINITIONS & TRANSFORMS
# ==============================================================================

# 1. DEFINE VARIABLES AND CLASSES FIRST
# 'default' sets up variables that Ren'Py tracks for saving/loading.
default display_value = 0
default roll_finished = False
default pc = None 

define narrator = Character(None)
define sys = Character("System", color="#ff5555") # The antagonistic force

# Variables to track the current run
default current_outcome = "none"
default chosen_approach = "none"


# ==============================================================================
# PYTHON LOGIC
# ==============================================================================


init python:
    import random
    import time

    class PlayerCharacter:
        def __init__(self, portrait_image):
            # --- 1. IMMUTABLE TAGS ---
            self.race = random.choice(["White", "Black", "South Asian", "Middle Eastern"])
            
            #self.gender = random.choice(["Cis Woman", "Trans Woman", "Non-binary", "Cis Man", "Trans Man"])

            # --- WEIGHTED GENDER LOGIC ---
            # We define the options and the 'weights' (probabilities)
            # Make sure weights sum up to 100 for easy percentage calculation.
            gender_options = ["Cis Woman", "Cis Man", "Non-binary", "Trans Woman", "Trans Man"]
            
            # Example: Trans = 10% each. Cis = 30% each. NB = 20%. 
            # Total: 30+30+20+10+10 = 100%
            gender_weights = [30, 30, 20, 10, 10]
            
            # random.choices returns a list, so we grab the first item [0]
            self.gender = random.choices(gender_options, weights=gender_weights, k=1)[0]
            
            # Skin Tone Logic
            if self.race == "White":
                self.skin_tone = "Light"
            else:
                self.skin_tone = random.choice(["Light-skinned", "Medium-skinned", "Dark-skinned"])
            
            self.origin = random.choice(["Global North", "Global South", "Conflict Zone"])
            
            # --- NEW: DISABILITY ---
            # "Invisible" disabilities might not add immediate friction but affect stamina
            # "Visible" disabilities (Wheelchair, Cane) add friction in inaccessible spaces
            self.disability = random.choice([
                "None", 
                "Mobility (Cane)", 
                "Mobility (Wheelchair)", 
                "Deaf/HoH", 
                "Chronic Pain", 
                "Neurodivergent"
            ])

            # --- 2. MUTABLE METERS ---
            self.economic_capital = random.randint(20, 80)
            self.social_capital = random.randint(20, 80)
            self.mental_resilience = 100 
            self.immigration_status = random.randint(10, 60) 

            # --- 3. SKILLS & LANGUAGES ---
            self.skills = {
                "Legal Literacy": random.choice([True, False]),
                #"Bureaucratic Navigation": random.choice([True, False]),
                "Code Switching": random.choice([True, False]),
            }
            
            # Language Dictionary 
            self.languages = {
                "Mother Tongue": True, # Always known
                "English": random.choice([True, False]),
                "Local Language": random.choice([True, False])
            }

            self.codename = random.choice(["The Traveler", "The Student", "The Professional", "The Artist", "The Parent", "The Exile"])
            # We will use a random color to represent the "Picture" for now
            #self.placeholder_color = random.choice(["#e74c3c", "#3498db", "#f1c40f", "#9b59b6", "#2ecc71"])

            # Pick a random image file name from your images folder
            #self.portrait = random.choice([
            #    "images/portrait1.png",
            #    "images/portrait2.png",
            #    "images/portrait3.png"
            #])
            self.portrait = portrait_image

        def get_profile_friction(self):
            friction = 0
            
            # Standard Bias
            if self.race != "White": friction += 2
            if self.skin_tone == "Dark-skinned": friction += 3
            #if self.visible_religion: friction += 5
            if self.gender in ["Trans Woman", "Non-binary"]: friction += 4
            if self.origin == "Conflict Zone": friction += 5
            
            # Disability Bias (Ableism)
            if self.disability != "None": 
                friction += 3
                
            # Language Barrier Friction
            if not self.languages["Local Language"]:
                friction += 4 # High penalty for not speaking the local language
                
            return friction
    

    def perform_roll(pc, approach_type):
        odds = calculate_outcome_odds(pc, approach_type)

        # Determine the result immediately
        final_roll = random.randint(1, 100)

        final_outcome = None
        
        if final_roll <= odds["good"]:
            final_outcome = "good"
        elif final_roll <= odds["good"] + odds["mixed"]:
            final_outcome = "mixed"
        else:
            final_outcome = "bad"

        # 3. Call the screen and PASS the outcome variable so we can see it
        # We add 'outcome=final_outcome' here
        renpy.call_screen("dice_roll", final_value=final_roll, outcome=final_outcome)
        
        return final_outcome

    # A simple function to calculate odds based on the specific approach and the player's current stats.
    def calculate_outcome_odds(pc, approach_type):
        
        # Base chances (total must equal 100 in the end)
        good = 40
        mixed = 40
        bad = 20
        
        # MODIFIERS based on Player Stats
        if approach_type == "loud":
            # low social capital means loud approaches arent that easy
            if pc.social_capital <= 50:
                bad += 30
                good -= 10
                mixed -= 20
        
        elif approach_type == "quiet":
            # Even quiet things are risky for undocumented folks
            if pc.immigration_status <= 50:
                bad += 10
                mixed += 10
                good -= 20
            # high economic capital means quiet things are easy
            if pc.economic_capital >= 50:
                good += 30
                bad -= 10
                mixed -= 20

        # Normalize to ensure they don't go below 0 or crazy high
        # (This is a simplified normalization for the template)
        total = good + mixed + bad
        return {
            "good": int((good / total) * 100),
            "mixed": int((mixed / total) * 100),
            "bad": int((bad / total) * 100)
        }
        

# 2. THE SCREEN DEFINITION
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





label start:

    scene black
    centered "{b}WELCOME TO THE RESISTANCE{/b}"
    
    jump map

    #jump quest_hub

label quest_hub:
    # Show the player the world map
    scene bg world_map # replace with our world map later

    "Struggles are happening everywhere. Please select a location"

    # The player selects a location from the world map
    menu:
        "Select Quest: Quest 01":
            jump quest_01
        "Select Quest: Quest 02":
            jump quest_02
        "End Game":
            return



label quest_01:
    # First we have to narrate the quest
    "Once upon a time, lorem ipsum dolor sit amet, consectetur adipiscing elit..."

    # Then the player chooses their character
    call character_select

    # Give the player some exposition
    "Some expositional stuff happens. Describe scene here..."

    # Then the player has a choice where they see probabilities of their action
    window hide
    call screen risk_assessment_menu(
        pc,
        prompt="How do you approach the situation?",
        option1_name="Loud", option1_type="loud",
        option2_name="Quiet", option2_type="quiet",
        option3_name="Violent", option3_type="violent"
    )

    # The screen returns the type chosen (e.g., "loud")
    $ chosen_approach = _return

    # Dice Rolling Animation
    #show text "{size=50}CALCULATING RISK...{/size}" at truecenter
    #pause 2.0 # Suspense

    # Calculate result logic
    $ current_outcome = perform_roll(pc, chosen_approach)

    #hide text

    # Outcome & Aftermath
    if current_outcome == "good":
        #"SUCCESS!"
        "The plan worked better than expected. Your stats aligned perfectly with the moment."
    elif current_outcome == "mixed":
        #"PARTIAL SUCCESS."
        "You managed to do it, but at a cost. The system noticed you."
    else:
        #"FAILURE."
        "Disaster. The system pushed back hard."

    # Conditional text based on stats
    if pc.get_profile_friction() > 5:
        "Because your Targeting Level is high, a drone lingers over you specifically, recording your face."

    # Escalation & Second Choice
    "The situation escalates. ........ You have another moment to react"

    menu:
        "Disperse into the crowd immediately.":
            $ final_choice = "flee"
        "Stand your ground and document the abuse.":
            $ final_choice = "document"
        "Call your NGO contact for legal aid.":
            $ final_choice = "legal"

    # Epilogue Reflection
    if final_choice == "flee":
        "You vanished into the night. Safe, but the message was weak."
    elif final_choice == "document":
        "You have footage. It might help later, but you are now on a watchlist."

    #  Final Text & Loop
    "The quest concludes. The struggle continues elsewhere."

    #jump quest_hub
    jump map


label quest_02:
    "Placeholder for Quest 2."
    #jump quest_hub
    jump map

label character_select:
    # ==== TOM's CHARACTER SELECTION CODE ====

    # 1. Define your pool of all possible images
    $ all_portraits = [
        "images/portrait1.png",
        "images/portrait2.png",
        "images/portrait3.png"
    ]
    
    # 2. Pick 3 UNIQUE images from that list. 
    # random.sample picks unique items. It will crash if you ask for 3 but only have 2 images.
    $ selected_portraits = random.sample(all_portraits, 3)

    # 3. Generate the characters, passing the specific images
    # We use selected_portraits[0], [1], and [2]
    $ candidate_1 = PlayerCharacter(selected_portraits[0])
    $ candidate_2 = PlayerCharacter(selected_portraits[1])
    $ candidate_3 = PlayerCharacter(selected_portraits[2])
    
    # 2. Put them in a list
    $ options = [candidate_1, candidate_2, candidate_3]
    
    # 3. Call the screen, passing the list
    # The screen will set the variable 'pc' to the one the user clicks
    call screen character_select(char_candidates=options)

    # 4. The game begins with the selected 'pc'
    # Show the overlay button for stats now that the game has started
    #show screen stats_button_overlay
    
    "You have selected: [pc.codename]."

    return


# ==============================================================================================================
# SCREENS
# ==============================================================================================================



screen stats_button_overlay():
    zorder 100
    frame:
        background None
        align (0.98, 0.02) 
        
        textbutton "STATS":
            # 1. The Magic Line:
            # The button works ONLY if 'pc' exists. Otherwise, it's disabled.
            sensitive (pc is not None)
            
            action Show("char_stats")
            
            # 2. Colors for different states:
            text_color "#ffffff"             # Normal (White)
            text_hover_color "#cccccc"       # Hover (Light Grey)
            text_insensitive_color "#444444" # Disabled/No Character (Dark Grey)


screen character_select(char_candidates):
    modal True
    
    # Background
    add "#000000"

    vbox:
        align (0.5, 0.5)
        spacing 30
        
        label "SELECT YOUR PROFILE" xalign 0.5 text_size 60 text_bold True

        hbox:
            align (0.5, 0.5)
            spacing 40
            
            for char in char_candidates:
                
                button:
                    # Size of the "Card"
                    xsize 400
                    ysize 750
                    background "#222"
                    hover_background "#333"
                    
                    # FIXED: Padding belongs to the button, not the vbox
                    padding (20, 20) 
                    
                    # ACTION: Select character and return
                    action [SetVariable("pc", char), Return()]
                    
                    vbox:
                        # Removed 'padding' from here
                        spacing 10
                        
                        # 1. CODENAME & IMAGE
                        text "[char.codename]" xalign 0.5 size 30 bold True color "#fff"
                        
                        #add Solid(char.placeholder_color) size (360, 200) xalign 0.5
                        add char.portrait size (360, 200) xalign 0.5

                        null height 20
                        
                        # 2. IMMUTABLE STATS
                        label "Background" text_size 24 text_color "#aaa"
                        text "Origin: [char.origin]" size 18
                        text "Race: [char.race]" size 18
                        text "Gender: [char.gender]" size 18
                        
                        if char.disability != "None":
                            text "Disability: [char.disability]" size 18 color "#ffaa00"
                        else:
                            text "Disability: None" size 18 color "#666"

                        null height 10

                        # 3. SKILLS & LANGUAGE
                        label "Known Skills" text_size 24 text_color "#aaa"
                        
                        # Languages
                        hbox:
                            spacing 10
                            if char.languages["English"]:
                                text "ENG" color "#8f8" size 20 bold True
                            else:
                                text "ENG" color "#444" size 20
                            
                            if char.languages["Local Language"]:
                                text "LOC" color "#8f8" size 20 bold True
                            else:
                                text "LOC" color "#444" size 20
                        
                        # Skills
                        vbox:
                            for skill, has_skill in char.skills.items():
                                if has_skill:
                                    text "• [skill]" size 16 color "#ddd"
                        
                        null height 20
                        
                        # 4. MYSTERY WARNING
                        #text "<i>Resources & Status unknown...</i>" xalign 0.5 color "#555" size 16


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