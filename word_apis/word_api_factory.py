from .wordle_api import get_todays_word
from .random_word_api import get_random_word

class ApiFactory:
    @staticmethod
    def get_word_from_api(choice: int):
        if choice == 1:
            return get_todays_word()
        elif choice == 2:
            return get_random_word()
        
def get_word_from_api(choice):
    return ApiFactory.get_word_from_api(choice)