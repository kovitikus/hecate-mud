from evennia.utils import create
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
        final_msg = self.char1.item.group_objects(self.two_coin_groupables, self.obj_loc)
        self.assertEqual("You group together coin1 and coin2.", final_msg)

    def test_group_objects2(self):
        final_msg = self.char1.item.group_objects(self.three_torch_groupables, self.obj_loc)
        self.assertEqual("You group together some crude torches into a pile.", final_msg)

    def test_group_objects3(self):
        final_msg = self.char1.item.group_objects(self.variety_groupables, self.obj_loc)
        self.assertEqual("You group together crude torch, piece of chalk, and dirty towel into a pile.", final_msg)

    def test_group_objects4(self):
        """
        Grouping logic should first separate the items into their perspective categories.
        It will then group the coins and return that string, while placing that string into
        the inventory grouping of the variety items. Resulting in a combined grouping.
        """
        combined_list = [*self.two_coin_groupables, *self.variety_groupables]
        final_msg = self.char1.item.group_objects(combined_list, self.obj_loc)
        temp = ("You group together coin1 and coin2.\nYou group together crude torch, "
                "piece of chalk, and dirty towel into a pile.")
        self.assertEqual(temp, final_msg)
    
    def test_group_quantity_objects1(self):
        final_msg = self.char1.item._group_quantity_objects(self.two_coin_groupables, self.obj_loc)
        self.assertEqual("You group together coin1 and coin2.", final_msg)

    def test_group_quanity_objects2(self):
        uncategorized_quantity_object = create_object(typeclass="items.objects.Object", key="misc",
            location=self.obj_loc)
        uncategorized_quantity_object.tags.add('quantity', category='groupable')

        self.two_coin_groupables.append(uncategorized_quantity_object)
        final_msg = self.char1.item._group_quantity_objects(self.two_coin_groupables, self.obj_loc)
        self.assertEqual("misc cannot be grouped.\nYou group together coin1 and coin2.", final_msg)

    def test_group_coins(self):
        qty_group_obj = self.char1.item._group_coins(self.two_coin_groupables, self.obj_loc)
        self.assertTrue(qty_group_obj.is_typeclass("items.objects.QuantityGroup", exact=True))
        self.assertEqual(0, qty_group_obj.db.coin['plat'])
        self.assertEqual(1, qty_group_obj.db.coin['gold'])
        self.assertEqual(226, qty_group_obj.db.coin['silver'])
        self.assertEqual(306, qty_group_obj.db.coin['copper'])
        self.assertEqual('a pile of coins', qty_group_obj.key)
        self.assertEqual(self.obj_loc, qty_group_obj.location)

    def test_group_inventory_objects1(self):
        final_msg = self.char1.item.group_objects(self.three_torch_groupables, self.obj_loc)
        self.assertEqual("You group together some crude torches into a pile.", final_msg)
    
    def test_group_inventory_objects1(self):
        final_msg = self.char1.item.group_objects(self.variety_groupables, self.obj_loc)
        self.assertEqual("You group together crude torch, piece of chalk, and dirty towel into a pile.", final_msg)
