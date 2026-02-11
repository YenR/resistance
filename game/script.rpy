# ==============================================================================
# DEFINITIONS & TRANSFORMS
# ==============================================================================

#Q: NOT USED?
#default display_value = 0
#default roll_finished = False

default pc = None 

default run_twists = {}

define narrator = Character(None)
define sys = Character("System", color="#ff5555") # The antagonistic force

# Variables to track the current run
default current_outcome = "none"
default chosen_approach = "none"

define config.menu_include_disabled = True

# Quest-specific dedaults
default quest_card_img = None

default suspicion = 0
default seeds_of_change = 0
default institutional_cover = "None"

default quest_failed = False
default quest_exit_title = "Quest Complete"
default quest_exit_body = ""

#ART QUEST
default art_resist_format = None

#STORYTELLER QUEST
default storyteller_influence = 0
default mouthbox_louder = False



default quest_start_seeds = 0
default quest_start_suspicion = 0
default quest_start_influence = 0

default quest_attempted = {"storyteller": False, "journalist": False, "artist": False}
default selected_quest = None



define QUESTS = {
    "storyteller": {"label": "quest_storyteller_briefing", "title": "Storyteller"},
    "journalist": {"label": "quest_journalist_briefing", "title": "Journalist"},
    "artist": {"label": "quest_artresist_briefing", "title": "Art Resistance"},
}


image mc neutral = "images/Character_[pc.archetype].png"


# ==============================================================================
# PYTHON LOGIC
# ==============================================================================


