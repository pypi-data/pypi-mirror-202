import unittest
from src.commons.utils import sqlescape

class TestSqlScape(unittest.TestCase):

    def test_sql_escape_simple_string(self):
        self.assertEqual(sqlescape("ABC"), "ABC", "Should be ABC")
    
    def test_sql_escape_a_string_with_line_breaks(self):
        self.assertEqual(sqlescape("ABC\nD\n\nEF"), "ABC' || CHR(13) || 'D' || CHR(13) || '' || CHR(13) || 'EF", "Should be ABC' || CHR(13) || 'D' || CHR(13) || '' || CHR(13) || 'EF")

    def test_sql_escape_a_string_with_single_quotes(self):
        self.assertEqual(sqlescape("A'B'C"), "A' || CHR(39) || 'B' || CHR(39) || 'C", "Should be A' || CHAR(39) || 'B' || CHAR(39) || 'C' || CHR(13) || 'DEF")

if __name__ == '__main__':
    unittest.main()
