"""
Package for APIS to fetch words
"""

from .wordle_api import get_todays_word
from .random_word_api import get_random_word
from .word_api_factory import get_word_from_api

__all__ = ['get_todays_word', 'get_random_word', 'get_word_from_api']