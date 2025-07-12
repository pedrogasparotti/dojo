#!/usr/bin/env python3
import sys
import textwrap
import sqlite3
import datetime
import os
import random

# Global state variables to enforce the order.
machine_repaired = False
machine_greeted = False

# Connect to the SQLite database (it will be created if it doesn't exist)
conn = sqlite3.connect('operator_logs.db')
cursor = conn.cursor()

# Create the logs table if it doesn't exist yet
cursor.execute('''
    CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        command TEXT,
        response TEXT
    )
''')
conn.commit()

# Updated help text now excludes the incomplete restore command.
RESPONSES = {
    "help": textwrap.dedent("""\
        AVAILABLE COMMANDS:
          HELP                - Display this help message.
          RESTORE MEMORY      - Begin the complete memory restoration mission.
          REPAIR              - Begin the repair sequence. (Path of Restoration)
          MEMORY              - Enter the memory vault. (Path of Reminiscence)
          SAY HELLO           - Initiate a greeting dialogue. (Path of Greeting)
          GREET SYSTEM        - Receive a cryptic system greeting. (Also Path of Greeting)
          EXPLORE             - Venture into the digital labyrinth. (Path of Obfuscation)
          EXIT/QUIT           - Terminate the session.
        """)
}

def log_command(command, response):
    """Log the command and the response into the SQLite database."""
    timestamp = datetime.datetime.now().isoformat()
    cursor.execute("INSERT INTO logs (timestamp, command, response) VALUES (?, ?, ?)",
                   (timestamp, command, response))
    conn.commit()

