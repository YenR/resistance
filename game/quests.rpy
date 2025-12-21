

label quest_03:
    "Placeholder for Quest 3."

    jump map 


label quest_02:


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

    # Give the player some exposition
    "Some expositional stuff happens. Describe scene here..."

    # Then the player has a choice where they see probabilities of their action
    window hide
    call screen risk_assessment_menu(
        pc,
        prompt="How do you approach the situation?",
        option1_name="Loud", option1_type="loud",
        option2_name="Quiet", option2_type="quiet",
        option3_name="Violent", option3_type="violent"
    )

    # The screen returns the type chosen (e.g., "loud")
    $ chosen_approach = _return

    # Dice Rolling Animation
    #show text "{size=50}CALCULATING RISK...{/size}" at truecenter
    #pause 2.0 # Suspense

    # Calculate result logic
    $ current_outcome = perform_roll(pc, chosen_approach)

    #hide text

    # Outcome & Aftermath
    if current_outcome == "good":
        #"SUCCESS!"
        "The plan worked better than expected. Your stats aligned perfectly with the moment."
    elif current_outcome == "mixed":
        #"PARTIAL SUCCESS."
        "You managed to do it, but at a cost. The system noticed you."
    else:
        #"FAILURE."
        "Disaster. The system pushed back hard."

    # Conditional text based on stats
    if pc.get_profile_friction() > 5:
        "Because your Targeting Level is high, a drone lingers over you specifically, recording your face."

    # Escalation & Second Choice
    "The situation escalates. ........ You have another moment to react"

    menu:
        "Disperse into the crowd immediately.":
            $ final_choice = "flee"
        "Stand your ground and document the abuse.":
            $ final_choice = "document"
        "Call your NGO contact for legal aid.":
            $ final_choice = "legal"

    # Epilogue Reflection
    if final_choice == "flee":
        "You vanished into the night. Safe, but the message was weak."
    elif final_choice == "document":
        "You have footage. It might help later, but you are now on a watchlist."

    #  Final Text & Loop
    "The quest concludes. The struggle continues elsewhere."

    #jump quest_hub
    jump map

    jump map 
    