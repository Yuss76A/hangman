import random
from words import word_list
import os
import time
import sys

def clear_screen():
    """
    Clear the console screen.
    Uses 'cls' command for Windows and 'clear' for Unix-based systems.
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def typewriter_effect(text, delay=0.01):
    """Simulates a typewriter effect for the given text."""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()


def walk_out():
    hangman = [
        "  O  ",
        " /|\\ ",
        " / \\ "
    ]
    screen_width = os.get_terminal_size().columns
    screen_height = os.get_terminal_size().lines

    # Calculate the starting and ending positions for the hangman
    start_x = 0
    start_y = int(screen_height / 2) - 2
    end_x = screen_width - len(hangman[0])
    end_y = int(screen_height / 2) - 2

    for i in range(screen_width // len(hangman[0])):
        clear_screen()

        # Display the success message above the hangman
        success_message = "The secret agent 003 was saved! Good job, agent!"
        print("\033[{};{}H{}".format(start_y - 2, int(screen_width / 2) - len(success_message) // 2, success_message))

        # Display the moving hangman
        for j, line in enumerate(hangman):
            print("\033[{};{}H{}".format(start_y + j, start_x, line))
        time.sleep(0.3)

        # Move the hangman towards the end position
        start_x += len(hangman[0])
        if start_x > end_x:
            break
    

def fall_from_tree():
    """
    Animate the hangman falling from the tree.
    Displays a series of ASCII frames showing the hangman's descent.
    """

    stages = [
        """
           --------
           |      |
           |      O
           |     \\|/
           |      |
           |     / \\
           -
        """,
        """
           --------
           |      
           |      O
           |     \\|/
           |      |
           |     / \\
           -
        """,
        """
           --------
           |      
           |      
           |      O
           |     \\|/
           |      |
           -     / \\
        """,
        """
           --------
           |      
           |      
           |      
           |      O
           |     \\|/
           -      |
                 / \\
        """,
        """
           --------
           |      
           |      
           |      
           |      
           |      O
           -     \\|/
                  |
                 / \\
        """
    ]
    for stage in stages:
        clear_screen()
        print(stage)
        time.sleep(0.5)
    print("You failed to save me, Agent.")


def display_welcome_message():
    """
    Display the game's introduction and obtain a valid username from the player.  # noqa
    Returns the validated username.
    """
    message = (
        "\n" + "*" * 70 + "\n"
        "*  HANGMAN ADVENTURE: THE WORD QUEST                               *\n"
        "*" + "-" * 68 + "*\n"
        "*  Mission: Decode the secret word and rescue the stick figure!    *\n"
        "*  Agent 003 is compromised. His life depends on your skills.      *\n"
        "*  His fate is in your knowledge.                                  *\n"
        "*  Rules of Engagement:                                            *\n"
        "*   - Guess letters or the entire word                             *\n"
        "*   - Each mistake brings the stick figure closer to peril         *\n"
        "*   - Use standard English letters only                            *\n"
        "*   - The secret words are drawn from the world of espionage       *\n"
        "*   - Full word guesses must match the secret word's length        *\n"
        "*" + "-" * 68 + "*\n"
        "*  Are you ready to begin your lexical journey?                    *\n"
        
    )
    
    typewriter_effect(message, delay=0.01)

    while True:
        print("Agent, your codename must be 1-10 letters long, English alphabet only.")  # noqa
        codename = input("Enter your secret agent codename: ").strip().capitalize()  # noqa
        if codename.isalpha() and 1 <= len(codename) <= 10:
            typewriter_effect(f"\nWelcome, Agent {codename}! Your word-saving mission starts now.\n", delay=0.01)  # noqa
            return codename
        else:
            print("Invalid codename. Stick to the protocol and try again.\n")


def get_word():
    """Select a random word from the imported word_list."""
    return random.choice(word_list).upper()


def display_hangman(tries):
    """Return a string representation of the hangman for the current number of tries."""  # noqa
    stages = [
        """
           --------
           |      |
           |      O
           |     \\|/
           |      |
           |     / \\
           -
        """,
        """
           --------
           |      |
           |      O
           |     \\|/
           |      |
           |     / 
           -
        """,
        """
           --------
           |      |
           |      O
           |     \\|/
           |      |
           |      
           -
        """,
        """
           --------
           |      |
           |      O
           |     \\|
           |      |
           |     
           -
        """,
        """
           --------
           |      |
           |      O
           |      |
           |      |
           |     
           -
        """,
        """
           --------
           |      |
           |      O
           |    
           |      
           |     
           -
        """,
        """
           --------
           |      |
           |      
           |    
           |      
           |     
           -
        """
    ]
    return stages[tries]


def ask_to_play_again():
    """Prompt the user for a new game and restart or exit based on response."""
    valid_response = False
    while not valid_response:
        response = input("Would you like to play again? (Y/N): ").strip().upper()  # noqa
        if response.startswith('Y'):
            chosen_word = get_word()
            play_round(chosen_word)
            valid_response = True
        elif response.startswith('N'):
            print("Thanks for playing! Goodbye.")
            exit()
        else:
            print("Invalid response. Please enter 'Y' for yes or 'N' for no.")


def play_round(word):
    """Conduct a single round of the Hangman game.
    This function manages the game logic, including user input,
    score tracking, and game state updates.
    """
    score = 0  
    points_per_letter = 5  
    points_per_word = 20
    penalty_points = 5

    masked_word = ["_" for _ in word]
    has_guessed_correctly = False
    correct_guesses = []
    incorrect_guesses = []
    guessed_full_words = []
    remaining_lives = 6

    print(display_hangman(remaining_lives))
    print(f"This word has {len(word)} letters.\n")
    print(" ".join(masked_word), "\n")

    while not has_guessed_correctly and remaining_lives > 0:
        suggestion = input("Enter your guess (letter or word): ").strip().upper()  # noqa

        if len(suggestion) == 1 and suggestion.isalpha():
            if suggestion in correct_guesses or suggestion in incorrect_guesses:  # noqa
                print(f"You've already guessed the letter '{suggestion}'. Try again.")  # noqa
            elif suggestion not in word:
                print(f"Unfortunately, '{suggestion}' is not in the word.")
                remaining_lives -= 1
                incorrect_guesses.append(suggestion)
                if score >= penalty_points:
                    score -= penalty_points
                    print(f"Incorrect letter guess! {penalty_points} points deducted.")  # noqa
                else:
                    print("Incorrect letter guess! Not enough points to deduct.")  # noqa
            else:
                print(f"Nice job! '{suggestion}' is present in the word.")
                correct_guesses.append(suggestion)
                score += points_per_letter
                word_list = list(masked_word)
                for idx, char in enumerate(word):
                    if char == suggestion:
                        word_list[idx] = suggestion
                masked_word = "".join(word_list)
                if "_" not in masked_word:
                    has_guessed_correctly = True

        elif len(suggestion) == len(word) and suggestion.isalpha():
            if suggestion in guessed_full_words:
                print(f"You've already guessed the word '{suggestion}'. Try a different word.")  # noqa
            elif suggestion != word:
                print(f"'{suggestion}' is not the correct word.")
                remaining_lives -= 1
                guessed_full_words.append(suggestion)
                if score >= penalty_points:
                    score -= penalty_points
                    print(f"Incorrect full word guess! {penalty_points} points deducted.")  # noqa
                else:
                    print("Incorrect full word guess! Not enough points to deduct.")  # noqa
                print(f"Score after deduction: {score}")
            else:
                has_guessed_correctly = True
                masked_word = list(word)
                score += points_per_word

        else:
            print("Invalid input. Please guess either a single letter or the full word.")  # noqa

        print(display_hangman(remaining_lives))
        print(f"The word contains {len(word)} letters.\n")
        print(" ".join(masked_word), "\n")
        print(f"Correct letters guessed: {', '.join(sorted(correct_guesses))}")
        print(f"Incorrect letters guessed: {', '.join(sorted(incorrect_guesses))}")  # noqa
        print(f"Complete words guessed: {', '.join(guessed_full_words)}", "\n")
        print(f"Current Score: {score}")

    if has_guessed_correctly:
        print("Well done! You've successfully saved the hangman!\n")
        walk_out()
        time.sleep(2)
    else:
        print(f"You failed, Agent. This failure runs deep. The word was '{word}'. Better luck next time.\n")  # noqa
        time.sleep(3)

        fall_from_tree()

    ask_to_play_again()

# Entry point of the script


if __name__ == "__main__":
    codename = display_welcome_message()
    
    while True:
        word = get_word()
        play_round(word)
    print("Thanks for playing!")
