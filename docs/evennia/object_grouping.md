Hecate is my MUD. You can find the source code for all of this logic over on my GitHub. It is both open-source and public domain.

https://github.com/kovitikus/hecate

***
### Table of Contents
* [Introduction](https://github.com/kovitikus/hecate/blob/master/docs/evennia/object_grouping.md#introduction)
* [Object Categorization](https://github.com/kovitikus/hecate/blob/master/docs/evennia/object_grouping.md#object-categorization)
	* [Coin Objects](https://github.com/kovitikus/hecate/blob/master/docs/evennia/object_grouping.md#coin-objects)
	* [Quantity Objects](https://github.com/kovitikus/hecate/blob/master/docs/evennia/object_grouping.md#quantity-objects)
	* [Inventory Objects](https://github.com/kovitikus/hecate/blob/master/docs/evennia/object_grouping.md#inventory-objects)
* [Command Logic](https://github.com/kovitikus/hecate/blob/master/docs/evennia/object_grouping.md#command-logic)
	* [Group Command](https://github.com/kovitikus/hecate/blob/master/docs/evennia/object_grouping.md#group-command)
	* [Ungroup Command](https://github.com/kovitikus/hecate/blob/master/docs/evennia/object_grouping.md#ungroup-command)
	* [Split Command](https://github.com/kovitikus/hecate/blob/master/docs/evennia/object_grouping.md#split-command)
* [ItemHandler Methods](https://github.com/kovitikus/hecate/blob/master/docs/evennia/object_grouping.md#itemhandler-methods)
	* [Group Objects Method](https://github.com/kovitikus/hecate/blob/master/docs/evennia/object_grouping.md#group-objects-method)
	* [Group Coins Method](https://github.com/kovitikus/hecate/blob/master/docs/evennia/object_grouping.md#group-coins-method)
	* [Group Quantity Objects Method](https://github.com/kovitikus/hecate/blob/master/docs/evennia/object_grouping.md#group-quantity-objects-method)
	* [Group Inventory Objects Method](https://github.com/kovitikus/hecate/blob/master/docs/evennia/object_grouping.md#group-inventory-objects-method)
	* [Ungroup Objects Method](https://github.com/kovitikus/hecate/blob/master/docs/evennia/object_grouping.md#ungroup-objects-method)
	* [Ungroup Coins Method](https://github.com/kovitikus/hecate/blob/master/docs/evennia/object_grouping.md#ungroup-coins-method)
	* [Split Group Method](https://github.com/kovitikus/hecate/blob/master/docs/evennia/object_grouping.md#split-group-method)
	* [Split Coins Method](https://github.com/kovitikus/hecate/blob/master/docs/evennia/object_grouping.md#split-coins-method)
	* [Split Quantity Objects Method](https://github.com/kovitikus/hecate/blob/master/docs/evennia/object_grouping.md#split-quantity-objects-method)
	* [Split Inventory Objects Method](https://github.com/kovitikus/hecate/blob/master/docs/evennia/object_grouping.md#split-inventory-objects-method)
* [Test ItemHandler  Module](https://github.com/kovitikus/hecate/blob/master/docs/evennia/object_grouping.md#test-itemhandler-module)
* [Coin Module](https://github.com/kovitikus/hecate/blob/master/docs/evennia/object_grouping.md#coin-module)
* [Item Prototypes Module]

***
### Introduction
[Return to Table of Contents](https://github.com/kovitikus/hecate/blob/master/docs/evennia/object_grouping.md#table-of-contents)

I still have some cleanup to do, including a bit of additional functionality I wanted to write into the commands themselves, but the rest of what's missing is mostly just some docstrings and possible missing unit testing I want to consider.

I haven't yet wrote any information to compliment this code yet, but I want to come back around and eventually explain everything in detail. I'll edit this post as I make updates. For now, I felt it was helpful to get the thread started and the code dumped in.

I'll go back through later and generate a table of contents, as well as add in source links to my project for each section.

***

### Object Categorization
[Return to Table of Contents](https://github.com/kovitikus/hecate/blob/master/docs/evennia/object_grouping.md#table-of-contents)

My object grouping logic is broken up into 3 categories: coins, quantity objects, and inventory objects.

Much of the functionality is handled through tags, of the category `groupable`. The only two typeclasses that are unique here are the Coin and InventoryGroup typeclasses, found here in my objects module.

https://github.com/kovitikus/hecate/blob/master/items/objects.py

These custom typeclasses serve mostly as a medium for the `return_appearance` hook to tell the player how much coin a coin object is worth and the contents of an inventory grouping.

#### Coin Objects
[Return to Table of Contents](https://github.com/kovitikus/hecate/blob/master/docs/evennia/object_grouping.md#table-of-contents)

Coins function as a dictionary on the object, as an attribute called coin. It consists of 4 currency tiers of coin: platinum, gold, silver, copper. Each of the tiers holds 999 in value, with the 1,000th value being pushed up to the next tier.

Grouping of coins is specific to my coin system, but the basic logic is there and may help others figure out how to approach their own coins. It becomes even easier if you have a single currency.

Physical coins, when grouped, will automatically generate the next tier of coin if the value hits the threshold. This may not be desirable for many games, but I decided that I'd rather destroy a bit of realism for the sake of convenience. Players can always generate a coin of a lower value by using the `split` command.

Coins in Hecate are generally non-existent. Meaning that most transactions just subtract or add coin directly to the player or object. The only time physical coins are generated is when they must be represented in the game world. Either with the player holding a coin in their character's hands or inside a container or on the ground in a room.

#### Quantity Objects
[Return to Table of Contents](https://github.com/kovitikus/hecate/blob/master/docs/evennia/object_grouping.md#table-of-contents)

Quantity objects are objects that have no unique attributes per object of that type. They are named as such because they are represented entirely by their quantity counter.

For example, if a rock has a weight attribute, but all rocks weigh the same, then there is no reason to preserve each object's weight value when grouped.

These types of objects are probably rare in most games, as you can easily add unique attributes to anything. A color specific to a type of object, a weight, a resource value, etc.

Quantity objects are grouped by preserving the first object of its kind encountered, and then adding a value to a quantity attribute. All subsequent quantity objects encountered during a grouping are destroyed and added to the counter.

To prevent players from ungrouping a pile of 10,000 rocks into 10,000 individual objects, there is no ungrouping logic written for quantity  objects. The player is forced to use the split command, which will either cut the pile into two or remove a specified number of objects from the pile (as a pile of its own, if greater than 1).

#### Inventory Objects
[Return to Table of Contents](https://github.com/kovitikus/hecate/blob/master/docs/evennia/object_grouping.md#table-of-contents)

Inventory objects are ones which have unique values on their attributes and must be preserved when grouping. Therefore, a container object is generated, to store items in its inventory or contents. Inventory objects that all have the same name spawn a pile of the same name, `a pile of torches`, for example. Any other type of grouping will spawn a variety pile, `a pile of various items`.

Most objects will fall into this category of grouping. Torches have a fuel counter on them, for example. Other objects may have unique attributes, such as color, quality, etc.

***
### Command Logic
[Return to Table of Contents](https://github.com/kovitikus/hecate/blob/master/docs/evennia/object_grouping.md#table-of-contents)

#### Group Command
```py
class CmdGroup(Command):
    """
    Usage:  group <objects>
            group my <objects>
            group <object> with <object>

    Groups items of the same type.
    Prioritizes items in the room. Specify 'my' to group items in your inventory.

    Example:
            > group torch
            You group together some torches.
    """
    key = 'group'
    aliases = ['stack',]

    def parse(self):
        caller = self.caller
        if not self.args:
            caller.msg("Usage:  group <my> <objects>")
            raise InterruptCommand
        args = self.args

        if re.search(r"(my)", args):
            self.args = args.split(' ', 1)[1].strip()
            self.obj_loc = caller
        elif re.search(r"(with)", args):
            args = args.split('with', 1)
            arg1 = args[0].strip()
            arg2 = args[1].strip()
            self.args = [arg1, arg2]
            self.obj_loc = caller.location
        else:
            self.args = args.strip()
            self.obj_loc = caller.location
        
    def func(self):
        caller = self.caller
        args = self.args
        obj_loc = self.obj_loc

        objects = caller.search(args, location=obj_loc, quiet=True)
        if len(objects) == 0:
            caller.msg(f"{args} was not found!")
            return
        elif len(objects) == 1:
            caller.msg(f"Only 1 {args} was found!")
            return
        else:
            msg = caller.item.group_objects(objects, obj_loc)
            caller.msg(msg)
```

#### Ungroup Command
[Return to Table of Contents](https://github.com/kovitikus/hecate/blob/master/docs/evennia/object_grouping.md#table-of-contents)
```py
class CmdUngroup(Command):
    """
    Usage:  ungroup <group>
            ungroup my <group>

    Ungroups a pile of objects.
    Prioritizes items in the room. Specify 'my' to group items in your inventory.
    Coins only ungroup if the pile contains more than one type of coin; use split instead.

    Example:
            ungroup torches
            You separate a pile of torches.
    """
    key = 'ungroup'
    aliases = ['unstack',]
    def parse(self):
        caller = self.caller
        if not self.args:
            caller.msg("Usage:  ungroup <object>")
            raise InterruptCommand

        if re.search(r"(my)", self.args):
            self.args = self.args.split(' ', 1)[0].strip()
            self.obj_loc = self.caller
        else:
            self.args = self.args.strip()
            self.obj_loc = self.caller.location

    def func(self):
        caller = self.caller
        args = self.args

        obj = caller.search(args)
        if obj:
            msg = caller.item.ungroup_objects(obj, self.obj_loc)
            caller.msg(msg)
```

#### Split Command
[Return to Table of Contents](https://github.com/kovitikus/hecate/blob/master/docs/evennia/object_grouping.md#table-of-contents)
```py
class CmdSplit(Command):
    """
    Usage:  split <object>
            split my <object>
            split 3 gold from <object>
            split 3 torch from my <object>

    """
    key = 'split'
    def parse(self):
        caller = self.caller
        if not self.args:
            caller.msg("Usage:  split <my> <object> | split # <object> from <my> <object>")
            raise InterruptCommand
        else:
            args = self.args

        if 'my' and not 'from' in args:
            # split my pile
            self.split_type = 'default'
            self.pile = args.split(' ', 1)[1].strip()
            self.pile_loc = caller

        elif 'from' and not 'my' in args:
            # split # object from pile
            self.split_type = 'from'
            args = args.split('from', 1) # args = [' # object ', ' pile']

            extract_obj = args[0].strip().split(' ', 1) # extract_obj = ['#', 'object']
            self.quantity = extract_obj[0] # quantity = '#'
            if not self.quantity > 0:
                caller.msg("Quantity must be greater than zero!")
                raise InterruptCommand
            self.extract_obj = extract_obj[1] # extract_obj = 'object'

            self.pile = args[1].strip()
            self.pile_loc = caller.location

        elif 'from' and 'my' in args:
            # split # object from my pile
            self.split_type = 'from'
            args = args.split('from', 1) # args = [' # object', ' my pile']

            extract_obj = args[0].strip().split(' ', 1) # extract_obj = ['#', 'object']
            self.quantity = extract_obj[0] # quantity = '#'
            if not self.quantity > 0:
                caller.msg("Quantity must be greater than zero!")
                raise InterruptCommand
            self.extract_obj = extract_obj[1] # extract_obj = 'object'

            self.pile = args[1].strip().split(' ', 1)[1]
            self.pile_loc = caller

        else:
            # split object
            self.split_type = 'default'
            self.pile = args.strip()
            self.pile_loc = caller.location

    def func(self):
        caller = self.caller
        split_type = self.split_type
        pile = self.pile
        pile_loc = self.pile_loc

        pile = caller.search(pile, location=pile_loc, quiet=True)[0]
        if pile is not None:
            if split_type == 'default':
                msg = caller.item.split_group(split_type, pile, pile_loc)
            elif split_type == 'from':
                msg = caller.item.split_group(split_type, pile, pile_loc, self.quantity, self.extract_obj)

        caller.msg(msg)
```

***

### ItemHandler methods
[Return to Table of Contents](https://github.com/kovitikus/hecate/blob/master/docs/evennia/object_grouping.md#table-of-contents)

#### Group Objects Method
* Docstring explanation is incorrect about group objects. I haven't updated in awhile and I will fix it as part of my final pass over all of this. Objects are grouped into 3 categories, coins, quantity, and inventory.
```py
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
        if coin_msg:
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
        if qty_msg or coin_msg:
            msg = f"{msg}\n"
        msg = f"{msg}{inv_msg}"

    return msg
```

#### Group Coins Method
[Return to Table of Contents](https://github.com/kovitikus/hecate/blob/master/docs/evennia/object_grouping.md#table-of-contents)
```py
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
```

#### Group Quantity Objects Method
[Return to Table of Contents](https://github.com/kovitikus/hecate/blob/master/docs/evennia/object_grouping.md#table-of-contents)
```py
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
```

#### Group Inventory Objects Method
[Return to Table of Contents](https://github.com/kovitikus/hecate/blob/master/docs/evennia/object_grouping.md#table-of-contents)
```py
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
```

### Ungroup Objects Method
[Return to Table of Contents](https://github.com/kovitikus/hecate/blob/master/docs/evennia/object_grouping.md#table-of-contents)
```py
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
```

#### Ungroup Coins Method
[Return to Table of Contents](https://github.com/kovitikus/hecate/blob/master/docs/evennia/object_grouping.md#table-of-contents)
```py
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
```

#### Split Group Method
[Return to Table of Contents](https://github.com/kovitikus/hecate/blob/master/docs/evennia/object_grouping.md#table-of-contents)
```py
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
```

#### Split Coins Method
[Return to Table of Contents](https://github.com/kovitikus/hecate/blob/master/docs/evennia/object_grouping.md#table-of-contents)
```py
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
```

#### Split Quantity Objects method
[Return to Table of Contents](https://github.com/kovitikus/hecate/blob/master/docs/evennia/object_grouping.md#table-of-contents)
```py
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
```

#### Split Inventory Objects Method
[Return to Table of Contents](https://github.com/kovitikus/hecate/blob/master/docs/evennia/object_grouping.md#table-of-contents)
```py
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
```

***

### Test ItemHandler Module
[Return to Table of Contents](https://github.com/kovitikus/hecate/blob/master/docs/evennia/object_grouping.md#table-of-contents)
Some of this may have pointless repetition. I wasn't sure if I should test the submethods or just the parent ones. I also don't know if I have full test coverage of all possibilities, so I'll likely be updating this a bit in the future.

(Just group objects with coins thrown in, or specifically the group coins method as well.)

I also use my own custom test class, which is very similiar to the EvenniaTest class, but generates some stuff specific to my project that is needed. Some of that will likely change though.

```py
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
```

***

### Coin Module
[Return to Table of Contents](https://github.com/kovitikus/hecate/blob/master/docs/evennia/object_grouping.md#table-of-contents)
This is pretty useful to have, and I rely heavily on it, but it is specific to my project. I'll include it anyways, so that the coin grouping makes better sense.

```py
from evennia.prototypes.spawner import spawn

def return_all_coin_types(coin_dict):
    """
    Takes a coin dictionary and returns the value of all 4 types of coins, as individual variables.

    If a coin dictionary is not provided, the method attempts to pull one from the owner object.
    If that fails, a coin dictionary is created with all 0 values.

    Keyword Arguments:
        coin_dict (dict): A dictionary of coins and their values.

    Returns:
        plat (int): The value of platinum coin.
        gold (int): The value of gold coin.
        silver (int): The value of silver coin.
        copper (int): The value of copper coin.
    """
    return coin_dict['plat'], coin_dict['gold'], coin_dict['silver'], coin_dict['copper']

def all_coin_types_to_string(coin_dict):
    """
    Converts all coin elements into a string, no matter their value.

    Keyword Arguments:
        coin_dict (dict): A dictionary consisting of all 4 coin types.

    Returns:
        (string): The resulting string.
    """
    return f"{coin_dict['plat']}p {coin_dict['gold']}g {coin_dict['silver']}s {coin_dict['copper']}c"

def positive_coin_types_to_string(coin_dict):
    """
    Converts only the coin elements that are greater than 0 into a string.

    Arguments:
        coin_dict (dict): A dictionary consisting of all 4 coin types.

    Returns:
        (string): The resulting string.
    """
    plat = ""
    gold = ""
    silver = ""
    copper = ""
    if coin_dict['plat'] > 0:
        plat = f"{coin_dict['plat']}p "
    if coin_dict['gold'] > 0:
        gold = f"{coin_dict['gold']}g "
    if coin_dict['silver'] > 0:
        silver = f"{coin_dict['silver']}s "
    if coin_dict['copper'] > 0:
        copper = f"{coin_dict['copper']}c"
    return f"{plat}{gold}{silver}{copper}".strip()

def balance_coin_dict(coin_dict):
    """
    Takes a coin dictionary and balances all coins in excess of 999.
    Pushes the quotient of 1,000 up to the next coin type and leaves the remainder.

    Arguments:
        coin_dict (dict): A dictionary consisting of all 4 coin types.

    Returns:
        coin_dict (dict): A dictionary consisting of all 4 coin types.
    """
    def quotient(value):
        return value // 1_000
    def remainder(value):
        return value % 1_000

    plat, gold, silver, copper = return_all_coin_types(coin_dict=coin_dict)

    if copper > 999:
        silver += quotient(copper)
        copper = remainder(copper)

    if silver > 999:
        gold += quotient(silver)
        silver = remainder(silver)
    
    if gold > 999:
        plat += quotient(gold)
        gold = remainder(gold)

    return create_coin_dict(plat=plat, gold=gold, silver=silver, copper=copper)

def convert_coin_type(plat=0, gold=0, silver=0, copper=0, result_type='copper'):
    """
    Converts any number of coin types into a single type of coin.
    For example, it can convert 585433 copper + 35 plat into silver.
    (Don't worry about how much silver that is. It's what this method is for!)

    Converting upward will likely result in a float, whereas only converting downward
    will always result in an integer. This is critical information to keep in mind when
    using this method.

    Keyword Arguments:
        plat (int): Amount of platinum to convert.
        gold (int): Amount of gold to convert.
        silver (int): Amount of silver to convert.
        coppper (int): Amount of copper to convert.
        result_type (string): The type of coin the result should be. Defaults to copper.

    Returns:
        plat (int) or (float)
        gold (int) or (float)
        silver (int) or (float)
        coppper (int) or (float)
    """
    def convert_upward(current_tier_amount):
        return current_tier_amount / 1_000
    def convert_downward(current_tier_amount):
        return current_tier_amount * 1_000

    if result_type == 'plat':
        silver += convert_upward(copper)
        gold += convert_upward(silver)
        plat += convert_upward(gold)
        return plat
    elif result_type == 'gold':
        silver += convert_upward(copper)
        gold += convert_upward(silver)
        gold += convert_downward(plat)
        return gold
    elif result_type == 'silver':
        silver += convert_upward(copper)
        gold += convert_downward(plat)
        silver += convert_downward(gold)
        return silver
    else: # result_type == copper
        gold += convert_downward(plat)
        silver += convert_downward(gold)
        copper += convert_downward(silver)
        return copper

def create_coin_dict(plat=0, gold=0, silver=0, copper=0):
    """
    Creates a new dictionary with all 4 coin types.
    Any coin type that doesn't have a value passed to this method defaults to 0.

    Keyword Arguments:
        plat (int): The value of platinum coin.
        gold (int): The value of gold coin.
        silver (int): The value of silver coin.
        copper (int): The value of copper coin.
    Returns:
        coin_dict (dict): A dictionary consisting of all 4 coin types. 
    """
    return {'plat': plat, 'gold': gold, 'silver': silver, 'copper': copper}

def coin_dict_to_copper(coin_dict):
    """
    Converts a coin dictionary down to a total amount of copper.

    Arguments:
        coin_dict (dict): A dictionary consisting of all 4 coin types.

    Returns:
        copper (int): The total copper value of the coin dictionary.
    """
    return convert_coin_type(**coin_dict)

def copper_to_coin_dict(copper):
    """
    Takes any amount of coppper and converts it into a dictionary with that same
    amount of copper.
    It then balances the dictionary, pushing values above 999 up to the next coin type.

    Arguments:
        copper (int): The amount of copper to convert into a coin dictionary.

    Returns:
        coin_dict (dict): A dictionary consisting of all 4 coin types.
    """
    return balance_coin_dict(create_coin_dict(copper=copper))

def is_homogenized(coin_dict):
    """
    Checks a coin dictionary to find out if there's only 1 type of coin with a value above 0.

    Arguments:
        coin_dict (dict): A dictionary consisting of all 4 coin types.
    
    Returns:
        is_homogenized (boolean): True or False
    """
    num = 0
    for coin_value in coin_dict.values():
        if coin_value > 0:
            num += 1
    if num > 1:
        return False
    else:
        return True

def generate_coin_object(coin_dict=None, copper=None):
    """
    Determines what type of coin object and key to generate based on the coin dictionary.

    Keyword Arguments:
        coin_dict (dict): A dictionary consisting of all 4 coin types.
        copper (integer): A value representing the total amount of coin.

    Returns:
        coin_obj (object): The final spawned object, with its key properly set.
    """
    if copper is not None:
        coin_dict = copper_to_coin_dict(copper)
    elif coin_dict is None and copper is None:
        coin_dict = create_coin_dict()
        # A coin must have some sort of value, therefore generate a single copper coin.
        coin_dict['copper'] = 1

    homogenized = is_homogenized(coin_dict)
    coin_prototype = None
    pluralized = False

    if homogenized:
        for coin_type, coin_value in coin_dict.items():
            if coin_value > 0:
                coin_prototype = f"{coin_type}_coin"
            if coin_value > 1:
                pluralized = True
    else:
        coin_prototype = 'coin_pile'

    coin_obj = spawn(coin_prototype)[0]
    coin_obj.db.coin = coin_dict

    if pluralized:
        coin_obj.key = f"a pile of {coin_obj.db.plural_key}"

    return coin_obj
```

***

[Return to Table of Contents](https://github.com/kovitikus/hecate/blob/master/docs/evennia/object_grouping.md#table-of-contents)

The last thing I'll include here is a link to my prototypes, because they are also used in my logic, but specific to my project. It does include my coin prototypes, which I rely on heavily for coin management.

These types of things are subject to change.

https://github.com/kovitikus/hecate/blob/master/items/item_prototypes.py