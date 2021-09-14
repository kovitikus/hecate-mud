from misc.test_resources import HecateTest
from misc import coin

class TestCoin(HecateTest):
    def setUp(self):
        super().setUp()
        self.coin_dict1 = {'plat': 27, 'gold': 48, 'silver': 125, 'copper': 88}
        self.coin_dict2 = {'plat': 233, 'gold': 0, 'silver': 41, 'copper': 0}

    def test_return_all_coin_types(self):
        plat, gold, silver, copper = coin.return_all_coin_types(coin_dict=self.coin_dict1)
        self.assertEqual( 27, plat)
        self.assertEqual( 48, gold)
        self.assertEqual( 125, silver)
        self.assertEqual( 88, copper)

    def test_copper_to_coin_dict(self):
        copper = 8323
        coin_dict = coin.copper_to_coin_dict(copper)
        self.assertEqual(323, coin_dict['copper'])
        self.assertEqual(8, coin_dict['silver'])
        self.assertEqual(0, coin_dict['gold'])
        self.assertEqual(0, coin_dict['plat'])

    def test_all_coin_types_to_string(self):
        coin_str = (f"{self.coin_dict1['plat']}p {self.coin_dict1['gold']}g "
            f"{self.coin_dict1['silver']}s {self.coin_dict1['copper']}c")
        result_str = coin.all_coin_types_to_string(self.coin_dict1)
        self.assertEqual(coin_str, result_str)

    def test_positive_coin_types_to_string(self):
        coin_str = f"{self.coin_dict2['plat']}p {self.coin_dict2['silver']}s"
        result_str = coin.positive_coin_types_to_string(self.coin_dict2)
        self.assertEqual(coin_str, result_str)

    def test_balance_coin_dict(self):
        unbalanced_coin_dict = {'plat': 2358, 'gold': 1280, 'silver': 998, 'copper': 2200}
        balanced_coin_dict = {'plat': 2359, 'gold': 281, 'silver': 0, 'copper': 200}

        result_coin_dict = coin.balance_coin_dict(unbalanced_coin_dict)
        self.assertEqual(balanced_coin_dict['plat'], result_coin_dict['plat'])
        self.assertEqual(balanced_coin_dict['gold'], result_coin_dict['gold'])
        self.assertEqual(balanced_coin_dict['silver'], result_coin_dict['silver'])
        self.assertEqual(balanced_coin_dict['copper'], result_coin_dict['copper'])

    def test_convert_coin_type(self):
        plat = 2
        gold = 2
        silver = 2
        copper = 2

        plat_result = coin.convert_coin_type(plat=plat, gold=gold, silver=silver,
            copper=copper, result_type='plat')
        self.assertEqual(2.002002002, plat_result)

        gold_result = coin.convert_coin_type(plat=plat, gold=gold, silver=silver,
            copper=copper, result_type='gold')
        self.assertEqual(2_002.002002, gold_result)

        silver_result = coin.convert_coin_type(plat=plat, gold=gold, silver=silver,
            copper=copper, result_type='silver')
        self.assertEqual(2_002_002.002, silver_result)

        copper_result = coin.convert_coin_type(plat=plat, gold=gold, silver=silver,
            copper=copper)
        self.assertEqual(2_002_002_002, copper_result)

    def test_create_coin_dict(self):
        plat = 55
        gold = 55
        silver = 55
        copper = 55

        result_dict = coin.create_coin_dict(plat=plat, gold=gold, silver=silver,
            copper=copper)
        self.assertEqual(plat, result_dict['plat'])
        self.assertEqual(gold, result_dict['gold'])
        self.assertEqual(silver, result_dict['silver'])
        self.assertEqual(copper, result_dict['copper'])

    def test_coin_dict_to_copper(self):
        coin_dict = {}
        coin_dict['plat'] = 2
        coin_dict['gold'] = 2
        coin_dict['silver'] = 2
        coin_dict['copper'] = 2

        copper_result = coin.coin_dict_to_copper(coin_dict)
        self.assertEqual(2_002_002_002, copper_result)

    def test_copper_to_coin_dict(self):
        copper = 2_002_002_002

        result_dict = coin.copper_to_coin_dict(copper)
        self.assertEqual(2, result_dict['plat'])
        self.assertEqual(2, result_dict['gold'])
        self.assertEqual(2, result_dict['silver'])
        self.assertEqual(2, result_dict['copper'])
