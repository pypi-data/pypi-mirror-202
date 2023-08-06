import unittest
from src.commons.utils import is_site

class TestIsSite(unittest.TestCase):

    def test_1262_YukonJusticeCentre_Site_xlsm_is_site(self):
        self.assertEqual(is_site("1262-YukonJusticeCentre-Site.xlsm"), True, "Should be True")

    def test_1278_LiquorWarehouse_amp_Offices_Site1_xlsm_is_site(self):
        self.assertEqual(is_site("1278-LiquorWarehouse&amp;Offices-Site1.xlsm"), True, "Should be True")

if __name__ == '__main__':
    unittest.main()
