import requests
from datetime import datetime
from typing import Optional

class WordleAPI:
    BASE_URL = "https://www.nytimes.com/svc/wordle/v2"
    
    @classmethod
    def get_todays_word(cls) -> str:
        today = datetime.now().strftime("%Y-%m-%d")

        url = f"{cls.BASE_URL}/{today}.json"
        
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            word = data.get('solution')
            if not word:
                raise ValueError("API response does not contain a valid word")
            
            return word.lower()
            
        except requests.exceptions.Timeout:
            raise ConnectionError("Request timed out. The API may be unavailable.")
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Failed to fetch word from API: {e}")
        except (KeyError, ValueError) as e:
            raise ValueError(f"Invalid API response format: {e}")

def get_todays_word() -> str:
    return WordleAPI.get_todays_word()