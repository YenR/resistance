
label quest_journalist_briefing:
    
    call quest_enter

# ==============================================================================
# BRIEFING
# ==============================================================================

    "Once upon a time, there was a nation."
    " It spoke of unity. It spoke of progress."
    " It never seemed to address the shadows."

    "But the shadows had stories of their own."
    " Every citizen was given a narrative."
    " A carefully crafted account of history, of belonging, of duty."

    "The narrative spoke of a glorious past."
    " There were no dissenting voices."

    "And slowly, people stopped questioning the broadcast."
    " Then they stopped sharing their own experiences."
    
    "Soon enough, it began to sound like the truth they knew was all there ever was."

    play music "audio/HoliznaCC0-Anxiety.mp3"

    $ quest_card_img = "images/Quest_page_Shadow.png"
    call show_quest_card

    # "Please select who is going to resist the narrative."
    # Assuming character_select is a global call defined elsewhere
    # call character_select

    jump quest_journalist_office

# ==============================================================================
# PART 1: Talking to the Boss
# ==============================================================================

label quest_journalist_office:

    scene office quest 
    # Placeholder background name
    with fade

    "It’s another busy workday at the news office."
    "A controlled chaos of chipped desks, flickering fluorescent lights, and clatter of repurposed typewriters."
    "The air smells faintly of stale chai and cheap paper."

    "You see your boss sitting behind their desk, an island of controlled order amidst the surrounding mess."


    "You clutch the dossier you’ve spent countless nights preparing."
    "Your notes are practically spilling out."

    "You remember the riots. You remember the silence that followed."
    "And you remember a truth buried beneath layers of carefully constructed lies."

    "Your boss speaks without looking up."
    "\"You wanted to see me. Make it quick. Deadline’s breathing down my neck.\""

# ==============================================================================
# CALCULATE RISK
# ==============================================================================

    # FAIL CHANCE (0–100): higher = more likely to fail

    # Friction increases difficulty because the boss values the journalist less due to caste/religion
    #$ odds_convince = 35 + (suspicion * 10) + pc.get_profile_friction()

    $ risk_convince = 20 + suspicion * 5 + int(pc.get_profile_friction() * 0.4)
    $ risk_convince = min(85, risk_convince)
    
    # Going solo is safer socially (boss doesn't yell at you now) but riskier later (no cover)
    #Not used? 
    #$ odds_solo = 10 

# ==============================================================================
# CHOICE
# ==============================================================================


    menu:
        "How do you handle the dossier?"
        "Present the file on the riots.":
            jump quest_journalist_boss_confrontation
        "Say it was nothing. Go solo.":
            jump quest_journalist_go_solo

    # call screen risk_assessment_menu_2options(
    #     pc,
    #     prompt="How do you handle the dossier?",
    #     option1="Present the file on the riots.", option1tt="{}% Chance of Rejection".format(odds_convince), 
    #     option2="Say it was nothing. Go solo.", option2tt="Safest now, riskier later."
    # )
    # $ chosen_approach = _return

    # if chosen_approach == "Present the file on the riots.":
    #     jump quest_journalist_boss_confrontation
    # else:
    #     jump quest_journalist_go_solo

# ==============================================================================
# CHOICE
# ==============================================================================

label quest_journalist_boss_confrontation:

    "You place the file on the desk."
    "\"The riots… it's been years since that,\", your boss says."
    " \"And you want us to dredge this up now? Why?\""

    menu:
        "Frame it as a major scoop":
            "\"This is the story everyone is afraid to write. It will put this paper on the map.\""
            # Slight bonus for appealing to greed
            $ risk_convince -= 10 
        
        "Focus on inconsistencies":
            "\"The official reports don't match the body count. It's sloppy. We can prove it.\""

    $ risk_convince = max(5, min(85, risk_convince))
    $ current_outcome = perform_roll(risk_convince)

    if current_outcome == "good":
        "The boss sighs, tapping a pen against the desk."
        "\"Alright. Fine. But do not expect the news agency to back you up if you’re caught.\""
        ""
        $ institutional_cover = "Some" 
        jump quest_journalist_infiltration
    else:
        "The boss shoves the file back at you."
        "\"We print news, not ghost stories. Get back to work.\""
        "You take the file. You're doing this without them anwyays!"
        $ institutional_cover = "None"
        jump quest_journalist_infiltration


label quest_journalist_go_solo:
    
    "You hesitate."
    "\"Nothing,\" you say. \"Just checking the deadline.\""


    "You walk away, clutching the dossier tighter."
    "If the paper won't sanction the investigation, you will become the investigation."
    $ institutional_cover = "None"
    
    jump quest_journalist_infiltration

