from evennia.utils.create import create_object
from misc.test_resources import HecateTest

class TestItemHandler(HecateTest):
    def setUp(self):
        super().setUp()
        self.obj_loc = self.room1
        coin1_value = 328982 # (0 plat, 0 gold, 328 silver, 982 copper)
        coin2_value = 897324 # (0 plat, 0 gold, 897 silver, 324 copper)
        # Total value of coin1 + coin2 = 1,226,306 (0 plat, 1 gold, 226 silver, 306 copper)

        coin1 = create_object(typeclass="items.objects.Coin", key="coin1", location=self.obj_loc)
        coin1.db.coin = coin1.currency.copper_to_coin_dict(coin1_value)

        coin2 = create_object(typeclass="items.objects.Coin", key="coin2", location=self.obj_loc)
        coin2.db.coin = coin2.currency.copper_to_coin_dict(coin2_value)

        self.two_coin_groupables = [coin1, coin2]

        #--------------------------

        torch1 = create_object(typeclass="items.objects.Torch", key="crude torch",
            location=self.obj_loc)
        torch2 = create_object(typeclass="items.objects.Torch", key="crude torch",
            location=self.obj_loc)
        torch3 = create_object(typeclass="items.objects.Torch", key="crude torch",
            location=self.obj_loc)
        self.three_torch_groupables = [torch1, torch2, torch3]

        #--------------------------

        chalk1 = create_object(typeclass="items.objects.Object", key="piece of chalk",
            location=self.obj_loc)
        chalk1.tags.add('inventory', category='groupable')

        towel1 = create_object(typeclass="items.objects.Object", key="dirty towel",
            location=self.obj_loc)
        towel1.tags.add('inventory', category='groupable')

        self.variety_groupables = [torch1, chalk1, towel1]

    def test_group_objects1(self):
        """
        Tests the outcome of 2 grouped coins.
        """
        final_msg = self.char1.item.group_objects(self.two_coin_groupables, self.obj_loc)
        self.assertEqual("You group together coin1 and coin2.", final_msg)

        # Assess the final group object.
        coin_pile = self.obj_loc.contents[-1]
        self.assertTrue(coin_pile is not None)
        self.assertEqual('a pile of coins', coin_pile.key)
        self.assertTrue(coin_pile.is_typeclass("items.objects.QuantityGroup", exact=True))
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
        self.assertEqual("You group together some crude torches into a pile.", final_msg)

        # Asssess the final group object.
        torch_pile = self.obj_loc.contents[-1]
        self.assertTrue(torch_pile is not None)
        self.assertEqual('a pile of crude torches', torch_pile.key)
        self.assertTrue(torch_pile.is_typeclass("items.objects.InventoryGroup", exact=True))
        self.assertTrue(torch_pile.attributes.has('quantity'))
        self.assertEqual(3, torch_pile.db.quantity)
        self.assertEqual(3, len(torch_pile.contents))
        self.assertEqual("crude torch", torch_pile.contents[0].key)
        self.assertEqual("crude torch", torch_pile.contents[1].key)
        self.assertEqual("crude torch", torch_pile.contents[2].key)

    def test_group_objects3(self):
        """
        Tests the outcome of 3 grouped inventory objects that have different keys.
        """
        final_msg = self.char1.item.group_objects(self.variety_groupables, self.obj_loc)
        self.assertEqual("You group together crude torch, piece of chalk, and dirty towel into a pile.", final_msg)

        # Asssess the final group object.
        variety_pile = self.obj_loc.contents[-1]
        self.assertTrue(variety_pile is not None)
        self.assertEqual('a pile of various items', variety_pile.key)
        self.assertTrue(variety_pile.is_typeclass("items.objects.InventoryGroup", exact=True))
        self.assertTrue(variety_pile.attributes.has('quantity'))
        self.assertEqual(3, variety_pile.db.quantity)
        self.assertEqual(3, len(variety_pile.contents))
        self.assertEqual("crude torch", variety_pile.contents[0].key)
        self.assertEqual("piece of chalk", variety_pile.contents[1].key)
        self.assertEqual("dirty towel", variety_pile.contents[2].key)

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
        temp = ("You group together coin1 and coin2.\nYou group together crude torch, "
                "piece of chalk, and dirty towel into a pile.")
        self.assertEqual(temp, final_msg)

        # Assess the final coin group object.
        coin_pile = self.obj_loc.contents[-2]
        self.assertTrue(coin_pile is not None)
        self.assertEqual('a pile of coins', coin_pile.key)
        self.assertTrue(coin_pile.is_typeclass("items.objects.QuantityGroup", exact=True))
        self.assertTrue(coin_pile.attributes.has('coin'))
        self.assertEqual(0, coin_pile.db.coin['plat'])
        self.assertEqual(1, coin_pile.db.coin['gold'])
        self.assertEqual(226, coin_pile.db.coin['silver'])
        self.assertEqual(306, coin_pile.db.coin['copper'])

        # Asssess the final variety group object.
        variety_pile = self.obj_loc.contents[-1]
        self.assertTrue(variety_pile is not None)
        self.assertEqual('a pile of various items', variety_pile.key)
        self.assertTrue(variety_pile.is_typeclass("items.objects.InventoryGroup", exact=True))
        self.assertTrue(variety_pile.attributes.has('quantity'))
        self.assertEqual(3, variety_pile.db.quantity)
        self.assertEqual(3, len(variety_pile.contents))
        self.assertEqual("crude torch", variety_pile.contents[0].key)
        self.assertEqual("piece of chalk", variety_pile.contents[1].key)
        self.assertEqual("dirty towel", variety_pile.contents[2].key)
    
    def test_group_quantity_objects1(self):
        """
        Tests the outcome of 2 grouped coins.
        """
        final_msg = self.char1.item._group_quantity_objects(self.two_coin_groupables, self.obj_loc)
        self.assertEqual("You group together coin1 and coin2.", final_msg)

    def test_group_quanity_objects2(self):
        """
        Tests the outcome of 1 misc quantity obj and 2 grouped coins.
        """
        misc_quantity_object = create_object(typeclass="items.objects.Object", key="misc",
            location=self.obj_loc)
        misc_quantity_object.tags.add('quantity', category='groupable')

        self.two_coin_groupables.append(misc_quantity_object)
        final_msg = self.char1.item._group_quantity_objects(self.two_coin_groupables, self.obj_loc)
        self.assertEqual("misc cannot be grouped.\nYou group together coin1 and coin2.", final_msg)

    def test_group_coins(self):
        """
        Tests the outcome of 2 grouped coins.
        """
        self.assertEqual(2, len(self.two_coin_groupables))
        qty_group_obj = self.char1.item._group_coins(self.two_coin_groupables, self.obj_loc)
        self.assertTrue(qty_group_obj.is_typeclass("items.objects.QuantityGroup", exact=True))
        self.assertEqual(0, qty_group_obj.db.coin['plat'])
        self.assertEqual(1, qty_group_obj.db.coin['gold'])
        self.assertEqual(226, qty_group_obj.db.coin['silver'])
        self.assertEqual(306, qty_group_obj.db.coin['copper'])
        self.assertEqual('a pile of coins', qty_group_obj.key)
        self.assertEqual(self.obj_loc, qty_group_obj.location)

    def test_group_inventory_objects1(self):
        """
        Tests the outcome of 3 grouped inventory objects that all have the same key.
        """
        final_msg = self.char1.item.group_objects(self.three_torch_groupables, self.obj_loc)
        self.assertEqual("You group together some crude torches into a pile.", final_msg)

        # Asssess the final group object.
        torch_pile = self.obj_loc.contents[-1]
        self.assertTrue(torch_pile is not None)
        self.assertEqual('a pile of crude torches', torch_pile.key)
        self.assertTrue(torch_pile.is_typeclass("items.objects.InventoryGroup", exact=True))
        self.assertTrue(torch_pile.attributes.has('quantity'))
        self.assertEqual(3, torch_pile.db.quantity)
        self.assertEqual(3, len(torch_pile.contents))
        self.assertEqual("crude torch", torch_pile.contents[0].key)
        self.assertEqual("crude torch", torch_pile.contents[1].key)
        self.assertEqual("crude torch", torch_pile.contents[2].key)
    
    def test_group_inventory_objects1(self):
        """
        Tests the outcome of 3 grouped inventory objects that have different keys.
        """
        final_msg = self.char1.item.group_objects(self.variety_groupables, self.obj_loc)
        self.assertEqual("You group together crude torch, piece of chalk, and dirty towel into a pile.", final_msg)

        # Asssess the final group object.
        variety_pile = self.obj_loc.contents[-1]
        self.assertTrue(variety_pile is not None)
        self.assertEqual('a pile of various items', variety_pile.key)
        self.assertTrue(variety_pile.is_typeclass("items.objects.InventoryGroup", exact=True))
        self.assertTrue(variety_pile.attributes.has('quantity'))
        self.assertEqual(3, variety_pile.db.quantity)
        self.assertEqual(3, len(variety_pile.contents))
        self.assertEqual("crude torch", variety_pile.contents[0].key)
        self.assertEqual("piece of chalk", variety_pile.contents[1].key)
        self.assertEqual("dirty towel", variety_pile.contents[2].key)
