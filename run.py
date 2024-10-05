import random
from words import word_list


def display_welcome_message():
    """
    Display the game's introduction and obtain a valid username from the player.
    Returns the validated username.
    """
    print("\n" + "*" * 70)
    print("*  HANGMAN ADVENTURE: THE WORD QUEST                               *")
    print("*" + "-" * 68 + "*")
    print("*  Mission: Decode the secret word and rescue the stick figure!    *")
    print("*  Rules of Engagement:                                            *")
    print("*   - Guess letters or the entire word                             *")
    print("*   - Each mistake brings the stick figure closer to peril         *")
    print("*   - Use standard English letters only                            *")
    print("*   - Full word guesses must match the secret word's length        *")
    print("*" + "-" * 68 + "*")
    print("*  Are you ready to begin your lexical journey?                    *")
    print("*" * 70 + "\n")

    while True:
        print("Agent, your codename must be 1-10 letters long, English alphabet only.")
        codename = input("Enter your secret agent codename: ").strip().capitalize()
        
        if codename.isalpha() and 1 <= len(codename) <= 10:
            print(f"\nWelcome, Agent {codename}! Your word-saving mission starts now.\n")
            return codename
        else:
            print("Invalid codename. Stick to the protocol and try again.\n")


def get_word():
    """Select a random word from the imported word_list."""
    return random.choice(word_list).upper()


def display_hangman(tries):
    """Return a string representation of the hangman for the current number of tries."""
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
        response = input("Would you like to play again? (Y/N): ").strip().upper()
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
        suggestion = input("Enter your guess (letter or word): ").strip().upper()

        if len(suggestion) == 1 and suggestion.isalpha():
            if suggestion in correct_guesses or suggestion in incorrect_guesses:
                print(f"You've already guessed the letter '{suggestion}'. Try again.")
            elif suggestion not in word:
                print(f"Unfortunately, '{suggestion}' is not in the word.")
                remaining_lives -= 1
                incorrect_guesses.append(suggestion)
            else:
                print(f"Nice job! '{suggestion}' is present in the word.")
                correct_guesses.append(suggestion)
                word_list = list(masked_word)
                for idx, char in enumerate(word):
                    if char == suggestion:
                        word_list[idx] = suggestion
                masked_word = "".join(word_list)
                
                if "_" not in masked_word:
                    has_guessed_correctly = True

        elif len(suggestion) == len(word) and suggestion.isalpha():
            if suggestion in guessed_full_words:
                print(f"You've already guessed the word '{suggestion}'. Try a different word.")
            elif suggestion != word:
                print(f"'{suggestion}' is not the correct word.")
                remaining_lives -= 1
                guessed_full_words.append(suggestion)
            else:
                has_guessed_correctly = True
                masked_word = word

        else:
            print("Invalid input. Please guess either a single letter or the full word.")

        print(display_hangman(remaining_lives))
        print(f"The word contains {len(word)} letters.\n")
        print(masked_word, "\n")
        print(f"Correct letters guessed: {', '.join(sorted(correct_guesses))}")
        print(f"Incorrect letters guessed: {', '.join(sorted(incorrect_guesses))}")
        print(f"Complete words guessed: {', '.join(guessed_full_words)}", "\n")

    if has_guessed_correctly:
        print("Well done! You've successfully saved the hangman!\n")
    else:
        print(f"Oh no! You've run out of attempts. The word was '{word}'. Better luck next time.\n")

    ask_to_play_again()

# Entry point of the script


if __name__ == "__main__":
    player_name = display_welcome_message()
    word = get_word()
    play_round(word)