

label quest_03:
    "Placeholder for Quest 3."

    jump map 


label quest_02:
    
    stop music
    
    scene black
    with fade


    "Once upon a time, there was a Storyteller."


    "He spoke plainly.\nHe spoke calmly.\nHe never seemed to say very much at all."

    "But he had a way with words."

    "If he repeated a sentence often enough,\nit began to sound like it had always been true."

    "Every household was given a machine.\nA small box with a single mouth.\nIt spoke in the Storyteller’s voice."

    "It told his stories in the morning.\nIt told his stories at night."

    "There were no new stories.\nBut people still listened."

    "At first, people listened with half an ear.\nThen they stopped turning it off.\nThen they stopped noticing it was on."

    "And slowly, people forgot they had stories of their own.\nThey forgot their neighbours did, too."

    "Soon enough, it began to sound like the Story they know had never been anything else."

    play music "audio/HoliznaCC0-Ukraine.mp3"

    # 1. HIDE THE TEXTBOX
    # This ensures the user doesn't see the empty dialogue box.
    window hide

    # 2. SET THE SCENE
    # 'scene black' clears the screen. 
    # Then we show your title image. 'truecenter' aligns it perfectly.
    scene black
    show expression "images/Quest2_page.png" as title_img at truecenter

    # 3. FADE IN (The "Slow" part)
    # Dissolve(3.0) means it takes 3.0 seconds to fade in.
    with Dissolve(3.0)

    # 4. WAIT FOR CLICK
    # 'pause' without a number waits indefinitely until the user clicks.
    pause

    # 5. FADE OUT & RESET
    # We hide the image with a faster fade, then bring the window back.
    hide title_img
    with Dissolve(1.0)
    
    # Reveal the textbox again for the game to start
    window show


    "Please select who is going to resist the storyteller."


    # Then the player chooses their character
    call character_select



    "You arrive in a small town where every room has a \"mouth-box\"."

    "You are looking from your hotel room, outside, watching people pass by. Your room has the box as well. You listen with half an ear.\nYou think to yourself that you would never believe what it’s saying."

    "You get dressed and decide to go to…"

    menu:
        "You get dressed and decide to go to…"
        "The Library:\nYou heard of an underground operation running in this town through a library, you’re not sure if the information is secure or a trap setup by the Storyteller":
            jump quest_storyteller_library_1
        "The Supermarket:\nYou want to talk to the locals here and see if they really do believe the Storyteller" if False:
            jump quest_storyteller_supermarket_1 



label quest_storyteller_library_1:

    scene library
    with fade

    "The library is easy to find."
    "It sits in the middle of town like it has always belonged there."

    "A banner hangs above the door:"
    "\"{i}THE STORY KEEPS US TOGETHER{/i}\""

    "You hesitate before entering."

    "You heard a rumor."
    "An underground operation."
    "A library that still remembers other voices."

    "Or…"
    "a trap staged by someone who knows exactly what you came to do."

    "Inside, the air smells like paper and dust."

    "A Mouth-Box sits on the front desk."

    "Behind the desk, a librarian looks up."

    menu:
        "How do you approach?"
        "Ask for Local History":
            jump quest_storyteller_library_localhistory

        "Mention the Mouth-Box":
            jump quest_storyteller_library_mouthbox



label quest_storyteller_library_localhistory:
    "You keep your voice small."
    "\"Do you have… local history?\""

    "The librarian looks up like you’ve interrupted something important."
    "Their eyes flick over you—shoes, hands, face — then they stop caring."

    "\"Local history.\""
    "Not a question. Not an answer. Just the words, repeated back at you."

    "A pause."
    "A sigh that sounds like it has been practiced."

    "\"Aisle three,\" they say."
    "\"Approved records.\""

    "They tap the desk once, impatient."
    "\"Don’t linger.\""

    "The Mouth-Box on the desk clicks softly, like it heard that."

    jump quest_storyteller_library_aisles

