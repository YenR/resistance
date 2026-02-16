
label quest_artresist_briefing:

    call quest_enter
    call travel_to_quest(required_papers=2)
    
    $ quest_endings = {
        "good":    "Your art draws a crowd far beyond campus expectations.\nWhat began as one voice becomes many.",
        "neutral": "Institutional pushback limits your reach.\nBut within smaller groups, it resonates deeply.",
        "bad":     "Your message was cut short.\nBut the need to speak remains."
    }

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

    scene art quest 2
    with fade

    "You take a breath. You\'re going to make something anyway."

# ==============================================================================
#‼️ CHOICE
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
#‼️ CHOICE - GAME
# ==============================================================================

    $ risk_distribution, tip_distribution = calc_choice_risk(
        base=30,
        suspicion=suspicion,
        pc=pc,
        spotlight="language", 
        strength_keyword="Art & storytelling" #Shivi: for the game I think Art & storytelling fits best
        )
    

    
    call screen risk_assessment_menu_2options(
        pc,
        prompt="How do you launch the game?",

        option1="Post it on the university Discord",
        option1tt="{}% Chance of Failure\n{}".format(risk_distribution + 10, tip_distribution),

        option2="Put it on a USB and hand it out anonymously",
        option2tt="{}% Chance of Failure\n{}".format(risk_distribution, tip_distribution),

        option3="Upload it to a public platform under a fake name",
        option3tt="{}% Chance of Failure\n{}".format(risk_distribution - 10, tip_distribution)
    )
    
    $ chosen_approach = _return

    if chosen_approach == "Post it on the university Discord":
        $ risk_distribution += 10
        "It spreads fast. And someone flags it."

    elif chosen_approach == "Put it on a USB and hand it out anonymously":
        "Old school. Low traceability. Slower spread."

    else:
        $ risk_distribution -= 10
        "You can\'t resist putting your art out in the open."

    jump artresist_resolve

    # menu:
    #     "How do you launch the game?"
    #     "Post it on the university Discord":
    #         "It spreads fast. And someone flags it."

    #     "Put it on a USB and hand it out anonymously":
    #         "Old school. Low traceability. Slower spread."

    #     "Upload it to a public platform under a fake name":
    #         "You can\'t resist putting your art out in the open."

    # jump artresist_resolve


label quest_artresist_drag:

    "You paint your face with campus colors, then *scramble them*."

# ==============================================================================
#‼️ CHOICE - DRAG
# ==============================================================================

    $ risk_distribution, tip_distribution = calc_choice_risk(
        base=20,
        suspicion=suspicion,
        pc=pc,
        spotlight="", 
        strength_keyword="Charisma" #Shivi: for drag I think public speaking or charisma fits best
        )

    call screen risk_assessment_menu_2options(
        pc,
        prompt="What\'s your opening number?",

        option1="Lip sync to a rewritten diversity commercial",
        option1tt="{}% Chance of Failure\n{}".format(risk_distribution + 10, tip_distribution),

        option2="Spoken word poem in full drag",
        option2tt="{}% Chance of Failure\n{}".format(risk_distribution, tip_distribution),
    )

    # menu:
    #     "What\'s your opening number?"
    #     "Lip sync to a rewritten diversity commercial":
    #         "Can I get an amen?"

    #     "Spoken word poem in full drag":
    #         "No metaphors. Just stilettos."

    $ chosen_approach = _return

    if chosen_approach == "Lip sync to a rewritten diversity commercial":
        $ risk_distribution += 10
        "Can I get an amen?"

    else:
        "No metaphors. Just stilettos."

    jump artresist_resolve

label quest_artresist_zine:

    "You collect stories. Type them up. Print them out at 2 a.m."

    "You fold each one by hand."

# ==============================================================================
#‼️ CHOICE - ZINE
# ==============================================================================

    $ risk_distribution, tip_distribution = calc_choice_risk(
        base=20,
        suspicion=suspicion,
        pc=pc,
        spotlight="savings", 
        strength_keyword="Communication" #Shivi: for Zine I think journalism or communication would help
        )

    call screen risk_assessment_menu_2options(
        pc,
        prompt="How do you distribute it?",

        option1="Leave copies in admin mailboxes",
        option1tt="{}% Chance of Failure\n{}".format(risk_distribution + 10, tip_distribution),

        option2="Slide it under dorm doors at night",
        option2tt="{}% Chance of Failure\n{}".format(risk_distribution, tip_distribution),
    )

    $ chosen_approach = _return

    if chosen_approach == "Leave copies in admin mailboxes":
        $ risk_distribution += 10
        "Direct action. Sharp risk."
    else:
        "It feels like ghost work. But someone will read it."

    # menu:
    #     "How do you distribute it?"
    #     "Leave copies in admin mailboxes":
    #         "Direct action. Sharp risk."
    #     "Slide it under dorm doors at night":
    #         "It feels like ghost work. But someone will read it."

    jump artresist_resolve




# ==============================================================================
# ROLL THE DICE 
# ==============================================================================


label artresist_resolve:
    # $ risk = 20 + (suspicion * 5) + int(pc.get_profile_friction() * 0.5)
    # $ risk = min(90, risk)

    $ current_outcome = perform_roll(risk_distribution)

    if current_outcome == "good":
        jump quest_artresist_success
    else:
        jump quest_artresist_failure




label quest_artresist_success:

    "You did it."

    "You created something that cut through the noise."

    "You don\'t know who it changed, but you know someone stayed up thinking about it."

    $ seeds_of_change += 3
    
    $ quest_summaries["artist"] = quest_endings["good"]

    jump quest_exit_art


label quest_artresist_failure:

    "It didn’t go the way you hoped."

    "You got a warning. Maybe more."

    "But later, someone finds you."

    # Shivi: changing the next line based on the medium the player chose
    # I'm adding two new lines for game and drag

    if art_resist_format == "game":
        "\"I played it. I saw it. I needed it.\""
        
    elif art_resist_format == "drag":
        "\"I saw it. I felt it. I needed it.\""
        
    else:
        #Shivi: this was the default before
        "\"I read it. I saw it. I needed it.\""

    $ seeds_of_change += 1
    
    $ quest_summaries["artist"] = quest_endings["neutral"]

    jump quest_exit_art



label quest_exit_art(title="Quest Complete", body="", failed=False):
    call end_quest
    call screen quest_summary(title=title, body=body)
    return