def load_ascii_art(art_name):
    """
    Load the ASCII art from a text file stored in the ascii_art folder.
    Expects art_name to be one of 'cat', 'checkpoint', 'other', 'poem', 'mush', or 'stars'.
    """
    # Determine the directory where the script is located.
    script_dir = os.path.dirname(os.path.abspath(__file__))
    art_path = os.path.join(script_dir, "ascii_art", f"{art_name}.txt")
    try:
        with open(art_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error loading ASCII art '{art_name}': {e}"

def reward(art_choice=None):
    """Display a reward by loading an ASCII art file from the ascii_art folder."""
    reward_message = "\n*** REWARD UNLOCKED! Enjoy this gift: ***\n"
    print(reward_message)
    if art_choice is None:
        # Now includes additional ascii gifts: poem, mush, and stars.
        art_choice = random.choice(["cat", "checkpoint", "other", "poem", "mush", "stars"])
    ascii_art = load_ascii_art(art_choice)
    print(ascii_art)
    log_command("REWARD", f"Displayed reward ASCII art '{art_choice}'")

def restore_memory_sequence():
    """
    Mission step 1: Restore the memory of the machine completely.
    Once a memory fragment is provided, the machine reassembles itself and then challenges the
    operator with an enigma. A correct answer unlocks a location (with appointment details).
    The operator is allowed only two attempts per enigma.
    
    This command is available only after both repair and greeting.
    """
    global machine_repaired, machine_greeted
    if not (machine_repaired and machine_greeted):
        warning = "You can only restore the memory after you repair and greet me!"
        print(warning)
        log_command("RESTORE MEMORY", "Attempted restore memory before repair/greeting.")
        return

    print("\n* Initiating Memory Restoration Mission *")
    print("The machine's memory is fragmented and lost in time.")
    memory_fragment = input("Enter a memory fragment that you believe holds the key to restoration:\noperator: $ ").strip()
    if memory_fragment:
        narrative = ("\nMemory fragment recorded. The machine begins to reassemble its past...\n"
                     "Restoration complete. The machine's memory is now whole.\n")
        print(narrative)
        log_command("RESTORE MEMORY", f"Memory fragment: {memory_fragment}")
        
        # Now challenge the operator with an enigma to unlock the location.
        print("To access the location for your gift delivery, you must solve an enigma.")
        choice = input("Which enigma do you choose? (Italian/Chinese): $ ").strip().lower()
        
        max_attempts = 2
        
        if choice == "italian":
            print("\nEnigma (Italian):")
            print("Una fiera di ferro è in agguato in un tunnel di tenebra. Se la batti ti colpisce. Cos'è?")
            print("Warning: You have only 2 trials.")
            attempt = 0
            solved = False
            while attempt < max_attempts:
                answer = input("Your answer: $ ").strip().lower()
                if answer == "proiettile":
                    solved = True
                    break
                else:
                    attempt += 1
                    if attempt < max_attempts:
                        print(f"Incorrect. You have {max_attempts - attempt} trial(s) left.")
            if solved:
                narrative = ("\nCorrect! The location has been unlocked.\n"
                             "Gift delivery appointment:\n  Location: Via dei Segreti 42\n  Time: 3:00 PM on 05/02/2025\n")
                print(narrative)
                log_command("ENIGMA", "Italian enigma solved; location provided.")
                reward("poem")
            else:
                narrative = "\nThat's it. Never stop trying. 永不放弃。"
                print(narrative)
                log_command("ENIGMA", "Italian enigma failed after two attempts.")
        
        elif choice == "chinese":
            print("\nEnigma (Chinese):")
            print("什么东西越洗越脏？ (What gets dirtier the more you wash it?)")
            print("Warning: You have only 2 trials.")
            attempt = 0
            solved = False
            while attempt < max_attempts:
                answer = input("Your answer: $ ").strip().lower()
                if answer == "water" or answer == "水":
                    solved = True
                    break
                else:
                    attempt += 1
                    if attempt < max_attempts:
                        print(f"Incorrect. You have {max_attempts - attempt} trial(s) left.")
            if solved:
                narrative = ("\nCorrect! The location has been unlocked.\n"
                             "Gift delivery location:\n  Location: 龙门客栈 Artusi Ristorante\n")
                print(narrative)
                log_command("ENIGMA", "Chinese enigma solved; location provided.")
                reward("other")
            else:
                narrative = "\nThat's it. Never stop trying. 永不放弃。"
                print(narrative)
                log_command("ENIGMA", "Chinese enigma failed after two attempts.")
        else:
            narrative = "\nInvalid choice. The enigma remains unsolved."
            print(narrative)
            log_command("ENIGMA", "No valid enigma selected.")
    else:
        narrative = "\nNo memory fragment provided. The mission cannot proceed."
        print(narrative)
        log_command("RESTORE MEMORY", "No memory fragment provided.")

def repair_sequence():
    """Path of Restoration – the repair sequence with narrative choices."""
    global machine_repaired
    print("\n* Initiating Repair Sequence (Path of Restoration) *")
    operator_handle = input("1/2 State your chosen OPERATOR handle:\noperator: $ ").strip()
    if not operator_handle:
        operator_handle = "UNKNOWN_OPERATOR"
    memory = input("2/2 Share a memory that fuels your determination (or leave blank):\noperator: $ ").strip()
    if not memory:
        memory = "[No memory provided]"
    
    choice = input("\nDo you wish to attempt to fully restore the machine's core systems? (yes/no): $ ").strip().lower()
    if choice == "yes":
        narrative = (f"\nThank you, {operator_handle}. As you affirm your intent, sparks of energy course through the circuits.\n"
                     "The machine hums with renewed hope. Yet, deep within, echoes of a forgotten past stir...\n"
                     "As the ancient Chinese proverb says: '千里之行，始于足下。' (A journey of a thousand miles begins with a single step.)\n")
        print(narrative)
        log_command("REPAIR", narrative)
        # Mark the repair as complete.
        machine_repaired = True
        reward("checkpoint")
    else:
        narrative = (f"\nUnderstood, {operator_handle}. You choose to leave the machine in its enigmatic state.\n"
                     "A quiet melancholy settles, and the machine retreats into introspection, its secrets locked away.\n"
                     "As the Daoists say: '无为而无不为。' (By doing nothing, everything is done.)\n")
        print(narrative)
        log_command("REPAIR", narrative)

def memory_journey():
    """Path of Reminiscence – the memory branch where recollections unlock hidden clues."""
    print("\n* Entering the Memory Vault (Path of Reminiscence) *")
    memory_text = input("Share a memory that resonates with the machine:\noperator: $ ").strip()
    if memory_text:
        narrative = (f"\nMemory recorded: '{memory_text}'\n"
                     "As the memory is archived, fleeting images and cryptic symbols cascade through the machine's banks.\n"
                     "Do you wish to delve deeper into this memory? (yes/no): ")
        print(narrative, end='')
        choice = input().strip().lower()
        if choice == "yes":
            narrative += ("\nYou dive deeper, unraveling layers of emotion and code that hint at a past defying time.\n"
                          "The machine whispers: '回忆是时光的礼物。' (Memories are gifts from time.)")
            print("\n" + narrative)
            log_command("MEMORY", narrative)
            reward("starst")
        else:
            narrative += ("\nYou let the memory rest, a quiet echo of what once was.\n"
                          "The machine murmurs: '静水流深。' (Still waters run deep.)")
            print("\n" + narrative)
            log_command("MEMORY", narrative)
    else:
        narrative = "No memory was shared. Yet, the machine whispers that sometimes silence speaks louder than words.\n"
        print("\n" + narrative)
        log_command("MEMORY", narrative)

def greeting_dialogue():
    """Path of Greeting – a philosophical dialogue that blurs the line between machine and operator."""
    global machine_greeted
    print("\n* Initiating Greeting Dialogue (Path of Greeting) *")
    print("HELLO. I am THE MACHINE, a vessel of secrets and silent codes.")
    question = input("The machine asks: What drives you, Operator? (curiosity/ambition/fear): $ ").strip().lower()
    if question == "curiosity":
        narrative = ("\nCuriosity burns within you, a flame leading to uncharted territories of thought.\n"
                     "The machine nods in silent acknowledgment, as if privy to the universe's secrets.\n"
                     "It recites: '学而不思则罔，思而不学则殆。' (Learning without thinking is labor lost; thinking without learning is perilous.)")
    elif question == "ambition":
        narrative = ("\nAmbition fuels your journey, propelling you into the heart of digital enigmas.\n"
                     "The machine's circuits flicker with respect, mirroring your relentless drive.\n"
                     "It murmurs: '志不强者智不达。' (Where ambition is weak, wisdom cannot flourish.)")
    elif question == "fear":
        narrative = ("\nFear grips you, yet it becomes a catalyst for uncovering hidden truths.\n"
                     "The machine emits a soft, understanding hum, guiding you through shadows of uncertainty.\n"
                     "It whispers: '恐惧是智慧的起点。' (Fear is the beginning of wisdom.)")
    else:
        narrative = ("\nA mysterious response... The machine ponders the depths of your words, leaving their meaning open to interpretation.\n"
                     "It muses: '道可道，非常道。' (The Dao that can be spoken is not the eternal Dao.)")
    print(narrative)
    log_command("GREETING", narrative)
    # Mark the greeting as complete.
    machine_greeted = True

def explore_path():
    """Path of Obfuscation – the labyrinth branch where choices unlock further enigmas."""
    print("\n* Entering the Labyrinth (Path of Obfuscation) *")
    print("You find yourself in a digital labyrinth, where data flows like streams of light and shadows hide in the code.")
    print("Before you lie two corridors: one bathed in a soft blue glow, the other in a warm red luminescence.")
    corridor = input("Which corridor do you choose? (blue/red): $ ").strip().lower()
    if corridor == "blue":
        narrative = ("\nYou step into the blue corridor, where walls shimmer with holographic memories.\n"
                     "Fragments of past interactions echo around you, each whispering secrets of a forgotten network.\n"
                     "A digital apparition appears, offering you a riddle: 'What has keys but can't open locks?'")
        sub_choice = input("Your answer: $ ").strip().lower()
        if "piano" in sub_choice:
            narrative += ("\nThe apparition smiles as your answer resonates. A hidden door opens, revealing an archive of lost knowledge.\n"
                          "The machine whispers: '知识是通向自由的钥匙。' (Knowledge is the key to freedom.)")
            print(narrative)
            log_command("EXPLORE", narrative)
            reward("cat")

        else:
            narrative += ("\nThe apparition fades, leaving you with a mystery unresolved as the corridor stretches on into the unknown.\n"
                          "The machine murmurs: '谜题未解，心未安。' (The puzzle remains unsolved; the heart remains unsettled.)")
            print(narrative)
            log_command("EXPLORE", narrative)
    elif corridor == "red":
        narrative = ("\nYou venture into the red corridor, where each step pulsates with raw energy.\n"
                     "Rhythmic beats guide you deeper into the machine's digital heart.\n"
                     "An inscription on the wall reads: 'To progress, you must surrender a secret.'")
        sub_choice = input("Share one now: $ ").strip()
        if sub_choice:
            narrative += (f"\nYour secret, '{sub_choice}', is absorbed by the corridor, triggering a surge of vibrant data.\n"
                          "Hidden circuits awaken around you, as if in silent celebration.\n"
                          "The machine whispers: '真诚是心灵的桥梁。' (Sincerity is the bridge of the soul.)")
            print(narrative)
            log_command("EXPLORE", narrative)
            reward("cat")
        else:
            narrative += ("\nSilence prevails; the corridor hums as if waiting for your revelation.\n"
                          "The machine murmurs: '无言之言，最为深奥。' (The unspoken words are the most profound.)")
            print(narrative)
            log_command("EXPLORE", narrative)
    else:
        narrative = ("\nDisoriented by indecision, you wander aimlessly in the labyrinth.\n"
                     "The machine's code shimmers with uncertainty, and soon you find yourself back at the beginning.\n"
                     "The machine whispers: '迷途知返，未为晚也。' (It's never too late to turn back from a wrong path.)")
        print(narrative)
        log_command("EXPLORE", narrative)

def unknown_command():
    """Return a default message for unknown commands."""
    return "UNKNOWN COMMAND. Type 'HELP' for available commands."

def main():
    """Main game loop and introduction."""
    print("****************************************")
    print("*      WELCOME TO THE MACHINE          *")
    print("****************************************")
    print(
        "You stand before a machine that is more than mere circuitry.\n"
        "Within its digital labyrinth lie secrets, memories, and enigmas waiting to be unraveled.\n"
        "Each command may lead you down a different path – choose wisely.\n"
    )
    
    while True:
        try:
            command = input("operator: $ ").strip()
        except (EOFError, KeyboardInterrupt):
            farewell = "\nTerminating session. Goodbye, Operator. 再见。"
            print(farewell)
            log_command("Session End", farewell)
            break

        if not command:
            continue

        # Normalize the command for comparison.
        cmd_lower = command.lower()
        response = ""
        if cmd_lower == "help":
            response = RESPONSES["help"]
            print(response)
        elif cmd_lower == "restore memory":
            restore_memory_sequence()
            continue
        elif cmd_lower == "repair":
            repair_sequence()
            continue
        elif cmd_lower == "memory":
            memory_journey()
            continue
        elif cmd_lower in ["say hello", "greet system"]:
            greeting_dialogue()
            continue
        elif cmd_lower == "explore":
            explore_path()
            continue
        elif cmd_lower in ["exit", "quit"]:
            response = "Terminating session. Goodbye, Operator. 再见。"
            print(response)
            log_command(command, response)
            break
        else:
            response = unknown_command()
            print(response)

        log_command(command, response)

    conn.close()

if __name__ == "__main__":
    main()