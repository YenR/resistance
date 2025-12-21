label quest_artresist_briefing:

    "Once upon a time, there was a school that called itself a sanctuary."

    "Its walls were covered in words like *belonging*, *equity*, and *freedom of thought*."

    "It said: *All stories are welcome here.*"

    "But some names were always mispronounced."
    "Some questions always went unanswered."
    "Some truths are called 'aggressive', or 'divisive'."

    # 1. HIDE THE TEXTBOX
    # This ensures the user doesn't see the empty dialogue box.
    window hide

    # 2. SET THE SCENE
    # 'scene black' clears the screen. 
    # Then we show your title image. 'truecenter' aligns it perfectly.
    scene black
    show expression "images/Quest_page_Art.png" as title_img at truecenter

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

    "Please select who is going to resist the university."

    # Then the player chooses their character
    call character_select

    jump quest_artresist_intro


label quest_artresist_intro:

    scene art quest
    with fade

    "You sit alone in the courtyard."

    "The university banners flap proudly: {i}DIVERSITY IS OUR STRENGTH{/i}."

    "But you remember the professor who mocked your name."
    "The security guard who asked for your ID. "
    "The thesis advisor who called your project 'too political.'"

    "You take a breath. You\'re going to make something anyway."

    menu:
        "What form will your resistance take?"
        "A video game about resistance":
            "You start sketching the first level, you keep going… You want to tell not just your story through the game characters, but stories of your friends as well."
            jump  quest_artresist_game
        "A drag show about fake diversity marketing.":
            "If the diversity is fake, the glamour will be real."
            jump quest_artresist_drag
        "An anonymous zine telling the truth of your classmates’ stories.":
            "You collect whispers and turn them into pages."
            jump quest_artresist_zine

label quest_artresist_game:

    "You stay up late sketching out scenes."
    "You don\'t code much, but you know what it should *feel* like."

    menu:
        "How do you launch the game?"
        "Post it on the university Discord":
            "It spreads fast. And someone flags it."

        "Put it on a USB and hand it out anonymously":
            "Old school. Low traceability. Slower spread."

        "Upload it to a public platform under a fake name":
            "You can\'t resist putting your art out in the open."


    $ odds = 25 + (suspicion * 10) + pc.get_profile_friction()
    $ current_outcome = perform_roll_tom(odds)

    if current_outcome == "good":
        jump quest_artresist_success
    else:
        jump quest_artresist_failure

label quest_artresist_drag:

    "You paint your face with campus colors, then *scramble them*."

    menu:
        "What\'s your opening number?"
        "Lip sync to a rewritten diversity commercial":
            ""

        "Spoken word poem in full drag":
            "No metaphors. Just stilettos."

    $ odds = 25 + (suspicion * 10) + pc.get_profile_friction()
    $ current_outcome = perform_roll_tom(odds)

    if current_outcome == "good":
        jump quest_artresist_success
    else:
        jump quest_artresist_failure

label quest_artresist_zine:

    "You collect stories. Type them up. Print them out at 2 a.m."

    "You fold each one by hand."

    menu:
        "How do you distribute it?"
        "Leave copies in admin mailboxes":
            "Direct action. Sharp risk."
        "Slide it under dorm doors at night":
            "It feels like ghost work. But someone will read it."


    $ odds = 25 + (suspicion * 10) + pc.get_profile_friction()
    $ current_outcome = perform_roll_tom(odds)

    if current_outcome == "good":
        jump quest_artresist_success
    else:
        jump quest_artresist_failure


label quest_artresist_success:

    "You did it."

    "You created something that cut through the noise."

    "You don\'t know who it changed, but you know someone stayed up thinking about it."

    $ seeds_of_change += 3

    return

label quest_artresist_failure:

    "It didn’t go the way you hoped."

    "You got a warning. Maybe more."

    "But later, someone finds you."

    "\"I read it. I saw it. I needed it.\""

    $ seeds_of_change += 1

    return


