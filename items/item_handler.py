from evennia.utils import create
from evennia.utils.create import create_object
from evennia.utils.utils import variable_from_module

from misc import general_mechanics as gen_mec

'''
This handler decides functions related to items, such as get, put, stacking, etc.
'''

class ItemHandler():
    def __init__(self, owner):
        self.owner = owner
        self.items_dict = variable_from_module("items.items", variable='items')

    def get_object(self, obj, container, owner_possess):
        #TODO: Allow auto-stow of items in hand and continue to pick up obj if more than one exists in location.
        owner = self.owner
        main_wield, off_wield, both_wield  = owner.db.wielding.values()
        main_hand, off_hand = owner.db.hands.values()
        use_main_hand, use_off_hand = False, False
        owner_msg = ''
        others_msg = ''
        
        if obj in [main_hand, off_hand]:
            owner.msg(f"You are already carrying {obj.name}.")
            return

        # calling at_before_get hook method
        if not obj.at_before_get(owner):
            return
        
        # TODO: Check for free inventory slots.
        # inventory_dict = dict(owner.db.inventory)
        # if inventory_dict['occupied_slots'] < inventory_dict['max_slots']:
        #     free_slot = True

        # All restriction checks passed, move the object to the owner.
        obj.move_to(owner, quiet=True, move_hooks=False)

        #---------------------------[Hand Logic]---------------------------#
        # Items should prefer an open hand first and foremost.
        # When both hands are occupied, but neither are wielding, prefer the dominate hand.
        # Offhand should be used as a last resort, as this is a shield
        #------------------------------------------------------------------#
        
        if both_wield is not None:
            use_main_hand = False
            use_off_hand = True
            owner_msg = f"You stop wielding {both_wield.name}."
            others_msg = f"{owner.name} stops wielding {both_wield.name}."
            owner.db.wielding['both'] = None

        if main_hand == None:
            use_main_hand = True
        elif off_hand == None:
            use_off_hand = True
        else: # Both hands are full.
            if main_wield and off_wield is not None: # Both hands are wielding, prefer main hand to preserve shield.
                use_main_hand = True
                owner_msg = f"You stop wielding and stow away {main_hand.name}."
                others_msg = f"{owner.name} stops wielding and stows away {main_hand.name}."
                owner.db.wielding['main'] = None
                owner.db.hands['main'] = None
            elif main_wield == None:
                use_main_hand = True
                owner.db.wielding['main'] = None
                owner_msg = f"You stow away {main_hand.name} into your inventory."
                others_msg = f"{owner.name} stows away {main_hand.name} into their inventory."
                owner.db.hands['main'] = None
            elif off_wield == None:
                use_off_hand = True
                owner.db.wielding['off'] = None
                owner_msg = f"You stow away {off_hand.name} into your inventory."
                others_msg = f"{owner.name} stows away {off_hand.name} into their inventory."
                owner.db.hands['off'] = None

        if use_main_hand:
            owner.db.hands['main'] = obj
        elif use_off_hand:
            owner.db.hands['off'] = obj

        # TODO: Add an extra occupied inventory slot count.
        # owner.db.inventory_slots['occupied_slots'] +=1

        # Determine the nature of the object's origin.
        owner_msg = f"{owner_msg}\nYou get {obj.name}"
        others_msg = f"{others_msg}\n{owner.name} gets {obj.name}"
        if owner_possess:
            owner_msg = f"{owner_msg} from your inventory"
            others_msg = f"{others_msg} from their inventory"
        if container is not None:
            owner_msg = f"{owner_msg} from {container.name}"
            others_msg = f"{others_msg} from {container.name}"
        owner_msg = f"{owner_msg}."
        others_msg = f"{others_msg}."
        
        # Send out messages.
        owner.msg(owner_msg)
        owner.location.msg_contents(others_msg, exclude=owner)

        # calling at_get hook method
        obj.at_get(owner)

    def stow_object(self, obj):
        owner = self.owner
        main_hand, off_hand = owner.db.hands.values()
        wielding = owner.db.wielding
        main_wield, off_wield, both_wield  = wielding.values()
        
        if obj in [main_hand, off_hand]:
            # If the stowed object is currently wielded, stop wielding it and stow it.
            if obj in [main_wield, off_wield, both_wield]:
                owner.msg(f"You stop wielding {obj.name} and stow it away.")
                owner.location.msg_contents(f"{owner.name} stops wielding {obj.name} and stows it away.", exclude=owner)
                if obj == off_wield:
                    wielding['off'] = None
                elif obj == main_wield:
                    wielding['main'] = None
                else:
                    wielding['both'] = None
            else:
                owner.msg(f"You stow away {obj.name}.")
                owner.location.msg_contents(f"{owner.name} stows away {obj.name}.", exclude=owner)

            if obj == off_hand:
                owner.db.hands['off'] = None
            else:
                owner.db.hands['main'] = None
        elif obj.location == owner.location:
            owner.msg(f"You pick up {obj.name} and stow it away.")
            owner.location.msg_contents(f"{owner.name} picks up {obj.name} and stows it away.", exclude=owner)
            obj.move_to(owner, quiet=True)

        # calling at_get hook method
        obj.at_get(owner)

    def drop_object(self, obj):
        owner = self.owner
        main_hand, off_hand = owner.db.hands.values()
        wielding = owner.db.wielding
        main_wield, off_wield, both_wield  = wielding.values()

        # Call the object script's at_before_drop() method.
        if not obj.at_before_drop(owner):
            return
        
        if obj in [main_hand, off_hand]:
            # If the object is currently wielded, stop wielding it and drop it.
            if obj in [main_wield, off_wield, both_wield]:
                owner.msg(f"You stop wielding {obj.name} and drop it.")
                owner.location.msg_contents(f"{owner.name} stops wielding {obj.name} and drops it.", exclude=owner)
                if off_wield:
                    wielding['off'] = None
                else:
                    wielding['main'], wielding['both'] = None, None
            else:
                owner.msg(f"You drop {obj.name}.")
                owner.location.msg_contents(f"{owner.name} drops {obj.name}.", exclude=owner)
            if obj == off_hand:
                owner.db.hands['off'] = None
            else:
                owner.db.hands['main'] = None
        elif obj.location == owner:
            owner.msg(f"You pull {obj.name} from your inventory and drop it on the ground.")
            owner.location.msg_contents(f"{owner.name} pulls {obj.name} from their inventory and drops it on the ground.", exclude=owner)
        elif obj.location == owner.location:
            owner.msg(f"{obj.name} is already on the ground.")
            return

        obj.move_to(owner.location, quiet=True)

        # Call the object script's at_drop() method.
        obj.at_drop(owner)

    def group_objects(self, objects, obj_loc):
        """
        Takes a list of objects and organizes them into two categories:
            Objects that are unique and grouped as inventory.
            Objects that are identical and grouped as a quantity attribute.
        
        Generates a new group object and transfers the listed objects into this group object.

        Arguments:
            objects (list): This is the list of objects passed in from the grouping command.
            obj_loc (object): This is a reference to the object that houses the listed objects.
                This is often times a room or the player's character.
        
        Returns:
            msg (string): The resulting string of the grouping action, which is sent back to the
                caller of the command.
        """
        msg = ''
        coin_msg = False
        qty_msg = False
        inv_msg = False
        groupables = []
        coin_groupables = []
        qty_groupables = []
        inv_groupables = []
        

    #==[Parse the objects into appropriate lists.]==#
        # Filter ungroupables from the list.
        for obj in objects:
            if obj.tags.get(category='groupable'):
                groupables.append(obj)
            else:
                # Generate error strings for each object not able to be grouped.
                msg = f"{msg}{obj} is not able to be grouped.\n"

        if len(groupables) < 2:
            # Only one of the objects was groupable. Method requires at least 2 objects to group.
            msg = f"{msg}|rNot enough objects to group. Request aborted!|n"
            return msg

        # Sort objects into quantity or inventory group type lists.
        for obj in groupables:
            if obj.tags.get('coin', category='groupable'):
                coin_groupables.append(obj)
            elif obj.tags.get('quantity', category='groupable'):
                qty_groupables.append(obj)
            elif obj.tags.get('inventory', category='groupable'):
                inv_groupables.append(obj)

    #==[Execute the grouping and generate result strings.]==#
        # Coin Groupables
        if len(coin_groupables) > 1:
            coin_msg = self._group_coins(coin_groupables, obj_loc)
            msg = f"{msg}{coin_msg}"
        # Quantity Groupables
        if len(qty_groupables) > 1:
            # This object is a quantity object, but there is currently no logic to handle it.
            obj_names = gen_mec.comma_separated_string_list(gen_mec.objects_to_strings(qty_groupables))
            qty_msg = f"{obj_names} cannot be grouped. (Code functionality doesn't exist yet!)"
            if coin_msg:
                msg = f"{msg}\n"
            msg = f"{msg}{qty_msg}"
        # Inventory Groupables
        if len(inv_groupables) > 1:
            inv_msg = self._group_inventory_objects(inv_groupables, obj_loc)
            if qty_msg or coin_msg:
                msg = f"{msg}\n"
            msg = f"{msg}{inv_msg}"

        return msg

    def _group_coins(self, coin_groupables, obj_loc):
        """
        Creates a pile of coins.

        Arguments:
            coin_groupables (list): The coin objects to be grouped.
            obj_loc (object): The object that contains these groupable objects. Their location.
        Returns:
            coin_msg (string): The resulting string of the grouping action, which is sent back to the
                caller of the command.
        """
        coin_names = gen_mec.comma_separated_string_list(gen_mec.objects_to_strings(coin_groupables))

        total_copper = 0
        coin_group_obj = create_object(key='a pile of coins', typeclass='items.objects.Coin',
            location=obj_loc)
        for obj in coin_groupables:
            total_copper += obj.currency.coin_dict_to_copper(obj.db.coin)
        
        for obj in coin_groupables:
            obj.delete()

        coin_group_obj.db.coin = coin_group_obj.currency.copper_to_coin_dict(total_copper)

        coin_msg = f"You group together {coin_names}."

        return coin_msg

    def _group_inventory_objects(self, inv_groupables, obj_loc):
        """
        Groups together objects with unique properties by generating a group object and placing
        the groupable objects into its inventory.
        If all objects have the same key, a pile is generated with the key of the objects being grouped.
        
        Arguments:
            inv_groupables (list): A list of groupable objects to be placed in the inventory.
            obj_loc (object): The object that contains these groupable objects. Their location.

        Returns:
            inv_msg: The resulting string that is sent back to the caller that executed the grouping
                command.
        """
        inv_msg = ''
        inv_quantity = 0
        group_groupables = []

        # Separate out objects that are already groups, for additional parsing.
        temp_list = list(inv_groupables)
        for obj in temp_list:
            if obj.is_typeclass("items.objects.InventoryGroup", exact=True):
                group_groupables.append(obj)
                inv_groupables.remove(obj)

        # Generate a string to inform the user they are combining groups.
        # Dump the contents of each group into the inv_groupables for normal combining operations.
        if len(group_groupables) > 0:
            group_str_list = gen_mec.comma_separated_string_list(gen_mec.objects_to_strings(group_groupables))
            inv_msg = f"{inv_msg}You combine the contents of {group_str_list}.\n"
            for group in group_groupables:
                inv_groupables.extend(group.contents)
                group.delete()

        # Check if all objects in the inv_groupables list have the same name.
        same_name = gen_mec.all_same(gen_mec.objects_to_strings(inv_groupables))

        if same_name:
            # Create a pile of the same name of the groupable objects.
            inv_group_obj = create_object(key=f'a pile of {inv_groupables[0].name}es', 
                typeclass='items.objects.InventoryGroup', 
                location=obj_loc)
            inv_msg = f"{inv_msg}You group together some {inv_groupables[0].name}es."
        else:
            # Items have various names and the pile should be generic.
            item_str_list = gen_mec.comma_separated_string_list(gen_mec.objects_to_strings(inv_groupables))
            inv_group_obj = create_object(key=f"a pile of various items", 
                typeclass='items.objects.InventoryGroup', 
                location=obj_loc)
            inv_msg = f"{inv_msg}You group together {item_str_list}."

        # Pile object is generated, time to move groupables into its inventory.
        for obj in inv_groupables:
            obj.move_to(inv_group_obj, quiet=True, move_hooks=False)
            inv_quantity += 1
        inv_group_obj.db.quantity = inv_quantity

        return inv_msg

    def ungroup_objects(self, group_obj, obj_loc):
        """
        Ungroups grouped objects.

        Arguments:
            group_obj (object): The group object to ungroup.
            obj_loc (object): The object that contains these groupable objects. Their location.
        
        Returns:
            msg (string): The resulting message that will be sent back to the caller that executed
                the ungroup command.
        """
        delete_group_obj = False
        # Coin Groupable
        if group_obj.tags.get('coin', category='groupable'):
            msg, delete_group_obj = self._ungroup_coins(group_obj, obj_loc)
        # Quantity Groupable
        elif group_obj.tags.get('quantity', category='groupable'):
            msg = "You cannot ungroup a homogenized group. Use the split command instead."
        # Inventory Groupable
        elif group_obj.is_typeclass('items.objects.InventoryGroup'):
            group_contents = list(group_obj.contents)
            for x in group_contents:
                x.move_to(obj_loc, quiet=True, move_hooks=False)
            msg = (f"You ungroup {group_obj.name}, producing "
                f"{gen_mec.comma_separated_string_list(gen_mec.objects_to_strings(group_contents))}.")
            delete_group_obj = True

        if delete_group_obj:
            group_obj.delete()
        return msg

    def _ungroup_coins(self, group_obj, obj_loc):
        """
        Takes a pile of coins and ungroups them into the 4 coin types. (Plat, Gold, Silver, Copper)
        Will NOT ungroup a coin pile if it is already a single type of coin. (100 gold into 100 objects)
        Single coin objects are only generated from this action if they are part of a coin pile
        that contains additional coin types.

        Arguments:
            group_obj (object): The pile of coins to ungroup.
            obj_loc (object): The location that the group_obj resides and the ungroup objects will
                be placed in.
        
        Returns:
            msg (string): The resulting message that will be sent back to the caller that executed
                the ungroup command.
            delete_group_obj (boolean): Determines if the group_obj (original pile of coins) will be
                deleted in the main ungroup_objects() method. This is set to false if the coins are
                only of a single type of coin.
        """
        def create_coin(coin_type, coin_value, group_obj, obj_loc):
            """
            A helper method to allow a single point of coin generation and removal of its value from
            the original group_obj, no matter the coin type being passed in.

            Arguments:
                coin_type (string): The coin type being evaluated within this group_obj.
                coin_value (integer): The value of the specific coin type.
                group_obj (object): The pile of coins to ungroup.
                obj_loc (object): The location that the group_obj resides and the ungroup objects will
                    be placed in.
            Returns:
                coin_obj.key (string): The name of the resulting coin that has been separated from
                    the group_obj
            """
            # Fix the name for platinum coins.
            if coin_type == 'plat':
                coin_name = 'platinum'
            else:
                coin_name = coin_type

            # Abandon the ungrouping if the coin value is 0 for the coin type.
            if coin_value < 1:
                return None

            if coin_value > 1:
                coin_obj = create_object(key=f"a pile of {coin_name} coins", location=obj_loc,
                    typeclass='items.objects.Coin')
            elif coin_value == 1:
                coin_obj = create_object(key=f"a {coin_name} coin", location=obj_loc,
                    typeclass='items.objects.Coin')
            if coin_obj is not None:
                coin_obj.db.coin[coin_type] = coin_value
                group_obj.db.coin['coin_type'] = 0
                return coin_obj.key
        #------------------------------------------------------------------------------------
        delete_group_obj = False
        num_of_coin_types = 0

        for value in group_obj.values():
            if value > 0:
                num_of_coin_types += 1
        if num_of_coin_types > 1:
            new_coin_names = []
            # Iterate over the group object's coin dictionary and generate new coin piles.
            for coin_type, coin_value in group_obj.db.coin.items():
                new_coin_name = create_coin(coin_type, coin_value, group_obj, obj_loc)
                if new_coin_name is not None:
                    new_coin_names.append(new_coin_name)
            # Generate the resulting string.
            names = gen_mec.comma_separated_string_list(new_coin_names)
            msg = f"You ungroup {group_obj.name}, producing {names}."
            delete_group_obj = True
        else:
            msg = (f"{group_obj.key} consists of a single coin type and cannot be ungrouped. "
                "Use the split command instead.")
        return msg, delete_group_obj

    def split_group(self, split_type, pile, obj_loc, quantity=0, qty_obj=None):
        """
        Arguments:
            obj_loc (object): The object that contains these groupable objects. Their location.
        """
        pile_name = pile.name

        if split_type == 'default':
            # This condition splits the pile as evenly as possible into 2 piles.
            # The original pile always contains the higher quantity of items, if not evenly split.
            pass
        elif split_type == 'from':
            if pile.is_typeclass('items.objects.QuantityGroup'):
                # This is a pile of coins, or other similar pile.
                if pile.tags.get('coin', category='currency'):
                    coin_dict = pile.attributes.get('coin')
                    coin_type = coin_dict.get(qty_obj)
                    if coin_type >= quantity:
                        coin_dict[coin_type] -= quantity
                        # We also have to determine here if the coin pile has homogenized and change its description.

                        # Now we need to make a new coin pile with the value of the
                        # new coins split from the original.

                    else:
                        # There's not enough coin in the pile to execute the action.
                        msg = f"{pile.name} doesn't container {quantity} of {qty_obj}!"
                        return msg
                pass
            elif pile.is_typeclass('items.objects.InventoryGroup'):
                # Object has contents
                qty_obj_names = []

                qty_objects = pile.search(qty_obj, location=pile, quiet=True)
                # Check that there are enough objects in the pile to meet requirements.
                if len(qty_objects) >= quantity:
                    num = 1
                    while num <= quantity:
                        obj = qty_objects.pop()
                        qty_obj_names.append(obj.name)
                        obj.move_to(obj_loc, quiet=True, move_hooks=False)
                        num += 1

                    msg = f"You split"
                    if gen_mec.all_same(qty_obj_names):
                        msg = f"{msg} {quantity} {qty_obj_names[0]}"
                    else:
                        msg = f"{msg} {gen_mec.comma_separated_string_list(qty_obj_names)}"
                    msg= f"{msg} from {pile_name}."
                else:
                    msg = f"There aren't {quantity} of {qty_obj} in {pile.name}!"
                    return msg

                # Check if the pile has 1 or less objects remaining.
                if len(pile.contents) == 1:
                    obj = pile.contents
                    obj.move_to(obj_loc, quiet=True, move_hooks=False)
                if len(pile.contents) == 0:
                    pile.delete()
        return msg

    def spawn(self, item_type, item_name=None):
        """
        Spawn an item from the items.items module.

        Returns:
            item (object): An item object of the Object typeclass.
        """
        owner = self.owner
        item_type_dict = self.items_dict.get(item_type, None)
        if not item_type_dict:
            owner.msg(f"|rWARNING! Could not find {item_type} from the items.items items dictionary "
                "within the ItemHandler spawn() method.|n")
            return

        location = owner
        tags = None
        attributes = None
        item = create_object(typeclass="items.objects.Object", key=item_name, location=location,
            home=None, tags=tags, attributes=attributes)
        return item
