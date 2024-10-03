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