# ==============================================================================
# PART 2: Going Undercover
# ==============================================================================


label quest_journalist_infiltration:

    scene art quest
    with fade

    "Weeks later."
    "You have used your connections to slip into the Ministry's annual gala as a server."


    "The room is upside down: The people who ordered the violence are here, eating tiny cakes, laughing."
    "While the people who suffered are serving the drinks."

    "You spot a corrupt official near the balcony."
    "They are speaking in low tones about 'cleaning up the loose ends' from the riots."

    "You need that conversation recorded."

# ==============================================================================
# CALCULATE RISK 
# ==============================================================================

    #$ risk_record = 30 + (suspicion * 10) + pc.get_profile_friction()
    $ risk_record = 30 + suspicion * 6 + int(pc.get_profile_friction() * 0.5)


    if institutional_cover == "Some":
        $ risk_record -= 10  # news agency protection
    else:
        $ risk_record += 10  # no backup, higher risk

    $ risk_record = max(5, min(90, risk_record))


# ==============================================================================
# CHOICE 
# ==============================================================================
    menu:
        "How do you get the evidence?"
        "Get close with a hidden mic (risky).":
            $ current_outcome = perform_roll(risk_record)
            if current_outcome == "good":
                jump quest_journalist_success_major
            else:
                jump quest_journalist_caught
        "Lip read from a distance.":
            jump quest_journalist_success_minor

    # call screen risk_assessment_menu_2options(
    #     pc,
    #     prompt="How do you get the evidence?",
    #     option1="Get close with a hidden mic.", option1tt="{}% Chance of Caught".format(odds_record), 
    #     option2="Lip read from a distance.", option2tt="Safe, but might miss details."
    # )
    # $ chosen_approach = _return

    # if chosen_approach == "Get close with a hidden mic.":
    #     $ current_outcome = perform_roll_tom(odds_record)
    #     if current_outcome == "good":
    #         jump quest_journalist_success_major
    #     else:
    #         jump quest_journalist_caught
    # else:
    #     # Lip reading is safer but gives less impact
    #     jump quest_journalist_success_minor


# ==============================================================================
# BIG SUCCESS
# ==============================================================================

label quest_journalist_success_major:
    
    "You drift closer with a tray of champagne."
    "The official is drunk on power."
    "\"The cover-up held,\" they say clearly. \"Religion A was never a threat, but the fear... the fear was useful.\""
    
    "Your recorder catches every word."
    "You slip away into the kitchen, heart hammering."
    
    $ seeds_of_change += 4
    jump quest_journalist_epilogue

# ==============================================================================
# MODERATE SUCCESS
# ==============================================================================
label quest_journalist_success_minor:

    "You stay back in the shadows."
    "You catch phrases: \"...never a threat...\" and \"...useful fear...\""
    "You write it down on a napkin immediately."
    
    "It's not a recording, but it's a lead. It's the start of a thread you can pull."
    
    $ seeds_of_change += 2
    jump quest_journalist_epilogue


# ==============================================================================
# FAIL
# ==============================================================================
label quest_journalist_caught:

    "You step too close."
    "The official turns, eyes narrowing."
    "\"You. I don't recognize you.\""

    "Security is called."
    "You have to dump the recording device in a flowerpot to avoid arrest."
    
    "You are thrown out, not arrested, but your cover is blown."
    "You lost the evidence, but you saw their fear. You know you are right."

    $ suspicion += 2
    $ seeds_of_change += 1
    
    jump quest_journalist_failure_epilogue

# ==============================================================================
# EPILOGUE(S)
# ==============================================================================

label quest_journalist_epilogue:

    scene black
    with fade

    "The story runs on Sunday."

    if institutional_cover == "None":
        "It runs on an anonymous blog, not the front page."
        "But it spreads. Whispers turn into conversations."
    else:
        "It runs on the front page. The city stops to read it."

    "You successfully expose the truth to the public."

    "Somewhere, a politician sweats. Somewhere, a survivor feels seen."

    #return
    jump quest_exit_cover_up


label quest_journalist_failure_epilogue:

    scene black
    with fade

    "You are back at your desk the next day."
    "The dossier is still there, but now you are watched."
    
    "The story is suppressed."

    
    "But you remember."
    "And now, they know that someone remembers."

    #return
    jump quest_exit_cover_up


label quest_exit_cover_up(title="Quest Complete", body="", failed=False):
    call end_quest
    call screen quest_summary(title=title, body=body)
    return