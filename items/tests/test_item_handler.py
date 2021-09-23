from evennia.utils.create import create_object
from evennia.prototypes.spawner import spawn

from misc import coin
from misc.test_resources import HecateTest

class TestItemHandler(HecateTest):
    def setUp(self):
        super().setUp()
        self.obj_loc = self.room1

    def setup_two_silver_coins(self):
        coin1_copper = 1_000 # (0 plat, 0 gold, 1 silver, 0 copper)
        coin2_copper = 1_000 # (0 plat, 0 gold, 1 silver, 0 copper)
        # Total value of coin1 + coin2 = 1,226,306 (0 plat, 0 gold, 2 silver, 30 copper)

        coin1 = coin.generate_coin_object(copper=coin1_copper)
        coin2 = coin.generate_coin_object(copper=coin2_copper)

        self.two_silver_coins = [coin1, coin2]
        for coin_obj in self.two_silver_coins:
            coin_obj.location = self.obj_loc

    def setup_two_coin_piles(self):
        coin1_copper = 328_982 # (0 plat, 0 gold, 328 silver, 982 copper)
        coin2_copper = 897_324 # (0 plat, 0 gold, 897 silver, 324 copper)
        # Total value of coin1 + coin2 = 1,226,306 (0 plat, 1 gold, 226 silver, 306 copper)

        coin1 = coin.generate_coin_object(copper=coin1_copper)
        coin2 = coin.generate_coin_object(copper=coin2_copper)

        self.two_coin_groupables = [coin1, coin2]
        for coin_obj in self.two_coin_groupables:
            coin_obj.location = self.obj_loc

    def setup_three_coin_piles(self):
        coin1_copper = 389_294 # (0 plat, 0 gold, 389 silver, 294 copper)
        coin2_copper = 849_283 # (0 plat, 0 gold, 849 silver, 283 copper)
        coin3_copper = 289_748 # (0 plat, 0 gold, 289 silver, 748 copper)
        # Total value of coin3 + coin4 + coin5 = 1,528,325 (0 plat, 1 gold, 528 silver, 325 copper)

        coin3 = coin.generate_coin_object(copper=coin1_copper)
        coin4 = coin.generate_coin_object(copper=coin2_copper)
        coin5 = coin.generate_coin_object(copper=coin3_copper)

        self.three_coin_groupables = [coin3, coin4, coin5]
        for coin_obj in self.three_coin_groupables:
            coin_obj.location = self.obj_loc

        # Total value of coins 1-5 = 2,754,631 (0 plat, 2 gold, 754 silver, 631 copper)

        #--------------------------
    def setup_three_torches(self):
        torch1 = spawn('crudely-made torch')[0]
        torch2 = spawn('crudely-made torch')[0]
        torch3 = spawn('crudely-made torch')[0]
        self.three_torch_groupables = [torch1, torch2, torch3]
        for torch in self.three_torch_groupables:
            torch.location = self.obj_loc

        #--------------------------
    def setup_variety_groupables(self):
        chalk1 = create_object(typeclass="items.objects.Object", key="piece of chalk",
            location=self.obj_loc)
        chalk1.tags.add('inventory', category='groupable')

        towel1 = create_object(typeclass="items.objects.Object", key="dirty towel",
            location=self.obj_loc)
        towel1.tags.add('inventory', category='groupable')

        cup1 = create_object(typeclass="items.objects.Object", key="tin cup",
            location=self.obj_loc)
        cup1.tags.add('inventory', category='groupable')

        self.variety_groupables = [chalk1, towel1, cup1]

        #---------------------------
    def setup_qty_groupables(self):
        rock1 = spawn('rock')[0]
        rock2 = spawn('rock')[0]
        self.qty_groupables = [rock1, rock2]
        for obj in self.qty_groupables:
            obj.location = self.obj_loc

    def test_group_objects1(self):
        """
        Tests the outcome of 2 grouped coins.
        """
        self.setup_two_coin_piles()

        result_msg = self.char1.item.group_objects(self.two_coin_groupables, self.obj_loc)
        expected_msg = "You combine a pile of coins and a pile of coins."
        self.assertEqual(expected_msg, result_msg)

        # Assess the final group object.
        coin_pile = self.obj_loc.contents[-1]
        self.assertTrue(coin_pile is not None)
        self.assertEqual('a pile of coins', coin_pile.key)
        self.assertTrue(coin_pile.is_typeclass("items.objects.Coin", exact=True))
        self.assertTrue(coin_pile.attributes.has('coin'))
        self.assertEqual(0, coin_pile.db.coin['plat'])
        self.assertEqual(1, coin_pile.db.coin['gold'])
        self.assertEqual(226, coin_pile.db.coin['silver'])
        self.assertEqual(306, coin_pile.db.coin['copper'])

    def test_group_objects2(self):
        """
        Tests the outcome of 2 grouped silver coins.
        """
        self.setup_two_silver_coins()

        result_msg = self.char1.item.group_objects(self.two_silver_coins, self.obj_loc)
        expected_msg = "You combine a silver coin and a silver coin."
        self.assertEqual(expected_msg, result_msg)

        # Assess the final group object.
        coin_pile = self.obj_loc.contents[-1]
        self.assertTrue(coin_pile is not None)
        self.assertEqual('a pile of silver coins', coin_pile.key)
        self.assertTrue(coin_pile.is_typeclass("items.objects.Coin", exact=True))
        self.assertTrue(coin_pile.attributes.has('coin'))
        self.assertEqual(0, coin_pile.db.coin['plat'])
        self.assertEqual(0, coin_pile.db.coin['gold'])
        self.assertEqual(2, coin_pile.db.coin['silver'])
        self.assertEqual(0, coin_pile.db.coin['copper'])


    def test_group_objects3(self):
        """
        Tests the outcome of 3 grouped inventory objects that all have the same key.
        """
        self.setup_three_torches()

        result_msg = self.char1.item.group_objects(self.three_torch_groupables, self.obj_loc)
        expected_msg = "You group together some crudely-made torches."
        self.assertEqual(expected_msg, result_msg)

        # Asssess the final group object.
        torch_pile = self.obj_loc.contents[-1]
        self.assertTrue(torch_pile is not None)
        self.assertEqual('a pile of crudely-made torches', torch_pile.key)
        self.assertTrue(torch_pile.is_typeclass("items.objects.InventoryGroup", exact=True))
        self.assertTrue(torch_pile.attributes.has('quantity'))
        self.assertEqual(3, torch_pile.db.quantity)
        self.assertEqual(3, len(torch_pile.contents))
        self.assertEqual("a crudely-made torch", torch_pile.contents[0].key)
        self.assertEqual("a crudely-made torch", torch_pile.contents[1].key)
        self.assertEqual("a crudely-made torch", torch_pile.contents[2].key)

    def test_group_objects4(self):
        """
        Tests the outcome of 3 grouped inventory objects that have different keys.
        """
        self.setup_variety_groupables()

        result_msg = self.char1.item.group_objects(self.variety_groupables, self.obj_loc)
        expected_msg = "You group together piece of chalk, dirty towel, and tin cup."
        self.assertEqual(expected_msg, result_msg)

        # Asssess the final group object.
        variety_pile = self.obj_loc.contents[-1]
        self.assertTrue(variety_pile is not None)
        self.assertEqual('a pile of various items', variety_pile.key)
        self.assertTrue(variety_pile.is_typeclass("items.objects.InventoryGroup", exact=True))
        self.assertTrue(variety_pile.attributes.has('quantity'))
        self.assertEqual(3, variety_pile.db.quantity)
        self.assertEqual(3, len(variety_pile.contents))
        self.assertEqual("piece of chalk", variety_pile.contents[0].key)
        self.assertEqual("dirty towel", variety_pile.contents[1].key)
        self.assertEqual("tin cup", variety_pile.contents[2].key)

    def test_group_objects5(self):
        """
        Tests the outcome of two different types of grouped objects, quantity and inventory, requested
        at the same time.

        Grouping logic should first separate the items into their perspective categories.
        Groups the coins first and places that string at the front of the inventory grouping string
        of the variety items. Results in a combined grouping string.
        """
        self.setup_two_coin_piles()
        self.setup_variety_groupables()

        combined_list = [*self.two_coin_groupables, *self.variety_groupables]
        result_msg = self.char1.item.group_objects(combined_list, self.obj_loc)
        expected_msg = ("You combine a pile of coins and a pile of coins.\n"
                "You group together piece of chalk, dirty towel, tin cup, and a pile of coins.")
        self.assertEqual(expected_msg, result_msg)

        variety_pile = self.obj_loc.contents[-1]

        # Assess the final coin group object.
        coin_pile = variety_pile.contents[-1]
        self.assertTrue(coin_pile is not None)
        self.assertEqual('a pile of coins', coin_pile.key)
        self.assertTrue(coin_pile.is_typeclass("items.objects.Coin", exact=True))
        self.assertTrue(coin_pile.attributes.has('coin'))
        self.assertEqual(0, coin_pile.db.coin['plat'])
        self.assertEqual(1, coin_pile.db.coin['gold'])
        self.assertEqual(226, coin_pile.db.coin['silver'])
        self.assertEqual(306, coin_pile.db.coin['copper'])

        # Asssess the final variety group object.
        
        self.assertTrue(variety_pile is not None)
        self.assertEqual('a pile of various items', variety_pile.key)
        self.assertTrue(variety_pile.is_typeclass("items.objects.InventoryGroup", exact=True))
        self.assertTrue(variety_pile.attributes.has('quantity'))
        self.assertEqual(4, variety_pile.db.quantity)
        self.assertEqual(4, len(variety_pile.contents))
        self.assertEqual("piece of chalk", variety_pile.contents[0].key)
        self.assertEqual("dirty towel", variety_pile.contents[1].key)
        self.assertEqual("tin cup", variety_pile.contents[2].key)

    def test_group_objects6(self):
        """
        Tests the outcome of 2 misc quantity obj and 2 grouped coins.
        """
        self.setup_two_coin_piles()
        self.setup_qty_groupables()

        self.two_coin_groupables.extend(self.qty_groupables)

        result_msg = self.char1.item.group_objects(self.two_coin_groupables, self.obj_loc)
        expected_msg = ("You combine a pile of coins and a pile of coins.\n"
            "You combine 2 rocks.")
        self.assertEqual(expected_msg, result_msg)

    def test_group_coins1(self):
        """
        Tests the outcome of 2 grouped coins.
        """
        self.setup_two_coin_piles()

        self.assertEqual(2, len(self.two_coin_groupables))
        result_msg, coin_pile = self.char1.item._group_coins(self.two_coin_groupables, self.obj_loc)
        expected_msg = "You combine a pile of coins and a pile of coins."
        self.assertEqual(expected_msg, result_msg)

        self.assertTrue(coin_pile.is_typeclass("items.objects.Coin", exact=True))
        self.assertEqual(0, coin_pile.db.coin['plat'])
        self.assertEqual(1, coin_pile.db.coin['gold'])
        self.assertEqual(226, coin_pile.db.coin['silver'])
        self.assertEqual(306, coin_pile.db.coin['copper'])
        self.assertEqual('a pile of coins', coin_pile.key)
        self.assertEqual(self.obj_loc, coin_pile.location)

    def test_group_coins2(self):
        """
        Tests the outcome of 2 grouped silver coins.
        """
        self.setup_two_silver_coins()

        result_msg = self.char1.item.group_objects(self.two_silver_coins, self.obj_loc)
        expected_msg = "You combine a silver coin and a silver coin."
        self.assertEqual(expected_msg, result_msg)

        # Assess the final group object.
        coin_pile = self.obj_loc.contents[-1]
        self.assertTrue(coin_pile is not None)
        self.assertEqual('a pile of silver coins', coin_pile.key)
        self.assertTrue(coin_pile.is_typeclass("items.objects.Coin", exact=True))
        self.assertTrue(coin_pile.attributes.has('coin'))
        self.assertEqual(0, coin_pile.db.coin['plat'])
        self.assertEqual(0, coin_pile.db.coin['gold'])
        self.assertEqual(2, coin_pile.db.coin['silver'])
        self.assertEqual(0, coin_pile.db.coin['copper'])

    def test_group_coins3(self):
        """
        Combines two groups of coins into one.
        """
        self.setup_two_coin_piles()
        self.setup_three_coin_piles()

        self.char1.item._group_coins(self.two_coin_groupables, self.obj_loc)
        self.char1.item._group_coins(self.three_coin_groupables, self.obj_loc)

        coin_groups = [self.obj_loc.contents[-2], self.obj_loc.contents[-1]]

        result_msg, coin_pile = self.char1.item._group_coins(coin_groups, self.obj_loc)
        expected_msg = "You combine a pile of coins and a pile of coins."
        self.assertEqual(expected_msg, result_msg)

        self.assertTrue(coin_pile.is_typeclass("items.objects.Coin", exact=True))
        self.assertEqual(0, coin_pile.db.coin['plat'])
        self.assertEqual(2, coin_pile.db.coin['gold'])
        self.assertEqual(754, coin_pile.db.coin['silver'])
        self.assertEqual(631, coin_pile.db.coin['copper'])
        self.assertEqual('a pile of coins', coin_pile.key)
        self.assertEqual(self.obj_loc, coin_pile.location)

    def test_group_inventory_objects1(self):
        """
        Tests the outcome of 3 grouped inventory objects that all have the same key.
        """
        self.setup_three_torches()

        result_msg = self.char1.item._group_inventory_objects(self.three_torch_groupables,
            self.obj_loc)
        expected_msg = "You group together some crudely-made torches."
        self.assertEqual(expected_msg, result_msg)

        # Asssess the final group object.
        torch_pile = self.obj_loc.contents[-1]
        self.assertTrue(torch_pile is not None)
        self.assertEqual('a pile of crudely-made torches', torch_pile.key)
        self.assertTrue(torch_pile.is_typeclass("items.objects.InventoryGroup", exact=True))
        self.assertTrue(torch_pile.attributes.has('quantity'))
        self.assertEqual(3, torch_pile.db.quantity)
        self.assertEqual(3, len(torch_pile.contents))
        self.assertEqual("a crudely-made torch", torch_pile.contents[0].key)
        self.assertEqual("a crudely-made torch", torch_pile.contents[1].key)
        self.assertEqual("a crudely-made torch", torch_pile.contents[2].key)
    
    def test_group_inventory_objects2(self):
        """
        Tests the outcome of 3 grouped inventory objects that have different keys.
        """
        self.setup_variety_groupables()

        result_msg = self.char1.item._group_inventory_objects(self.variety_groupables, self.obj_loc)
        expected_msg = "You group together piece of chalk, dirty towel, and tin cup."
        self.assertEqual(expected_msg, result_msg)

        # Asssess the final group object.
        variety_pile = self.obj_loc.contents[-1]
        self.assertTrue(variety_pile is not None)
        self.assertEqual('a pile of various items', variety_pile.key)
        self.assertTrue(variety_pile.is_typeclass("items.objects.InventoryGroup", exact=True))
        self.assertTrue(variety_pile.attributes.has('quantity'))
        self.assertEqual(3, variety_pile.db.quantity)
        self.assertEqual(3, len(variety_pile.contents))
        self.assertEqual("piece of chalk", variety_pile.contents[0].key)
        self.assertEqual("dirty towel", variety_pile.contents[1].key)
        self.assertEqual("tin cup", variety_pile.contents[2].key)

    def test_group_inventory_objects3(self):
        """
        Tests the outcome of combining a pile of items with a single item.
        """
        self.setup_three_torches()
        self.setup_variety_groupables()

        self.char1.item.group_objects(self.three_torch_groupables, self.obj_loc)
        torch_pile = self.obj_loc.contents[-1]
        self.char1.item.group_objects(self.variety_groupables, self.obj_loc)
        variety_pile = self.obj_loc.contents[-1]
        piles = [torch_pile, variety_pile]

        result_msg = self.char1.item._group_inventory_objects(piles, self.obj_loc)
        result_pile = self.obj_loc.contents[-1]
        expected_msg = (
            "You combine the contents of a pile of crudely-made torches and a pile of various items.\n"
            "You group together a crudely-made torch, a crudely-made torch, a crudely-made torch, "
            "piece of chalk, dirty towel, and tin cup."
        )

        self.assertEqual(expected_msg, result_msg)
        self.assertEqual("a pile of various items", result_pile.key)
        self.assertTrue(result_pile.is_typeclass("items.objects.InventoryGroup", exact=True))
        self.assertEqual(6, len(result_pile.contents))
        self.assertEqual(6, result_pile.db.quantity)
        self.assertEqual("a crudely-made torch", result_pile.contents[0].key)
        self.assertEqual("a crudely-made torch", result_pile.contents[1].key)
        self.assertEqual("a crudely-made torch", result_pile.contents[2].key)
        self.assertEqual("piece of chalk", result_pile.contents[3].key)
        self.assertEqual("dirty towel", result_pile.contents[4].key)
        self.assertEqual("tin cup", result_pile.contents[5].key)

    def test_ungroup_objects1(self):
        """
        Testing of coin group ungrouping.
        """
        self.setup_two_coin_piles()

        self.char1.item.group_objects(self.two_coin_groupables, self.obj_loc)
        coin_pile = self.obj_loc.contents[-1]

        result_msg = self.char1.item.ungroup_objects(coin_pile, self.obj_loc)
        expected_msg = ("You ungroup a pile of coins, producing a gold coin, a pile of silver coins, "
            "and a pile of copper coins.")
        self.assertEqual(expected_msg, result_msg)

        gold_coin = self.obj_loc.contents[-3]
        silver_pile = self.obj_loc.contents[-2]
        copper_pile = self.obj_loc.contents[-1]

        self.assertEqual(1, gold_coin.db.coin['gold'])
        self.assertEqual('a gold coin', gold_coin.key)
        self.assertEqual(226, silver_pile.db.coin['silver'])
        self.assertEqual(306, copper_pile.db.coin['copper'])

    def test_ungroup_objects2(self):
        """
        Testing of quantity group ungrouping.
        """
        self.setup_qty_groupables()

        self.char1.item.group_objects(self.qty_groupables, self.obj_loc)
        rock_pile = self.obj_loc.contents[-1]

        result_msg = self.char1.item.ungroup_objects(rock_pile, self.obj_loc)
        expected_msg = "You cannot ungroup a homogenized group. Use the split command instead."
        self.assertEqual(expected_msg, result_msg)

    def test_ungroup_objects3(self):
        """
        Testing of inventory group ungrouping, with all same named objects.
        """
        self.setup_three_torches()

        self.char1.item.group_objects(self.three_torch_groupables, self.obj_loc)
        torch_pile = self.obj_loc.contents[-1]

        result_msg = self.char1.item.ungroup_objects(torch_pile, self.obj_loc)
        expected_msg = ("You ungroup a pile of crudely-made torches, producing a crudely-made torch, "
        "a crudely-made torch, and a crudely-made torch.")

        self.assertEqual(expected_msg, result_msg)

    def test_split_group1(self):
        self.setup_two_coin_piles()

        # Total value of coin1 + coin2 = 1,226,306 (0 plat, 1 gold, 226 silver, 306 copper)
        self.char1.item.group_objects(self.two_coin_groupables, self.obj_loc)
        coin_pile = self.obj_loc.contents[-1]

        split_type = 'default'

        result_msg = self.char1.item.split_group(split_type, coin_pile, self.obj_loc)
        expected_msg = "You split a pile of coins into a pile of coins and a pile of coins."
        self.assertEqual(expected_msg, result_msg)

        original_coin_pile = self.obj_loc.contents[-2]
        new_coin_pile = self.obj_loc.contents[-1]

        # Check original coin pile
        plat = original_coin_pile.db.coin['plat']
        gold = original_coin_pile.db.coin['gold']
        silver = original_coin_pile.db.coin['silver']
        copper = original_coin_pile.db.coin['copper']

        self.assertEqual(plat, 0)
        self.assertEqual(gold, 0)
        self.assertEqual(silver, 613)
        self.assertEqual(copper, 153)

        # Check new coin pile
        plat = new_coin_pile.db.coin['plat']
        gold = new_coin_pile.db.coin['gold']
        silver = new_coin_pile.db.coin['silver']
        copper = new_coin_pile.db.coin['copper']

        self.assertEqual(plat, 0)
        self.assertEqual(gold, 0)
        self.assertEqual(silver, 613)
        self.assertEqual(copper, 153)

        # Test splitting 2 silver coins.
        self.setup_two_silver_coins()

        self.char1.item.group_objects(self.two_silver_coins, self.obj_loc)
        coin_pile = self.obj_loc.contents[-1]
        result_msg = self.char1.item.split_group(split_type, coin_pile, self.obj_loc)
        expected_msg = "You split a pile of silver coins into a silver coin and a silver coin."
        self.assertEqual(expected_msg, result_msg)

        # Assess the final 2 coins.
        silver_coin1 = self.obj_loc.contents[-2]
        silver_coin2 = self.obj_loc.contents[-1]

        self.assertEqual('a silver coin', silver_coin1.key)
        self.assertTrue(silver_coin1.is_typeclass("items.objects.Coin", exact=True))
        self.assertTrue(silver_coin1.attributes.has('coin'))
        self.assertEqual(0, silver_coin1.db.coin['plat'])
        self.assertEqual(0, silver_coin1.db.coin['gold'])
        self.assertEqual(1, silver_coin1.db.coin['silver'])
        self.assertEqual(0, silver_coin1.db.coin['copper'])

        self.assertEqual('a silver coin', silver_coin2.key)
        self.assertTrue(silver_coin2.is_typeclass("items.objects.Coin", exact=True))
        self.assertTrue(silver_coin2.attributes.has('coin'))
        self.assertEqual(0, silver_coin2.db.coin['plat'])
        self.assertEqual(0, silver_coin2.db.coin['gold'])
        self.assertEqual(1, silver_coin2.db.coin['silver'])
        self.assertEqual(0, silver_coin2.db.coin['copper'])

    def test_split_group2(self):
        self.setup_two_coin_piles()

        # Total value of coin1 + coin2 = 1,226,306 (0 plat, 1 gold, 226 silver, 306 copper)
        self.char1.item.group_objects(self.two_coin_groupables, self.obj_loc)
        coin_pile = self.obj_loc.contents[-1]

        split_type = 'from'

        result_msg = self.char1.item.split_group(split_type, coin_pile, self.obj_loc, quantity=1,
            extract_obj='gold')
        expected_msg = "You split a gold coin from a pile of coins, leaving a pile of coins."
        self.assertEqual(expected_msg, result_msg)

        original_coin_pile = self.obj_loc.contents[-2]
        gold_coin = self.obj_loc.contents[-1]

        # Check original coin pile
        plat = original_coin_pile.db.coin['plat']
        gold = original_coin_pile.db.coin['gold']
        silver = original_coin_pile.db.coin['silver']
        copper = original_coin_pile.db.coin['copper']

        self.assertEqual(plat, 0)
        self.assertEqual(gold, 0)
        self.assertEqual(silver, 226)
        self.assertEqual(copper, 306)

        # Check gold coin
        plat = gold_coin.db.coin['plat']
        gold = gold_coin.db.coin['gold']
        silver = gold_coin.db.coin['silver']
        copper = gold_coin.db.coin['copper']

        self.assertEqual(plat, 0)
        self.assertEqual(gold, 1)
        self.assertEqual(silver, 0)
        self.assertEqual(copper, 0)
    
    def test_split_group3(self):
        """
        Attempt to split a single copper coin.
        """
        copper_coin = spawn('copper_coin')[0]
        copper_coin.db.coin = coin.copper_to_coin_dict(1)
        copper_coin.location = self.obj_loc

        split_type = 'default'

        result_msg = self.char1.item.split_group(split_type, copper_coin, self.obj_loc)
        expected_msg = "You cannot split 1 copper!"
        self.assertEqual(expected_msg, result_msg)
