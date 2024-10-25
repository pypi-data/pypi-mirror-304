# tests/test_dafdo.py
import unittest
from dafdo.parser import DafdoParser

class TestDafdoParser(unittest.TestCase):
    def test_parsing(self):
        code = "<dfd>\nTulis iki 'Halo donya!'\n</jawa>"
        parser = DafdoParser(code)
        result = parser.parse()
        self.assertIn("<p>Halo donya!</p>", result)
        
if __name__ == '__main__':
    unittest.main()