label quest_storyteller_library_aisles:
    "-- not implemented -- "
    jump map


label quest_storyteller_library_mouthbox:

    "You let your eyes drift to the Mouth-Box."
    "\"It’s loud,\" you say, lightly."

    "The librarian’s expression doesn’t change."
    "If anything, it gets worse."

    "\"Of course it’s loud,\" they say."
    "\"That’s the point.\""

    "The librarian’s jaw tightens."
    "\"Keep your voice down,\" they mutter."
    "\"And don’t make it my problem.\""

    # 🎲 Dice roll
    $ last_roll = renpy.random.randint(1, 100)
    $ threshold = 55 + (suspicion * 10)

    if last_roll < threshold:
        jump quest_storyteller_library_mouthbox_fail
    else:
        jump quest_storyteller_library_mouthbox_success


label quest_storyteller_library_mouthbox_success:

    "The librarian stares at you for one long second."
    "Measuring."
    "Weighing."

    "\"Tourist?\" they say, like an accusation."

    "Then—without softening—"
    "\"If you want quiet, you go to the reading room.\""
    "The Mouth-Box chirps over them."

    "The librarian leans closer."
    "\"Back hall,\" they murmur."
    "\"Knock twice.\""

    "They straighten up immediately."
    "\"And don’t come back to my desk.\""

    jump quest_storyteller_library_readingroom

label quest_storyteller_library_mouthbox_fail:

    "The librarian’s face changes."
    "Not slowly."
    "Like a switch."

    "\"Loud?\" they snap."
    "\"You walk in here and start complaining?\""

    "Their voice climbs."
    "People look up from tables."

    "\"You outsiders come to our town and act like we owe you something.\""
    "\"Always questions. Always demands.\""
    "\"Always dissatisfied.\""

    "The librarian’s hand slaps the desk."
    with vpunch

    "\"Do us all a favor—stay out of here.\""

    "The Mouth-Box clicks on, bright and eager."
    "{i}STAY OUT OF HERE.{/i}"

    "The librarian talks over it, louder still."
    "\"We’re tired of you people stirring things up.\""
    "\"We’re tired of you making problems.\""

    "The Mouth-Box answers, louder—too loud."
    "{i}TIRED OF YOU.{/i}"

    "A chair scrapes somewhere behind you."
    "Someone mutters something that sounds like agreement."

    "You lower your gaze."
    "You step back."
    "You leave without arguing."

    $ suspicion += 1
    $ mouthbox_louder = True

    "Outside, you exhale—"
    "and only then realize you were holding your breath."

    jump quest_storyteller_supermarket_1



label quest_storyteller_supermarket_1:
    "-- not implemented -- "
    jump map
    

label quest_storyteller_library_readingroom:

    "You knock twice."

    "Tap. Tap."

    "Nothing stops you."
    "The door is unlocked."

    "You step inside."

    "A normal room."
    "Tables. Books spread open."
    "Tea cooling in cups."

    "Two older people look up at the same time."

    "First: alertness."
    "Then: fear."
    "Then—carefully—curiosity."

    "You scan the walls."

    "No Mouth-Box."

    "On the table, something dark and rectangular."
    "A book?"

    "No."
    "A notebook."

    "And a pen."

    "You heard people are not allowed to write here."

    "You greet them carefully."

    "\"You’re not from here,\" one of them says."
    "Not accusing. Measuring."

    "\"A foreigner,\" the other adds."
    "\"What brings you to a room like this?\""


    menu:
        "What do you say?"
        "“I’m here to hear your stories.”":
            jump quest_storyteller_readingroom_stories
        "“I’m here to kick the Storyteller’s butt.”":
            jump quest_storyteller_readingroom_butt


label quest_storyteller_readingroom_stories:

    "For a second, neither of them speaks."

    "Then the one with the notebook presses their fingers to the cover."
    "\"Stories…\" they echo."
    "The other’s eyes shine."

    "\"Careful,\" the first one murmurs."
    "\"We don’t say that word loudly.\""

    jump quest_storyteller_readingroom_test


