"""
Wordle API Package - Fetch daily Wordle words from NYT
"""

from .api import WordleAPI, get_todays_word

__all__ = ['WordleAPI', 'get_todays_word']