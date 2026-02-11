
label quest_artresist_briefing:

    call quest_enter

# ==============================================================================
# BRIEFING
# ==============================================================================

    "Once upon a time, there was a school that called itself a sanctuary."

    "Its walls were covered in words like *belonging*, *equity*, and *freedom of thought*."

    "It said: *All stories are welcome here.*"

    "But some names were always mispronounced."
    "Some questions always went unanswered."
    "Some truths are called 'aggressive', or 'divisive'."

    play music "audio/HoliznaCC0-DownInTheBasement.mp3"

    $ quest_card_img = "images/Quest_page_Art.png"
    call show_quest_card

    #show expression "images/Quest_page_Art.png" as title_img at truecenter

    #"Please select who is going to resist."

    # Then the player chooses their character
    #call character_select

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

# ==============================================================================
# CHOICE
# ==============================================================================

    menu:
        "What form will your resistance take?"
        "A video game about resistance":
            "You start sketching the first level, you keep going… You want to tell not just your story through the game characters, but stories of your friends as well."
            $ art_resist_format = "game"
            jump  quest_artresist_game
        "A drag show about fake diversity marketing.":
            "If the diversity is fake, the glamour will be real."
            $ art_resist_format = "drag"
            jump quest_artresist_drag
        "An anonymous zine telling the truth of your classmates’ stories.":
            $ art_resist_format = "zine"
            "You collect whispers and turn them into pages."
            jump quest_artresist_zine


label quest_artresist_game:

    "You stay up late sketching out scenes."
    "You don\'t code much, but you know what it should *feel* like."

# ==============================================================================
# CHOICE - GAME
# ==============================================================================

    menu:
        "How do you launch the game?"
        "Post it on the university Discord":
            "It spreads fast. And someone flags it."

        "Put it on a USB and hand it out anonymously":
            "Old school. Low traceability. Slower spread."

        "Upload it to a public platform under a fake name":
            "You can\'t resist putting your art out in the open."

    jump artresist_resolve


label quest_artresist_drag:

    "You paint your face with campus colors, then *scramble them*."

# ==============================================================================
# CHOICE - DRAG
# ==============================================================================

    menu:
        "What\'s your opening number?"
        "Lip sync to a rewritten diversity commercial":
            "Can I get an amen?"

        "Spoken word poem in full drag":
            "No metaphors. Just stilettos."

    jump artresist_resolve

label quest_artresist_zine:

    "You collect stories. Type them up. Print them out at 2 a.m."

    "You fold each one by hand."

# ==============================================================================
# CHOICE - ZINE
# ==============================================================================

    menu:
        "How do you distribute it?"
        "Leave copies in admin mailboxes":
            "Direct action. Sharp risk."
        "Slide it under dorm doors at night":
            "It feels like ghost work. But someone will read it."

    jump artresist_resolve


# ==============================================================================
# ROLL THE DICE 
# ==============================================================================

label artresist_resolve:
    $ risk = 20 + (suspicion * 5) + int(pc.get_profile_friction() * 0.5)
    $ risk = min(90, risk)

    $ current_outcome = perform_roll(risk)

    if current_outcome == "good":
        jump quest_artresist_success
    else:
        jump quest_artresist_failure




label quest_artresist_success:

    "You did it."

    "You created something that cut through the noise."

    "You don\'t know who it changed, but you know someone stayed up thinking about it."

    $ seeds_of_change += 3

    jump quest_exit_art


label quest_artresist_failure:

    "It didn’t go the way you hoped."

    "You got a warning. Maybe more."

    "But later, someone finds you."

    "\"I read it. I saw it. I needed it.\""

    $ seeds_of_change += 1

    jump quest_exit_art



label quest_exit_art(title="Quest Complete", body="", failed=False):
    call end_quest
    call screen quest_summary(title=title, body=body)
    return