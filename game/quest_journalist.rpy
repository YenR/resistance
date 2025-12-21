$ news_company_backing = None

label quest_04:
    stop music

    scene black
    with fade

    "{i}Once upon a time, there was a nation.{/i}"

    "{i}It spoke of unity.\nIt spoke of progress.\nIt never seemed to address the shadows.{/i}"

    "{i}But the shadows had stories of their own.{/i}"

    "{i}Every citizen was given a narrative.\nA carefully crafted account of history, of belonging, of duty.\nIt was broadcast from every screen, echoed in every classroom.{/i}"

    "{i}The narrative spoke of a glorious past.\nThe narrative spoke of a harmonious present.\nThere were no dissenting voices.{/i}"

    "{i}And slowly, people stopped questioning the broadcast.\nThen they stopped sharing their own experiences.\nThey stopped remembering a time before the broadcast.{/i}"

    "{i}Soon enough, it began to sound like the truth they knew was all there ever was.{/i}"

    
    #play music indian journalist

    # 1. HIDE THE TEXTBOX
    # This ensures the user doesn't see the empty dialogue box.
    window hide

    # 2. SET THE SCENE
    # 'scene black' clears the screen. 
    # Then we show your title image. 'truecenter' aligns it perfectly.
    scene black
    #show expression "images/quest1_page.png" as title_img at truecenter

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

    "Please select who is going to resist the government."


    # Then the player chooses their character
    call character_select

    "It\'s another busy workday at the news office."

    "You take in the controlled chaos of chipped desks, flickering fluorescent lights, and the clatter of repurposed typewriters."

    "The air smells faintly of stale chai and cheap paper."

    "Your boss sits behind their desk. An island of controlled order amongst the chaos."

    "They do not look up as you approach."

    "\"You wanted to see me. Make it quick. Deadline\'s breathing down my neck.\""

    "You clutch your dossier."
    
    "The riots. The cover-up. The names."

    "You remember the smoke."
    
    "You remember the silence that came after."

    "You\'re not going to let the truth of the riots remain buried."
    
    "But you need the newspaper\'s support if you\'re gonna pull this off."

    menu:
        "How do you approach?"

        "Present your file on past riots in the country, detailing potential government involvement and the need for investigation.":
            jump quest_journalist_office_present
        
        "Hint towards your research to test the waters.":
            jump quest_journalist_office_hint

        "Say it was nothing. Begin the investigation by yourself.":
            jump quest_journalist_office_nothing
        
label quest_journalist_office_present:
    "You slam the folder down. Gently."

    "\"The Riots from a few years ago...\", you say"
    
    "\"They weren't a clash, they were a purge.\""

    "The boss stops typing."

    "Slowly, they look at the file. They see the victims' names."

    "They see the reports you have gathered."

    "They understand the implication."

    "They turn to you with an expression of distaste on their face."

    "\"That's ancient history,\" they say."

    "\"Why dredge this up now? The readership doesn't want to read about... that community.\""

    if pc.social_capital >= 50:
        jump quest_journalist_office_present_success
    else:
        jump quest_journalist_office_present_fail

    

label quest_journalist_office_present_success:
    "The boss flips a page."

    "Pauses on a photograph of a burning shop."

    "They sigh. It's not empathy, it's calculation."

    "\"If we run this... the Ministry will pull our ads.\""

    "They look up, eyes hard."

    "\"But if we don't, the foreign press will.\""

    "\"Get me a confession. A real one. On tape.\""

    "\"And don't use your press pass. If you get caught... well, you know how police treat people from your neighborhood.\""

    $ news_company_backing = "High"

    "You have the Editor's reluctant backing."

    jump quest_journalist_infiltration_briefing


label quest_journalist_office_present_fail:
    "The boss pushes the file back."

    "\"You people,\" they sigh."

    "\"Always looking for wounds to salt.\""

    "\"We report 'National News'. Not sectarian grievances.\""

    "\"Get back to your desk.... Or clear it out.\""

    "You take the file."

    "Your hands are shaking. Not from fear."

    "From rage."

    "You know exactly why they won't run it."

    "You're doing this anyway."

    $ news_company_backing = "None"

    jump quest_journalist_infiltration_briefing

label quest_journalist_office_hint:
    "You hesitate."

    "You mention a 'corruption piece' regarding the gala."

    "You leave out the riots. You leave out the blood."

    "The boss waves a hand."

    "\"Politics as usual? Fine. But don't waste resources.\""

    "It's a half-approval."

    "You have no backup, but you haven't been fired."

    $ news_company_backing = "Medium"

    jump quest_journalist_infiltration_briefing

label quest_journalist_office_nothing:
    "You look at the boss."

    "You look at the comfortable chair, the sacred thread on their wrist, the indifference."

    "\"Nothing,\" you say."

    "\"Just checking the sports layout.\""

    "You walk out."

    "This way, they can't say no."

    "But if you scream for help, no one is coming."

    $ news_company_backing = "None"

    jump quest_journalist_infiltration_briefing

label quest_journalist_infiltration_briefing:
    with fade

    "You make your way to the Gala at night."

    "Celebrating 'Unity Day'."

    "Held in the Minister's private compound."

    "The people who gave the orders will be there."
    
    "Drinking champagne."
    
    "Laughing."

    "You stand outside the perimeter."
    
    "Security is tight."
    


