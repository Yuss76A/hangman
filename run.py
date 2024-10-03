import random
from words import word_list

def display_welcome_message():
    """Show a welcome message and request a valid username from the player."""
    print("=" * 66)
    print("|| Welcome to the Hangman Challenge!                             ||")
    print("|| Your goal is to uncover the hidden word and save the stickman.||")
    print("|| Guess one letter at a time, or attempt to guess the full word.||")
    print("|| Each incorrect guess costs you a life and moves the stickman  ||")
    print("|| closer to danger!                                             ||")
    print("|| Use only letters from the English alphabet.                  ||")
    print("|| If guessing a word, ensure it matches the length of the hidden||")
    print("|| word.                                                        ||")
    print("|| Enter a username to begin your quest!                         ||")
    print("=" * 66)
    print()

    while True:
        username = input("Please enter a username:").strip()
        if username.isalpha() and 1 <= len(username) <= 10:
            print(f"\nWelcome, {username}! Let's start the game!\n")
            return username
        else:
            print("Username must contain 1 to 10 letters from the English alphabet.\n")

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
    guessed_chars = []
    guessed_full_words = []
    remaining_lives = 6

    print(display_hangman(remaining_lives))
    print(f"This word has {len(word)} letters.\n")
    print(masked_word, "\n")

    while not has_guessed_correctly and remaining_lives > 0:
        suggestion = input("Enter your guess (letter or word): ").strip().upper()

        if len(suggestion) == 1 and suggestion.isalpha():
            if suggestion in guessed_chars:
                print(f"You've already guessed the letter '{suggestion}'. Try again.")
            elif suggestion not in word:
                print(f"Unfortunately, '{suggestion}' is not in the word.")
                remaining_lives -= 1
                guessed_chars.append(suggestion)
            else:
                print(f"Nice job! '{suggestion}' is present in the word.")
                guessed_chars.append(suggestion)
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
        print(f"Letters guessed so far: {guessed_chars}")
        print(f"Complete words guessed so far: {guessed_full_words}", "\n")

    
    if has_guessed_correctly:
        print("Well done! You've successfully saved the hangman!\n")
    else:
        print(f"Oh no! You've run out of attempts. The word was '{word}'. Better luck next time.\n")

    ask_to_play_again()
