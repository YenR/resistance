label quest_journalist_briefing:
    
    # 1. SETUP & ATMOSPHERE
    stop music fadeout 2.0
    scene black
    with fade

    #default suspicion = 0
    #default seeds_of_change = 0

    # 2. THE "ONCE UPON A TIME" INTRO (Theme requirement)
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
    ""

    # 3. TITLE CARD
    window hide
    scene black
    # Placeholder for a title image, similar to quest_mini.rpy
    show expression "images/Quest_page_Shadow.png" as title_img at truecenter
    with Dissolve(3.0)
    pause
    hide title_img
    with Dissolve(1.0)
    window show

    "Please select who is going to resist the narrative."
    # Assuming character_select is a global call defined elsewhere
    call character_select

    jump quest_journalist_office


label quest_journalist_office:

    # BEAT 1: THE BRIEFING (The Boss)
    
    scene office quest 
    # Placeholder background name
    with fade

    "It’s another busy workday at the news office."
    "A controlled chaos of chipped desks, flickering fluorescent lights, and clatter of repurposed typewriters."
    "The air smells faintly of stale chai and cheap paper."

    "You see your boss sitting behind their desk, an island of controlled order amidst the surrounding mess."
    ""

    "You clutch the dossier you’ve spent countless nights preparing."
    "Your notes are practically spilling out."

    "You remember the riots. You remember the silence that followed."
    "And you remember a truth buried beneath layers of carefully constructed lies."

    "Your boss speaks without looking up."
    "\"You wanted to see me. Make it quick. Deadline’s breathing down my neck.\""
    ""

    # CALCULATE ODDS
    # Friction increases difficulty because the boss values the journalist less due to caste/religion
    $ odds_convince = 35 + (suspicion * 10) + pc.get_profile_friction()
    
    # Going solo is safer socially (boss doesn't yell at you now) but riskier later (no cover)
    $ odds_solo = 10 

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


label quest_journalist_boss_confrontation:

    "You place the file on the desk."
    "\"The riots… it's been years since that,\", your boss says."
    " \"And you want us to dredge this up now? Why?\""

    menu:
        "Frame it as a major scoop":
            "\"This is the story everyone is afraid to write. It will put this paper on the map.\""
            # Slight bonus for appealing to greed
            $ odds_convince -= 10 
        
        "Focus on inconsistencies":
            "\"The official reports don't match the body count. It's sloppy. We can prove it.\""

    $ current_outcome = perform_roll_tom(odds_convince)

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
    ""

    "You walk away, clutching the dossier tighter."
    "If the paper won't sanction the investigation, you will become the investigation."
    $ institutional_cover = "None"
    
    jump quest_journalist_infiltration


label quest_journalist_infiltration:

    # BEAT 2: THE APPROACH (Going Undercover)

    scene art quest
    with fade

    "Weeks later."
    "You have used your connections to slip into the Ministry's annual gala as a server."
    ""

    "The room is upside down: The people who ordered the violence are here, eating tiny cakes, laughing."
    "While the people who suffered are serving the drinks."

    "You spot a corrupt official near the balcony."
    "They are speaking in low tones about 'cleaning up the loose ends' from the riots."

    "You need that conversation recorded."

    $ odds_record = 30 + (suspicion * 10) + pc.get_profile_friction()

    

    menu:
        "How do you get the evidence?"
        "Get close with a hidden mic (risky).":
            $ current_outcome = perform_roll_tom(odds_record)
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


label quest_journalist_success_major:
    
    "You drift closer with a tray of champagne."
    "The official is drunk on power."
    "\"The cover-up held,\" they say clearly. \"Religion A was never a threat, but the fear... the fear was useful.\""
    
    "Your recorder catches every word."
    "You slip away into the kitchen, heart hammering."
    
    $ seeds_of_change += 4
    jump quest_journalist_epilogue


label quest_journalist_success_minor:

    "You stay back in the shadows."
    "You catch phrases: \"...never a threat...\" and \"...useful fear...\""
    "You write it down on a napkin immediately."
    
    "It's not a recording, but it's a lead. It's the start of a thread you can pull."
    
    $ seeds_of_change += 2
    jump quest_journalist_epilogue


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


label quest_journalist_epilogue:

    scene black
    with fade

    "The story runs on Sunday."
    "" 
    
    if institutional_cover == "None":
        "It runs on an anonymous blog, not the front page."
        "But it spreads. Whispers turn into conversations."
    else:
        "It runs on the front page. The city stops to read it."

    "You successfully expose the truth to the public."
    ""
    "Somewhere, a politician sweats. Somewhere, a survivor feels seen."

    return


label quest_journalist_failure_epilogue:

    scene black
    with fade

    "You are back at your desk the next day."
    "The dossier is still there, but now you are watched."
    
    "The story is suppressed."
    ""
    
    "But you remember."
    "And now, they know that someone remembers."

    return