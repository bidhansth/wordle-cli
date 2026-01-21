import requests

class RandomWordAPI:
    WORD_LENGTH = 5
    BASE_URL = "https://random-word-api.herokuapp.com/word"
    
    @classmethod
    def get_random_word(cls) -> str:
        url = f"{cls.BASE_URL}?length={cls.WORD_LENGTH}"
        
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            word = response.json()[0]
            if not word:
                raise ValueError("API response does not contain a valid word")
            
            return word.lower()
            
        except requests.exceptions.Timeout:
            raise ConnectionError("Request timed out. The API may be unavailable.")
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Failed to fetch word from API: {e}")
        except (KeyError, ValueError) as e:
            raise ValueError(f"Invalid API response format: {e}")

def get_random_word() -> str:
    return RandomWordAPI.get_random_word()