label quest_storyteller_readingroom_butt:

    "The older person with the tea huffs a laugh."
    "\"Calm down, child,\" they say."

    "\"If you want to fight him,\" the other one says,"
    "\"You do it with stories that aren’t his.\""

    jump quest_storyteller_readingroom_test


label quest_storyteller_readingroom_test:

    $ last_roll = renpy.random.randint(1, 100)
    $ threshold = 55 + (suspicion * 10) + story_mod

    if last_roll < threshold:
        jump quest_storyteller_readingroom_test_fail
    else:
        jump quest_storyteller_readingroom_test_success


label quest_storyteller_readingroom_test_fail:

    "\"No,\" one of them says quietly."
    "\"Not today.\""

    "The other turns their teacup a few degrees."
    "A tiny reset."

    "\"Finish your tea,\" they murmur."
    "\"Then leave like you never found this room.\""

    $ suspicion += 1
    return

label quest_storyteller_readingroom_test_success:

    "The notebook is pushed toward you."
    "\"One line at a time,\" one of them murmurs."
    "\"If you hear steps—stop.\""

    $ seeds_of_change += 2
    $ suspicion += 1

    "You pick up the pen."
    "It feels heavier than it should."

    "They begin with something small."
    "A name."
    "A neighbor."
    "You write."

    jump quest_storyteller_readingroom_write


label quest_storyteller_readingroom_write:

    "The notebook is opened between you like a small, dangerous altar."
    "They begin to talk."
    "You begin to write."

    $ pages_written = 0
    jump quest_storyteller_readingroom_write_loop


label quest_storyteller_readingroom_write_loop:

    # ✍️ Write one “page”
    $ pages_written += 1
    $ seeds_of_change += 2
    $ suspicion += 1

    if pages_written == 1:
        "A neighbour’s story."
        "A small kindness. A small betrayal."
        "You write it down."
    elif pages_written == 2:
        "A family story."
        "A lost job. A closed door. A name changed to survive."
        "You write faster."
    elif pages_written == 3:
        "A story that makes one of them swallow hard before speaking."
        "You feel the pen hesitate, then continue."
    else:
        "More stories."
        "More names."
        "The manuscript grows heavier with every line."

    # 🎲 Risk check each page (more suspicion = more danger)
    $ roll = renpy.random.randint(1, 100)
    $ risk = min(90, 35 + (suspicion * 12))  # tune numbers as you like

    if roll <= risk:
        jump quest_storyteller_readingroom_caught

    # 🧭 Choice: keep writing or stop
    menu:
        "Do you keep writing?"
        "Keep writing":
            jump quest_storyteller_readingroom_write_loop
        "Stop. Hide the manuscript.":
            jump quest_storyteller_readingroom_escape


label quest_storyteller_readingroom_caught:

    "Footsteps in the hall."
    "Not rushed."
    "Certain."

    "The older couple moves at once—too late."
    "The notebook is still warm from your hand."

    "The door opens."

    "Later, you are thrown into a cell together."

    "A Mouth-Box waits in the corner."
    "It speaks softly at first."
    "Then louder."
    "Then constantly."

    "Eventually, the cell begins to resemble a box, too."

    # TODO: consider adding game over message

    return


label quest_storyteller_readingroom_escape:

    "You set the pen down."

    "One of them closes the notebook immediately."
    "The other moves the tea cups—small, deliberate motions—"
    "until the table looks boring again."

    "\"Good,\" one of them says. \"Enough.\""

    "They tear out a single page without ceremony."
    "Fold it twice."
    "Press it into your hand."

    "\"Don’t read it here,\" they murmur."
    "\"And don’t carry it where you can be searched.\""

    "The notebook is gone before you can look up."

    # TODO: add popup that tells you seeds of change

    jump map
