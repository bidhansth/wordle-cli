from collections import defaultdict
import os
from wordle_api import get_todays_word

class Wordle:
    WORD_LENGTH = 5
    MAX_TRIES = 6
    COLORS = {
        'green': '\033[92m',
        'yellow': '\033[93m',
        'gray': '\033[90m',
        'red': '\033[91m',
        'white': '\033[97m',
        'reset': '\033[0m'
    }
    KEYBOARD = ['QWERTYUIOP','ASDFGHJKL','ZXCVBNM']

    def __init__(self):
        self.welcome()
        self.play()

    @staticmethod
    def line_break(position):
        def decorator(func):
            def wrapper(*args, **kwargs):
                if position in ("top", "both"):
                    print()
                result = func(*args, **kwargs)
                if position in ("bottom", "both"):
                    print()
                return result
            return wrapper
        return decorator
    
    @staticmethod
    def clear(order):
        def decorator(func):
            def wrapper(*args, **kwargs):
                if order in ("before", "both"):
                    os.system('cls' if os.name == 'nt' else 'clear')
                result = func(*args, **kwargs)
                if order in ("after", "both"):
                    os.system('cls' if os.name == 'nt' else 'clear')
                return result
            return wrapper
        return decorator


    @clear("before")
    @line_break("top")
    def welcome(self):
        print("""Welcome to CLI Wordle\n
Please choose a mode:
1. Online Mode (Word fetched from NY Times)
2. Friend Mode (Word input by your friend)\n""")
        while True:
            choice = int(input("Enter your choice (1/2):\t"))
            if choice == 1:
                self.get_word_from_api()
                break
            elif choice == 2:
                self.get_answer()
                break
            else:
                print("Invalid choice.\n")

    def get_word_from_api(self):
        try:
            self.answer = get_todays_word().lower()
        except (ConnectionError, ValueError) as e:
            print(f"""Could not fetch the word from NY Times Server.
Please try again or choose Friend mode.\n
Error: {e}""")
            self.welcome()
        

    @line_break("both")
    @clear("after")
    def get_answer(self):
        while True:
            word = input(f"Enter a {self.WORD_LENGTH} letter word\t")
            if len(word) == self.WORD_LENGTH and word.isalpha():
                self.answer = word.lower()
                os.system('cls' if os.name == 'nt' else 'clear')
                break
            else:
                print(f"Word must be {self.WORD_LENGTH} letters. No numbers or symbols")
    
    @line_break("top")
    @clear("before")
    def display_history(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        for guess, result in self.history:
            colored_guess = ""
            for char, state in zip(guess, result):
                colored_guess += f"{self.COLORS[state]}{char.upper()}{self.COLORS['reset']} "
            print(colored_guess)

    def update_keyboard(self, guess, result):
        for char, state in zip(guess, result):
            if state == "green":
                self.letter_status[char] = state
            elif state == "yellow":
                if self.letter_status[char] != "green":
                    self.letter_status[char] = state
            elif state == "white":
                if self.letter_status[char] not in ("green", "yellow"):
                    self.letter_status[char] = "red"

    @line_break("both")
    def display_keyboard(self):
        for row in self.KEYBOARD:
            display_row = ""
            for letter in row:
                color = self.COLORS[self.letter_status[letter.lower()]]
                display_row += f"{color}{letter}{self.COLORS['reset']} "
            print(display_row)

    def play(self):
        self.history = []
        self.letter_status = defaultdict(lambda: "gray")
        tries = 1
        win = False

        while tries <= self.MAX_TRIES:
            guess = input(f"Guess {tries}/{self.MAX_TRIES}\t").lower()
            if len(guess) != self.WORD_LENGTH or not guess.isalpha():
                print(f"Guess must be {self.WORD_LENGTH} letters. No numbers or symbols")
                continue

            win = self.evaluate(guess)
            if win:
                print(f"Congrats! You guessed the word in {tries} tries.\n")
                break

            tries += 1
        
        if not win:
            print(f"""Sorry, you're out of tries.
The word was {self.answer}""")
            
        self.rerun()
            
    def rerun(self):
        if input("Would you like to play again? (y/n):\t").lower() == "y":
            self.welcome()
            self.play()


    def evaluate(self, guess: str) -> bool:
        result = [""] * self.WORD_LENGTH #to track user's guesses letters as green/yellow
        remaining_letters = list(self.answer) #to store which letters to check

        for i in range(self.WORD_LENGTH):
            if guess[i] == self.answer[i]:
                result[i] = "green" #track correct letters
                remaining_letters[i] = None #remove correct letter from being checked in next step for yellow

        for i in range(self.WORD_LENGTH):
            if result[i] == "": #do not check green letters
                if guess[i] in remaining_letters: #correct letter in incorrect place
                    result[i] = "yellow"
                    remaining_letters[remaining_letters.index(guess[i])] = None
                    #letter must be removed from remaining letters to avoid duplicate yellow letters
                else:
                    result[i] = "white"
        
        self.history.append((guess, result))
        self.display_history()
        self.update_keyboard(guess, result)
        self.display_keyboard()
        if guess == self.answer:
            return True
            
if __name__ == "__main__":
    Wordle()