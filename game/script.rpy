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
            # Example traits
            self.background = random.choice(["Law Student", "Journalist", "Laborer"])
            self.identity_markers = ["Muslim", "Woman"] 
            self.base_difficulty = 10 
            
            # Apply background bonuses
            self.law_bonus = 20 if self.background == "Law Student" else 0

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

    "You arrive at the airport. Background: [pc.background]."

    jump airport_encounter

label airport_encounter:
    # Calculate chances based on the specific character created above
    $ chance_comply = 50
    $ chance_rights = 75 + pc.law_bonus 

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


screen char_stats():
    modal True
    tag menu # This creates the "game menu" behavior (replaces Save/Load screens)

    # A dark background to dim the game
    add "#000000aa"

    frame:
        align (0.5, 0.5)
        padding (50, 50)
        xsize 600
        
        vbox:
            spacing 20
            
            label "Character Sheet" xalign 0.5 text_size 40
            
            null height 10 
            
            # FIXED: Using {b} instead of <b>
            text "{b}Background:{/b} [pc.background]" size 24
            
            $ identity_str = ", ".join(pc.identity_markers)
            text "{b}Identity:{/b} [identity_str]" size 24
            
            null height 10
            
            label "Active Modifiers" xalign 0.0 text_size 28
            
            hbox:
                spacing 200 
                vbox:
                    text "Base Difficulty:" color "#aaa"
                    text "Law Bonus:" color "#aaa"
                
                vbox:
                    text "[pc.base_difficulty]" xalign 1.0
                    text "+[pc.law_bonus]" color ("#0f0" if pc.law_bonus > 0 else "#fff") xalign 1.0

            null height 30
            
            # FIXED: 'Return()' exits the menu correctly
            textbutton "Close Stats":
                xalign 0.5
                action Return() 
                padding (20, 10)
                text_size 30