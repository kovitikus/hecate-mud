from evennia.utils.create import create_object
from evennia.prototypes.spawner import spawn
from misc.test_resources import HecateTest

class TestItemHandler(HecateTest):
    def setUp(self):
        super().setUp()
        self.obj_loc = self.room1
        coin1_value = 328982 # (0 plat, 0 gold, 328 silver, 982 copper)
        coin2_value = 897324 # (0 plat, 0 gold, 897 silver, 324 copper)
        # Total value of coin1 + coin2 = 1,226,306 (0 plat, 1 gold, 226 silver, 306 copper)

        coin1 = spawn('coin_pile')[0]
        coin1.db.coin = coin1.currency.copper_to_coin_dict(coin1_value)
        coin2 = spawn('coin_pile')[0]
        coin2.db.coin = coin2.currency.copper_to_coin_dict(coin2_value)

        self.two_coin_groupables = [coin1, coin2]
        for coin in self.two_coin_groupables:
            coin.location = self.obj_loc

        coin3_value = 389294
        coin4_value = 849283
        coin5_value = 289748
        # Total value of coin3 + coin4 + coin5 = 1,528,325 (0 plat, 1 gold, 528 silver, 325 copper)

        coin3 = spawn('coin_pile')[0]
        coin3.db.coin = coin3.currency.copper_to_coin_dict(coin3_value)
        coin4 = spawn('coin_pile')[0]
        coin4.db.coin = coin4.currency.copper_to_coin_dict(coin4_value)
        coin5 = spawn('coin_pile')[0]
        coin5.db.coin = coin5.currency.copper_to_coin_dict(coin5_value)

        self.three_coin_groupables = [coin3, coin4, coin5]
        for coin in self.three_coin_groupables:
            coin.location = self.obj_loc

        # Total value of coins 1-5 = 2,754,631 (0 plat, 2 gold, 754 silver, 631 copper)

        #--------------------------

        torch1 = spawn('crudely-made torch')[0]
        torch2 = spawn('crudely-made torch')[0]
        torch3 = spawn('crudely-made torch')[0]
        self.three_torch_groupables = [torch1, torch2, torch3]
        for torch in self.three_torch_groupables:
            torch.location = self.obj_loc

        #--------------------------

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

        rock1 = spawn('rock')[0]
        rock2 = spawn('rock')[0]
        self.qty_groupables = [rock1, rock2]
        for obj in self.qty_groupables:
            obj.location = self.obj_loc

    def test_group_objects1(self):
        """
        Tests the outcome of 2 grouped coins.
        """
        final_msg = self.char1.item.group_objects(self.two_coin_groupables, self.obj_loc)
        self.assertEqual("You combine a pile of coins and a pile of coins.", final_msg)

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
        Tests the outcome of 3 grouped inventory objects that all have the same key.
        """
        final_msg = self.char1.item.group_objects(self.three_torch_groupables, self.obj_loc)
        self.assertEqual("You group together some crudely-made torches.", final_msg)

        # Asssess the final group object.
        torch_pile = self.obj_loc.contents[-1]
        self.assertTrue(torch_pile is not None)
        self.assertEqual('a pile of crudely-made torches', torch_pile.key)
        self.assertTrue(torch_pile.is_typeclass("items.objects.InventoryGroup", exact=True))
        self.assertTrue(torch_pile.attributes.has('quantity'))
        self.assertEqual(3, torch_pile.db.quantity)
        self.assertEqual(3, len(torch_pile.contents))
        self.assertEqual("crudely-made torch", torch_pile.contents[0].key)
        self.assertEqual("crudely-made torch", torch_pile.contents[1].key)
        self.assertEqual("crudely-made torch", torch_pile.contents[2].key)

    def test_group_objects3(self):
        """
        Tests the outcome of 3 grouped inventory objects that have different keys.
        """
        final_msg = self.char1.item.group_objects(self.variety_groupables, self.obj_loc)
        self.assertEqual("You group together piece of chalk, dirty towel, and tin cup.", final_msg)

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

    def test_group_objects4(self):
        """
        Tests the outcome of two different types of grouped objects, quantity and inventory, requested
        at the same time.

        Grouping logic should first separate the items into their perspective categories.
        Groups the coins first and places that string at the front of the inventory grouping string
        of the variety items. Results in a combined grouping string.
        """
        combined_list = [*self.two_coin_groupables, *self.variety_groupables]
        final_msg = self.char1.item.group_objects(combined_list, self.obj_loc)
        temp = ("You combine a pile of coins and a pile of coins.\n"
                "You group together piece of chalk, dirty towel, tin cup, and a pile of coins.")
        self.assertEqual(temp, final_msg)

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

    def test_group_objects5(self):
        """
        Tests the outcome of 2 misc quantity obj and 2 grouped coins.
        """
        self.two_coin_groupables.extend(self.qty_groupables)

        final_msg = self.char1.item.group_objects(self.two_coin_groupables, self.obj_loc)
        expected_str = ("You combine a pile of coins and a pile of coins.\n"
            "You combine 2 rocks.")
        self.assertEqual(expected_str, final_msg)

    def test_group_coins1(self):
        """
        Tests the outcome of 2 grouped coins.
        """
        self.assertEqual(2, len(self.two_coin_groupables))
        final_msg = self.char1.item._group_coins(self.two_coin_groupables, self.obj_loc)
        coin_pile = self.obj_loc.contents[-1]
        self.assertTrue(coin_pile.is_typeclass("items.objects.Coin", exact=True))
        self.assertEqual(0, coin_pile.db.coin['plat'])
        self.assertEqual(1, coin_pile.db.coin['gold'])
        self.assertEqual(226, coin_pile.db.coin['silver'])
        self.assertEqual(306, coin_pile.db.coin['copper'])
        self.assertEqual('a pile of coins', coin_pile.key)
        self.assertEqual(self.obj_loc, coin_pile.location)

    def test_group_coins2(self):
        """
        Combines two groups of coins into one.
        """
        self.char1.item._group_coins(self.two_coin_groupables, self.obj_loc)
        self.char1.item._group_coins(self.three_coin_groupables, self.obj_loc)

        coin_groups = [self.obj_loc.contents[-2], self.obj_loc.contents[-1]]

        final_msg = self.char1.item._group_coins(coin_groups, self.obj_loc)
        coin_pile = self.obj_loc.contents[-1]
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
        final_msg = self.char1.item._group_inventory_objects(self.three_torch_groupables, self.obj_loc)
        self.assertEqual("You group together some crudely-made torches.", final_msg)

        # Asssess the final group object.
        torch_pile = self.obj_loc.contents[-1]
        self.assertTrue(torch_pile is not None)
        self.assertEqual('a pile of crudely-made torches', torch_pile.key)
        self.assertTrue(torch_pile.is_typeclass("items.objects.InventoryGroup", exact=True))
        self.assertTrue(torch_pile.attributes.has('quantity'))
        self.assertEqual(3, torch_pile.db.quantity)
        self.assertEqual(3, len(torch_pile.contents))
        self.assertEqual("crudely-made torch", torch_pile.contents[0].key)
        self.assertEqual("crudely-made torch", torch_pile.contents[1].key)
        self.assertEqual("crudely-made torch", torch_pile.contents[2].key)
    
    def test_group_inventory_objects2(self):
        """
        Tests the outcome of 3 grouped inventory objects that have different keys.
        """
        final_msg = self.char1.item._group_inventory_objects(self.variety_groupables, self.obj_loc)
        self.assertEqual("You group together piece of chalk, dirty towel, and tin cup.", final_msg)

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
        self.char1.item.group_objects(self.three_torch_groupables, self.obj_loc)
        torch_pile = self.obj_loc.contents[-1]
        self.char1.item.group_objects(self.variety_groupables, self.obj_loc)
        variety_pile = self.obj_loc.contents[-1]
        piles = [torch_pile, variety_pile]

        result_str = self.char1.item._group_inventory_objects(piles, self.obj_loc)
        result_pile = self.obj_loc.contents[-1]
        expected_str = (
            "You combine the contents of a pile of crudely-made torches and a pile of various items.\n"
            "You group together crudely-made torch, crudely-made torch, crudely-made torch, "
            "piece of chalk, dirty towel, and tin cup."
        )

        self.assertEqual(expected_str, result_str)
        self.assertEqual("a pile of various items", result_pile.key)
        self.assertTrue(result_pile.is_typeclass("items.objects.InventoryGroup", exact=True))
        self.assertEqual(6, len(result_pile.contents))
        self.assertEqual(6, result_pile.db.quantity)
        self.assertEqual("crudely-made torch", result_pile.contents[0].key)
        self.assertEqual("crudely-made torch", result_pile.contents[1].key)
        self.assertEqual("crudely-made torch", result_pile.contents[2].key)
        self.assertEqual("piece of chalk", result_pile.contents[3].key)
        self.assertEqual("dirty towel", result_pile.contents[4].key)
        self.assertEqual("tin cup", result_pile.contents[5].key)

    def test_ungroup_objects(self):
        self.char1.item.group_objects(self.two_coin_groupables, self.obj_loc)
        coin_pile = self.obj_loc.contents[-1]

        final_msg = self.char1.item.ungroup_objects(coin_pile, self.obj_loc)
        expected_msg = ("You ungroup a pile of coins, producing a gold coin, a pile of silver coins, "
            "and a pile of copper coins.")
        self.assertEqual(expected_msg, final_msg)

        gold_coin = self.obj_loc.contents[-3]
        silver_pile = self.obj_loc.contents[-2]
        copper_pile = self.obj_loc.contents[-1]

        self.assertEqual(1, gold_coin.db.coin['gold'])
        self.assertEqual('a gold coin', gold_coin.key)
        self.assertEqual(226, silver_pile.db.coin['silver'])
        self.assertEqual(306, copper_pile.db.coin['copper'])
