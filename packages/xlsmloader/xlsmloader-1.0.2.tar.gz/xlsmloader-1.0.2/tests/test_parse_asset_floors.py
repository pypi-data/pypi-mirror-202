import unittest
from src.commons.utils import parse_asset_floors

class TestParseAssetFloors(unittest.TestCase):

    def test_parse_asset_floor_1(self):
        self.assertEqual(parse_asset_floors(1), 1, "Should be 1")

    def test_parse_asset_floor_None(self):
        self.assertEqual(parse_asset_floors("None"), 0, "Should be 0")

    def test_parse_asset_floor_2_partially(self):
        self.assertEqual(parse_asset_floors("2 (partially)"), 2, "Should be 2")
    
    def test_parse_asset_floor_1_Mezzanine(self):
        self.assertEqual(parse_asset_floors("1 + Mezzanine"), 1, "Should be 1")
    
    def test_parse_asset_floor_Ground_Level_Exterior_Parking(self):
        self.assertEqual(parse_asset_floors("Ground Level Exterior Parking"), 0, "Should be 0")
    
    def test_parse_asset_floor_1_mechanical_2_floor_222(self):
        self.assertEqual(parse_asset_floors("1 + mechanical 2 floor 222"), 1, "Should be 1")

if __name__ == '__main__':
    unittest.main()
