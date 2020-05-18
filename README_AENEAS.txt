#valtyr

Notes:
    Named after the main figure in the Roman epic: Aeneid, the aeneas python script is a basic data visualization and organization tool for the Praetorian Crypto challenges.

    This tool has the ability to save last terminal output, fetch current highest unsolved challenge, and submit a solution to the current challenge.

    Aeneas also has the ability to detect a 'user' file which contains the user's email and JWT auth token.
    If a 'user' file is not detected in the current working dir, it creates one with a user specified email and stores the email and token.

Command Line:
    python3 aeneas.py

Help:
    ~type "list" for available commands~
    >list
    AVAILABLE COMMANDS
    hash:   see latest hash
    save:   save last output to progress.txt
    fetch:  retrieve current challenge
    solve:  submit a guess for the current challenge
    exit:   umm exit
