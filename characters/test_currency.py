from evennia.utils.create import create_object
from misc.test_resources import HecateTest

class TestCurrency(HecateTest):
    def test_copper_to_coin_dict(self):
        copper = 8323
        coin_dict = self.char1.currency.copper_to_coin_dict(copper)
        self.assertEqual(323, coin_dict['copper'])
        self.assertEqual(8, coin_dict['silver'])
        self.assertEqual(0, coin_dict['gold'])
        self.assertEqual(0, coin_dict['plat'])
