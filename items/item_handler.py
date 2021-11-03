from evennia.prototypes.spawner import spawn
from evennia.utils.create import create_object
from evennia.utils.utils import variable_from_module

from misc import general_mechanics as gen_mec
from misc import coin

'''
This handler decides functions related to items, such as get, put, stacking, etc.
'''

class ItemHandler():
    def __init__(self, owner):
        self.owner = owner
        self.items_dict = variable_from_module("items.items", variable='items')

    def group_objects(self, objects, obj_loc):
        """
        Takes a list of objects and groups them based on 3 categories:
            Coin objects that have a coin dictionary.
            Quantity objects that are identical in both key and attributes.
            All other objects that have unique attribute values and are grouped into a pile,
                which behaves like a container.

        Arguments:
            objects (list): This is the list of objects passed in from the grouping command.
            obj_loc (object): This is a reference to the object that houses the listed objects.
                This is often times a room or the player's character.
        
        Returns:
            msg (string): The resulting string of the grouping action, which is sent back to the
                caller of the command.
        """
        msg = ''
        coin_msg = None
        qty_msg = None
        inv_msg = None
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
            coin_msg, coin_group_obj = self._group_coins(coin_groupables, obj_loc)
            msg = f"{msg}{coin_msg}"

            # Reset the coin groupables and add the new coin object to the list.
            # This will be used to evaluate if the coins should be grouped with the inventory logic.
            coin_groupables.clear()
            coin_groupables.append(coin_group_obj)

        # Quantity Groupables
        if len(qty_groupables) > 1:
            # Merge and filter the list of quantity objects.
            qty_groupables, qty_names = self._group_quantity_objects(qty_groupables)

            obj_names = gen_mec.comma_separated_string_list(qty_names)
            qty_msg = f"You combine {obj_names}."
            if coin_msg is not None:
                msg = f"{msg}\n"
            msg = f"{msg}{qty_msg}"

        # Inventory Groupables
        # Decide if there are enough objects to group, including coin and quantity results.
        # Inventory groupales must still be at least 1 + 1 from either coin or quantity to execute.
        if len(inv_groupables) > 1 or len(inv_groupables) + len(coin_groupables) > 1 \
        or len(inv_groupables) + len(qty_groupables) > 1:
            inv_groupables.extend(coin_groupables)
            inv_groupables.extend(qty_groupables)
            inv_msg = self._group_inventory_objects(inv_groupables, obj_loc)
            if qty_msg is not None or coin_msg is not None:
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
            coin_group_obj (object): The new coin pile produced by this grouping.
        """
        coin_names = gen_mec.comma_separated_string_list(gen_mec.objects_to_strings(coin_groupables))

        total_copper = 0
        for obj in coin_groupables:
            total_copper += coin.coin_dict_to_copper(obj.db.coin)
        
        for obj in coin_groupables:
            obj.delete()

        coin_obj = coin.generate_coin_object(copper=total_copper)
        coin_obj.location = obj_loc

        coin_msg = f"You combine {coin_names}."

        return coin_msg, coin_obj

    def _group_quantity_objects(self, qty_groupables):
        """
        Combines objects that have no unique attributes into a single object.
        Adds the quantity value of duplicate objects to the first object found and then
        deletes any duplicates.

        Arguments:
            qty_groupables (list): The list of objects to iterate over and combine.
        
        Returns:
            qty_groupables (list): The filtered list of combined objects.
            qty_names (list): The quantity and name of each final object, used in the final string
                that is sent back to the caller of the grouping command.
        """
        qty_names = []
        qty_dict = {}
        # Spawn a new list to iterate over, while manipulating the qty_groupables list.
        test_list = list(qty_groupables)
        for obj in test_list:
            # Homogenize the name of the objects being combined. Account for groupings already
            # included for this object.
            obj_key = obj.db.singular_key

            if qty_dict.get(obj_key, None) is not None:
                # This is a duplicate of an already found object.
                # Add its quantity to the original object and delete the duplicate.
                qty_dict[obj_key].db.quantity += obj.db.quantity
                qty_groupables.remove(obj)
                obj.delete()
            else:
                # Generate a new dictionary key and assign the first object encountered.
                # Preserving the first object found also preserves the common properties assigned to
                # this object. Such as tags, etc.
                qty_dict[obj_key] = obj

        # Iterate over the list of final objects and modify the keys of grouped objects.
        for obj in qty_groupables:
            if obj.db.quantity > 1:
                obj.key = f"a pile of {obj.db.plural_key}"
            qty_names.append(f"{obj.db.quantity} {obj.db.plural_key}")

        return qty_groupables, qty_names

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
            inv_group_obj = create_object(key=f'a pile of {inv_groupables[0].db.plural_key}', 
                typeclass='items.objects.InventoryGroup', 
                location=obj_loc)
            inv_msg = f"{inv_msg}You group together some {inv_groupables[0].db.plural_key}."
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
            # Abandon the ungrouping if the coin value is 0 for the coin type.
            if coin_value < 1:
                return None

            temp_coin_dict = {}
            temp_coin_dict[coin_type] = coin_value
            coin_dict = coin.create_coin_dict(**temp_coin_dict)
            coin_obj = coin.generate_coin_object(coin_dict=coin_dict)
            coin_obj.location = obj_loc

            if coin_obj is not None:
                # Set the original group object's coin_type to zero, as it's been transferred over.
                group_obj.db.coin[coin_type] = 0
                # We only need to return the key here, because the new object is already generated
                # and its location has been set.
                return coin_obj.key
        #------------------------------------------------------------------------------------
        delete_group_obj = False
        if not coin.is_homogenized(group_obj.db.coin):
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

    def split_group(self, split_type, pile, obj_loc, quantity=0, extract_obj=None):
        """
        Arguments:
            obj_loc (object): The object that contains these groupable objects. Their location.
        """
        msg = ''
        pile_name = pile.name

        if pile.tags.get('coin', category='groupable'):
            msg = self._split_coins(split_type, pile, obj_loc, quantity, extract_obj, pile_name)

        elif pile.tags.get('quantity', category='groupable'):
            # This is a pile of quantity objects, or other similar pile.
            msg = self._split_quantity_objects(self, split_type, pile, obj_loc, quantity, pile_name)

        elif pile.is_typeclass('items.objects.InventoryGroup'):
            msg = self._split_inventory_objects(split_type, pile, obj_loc, quantity, extract_obj,
                pile_name)
        return msg

    def _split_coins(self, split_type, pile, obj_loc, quantity, extract_obj, pile_name):
        original_copper = 0
        new_copper = 0

        # Convert the coin into copper to do maths.
        total_copper = coin.coin_dict_to_copper(pile.db.coin)
        if split_type == 'default':
            if total_copper > 1:
                original_copper = (total_copper // 2) + (total_copper % 2)
                new_copper = total_copper // 2
            else:
                return "You cannot split 1 copper!"
        elif split_type == 'from':
            coin_type = 'plat' if extract_obj == 'platinum' else extract_obj
            temp_coin_dict = {}
            temp_coin_dict[coin_type] = quantity
            new_copper = coin.coin_dict_to_copper(temp_coin_dict)

            if new_copper > total_copper:
                return f"There isn't enough {extract_obj} to split from {pile_name}!"
            else:
                original_copper = total_copper - new_copper

        # Original pile no longer has a use and will be remade. Delete it.
        pile.delete()
        # Convert the coppers back to coin dictionaries.
        original_coin_dict = coin.balance_coin_dict(coin.copper_to_coin_dict(original_copper))
        new_coin_dict = coin.balance_coin_dict(coin.copper_to_coin_dict(new_copper))

        original_coin_obj = coin.generate_coin_object(coin_dict=original_coin_dict)
        original_coin_obj.location = obj_loc
        new_coin_obj = coin.generate_coin_object(coin_dict=new_coin_dict)
        new_coin_obj.location = obj_loc

        if split_type == 'default':
            msg = f"You split {pile_name} into {original_coin_obj.key} and {new_coin_obj.key}."
        elif split_type == 'from':
            msg = f"You split {new_coin_obj.key} from {pile_name}, leaving {original_coin_obj.key}."
        return msg

    def _split_quantity_objects(self, split_type, pile, obj_loc, quantity, extract_obj, pile_name):
        pile_qty = pile.attributes.get('quantity', default=0)
        if pile_qty <= 1:
            return f"{pile_name} has a quantity of {pile_qty} and cannot be split!"
        if split_type == 'default':
            original_pile_qty = (pile_qty // 2) + (pile_qty % 2)
            new_pile_qty = pile_qty // 2
        elif split_type == 'from':
            if quantity > pile_qty:
                return f"{pile_name} does not have {quantity} to split from itself!"

            original_pile_qty = pile_qty - quantity
            new_pile_qty = quantity

        pile.db.quantity = original_pile_qty
        new_pile = pile.copy()
        new_pile.db.quantity = new_pile_qty
        new_pile.location = obj_loc

        for pile in [pile, new_pile]:
            if pile.db.quantity > 1:
                pile.key = pile.db.plural_key
            else:
                pile.key = pile.db.singular_key

        if split_type == 'default':
            msg = f"You split {pile_name} into {pile.key} and {new_pile.key}."
        elif split_type == 'from':
            msg = f"You split {new_pile.key} from {pile_name}, leaving {pile.key}"
        return msg

    def _split_inventory_objects(self, split_type, pile, obj_loc, quantity, extract_obj, pile_name):
        """
        """
        msg = ''
        if split_type == 'default':
            pile_qty = len(pile)

            # Determine how many objects will be removed from the original pile.
            original_pile_qty = (pile_qty // 2) + (pile_qty % 2)
            new_pile_qty = pile_qty // 2

            new_pile_items = []
            # Grab references to all objects that are to be moved from the pile.
            # New pile objects are always taken from the backend of the pile's contents.
            # Due to list indexes starting at 0, the remaining quantity for the original pile
            # will actually be the starting index of the new pile's candidates.
            for index in range(original_pile_qty, pile_qty - 1):
                new_pile_items.append(pile.contents[index])
            
            new_pile_qty = len(new_pile_items)
            if new_pile_qty > 1:
                # There are more than one object being split from the original pile.
                if gen_mec.all_same(new_pile_items):
                    new_pile = create_object(typeclass="items.objects.InventoryGroup",
                        key=f"a pile of {new_pile_items[0].db.plural_key}", location=obj_loc)
                else:
                    new_pile = create_object(typeclass="items.objects.InventoryGroup",
                        key=f"a pile of various items", location=obj_loc)

                # Move the objects from the original pile to the new pile.
                for item in new_pile_items:
                    item.move_to(new_pile, quiet=True, move_hooks=False)

                # Set each pile's quantity attribute.
                pile.db.quantity = len(pile.contents)
                new_pile.db.quantity = len(new_pile.contents)
                msg = f"You split {pile.key} in two, creating {new_pile.key}"
            else:
                # The number of split objects is only 1 and is not a pile.
                # Move the object into the room.
                new_pile_items[0].move_to(obj_loc, quiet=True, move_hooks=False)
                msg = f"You split {new_pile_items[0]} from {pile.key}."
                
                
                # If only 1 object has been split from the pile, the original pile only has 1 or 2
                # objects remaining.
                if len(pile.contents) == 1:
                    for obj in pile.contents:
                        obj.move_to(obj_loc, quiet=True, move_hooks=False)
                        msg = f"{msg}\n{obj.key} is removed from {pile.key}. {pile.key} is no more."
                if len(pile.contents) == 0:
                    pile.delete()

        if split_type == 'from':
            extract_obj_names = []

            extract_objects = pile.search(extract_obj, location=pile, quiet=True)
            # Check that there are enough objects in the pile to meet requirements.
            if len(extract_objects) >= quantity:
                num = 1
                while num <= quantity:
                    obj = extract_objects.pop()
                    extract_obj_names.append(obj.name)
                    obj.move_to(obj_loc, quiet=True, move_hooks=False)
                    num += 1

                msg = f"You split"
                if gen_mec.all_same(extract_obj_names):
                    msg = f"{msg} {quantity} {extract_obj_names[0]}"
                else:
                    msg = f"{msg} {gen_mec.comma_separated_string_list(extract_obj_names)}"
                msg= f"{msg} from {pile_name}."
            else:
                msg = f"There aren't {quantity} of {extract_obj} in {pile.name}!"
                return msg

            # Check if the pile has 1 or less objects remaining.
            if len(pile.contents) == 1:
                obj = pile.contents[0]
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
