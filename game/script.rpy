# 1. DEFINE VARIABLES AND CLASSES FIRST
# 'default' sets up variables that Ren'Py tracks for saving/loading.
default display_value = 0
default roll_finished = False
default pc = None 

init python:
    import random
    import time

    class PlayerCharacter:
        def __init__(self):
            # --- 1. IMMUTABLE TAGS ---
            self.race = random.choice(["White", "Black", "South Asian", "Middle Eastern"])
            self.gender = random.choice(["Cis Woman", "Trans Woman", "Non-binary", "Cis Man", "Trans Man"])
            
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
                "Bureaucratic Navigation": random.choice([True, False]),
                "Code Switching": random.choice([True, False]),
            }
            
            # NEW: Language Dictionary (Name: Is_Known)
            self.languages = {
                "Mother Tongue": True, # Always known
                "English": random.choice([True, False]),
                "Local Language": random.choice([True, False])
            }

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
    

    def perform_roll(target_percent):
        # 1. Calculate the Target Score (same math as before)
        # 75% chance = need to roll 6 or higher on d20
        target_score = 21 - (target_percent / 5)
        
        # 2. Determine the result immediately
        final_roll = random.randint(1, 20)
        
        # 3. Call the screen and WAIT for the player to click "Continue"
        # The screen will return True or False based on the result
        result = renpy.call_screen("dice_roll", target=target_score, final_value=final_roll)
        
        return result

# 2. THE SCREEN DEFINITION
screen dice_roll(target, final_value):
    modal True
    zorder 100
    
    # Screen variables to track the animation state
    default rolls_left = 20  # How many times the number flickers
    default current_display = 0
    default is_finished = False

    frame:
        align (0.5, 0.5)
        padding (40, 40)
        background "#000000cc"
        
        vbox:
            spacing 20
            xalign 0.5
            
            text "Rolling..." xalign 0.5 size 40
            
            # Show the flickering number OR the final result
            text "[current_display]" size 100 color "#fff" xalign 0.5

            if is_finished:
                if final_value >= target:
                    text "SUCCESS" color "#0f0" xalign 0.5 size 50 bold True
                else:
                    text "FAILURE" color "#f00" xalign 0.5 size 50 bold True
                
                # Returns True (success) or False (fail) to the game script
                textbutton "Continue":
                    xalign 0.5
                    action Return(final_value >= target)

    # THE ANIMATION LOGIC
    # This timer runs only while the animation isn't finished
    if not is_finished:
        timer 0.05 repeat True action If(
            rolls_left > 0, 
            # If still rolling: decrease counter and pick random number
            [SetScreenVariable("rolls_left", rolls_left - 1), SetScreenVariable("current_display", renpy.random.randint(1, 20))],
            # If done rolling: set flag and show final number
            [SetScreenVariable("is_finished", True), SetScreenVariable("current_display", final_value)]
        )







# 3. THE GAME START
label start:
    
    # Initialize the character object here
    $ pc = PlayerCharacter()

    "You arrive at the airport. "

    jump airport_encounter

label airport_encounter:
    # Calculate chances based on the specific character created above
    $ chance_comply = 50
    $ chance_rights = 75 

    "Security stops you."

    menu:
        "Comply ([chance_comply]\% success)":
            # Note: We call perform_roll, not roll_dice
            $ success = perform_roll(chance_comply)
            
            if success:
                jump comply_success
            else:
                jump comply_fail

        "State your rights ([chance_rights]\% success)":
            $ success = perform_roll(chance_rights)
            
            if success:
                jump rights_success
            else:
                jump rights_fail

# 4. RESOLUTION LABELS
label comply_success:
    "You comply. They verify your documents and let you through."
    return

label comply_fail:
    "You comply, but they decide to detain you anyway."
    return

label rights_success:
    "You quote the relevant statutes. They back off."
    return

label rights_fail:
    "They don't care about your rights. Things escalate."
    return





## char stats screen

screen char_stats():
    modal True
    tag menu
    add "#1a1a1aee"

    frame:
        align (0.5, 0.5)
        xsize 1400
        ysize 1000
        padding (50, 50)
        
        vbox:
            spacing 20
            
            label "IDENTITY & STATUS" xalign 0.5 text_size 50
            
            null height 20
            
            hbox:
                spacing 80 # More space between columns
                
                # --- COLUMN 1: IDENTITY & DISABILITY ---
                vbox:
                    xsize 350
                    label "Profile" text_size 35 text_color "#aaa"
                    
                    text "Origin: [pc.origin]"
                    text "Race: [pc.race]"
                    text "Skin: [pc.skin_tone]"
                    text "Gender: [pc.gender]"
                    
                    # Disability Display
                    if pc.disability == "None":
                        text "Disability: None" color "#888"
                    else:
                        text "Disability: [pc.disability]" color "#ffaa00"

                    #if pc.visible_religion:
                    #    text "Vis. Religion: Yes" color "#ffaa00"
                    #else:
                    #    text "Vis. Religion: No"
                        
                    null height 20
                    
                    # Friction Score moved here for visibility
                    $ friction = pc.get_profile_friction()
                    frame:
                        background "#330000"
                        padding (10, 10)
                        text "Systemic Friction: +[friction]" color "#ff6666" size 28


                # --- COLUMN 2: SKILLS & LANGUAGES ---
                vbox:
                    xsize 300
                    label "Competencies" text_size 35 text_color "#aaa"
                    
                    # Language Section
                    label "{size=24}Languages{/size}" text_color "#ddd"
                    for lang, known in pc.languages.items():
                        if known:
                            text "✓ [lang]" color "#88ff88"
                        else:
                            text "✘ [lang]" color "#555" # Greyed out X
                    
                    null height 15
                    
                    # Skills Section
                    label "{size=24}Skills{/size}" text_color "#ddd"
                    for skill, has_skill in pc.skills.items():
                        if has_skill:
                            text "• [skill]" color "#88ff88"
                        else:
                            text "• [skill]" color "#444"


                # --- COLUMN 3: RESOURCES (BARS) ---
                vbox:
                    xsize 400
                    spacing 15
                    label "Resources" text_size 35 text_color "#aaa"

                    vbox:
                        text "Economic Capital ([pc.economic_capital]%)" size 22
                        bar:
                            value pc.economic_capital 
                            range 100 
                            ysize 25 
                            right_bar Solid("#333333")
                            left_bar Solid("#f1c40f")

                    vbox:
                        text "Social Network ([pc.social_capital]%)" size 22
                        bar:
                            value pc.social_capital 
                            range 100 
                            ysize 25 
                            right_bar Solid("#333333")
                            left_bar Solid("#3498db")

                    vbox:
                        text "Immigration Security ([pc.immigration_status]%)" size 22
                        bar:
                            value pc.immigration_status 
                            range 100 
                            ysize 25 
                            right_bar Solid("#333333")
                            left_bar Solid("#2ecc71")

                    vbox:
                        text "Mental Resilience ([pc.mental_resilience]%)" size 22
                        bar:
                            value pc.mental_resilience 
                            range 100 
                            ysize 25 
                            right_bar Solid("#333333")
                            left_bar Solid("#e74c3c")
            
            null height 30
            
            textbutton "Close":
                xalign 0.5
                action Return()
                padding (50, 20)
                text_size 30
                background "#444"