init python:
    import random
    #import renpy
    #random = renpy.random
    #import time

    def play_random_blip():
        # List your files here. 
        # If they are in the 'audio' folder, use "audio/filename.wav"
        blip_sounds = [
            "blipSelect1.wav", 
            "blipSelect2.wav", 
            "blipSelect3.wav", 
            "blipSelect4.wav"
        ]
        
        # Pick a random sound and play it on the 'sound' channel
        renpy.sound.play(renpy.random.choice(blip_sounds), relative_volume=0.1)

    def clamp(v, lo, hi):
        return max(lo, min(hi, int(v)))

    STAT_BONUS = {
        "papers":      {0: 0, 1: -3, 2: -6},
        "language":    {0: 0, 1: -3, 2: -6},
        "affiliation": {0: 0, 1: -3, 2: -6},
        "savings":     {0: 0, 1: -2, 2: -4},
    }

    def has_strength(pc, keyword):
        if not keyword:
            return False
        kw = keyword.lower()
        return any(kw in s.lower() for s in pc.strengths)

    def calc_choice_risk(base, suspicion, pc, spotlight=None, strength_keyword=None, suspicion_w=6, friction_w=0.5):
        # baseline you already use everywhere
        risk = base + suspicion * suspicion_w + int(pc.get_profile_friction() * friction_w)

        notes = []

        # spotlight stat bonus (reduces risk if stat is higher)
        if spotlight:
            val = getattr(pc, spotlight, 0)
            bonus = STAT_BONUS.get(spotlight, {}).get(val, 0)
            risk += bonus
            if bonus != 0:
                notes.append("{} helps ({}/2)".format(spotlight.capitalize(), val))
            else:
                notes.append("{} "Nothing to add. ({}/2)".format(spotlight.capitalize(), val))

        # tiny strength nudge
        if strength_keyword:
            if has_strength(pc, strength_keyword):
                risk -= 5
                notes.append("Strength: {}".format(strength_keyword))
            else:
                notes.append("Nothing to add. {}".format(strength_keyword))

        risk = max(5, min(90, int(risk)))
        tooltip = "\n".join(notes)
        return risk, tooltip


    class PlayerCharacter:
        def __init__(
            self,
            archetype,
            codename,
            portrait,
            strengths,
            gameplay,
            papers=1,
            language=1,
            affiliation=1,
            savings=1,
            visibility=20,
            starting_condition=""
        ):
            # Identity-free, situation-based sheet
            self.archetype = archetype
            self.codename = codename
            self.portrait = portrait

            self.strengths = strengths          # list of strings
            self.gameplay = gameplay            # list of strings like ["High Impact", "Low Visibility"]

            # Situation stats
            self.papers = clamp(papers, 0, 2)
            self.language = clamp(language, 0, 2)
            self.affiliation = clamp(affiliation, 0, 2)
            self.savings = clamp(savings, 0, 2)

            self.visibility = clamp(visibility, 0, 100)

            self.starting_condition = starting_condition


        def calc_risk(base, suspicion, pc, suspicion_w=6, friction_w=0.5, lo=5, hi=90):
            risk = base + suspicion * suspicion_w + int(pc.get_profile_friction() * friction_w)
            return max(lo, min(hi, risk))

        def get_profile_friction(self):
            """
            Higher friction = harder social terrain + less access.
            Used by risk formulas: risk = base + suspicion*X + pc.get_profile_friction()*Y
            """
            friction = 0

            # Missing access increases friction
            friction += (2 - self.papers) * 4
            friction += (2 - self.language) * 4
            friction += (2 - self.affiliation) * 3
            friction += (2 - self.savings) * 2

            # Being noticed makes everything sharper
            friction += int(self.visibility / 12)  # 0..8-ish

            return clamp(friction, 0, 90)

    # class PlayerCharacter:
    #     def __init__(self, portrait_image):
    #         # --- 1. IMMUTABLE TAGS ---
    #         self.race = random.choice(["White", "Black", "South Asian", "Middle Eastern"])

    #         # --- WEIGHTED GENDER LOGIC ---
    #         # We define the options and the 'weights' (probabilities)
    #         # Make sure weights sum up to 100 for easy percentage calculation.
    #         gender_options = ["Cis Woman", "Cis Man", "Non-binary", "Trans Woman", "Trans Man"]
            
    #         # Example: Trans = 10% each. Cis = 30% each. NB = 20%. 
    #         # Total: 30+30+20+10+10 = 100%
    #         gender_weights = [30, 30, 20, 10, 10]
            
    #         # random.choices returns a list, so we grab the first item [0]
    #         self.gender = random.choices(gender_options, weights=gender_weights, k=1)[0]
            
    #         # Skin Tone Logic
    #         if self.race == "White":
    #             self.skin_tone = "Light"
    #         else:
    #             self.skin_tone = random.choice(["Light-skinned", "Medium-skinned", "Dark-skinned"])
            
    #         self.origin = random.choice(["Global North", "Global South", "Conflict Zone"])
            
    #         # --- NEW: DISABILITY ---
    #         # "Invisible" disabilities might not add immediate friction but affect stamina
    #         # "Visible" disabilities (Wheelchair, Cane) add friction in inaccessible spaces
    #         self.disability = random.choice([
    #             "None", 
    #             "Mobility (Cane)", 
    #             "Mobility (Wheelchair)", 
    #             "Deaf/HoH", 
    #             "Chronic Pain", 
    #             "Neurodivergent"
    #         ])

    #         # --- 2. MUTABLE METERS ---
    #         self.economic_capital = random.randint(20, 80)
    #         self.social_capital = random.randint(20, 80)
    #         self.mental_resilience = 100 
    #         self.immigration_status = random.randint(10, 60) 

    #         # --- 3. SKILLS & LANGUAGES ---
    #         self.skills = {
    #             "Legal Literacy": random.choice([True, False]),
    #             #"Bureaucratic Navigation": random.choice([True, False]),
    #             "Code Switching": random.choice([True, False]),
    #         }
            
    #         # Language Dictionary 
    #         self.languages = {
    #             "Mother Tongue": True, # Always known
    #             "English": random.choice([True, False]),
    #             "Local Language": random.choice([True, False])
    #         }

    #         self.codename = random.choice(["The Traveler", "The Student", "The Professional", "The Artist", "The Parent", "The Exile"])

    #         self.portrait = portrait_image

    #     def get_profile_friction(self):
    #         friction = 0
            
    #         # Standard Bias
    #         if self.race != "White": friction += 4
    #         if self.skin_tone == "Dark-skinned": friction += 5
    #         #if self.visible_religion: friction += 5
    #         if self.gender in ["Trans Woman", "Non-binary"]: friction += 5
    #         if self.gender in ["Woman", "Trans Man"]: friction += 3
    #         if self.origin == "Conflict Zone": friction += 5
            
    #         # Disability Bias (Ableism)
    #         if self.disability != "None": 
    #             friction += 3
                
    #         # Language Barrier Friction
    #         if not self.languages["Local Language"]:
    #             friction += 5 # High penalty for not speaking the local language
    #         if not self.languages["English"]:
    #             friction += 3 # High penalty for not speaking English
                
    #         return friction


    #OLD NAME: def perform_roll_tom(odds):
    def perform_roll(fail_chance):

        fail_chance = max(0, min(100, int(fail_chance)))

        # Determine the result immediately
        roll = random.randint(1, 100)

        #outcome = None
        outcome = "bad" if roll <= fail_chance else "good"

        # if roll > fail_chance:
        #     outcome = "good"
        # else:
        #     outcome = "bad"

        #Call the screen and PASS the outcome variable so we can see it
        renpy.call_screen("dice_roll", final_value=roll, outcome=outcome)
        
        return outcome

        
    def add_influence(amount):
        store.storyteller_influence = max(0, min(100, store.storyteller_influence + int(amount)))
        store.succumbed_to_storyteller = (store.storyteller_influence >= 100)
        return store.succumbed_to_storyteller
            
    def signed(n):
        n = int(n)
        return "+{}".format(n) if n > 0 else str(n)

# ROLL FUNC IF WE WANT TO CHOOSE RESISTANCE MODE APPROACH AND HAVE IT AFFECT THE OUTCOME 

    # def perform_roll1(pc, approach_type):
    #     odds = calculate_outcome_odds(pc, approach_type)

    #     # Determine the result immediately
    #     final_roll = random.randint(1, 100)

    #     final_outcome = None
        
    #     if final_roll <= odds["good"]:
    #         final_outcome = "good"
    #     elif final_roll <= odds["good"] + odds["mixed"]:
    #         final_outcome = "mixed"
    #     else:
    #         final_outcome = "bad"

    #     # 3. Call the screen and PASS the outcome variable so we can see it
    #     # We add 'outcome=final_outcome' here
    #     renpy.call_screen("dice_roll", final_value=final_roll, outcome=final_outcome)
        
    #     return final_outcome

    # A simple function to calculate odds based on the specific approach and the player's current stats.
    # def calculate_outcome_odds(pc, approach_type):
        
    #     # Base chances (total must equal 100 in the end)
    #     good = 40
    #     mixed = 40
    #     bad = 20
        
    #     # MODIFIERS based on Player Stats
    #     if approach_type == "loud":
    #         # low social capital means loud approaches arent that easy
    #         if pc.social_capital <= 50:
    #             bad += 30
    #             good -= 10
    #             mixed -= 20
        
    #     elif approach_type == "quiet":
    #         # Even quiet things are risky for undocumented folks
    #         if pc.immigration_status <= 50:
    #             bad += 10
    #             mixed += 10
    #             good -= 20
    #         # high economic capital means quiet things are easy
    #         if pc.economic_capital >= 50:
    #             good += 30
    #             bad -= 10
    #             mixed -= 20

    #     # Normalize to ensure they don't go below 0 or crazy high
    #     # (This is a simplified normalization for the template)
    #     total = good + mixed + bad
    #     return {
    #         "good": int((good / total) * 100),
    #         "mixed": int((mixed / total) * 100),
    #         "bad": int((bad / total) * 100)
    #     }
        

label start:

    $ quest_attempted = {"storyteller": False, "journalist": False, "artist": False}


    scene black
    #centered "{b}WELCOME TO THE RESISTANCE{/b}"


    # 🕯️ Your file updates itself. (1 quiet shift per profile, once per run.)

    #centered "Your file updates itself."
    centered "Three profiles appear in the queue."

    python:
        run_twists = {}

        deck = [
            # 📄 Papers
            {"text": "A stamp lands somewhere. You don’t see where.", "mod": ( 1, 0, 0, 0)},
            {"text": "A form is missing. No one admits it existed.",   "mod": (-1, 0, 0, 0)},

            # 🗣️ Language
            {"text": "A sentence comes easier today.",               "mod": ( 0, 1, 0, 0)},
            {"text": "Your words don’t fit the room.",               "mod": ( 0,-1, 0, 0)},

            # 🏛️ Affiliation
            {"text": "An office with your name on the door.",                 "mod": ( 0, 0, 1, 0)},
            {"text": "No one remembers who you are supposed to be.",     "mod": ( 0, 0,-1, 0)},

            # 💰 Savings
            {"text": "Your pocket is lighter than it should be.",    "mod": ( 0, 0, 0,-1)},
            {"text": "You can afford one mistake. Not two.",         "mod": ( 0, 0, 0, 1)},
        ]

        archetypes = ["Journalist", "Engineer", "Artist"]

        # (Optional but nice): avoid duplicates by shuffling and taking the first 3
        renpy.random.shuffle(deck)

        for a, entry in zip(archetypes, deck[:len(archetypes)]):
            run_twists[a] = entry

    # # 🎲 System scan: assign 1 access twist per profile (once per run)
    # $ run_twists = {}
    # $ deck = [
    #     ("📄 Papers +1",      ( 1, 0, 0, 0)),
    #     ("📄 Papers -1",      (-1, 0, 0, 0)),
    #     ("🗣️ Language +1",    ( 0, 1, 0, 0)),
    #     ("🗣️ Language -1",    ( 0,-1, 0, 0)),
    #     ("🏛️ Affiliation +1", ( 0, 0, 1, 0)),
    #     ("🏛️ Affiliation -1", ( 0, 0,-1, 0)),
    #     ("💰 Savings +1",     ( 0, 0, 0, 1)),
    #     ("💰 Savings -1",     ( 0, 0, 0,-1)),
    # ]

    # $ for a in ["Journalist", "Engineer", "Artist"]:
    #     $ card, mod = random.choice(deck)
    #     $ run_twists[a] = {"card": card, "mod": mod}
    
    call character_select 

    with Dissolve(0.2)
    centered "Welcome to the resistance."



    jump map 

# ==============================================================================
# QUEST HELPERS
# ==============================================================================

label travel_to_quest(required_papers=1):
    # If papers too low, travel is harder / costs you something
    if pc.papers < required_papers:
        centered "Denied."
        #stamp sound? 

        #choose how to get in: pay a smuggler (if enough money) or based on char. strength 
        
    else:
        centered "Approved."
        #stamp sound? 
    return

label run_end:
    scene black
    with fade

    centered "You tried."
    centered "You did what you could."
    centered "Sometimes surviving the run is the resistance."

    centered " "
    centered "Run Summary:"
    centered "[seeds_of_change] seeds left behind."


    menu:
        "What now?"
        "Start a new run":
            $ pc = None
            $ seeds_of_change = 0
            $ suspicion = 0
            $ storyteller_influence = 0
            $ mouthbox_louder = False
            $ quest_attempted = {"storyteller": False, "journalist": False, "artist": False}
            jump start

        "Quit":
            return



label start_quest:
    # expects selected_quest to already be set (e.g. "storyteller")

    if quest_attempted.get(selected_quest, False):
        $ renpy.notify("Not again.")
        return

    $ quest_attempted[selected_quest] = True

    call quest_enter
    jump expression QUESTS[selected_quest]["label"]


label quest_enter:

    $ quest_start_seeds = seeds_of_change
    $ quest_start_suspicion = suspicion
    $ quest_start_influence = storyteller_influence

    # ✅ reset per-quest flags
    $ quest_failed = False
    $ mouthbox_louder = False

    stop music fadeout 0.5
    scene black
    with fade
    return

label end_quest:
    stop music fadeout 0.5
    window show
    return
     

label show_quest_card:
    # 1. HIDE THE TEXTBOX
    # This ensures the user doesn't see the empty dialogue box.
    window hide

    # 2. SET THE SCENE
    # we show your title image. 'truecenter' aligns it perfectly.
    show expression quest_card_img as quest_card at truecenter

    # 3. FADE IN (The "Slow" part)
    # Dissolve(3.0) means it takes 3.0 seconds to fade in.
    with Dissolve(3.0)

    # 4. WAIT FOR CLICK
    # 'pause' without a number waits indefinitely until the user clicks.
    pause

    # 5. FADE OUT & RESET
    # We hide the image with a faster fade, then bring the window back.
    hide quest_card
    with Dissolve(1.0)
    
    # Reveal the textbox again for the game to start
    window show
    return


# ==============================================================================
# CHARACTER SELECT 
# ==============================================================================


label character_select:
    if pc is not None:
        return

    window hide

    # $ j = run_twists.get("Journalist", {"card":"", "mod":(0,0,0,0)})
    # $ e = run_twists.get("Engineer",  {"card":"", "mod":(0,0,0,0)})
    # $ a = run_twists.get("Artist",    {"card":"", "mod":(0,0,0,0)})

    $ j = run_twists.get("Journalist", {"text":"", "mod":(0,0,0,0)})
    $ e = run_twists.get("Engineer",  {"text":"", "mod":(0,0,0,0)})
    $ a = run_twists.get("Artist",    {"text":"", "mod":(0,0,0,0)})


    $ options = [
        PlayerCharacter(
            archetype="Journalist",
            codename="J.",
            portrait="images/portrait1.png",
            strengths=["Journalism ", "Communication ", "Institutional cover "],
            gameplay=["High 🎯 Impact", "Medium 👁️ Visibility", "Moderate 🚓 Risk"],
            #papers=2, language=2, affiliation=2, savings=1, visibility=35

            papers=2 + j["mod"][0],
            language=2 + j["mod"][1],
            affiliation=2 + j["mod"][2],
            savings=1 + j["mod"][3],
            visibility=35,
            starting_condition = j.get("text", "Nothing changes today.")



        ),
        PlayerCharacter(
            archetype="Engineer",
            codename="E.",
            portrait="images/portrait2.png",
            strengths=["Engineering ", "Tech access ", "Community organizing "],
            gameplay=["Medium 🎯 Impact", "Low 👁️ Visibility", "Low-to-mid 🚓 Risk"],
            #papers=1, language=1, affiliation=1, savings=2, visibility=15
            papers=1 + e["mod"][0],
            language=1 + e["mod"][1],
            affiliation=1 + e["mod"][2],
            savings=2 + e["mod"][3],
            visibility=15,
            starting_condition = e.get("text", "Nothing changes today.")

        
        ),
        PlayerCharacter(
            archetype="Artist",
            codename="A.",
            portrait="images/portrait3.png",
            strengths=["Art & storytelling ", "Public speaking ", "Charisma "],
            gameplay=["High 🎯 Impact", "High 👁️ Visibility", "High 🚓 Risk"],
            #papers=1, language=2, affiliation=1, savings=1, visibility=55
            papers=1 + a["mod"][0],
            language=2 + a["mod"][1],
            affiliation=1 + a["mod"][2],
            savings=1 + a["mod"][3],
            visibility=55,
            starting_condition = a.get("text", "Nothing changes today.")

        ),
    ]

    call screen character_select(char_candidates=options)
    #show screen stats_button_overlay
    if pc is not None:
        $ renpy.notify("Your file updates itself. " + pc.starting_condition)

        # purely presentation: "processing"
        $ roll = renpy.random.randint(1, 100)
        #call screen dice_roll(final_value=roll, outcome="good")
        with Dissolve(0.4)
        call screen character_reveal(pc)

    window show
    return


# label character_select:
#     # ==== TOM's CHARACTER SELECTION CODE ====
#     window hide
#     # 1. Define your pool of all possible images
#     $ all_portraits = [
#         "images/portrait1.png",
#         "images/portrait2.png",
#         "images/portrait3.png"
#     ]
    
#     # 2. Pick 3 UNIQUE images from that list. 
#     # random.sample picks unique items. It will crash if you ask for 3 but only have 2 images.
#     $ selected_portraits = random.sample(all_portraits, 3)

#     # 3. Generate the characters, passing the specific images
#     # We use selected_portraits[0], [1], and [2]
#     $ candidate_1 = PlayerCharacter(selected_portraits[0])
#     $ candidate_2 = PlayerCharacter(selected_portraits[1])
#     $ candidate_3 = PlayerCharacter(selected_portraits[2])
    
#     # 2. Put them in a list
#     $ options = [candidate_1, candidate_2, candidate_3]
    
#     # 3. Call the screen, passing the list
#     # The screen will set the variable 'pc' to the one the user clicks
#     call screen character_select(char_candidates=options)

#     # 4. The game begins with the selected 'pc'
#     # Show the overlay button for stats now that the game has started
#     #show screen stats_button_overlay
    
#     #"You have selected: [pc.codename]."
#     window show
#     return




# ==============================================================================
# QUEST TEMPLATE
# ==============================================================================

# label quest_template:
#     # First we have to narrate the quest
#     "Once upon a time, lorem ipsum dolor sit amet, consectetur adipiscing elit..."

#     # Then the player chooses their character
#     call character_select

#     # Give the player some exposition
#     "Some expositional stuff happens. Describe scene here..."

#     # Then the player has a choice where they see probabilities of their action
#     window hide
#     call screen risk_assessment_menu(
#         pc,
#         prompt="How do you approach the situation?",
#         option1_name="Loud", option1_type="loud",
#         option2_name="Quiet", option2_type="quiet",
#         option3_name="Violent", option3_type="violent"
#     )

#     # The screen returns the type chosen (e.g., "loud")
#     $ chosen_approach = _return

#     # Dice Rolling Animation
#     #show text "{size=50}CALCULATING RISK...{/size}" at truecenter
#     #pause 2.0 # Suspense

#     # Calculate result logic
#     $ current_outcome = perform_roll(pc, chosen_approach)

#     #hide text

#     # Outcome & Aftermath
#     if current_outcome == "good":
#         #"SUCCESS!"
#         "The plan worked better than expected. Your stats aligned perfectly with the moment."
#     elif current_outcome == "mixed":
#         #"PARTIAL SUCCESS."
#         "You managed to do it, but at a cost. The system noticed you."
#     else:
#         #"FAILURE."
#         "Disaster. The system pushed back hard."

#     # Conditional text based on stats
#     if pc.get_profile_friction() > 5:
#         "Because your Targeting Level is high, a drone lingers over you specifically, recording your face."

#     # Escalation & Second Choice
#     "The situation escalates. ........ You have another moment to react"

#     menu:
#         "Disperse into the crowd immediately.":
#             $ final_choice = "flee"
#         "Stand your ground and document the abuse.":
#             $ final_choice = "document"
#         "Call your NGO contact for legal aid.":
#             $ final_choice = "legal"

#     # Epilogue Reflection
#     if final_choice == "flee":
#         "You vanished into the night. Safe, but the message was weak."
#     elif final_choice == "document":
#         "You have footage. It might help later, but you are now on a watchlist."

#     #  Final Text & Loop
#     "The quest concludes. The struggle continues elsewhere."

#     jump map