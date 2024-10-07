import random
from words import word_list


def display_welcome_message():
    """
    Display the game's introduction and obtain a valid username from the player.  # noqa
    Returns the validated username.
    """
    print("\n" + "*" * 70)
    print("*  HANGMAN ADVENTURE: THE WORD QUEST                               *")  # noqa
    print("*" + "-" * 68 + "*")
    print("*  Mission: Decode the secret word and rescue the stick figure!    *")  # noqa
    print("*  Rules of Engagement:                                            *")  # noqa
    print("*   - Guess letters or the entire word                             *")  # noqa
    print("*   - Each mistake brings the stick figure closer to peril         *")  # noqa
    print("*   - Use standard English letters only                            *")  # noqa
    print("*   - The secret words are drawn from the world of espionage       *")  # noqa
    print("*   - Full word guesses must match the secret word's length        *")  # noqa
    print("*" + "-" * 68 + "*")
    print("*  Are you ready to begin your lexical journey?                    *")  # noqa
    print("*" * 70 + "\n")

    while True:
        print("Agent, your codename must be 1-10 letters long, English alphabet only.")  # noqa
        codename = input("Enter your secret agent codename: ").strip().capitalize()  # noqa
        if codename.isalpha() and 1 <= len(codename) <= 10:
            print(f"\nWelcome, Agent {codename}! Your word-saving mission starts now.\n")  # noqa
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
    """Conduct a single round of the Hangman game."""
    score = 0  
    points_per_letter = 5  
    points_per_word = 20
    penalty_points = 5

    masked_word = "_" * len(word)
    has_guessed_correctly = False
    correct_guesses = []
    incorrect_guesses = []
    guessed_full_words = []
    remaining_lives = 6

    print(display_hangman(remaining_lives))
    print(f"This word has {len(word)} letters.\n")
    print(masked_word, "\n")

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
                    print(f"Incorrect letter guess! {penalty_points} points deducted.")
                else:
                    print("Incorrect letter guess! Not enough points to deduct.")
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
                    print(f"Incorrect full word guess! {penalty_points} points deducted.")
                else:
                    print("Incorrect full word guess! Not enough points to deduct.")
                print(f"Score after deduction: {score}")
            else:
                has_guessed_correctly = True
                masked_word = word
                score += points_per_word

        else:
            print("Invalid input. Please guess either a single letter or the full word.")  # noqa

        print(display_hangman(remaining_lives))
        print(f"The word contains {len(word)} letters.\n")
        print(masked_word, "\n")
        print(f"Correct letters guessed: {', '.join(sorted(correct_guesses))}")
        print(f"Incorrect letters guessed: {', '.join(sorted(incorrect_guesses))}")  # noqa
        print(f"Complete words guessed: {', '.join(guessed_full_words)}", "\n")
        print(f"Current Score: {score}")

    if has_guessed_correctly:
        print("Well done! You've successfully saved the hangman!\n")
    else:
        print(f"Oh no! You've run out of attempts. The word was '{word}'. Better luck next time.\n")  # noqa
        
    ask_to_play_again()

# Entry point of the script


if __name__ == "__main__":
    while display_welcome_message():
        word = get_word()
        play_round(word)
    print("Thanks for playing!")

