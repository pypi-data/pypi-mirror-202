import unittest
from src.commons.utils import extract_asset_name

class TestExtractAssertName(unittest.TestCase):

    def test_extract_asset_name_from_1222_Education_Building_Site(self):
        self.assertEqual(extract_asset_name("1222 - Education Building - Site"), "Education Building - Site", "Should be Education Building - Site")

    def test_extract_asset_name_from_Education_Building_Site(self):
        self.assertEqual(extract_asset_name("Education Building - Site"), "Education Building - Site", "Should be Education Building - Site")

    def test_extract_asset_name_from_1446_New_Core_Library_Site(self):
        self.assertEqual(extract_asset_name("1446-New Core Library - Site"), "New Core Library - Site", "Should be New Core Library - Site")

    def test_extract_asset_name_from_1446_New_Core_Library_Site(self):
        self.assertEqual(extract_asset_name("1366   -   Site Teen Parent Centre"), "Site Teen Parent Centre", "Should be Site Teen Parent Centre")

if __name__ == '__main__':
    unittest.main()
