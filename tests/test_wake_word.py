# tests/test_wake_word.py

import unittest
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.wake_word_listener import SAMI_WAKE_WORDS

class TestWakeWordDetection(unittest.TestCase):
    
    def test_sami_wake_words_set(self):
        """Test that all Sami variations are in the wake words set."""
        expected_sami_words = {"sami", "sammy", "samy", "samee", "saami", "sahmi", "sammi", "sam"}
        self.assertEqual(SAMI_WAKE_WORDS, expected_sami_words)
    
    def test_wake_words_are_lowercase(self):
        """Test that all wake words are lowercase."""
        for word in SAMI_WAKE_WORDS:
            self.assertEqual(word, word.lower())

if __name__ == "__main__":
    unittest.main()