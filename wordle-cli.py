class Wordle:
    WORD_LENGTH = 5
    MAX_TRIES = 6

    COLORS = {
        'green': '\033[92m',
        'yellow': '\033[93m',
        'reset': '\033[0m'
    }

    def __init__(self):
        self.welcome()
        self.get_answer()
        self.history = []
        self.play()

    def welcome(self):
        print("Welcome to CLI Wordle")

    def get_answer(self):
        while True:
            word = input(f"Enter a {self.WORD_LENGTH} letter word")
            if len(word) == self.WORD_LENGTH and word.isalpha():
                self.answer = word.lower()
                break
            else:
                print(f"Word must be {self.WORD_LENGTH} letters. No numbers or symbols")

    def display_history(self):
        for guess, result in self.history:
            colored_guess = ""
            for char, state in zip(guess, result):
                colored_guess += f"{self.COLORS[state]}{char.upper()}{self.COLORS['reset']} "
            print(colored_guess)

    def play(self):
        tries = 1
        win = False
        while tries <= self.MAX_TRIES:
            guess = input(f"Guess {tries}/{self.MAX_TRIES}").lower()
            if len(guess) != self.WORD_LENGTH or not guess.isalpha():
                print(f"Guess must be {self.WORD_LENGTH} letters. No numbers or symbols")
                continue
            
            win = self.evaluate(guess)
            if win:
                print(f"Congrats! You guessed the word in {tries} tries.")
                break

            tries += 1
        
        if not win:
            print(f"""Sorry, you're out of tries.
The word was {self.answer}""")

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
                    result[i] = "gray"
        
        self.history.append((guess, result))
        self.display_history()
        if guess == self.answer:
            return True
            
if __name__ == "__main__":
    Wordle()