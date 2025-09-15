# tests/test_wake_word.py

import unittest
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.wake_word_listener import SARAH_WAKE_WORDS

class TestWakeWordDetection(unittest.TestCase):
    
    def test_sarah_wake_words_set(self):
        """Test that all Sarah variations are in the wake words set."""
        expected_sarah_words = {"sarah", "sara", "sarra", "sarah", "sahra", "sahara", "sari", "sarae"}
        self.assertEqual(SARAH_WAKE_WORDS, expected_sarah_words)
    
    def test_wake_words_are_lowercase(self):
        """Test that all wake words are lowercase."""
        for word in SARAH_WAKE_WORDS:
            self.assertEqual(word, word.lower())

if __name__ == "__main__":
    unittest.main()