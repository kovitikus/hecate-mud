"""
Commands

Commands describe the input the account can do to the game.

"""

from evennia import Command as BaseCommand
from evennia import logger
from evennia.commands.default.building import ObjManipCommand
from evennia import InterruptCommand
from evennia.utils.evmenu import EvMenu
from evennia.utils import create, inherits_from
from world.skills import skillsets
from world.generic_str import article
from world import general_mechanics as gen_mec


class Command(BaseCommand):
    """
    Inherit from this if you want to create your own command styles
    from scratch.  Note that Evennia's default commands inherits from
    MuxCommand instead.

    Note that the class's `__doc__` string (this text) is
    used by Evennia to create the automatic help entry for
    the command, so make sure to document consistently here.

    Each Command implements the following methods, called
    in this order (only func() is actually required):
        - at_pre_cmd(): If this returns anything truthy, execution is aborted.
        - parse(): Should perform any extra parsing needed on self.args
            and store the result on self.
        - func(): Performs the actual work.
        - at_post_cmd(): Extra actions, often things done after
            every command, like prompts.
    """
    pass

class CmdDesc(Command):
    key = "desc"
    def func(self):
        caller = self.caller
        desc = caller.desc()
        self.msg(desc)

class CmdCharGen(Command):
    key = "chargen"

    def func(self):
        caller = self.caller
        EvMenu(caller, "world.chargen", startnode="main", cmd_on_exit="look", cmdset_mergetype="Replace", cmdset_priority=1,
       auto_quit=True, auto_look=True, auto_help=True)

class CmdLearnSkillset(Command):
    key = 'learn'
    """
    Usage: learn <skillset>
    """

    def parse(self):
        self.args = self.args.lstrip()
        caller = self.caller
        args = self.args
        
        if not args:
            caller.msg("Usage: learn <skillset>")
            raise InterruptCommand

        if args not in skillsets.VIABLE_SKILLSETS:
            caller.msg(f"{args} is not a viable skillset!")
            raise InterruptCommand

    def func(self):
        caller = self.caller
        if not self.args:
            caller.msg('Usage: learn <skillset> <skill>')
            return

        skillsets.learn_skillset(self.caller, self.args)

class CmdGrantSP(Command):
    key = '@grant-sp'
    '''
    Usage: @grant-sp <person> <number> <skillset>
    '''
    def parse(self):
        caller = self.caller
        args = self.args.lstrip()
        try:
            self.person, self.number, self.skillset = args.split(" ", 2)
        except ValueError:
            caller.msg("Requires 3 arguments. Usage: @grant-sp <person> <number> <skillset>")
            raise InterruptCommand

        self.char = caller.search(self.person)
        if not self.char:
            raise InterruptCommand

        try:
            self.number = int(self.number)
        except ValueError:
            caller.msg("The number must be an integer.")
            raise InterruptCommand
        print(f"Viable Skillsets: {skillsets.VIABLE_SKILLSETS}")
        if self.skillset not in skillsets.VIABLE_SKILLSETS:
            caller.msg(f"{self.skillset} is not a viable skillset!")
            raise InterruptCommand
    
    def func(self):
        caller = self.caller
        char = self.char
        num = self.number
        skillset = self.skillset
        skillset = char.attributes.get(skillset)
        skillset['total_sp'] += num
        caller.msg(f'Granted {char} {num} skillpoints in {self.skillset}.')

class CmdTest(Command):
    key = 'testy'

    def func(self):
        caller = self.caller
        #caller.msg("Command is currently disabled.")

        char = create.create_object(typeclass='typeclasses.characters.Character', key='char1')
        if char:
            caller.msg('Character was created.')
        equip_dic = char.attributes.get('equipment')
        caller.msg(f"This is the test character's current equipment: {str(equip_dic)}")
        bag = equip_dic.get('inventory_container')
        caller.msg(f"This is the bag we have equipped: {bag}")
        bag_max_slots = bag.db.max_slots
        char_max_slots = char.db.inventory_slots['max_slots']
        caller.msg(f"The bag's max slots: {bag_max_slots}")
        caller.msg(f"The character's max inventory slots: {char_max_slots}")
        success = char.delete()
        if success:
            caller.msg(f"Character was successfully deleted!")
        
        
        # caller.msg("This should be an image!")
        # caller.msg(image="https://i.imgur.com/2Wo1BpT.png")
        # caller.msg(video="https://youtu.be/YUOxwynb9UU")
        # caller.msg(video="https://vimeo.com/358147193")
        # caller.msg("Printing something to the log file!")
        # logger.log_msg("Something to the log file!!")
        # print("printing to the log file too!")

class CmdSkills(Command):
    """
    Prints the character's skills to the screen, along with related information such as Rank Score.

    Usage:
        skills
        skill
    """
    key = 'skills'
    aliases = ['skill']

    def func(self):
        caller = self.caller
        result = skillsets.generate_skill_list(caller)
        caller.msg(result)

class CmdInventory(Command):
    """
    Shows your inventory.

    Usage:
      inventory
      inv
      i
        Using inv by itself will result in a summary printed to the character.

        inv all or inv 1
            Lists all items in the inventory.
        inv fav or inv 2
        inv weap or inv 3
        inv armor or inv 4
        inv clothing 5
        inv containers 6
        inv jewelry 7
        inv relics 8
        inv consumables 9
        inv quest items 10
        inv crafting materials 11
        inv misc 12


    """
    key = "inventory"
    aliases = ["inv", "i"]
    locks = "cmd:all()"
    def parse(self):
        self.args = self.args.lstrip()
        args = self.args

        self.arg_type = get_arg_type(args)

    def func(self):
        """check inventory"""
        arg_type = self.arg_type
        caller = self.caller
        items = caller.contents
        left_hand, right_hand = caller.db.hands.values()
        equip_items = caller.db.equipment.values()

        # Remove hands and append all other items to a new list.
        filtered_items = []
        for i in items:
            if i not in [left_hand, right_hand, equip_items]:
                if i not in equip_items:
                    filtered_items.append(i)

        if not filtered_items:
            string = "Your inventory is empty."
        else:
            # if arg_type == 0:
                # Generate summary
                # Count the number of items in the inventory.
                # Show the maximum number of inventory slots.
                # Show each category that has an item and how many items are in the category
                # Show currency.
            if arg_type == 1:
                table = self.styled_table(border="header")
                string = get_all_items(filtered_items, table)
            else:
                final_list = get_inv_final_list(filtered_items, arg_type)

                table = self.styled_table(border="header")
                for item in final_list:
                    table.add_row(f"|C{item.name}|n {item.db.desc or ''}")
                
                category_string = get_category_string(arg_type)

                string = f"|wYou are carrying:\n{category_string}\n{table}"
        # Add currency
        string = f"{string}\n{gen_mec.return_currency(caller)}"
        caller.msg(string)

class CmdEquip(Command):
    """
    Head - Crown/Helmet/Hat
    Neck - Necklace/Amulet
    Shoulders - Shoulder Pads
    Chest - Chest Armor
    Arms - Sleeves
    Hands - Pair of Gloves
    Fingers - Rings (Maximum of 4 for balancing purposes.)
    Waist - Belt/Sash
    Thighs - Greaves
    Calves - Greaves
    Feet - Boots/Shoes/Sandals

    Bag - Satchel/Backpack/Sack/Bag (Determines maximum inventory slots.)

    Weapons
        - Any weapon can be manually wielded from the inventory or the ground via the `wield` command.
        - Equipped weapons are automatically wielded if no other weapon is manually wielded.
        - Shields and other offhands can also be equipped.
        - 2H weapons have a limit of 1 slot per type.
        - 1H weapons have a limit of 2 slots per type (Sword, Dagger, etc.) to compensate for dual-wielding.
        - Offhand weapons have a limit of 1 slot per type. (Shield, Tome, etc.)
    """
    key = 'equip'
    locks = "cmd:all()"

    def parse(self):
        if self.args:
            self.args = self.args.strip()

    def func(self):
        caller = self.caller
        left_hand, right_hand = caller.db.hands.values()
        hands = [left_hand, right_hand]
        

        if caller.attributes.has('equipment'):
            equip_dic = {}
            equip_dic = caller.attributes.get('equipment')
        else:
            caller.msg(f"You have no equipment!")

        if self.args:
            args = self.args
            item = caller.search(args, quiet=True)
            if item:

                #check the location of the item, if it is not in the inventory, add it to the inventory
                # if the inventory is full, return an error
                # if item.location == caller.location:
                    #not in hands or inventory, but on the ground of the room.
                # elif item.location == caller and in hands:
                    #item is in hands and doesn't count toward inventory, check if inventory is full and
                    #move item to inventory before equipping.
                # elif item.location == caller and not in hands:
                    #in inventory and not in hands, green light to go to equip section

                if item.tags.has('inventory_container'):
                    current_inventory_container = equip_dic.get('inventory_container')
                    if current_inventory_container != None:
                        if item.db.max_slots < current_inventory_container.db.max_slots:
                            caller.msg(f"Your currently equipped container is better than {item.get_display_name()}.")
                            return
                        else:
                            equip_dic['inventory_container'] = item
                            caller.db.inventory_slots['max_slots'] = item.db.max_slots

                if item.tags.has('chest'):
                    chest_slot = equip_dic.get('chest')
                    if chest_slot == None:
                        equip_dic['chest'] = item
                    else:
                        caller.msg("You must unequip your current chest piece first, before equipping a new one.")
                        return
        else:
            # List the equipment
            caller.equip.list_equipment()

class CmdUnequip(Command):
    pass

class CmdInhand(Command):
    key = 'inhand'
    aliases = 'inh'
    
    def func(self):
        caller = self.caller

        left_wield, right_wield, both_wield  = caller.db.wielding.values()

        left_hand, right_hand = caller.db.hands.values()

        if left_hand:
            left_item = left_hand.name
        else:
            left_item = 'nothing'

        if right_hand:
            right_item = right_hand.name
        else:
            right_item = 'nothing'

        if not left_hand and not right_hand:
            caller.msg(f"Your hands are empty.")
            return
        
        
        if left_wield and not right_wield:
            caller.msg(f"You are wielding {left_item} in your left hand and holding {right_item} in your right hand.")
        elif right_wield and not left_wield:
            caller.msg(f"You are holding {left_item} in your left hand and wielding {right_item} in your right hand.")
        elif left_wield and right_wield:
            caller.msg(f"You are wielding {left_item} in your left hand and {right_item} in your right hand.")
        elif both_wield:
            caller.msg(f"You are wielding {right_item} in both hands.")
        else:
            caller.msg(f"You are holding {left_item} in your left hand and {right_item} in your right hand.")

class CmdStand(Command):
    key = 'stand'
    def func(self):
        caller = self.caller
        db = caller.db
        if db.standing:
            caller.msg("You are already standing.")
            return
        else:
            db.standing = True
            db.kneeling = False
            db.sitting = False
            db.lying = False
            caller.msg("You stand up.")

class CmdSit(Command):
    key = 'sit'
    def func(self):
        caller = self.caller
        db = caller.db
        if db.sitting:
            caller.msg("You are already sitting.")
        else:
            db.standing = False
            db.kneeling = False
            db.sitting = True
            db.lying = False
            caller.msg("You sit down.")

class CmdKneel(Command):
    key = 'kneel'
    def func(self):
        caller = self.caller
        db = caller.db
        if db.kneeling:
            caller.msg("You are already kneeling.")
        else:
            db.standing = False
            db.kneeling = True
            db.sitting = False
            db.lying = False
            caller.msg("You kneel.")

class CmdLie(Command):
    key = 'lie'
    aliases = ['lay',]
    def func(self):
        caller = self.caller
        db = caller.db
        if db.lying:
            caller.msg("You are already lying down.")
        else:
            db.standing = False
            db.kneeling = False
            db.sitting = False
            db.lying = True
            caller.msg("You lie down.")

class CmdTakeFrom(Command):
    """
    Usage:
 
        take <item> from <container>
    
    Gets an item from the container, if it's in there.
    """
    key = 'take'
 
    def parse(self):
        # get args into 2 variables
        self.item_arg, self.container_arg = self.args.split("from")
        self.item_arg = self.item_arg.strip()
        self.container_arg = self.container_arg.strip()
     
           
 
    def func(self):
        caller = self.caller
        container_arg = self.container_arg
        item_arg = self.item_arg

        container = caller.search(container_arg, location=caller.location, quiet=True) # Check if container is in the room.
        if container:
            if len(container):
                container = container[0]
            item = caller.search(item_arg, location=container, quiet=True) # Check if the item is in the container.
            if item:
                if len(item):
                    item = item[0]
                item.move_to(caller, quiet=True) #move the item to the caller inventory
                caller.msg(f"You take {item} from {container}.")
                caller.location.msg_contents(f"{caller.name} takes {item} from {container}.", exclude=caller)
            else:
                caller.msg(f"{item_arg} isn't in {container}!")
        else:
            caller.msg(f"{container_arg} doesn't exist!")
            return

class CmdPut(Command):
    """
    Usage: 
        put <item> in <container>
    
    Finds an item around the character and puts it in a container.
    """
    key = 'put'

    def parse(self):
        self.item_arg, self.container_arg = self.args.split('in')
        self.item_arg = self.item_arg.strip()
        self.container_arg = self.container_arg.strip()

    def func(self):
        caller = self.caller
        item_arg = self.item_arg
        container_arg = self.container_arg

        # Find the item.
        # Location unset, search conducted within the character and its location.
        item = caller.search(item_arg, quiet=True)
        if item:
            if len(item):
                item = item[0]
            container = caller.search(container_arg, quiet=True)
            if container:
                if len(container):
                    container = container[0]
                if item.location == caller:
                    caller.msg(f"You place {item.name} in {container.name}.")
                    caller.msg_contents(f"{caller.name} places {item.name} in {container.name}.", exclude=caller)
                elif item.location == caller.location:
                    caller.msg(f"You pick up {item.name} and place it in {container.name}.")
                    caller.msg_contents(f"{caller.name} picks up {item.name} and places it in {container.name}.", exclude=caller)
                item.move_to(container, quiet=True)
            else:
                caller.msg(f"Could not find {container_arg}!")
        else:
            caller.msg(f"Could not find {item_arg}!")

class CmdGet(Command):
    """
    Pick up something.

    Usage:
      get <obj>

    Gets an object from your inventory or location and places it in your hands.
    """
    key = "get"
    # aliases = ["take",]
    locks = "cmd:all()"
    

    def func(self):
        """Implements the command."""
        #TODO: Fix the missing echo when picking up an item while wielding in both hands.
        #TODO: Allow auto-stow of items in hand and continue to pick up obj if more than one exists in location.
        caller = self.caller
        if not self.args:
            caller.msg("Get what?")
            return
        args = self.args.strip()

        left_wield, right_wield, both_wield  = caller.db.wielding.values()
        left_hand, right_hand = caller.db.hands.values()
        

        obj = caller.search(args, location=[caller.location, caller], quiet=True)
        if not obj:
            self.caller.msg(f"|r{args} cannot be found.|n")
            return
        if len(obj):
            obj = obj[0]
        if caller == obj:
            caller.msg("You can't get yourself.")
            return
        if not obj.access(caller, 'get'):
            if obj.db.get_err_msg:
                caller.msg(obj.db.get_err_msg)
            else:
                caller.msg("You can't get that.")
            return
        if obj in [left_hand, right_hand]:
            caller.msg(f"You are already carrying {obj.name}.")
            return

        # calling at_before_get hook method
        if not obj.at_before_get(caller):
            return
        
        # Check if wielding a single weapon/shield in left hand and stow it.
        if left_wield:
            caller.msg(f"You stop wielding {left_hand.name} and stow it away.")
            caller.db.hands['left'] = None
            caller.db.wielding['left'] = None

        # If both hands have objects, stow the dominate hand.
        if right_hand and left_hand:
            caller.msg(f"You stow away {right_hand.name}.")
            caller.location.msg_contents(f"{caller.name} stows away {right_hand.name}.", exclude=caller)
            caller.db.hands['right'] = None

        # Wielding with both hands technically only holds the item in the right hand (for now).
        # So we already know the left hand is free to get items.
        if both_wield:
            caller.msg(f"You stop wielding {both_wield.name}.")
            caller.location.msg_contents(f"{caller.name} stops wielding {both_wield.name}.", exclude=caller)
            caller.db.wielding['both'] = None

        # Decide the location of the item and echo it.
        elif obj.location == caller:
            caller.msg(f"You get {obj.name} from your inventory.")
            caller.location.msg_contents(f"{caller.name} gets {obj.name} from their inventory.", exclude=caller)
        elif obj.location == caller.location:
            caller.msg(f"You pick up {obj.name}.")
            caller.location.msg_contents(f"{caller.name} picks up {obj.name}.", exclude=caller)

        if right_hand and not left_hand:
            caller.db.hands['left'] = obj
        else:
            caller.db.hands['right'] = obj
        
        obj.move_to(caller, quiet=True)

        # calling at_get hook method
        obj.at_get(caller)

class CmdDrop(Command):
    """
    drop something
    Usage:
      drop <obj>
    Lets you drop an object from your inventory into the
    location you are currently in.
    """

    key = "drop"
    locks = "cmd:all()"
    

    def func(self):
        """Implement command"""

        caller = self.caller
        if not self.args:
            caller.msg("Drop what?")
            return
        args = self.args.strip()

        left_hand, right_hand = caller.db.hands.values()

        wielding = caller.db.wielding
        left_wield, right_wield, both_wield  = wielding.values()
        
        obj = caller.search(args, location=[caller, caller.location], quiet=True)
        if not obj:
            caller.msg(f"|rYou are not in possession of {args}.|n")
            return

        if len(obj):
            obj = obj[0]

        # Call the object script's at_before_drop() method.
        if not obj.at_before_drop(caller):
            return

        
        if obj in [left_hand, right_hand]:
            # If the object is currently wielded, stop wielding it and drop it.
            if obj in [left_wield, right_wield, both_wield]:
                caller.msg(f"You stop wielding {obj.name} and drop it.")
                caller.location.msg_contents(f"{caller.name} stops wielding {obj.name} and drops it.", exclude=caller)
                if left_wield:
                    wielding['left'] = None
                else:
                    wielding['right'], wielding['both'] = None, None
            else:
                caller.msg(f"You drop {obj.name}.")
                caller.location.msg_contents(f"{caller.name} drops {obj.name}.", exclude=caller)
            if obj == left_hand:
                caller.db.hands['left'] = None
            else:
                caller.db.hands['right'] = None
        elif obj.location == caller:
            caller.msg(f"You pull {obj.name} from your inventory and drop it on the ground.")
            caller.location.msg_contents(f"{caller.name} pulls {obj.name} from their inventory and drops it on the ground.", exclude=caller)
        elif obj.location == caller.location:
            caller.msg(f"The {obj.name} is already on the ground.")
            return

        obj.move_to(caller.location, quiet=True)

        # Call the object script's at_drop() method.
        obj.at_drop(caller)

class CmdStow(Command):
    """
    pick up something
    Usage:
      stow <obj>
    Picks up an object from your location and puts it in
    your inventory.
    """

    key = 'stow'
    locks = 'cmd:all()'
    

    def func(self):
        """implements the command."""
        caller = self.caller
        if not self.args:
            caller.msg("Stow what?")
            return
        args = self.args.strip()

        left_hand, right_hand = caller.db.hands.values()
        wielding = caller.db.wielding
        left_wield, right_wield, both_wield  = wielding.values()
        
        obj = caller.search(args, location=[caller.location, caller],
                            nofound_string=f"You can't find {args}.",
                            multimatch_string=f"There are more than one {args}.")
        if not obj:
            return
        if caller == obj:
            caller.msg("You can't get yourself.")
            return
        if not obj.access(caller, 'get'):
            if obj.db.get_err_msg:
                caller.msg(obj.db.get_err_msg)
            else:
                caller.msg("You can't get that.")
            return

        # calling at_before_get hook method
        if not obj.at_before_get(caller):
            return
        
        if obj in [left_hand, right_hand]:
            # If the stowed object is currently wielded, stop wielding it and stow it.
            if obj in [left_wield, right_wield, both_wield]:
                caller.msg(f"You stop wielding {obj.name} and stow it away.")
                caller.location.msg_contents(f"{caller.name} stops wielding {obj.name} and stows it away.", exclude=caller)
                if obj == left_wield:
                    wielding['left'] = None
                elif obj == right_wield:
                    wielding['right'] = None
                else:
                    wielding['both'] = None
            else:
                caller.msg(f"You stow away {obj.name}.")
                caller.location.msg_contents(f"{caller.name} stows away {obj.name}.", exclude=caller)
            if obj == left_hand:
                caller.db.hands['left'] = None
            else:
                caller.db.hands['right'] = None
        elif obj.location == caller.location:
            caller.msg(f"You pick up {obj.name} and stow it away.")
            caller.location.msg_contents(f"{caller.name} picks up {obj.name} and stows it away.", exclude=caller)
            obj.move_to(caller, quiet=True)
        elif obj.location == caller:
            caller.msg(f"You already have {obj.name} in your inventory.")
            return

        # calling at_get hook method
        obj.at_get(caller)

class CmdWield(Command):
    """
    Wield a weapon.
    
    Usage: wield <weapon>
    """
    key = 'wield'

    def func(self):
        caller = self.caller
        if not self.args:
            caller.msg("Usage: wield <weapon>")
            return
        args = self.args.strip()
        left_hand, right_hand = caller.db.hands.values()
        left_wield, right_wield, both_wield = caller.db.wielding.values()

        obj = caller.search(args, location=[caller],
                            nofound_string="You must be holding a weapon to wield it.",
                            multimatch_string=f"There are more than one {args}.")
        if not obj:
            return
        if obj == caller:
            caller.msg("You can't wield yourself.")
            return
        if not obj.attributes.get('wieldable'):
            caller.msg("That's not a wieldable item.")
        if obj in [left_wield, right_wield, both_wield]: # Check for an item already wielded.
            caller.msg(f"You are already wielding {obj.name}.")
            return

        hands_req = obj.attributes.get('wieldable')

        # Right hand is dominate.


        if obj not in [left_hand, right_hand]: # Automagically get the object from the inventory.
            if right_hand and not right_wield:
                caller.msg(f"You stow away {right_hand.name}.")
                caller.location.msg_contents(f"{caller.name} stows away {right_hand.name}.", exclude=caller)
                caller.db.hands['right'] = None
            caller.msg(f"You get {obj.name} from your inventory.")
            caller.location.msg_contents(f"{caller.name} gets {obj.name} from their inventory.", exclude=caller)
            caller.db.hands['right'] = obj
            # Refresh hand variables before the next check.
            left_hand, right_hand = caller.db.hands.values()
            
        
        if obj in [left_hand, right_hand]:
            if hands_req == 1:
                if inherits_from(obj, 'typeclasses.objects.OffHand'): #For wielding shields.
                    if obj == right_hand and not right_wield:
                        if left_hand: # If theres any item in the left hand, stow it first.
                            caller.db.hands['left'] = None
                            caller.msg(f"You stow away {left_hand.name}.")
                            caller.location.msg_contents(f"{caller.name} stows away {left_hand.name}.", exclude=caller)
                        # Send the offhand weapon to the left hand.
                        caller.db.hands['right'] = None
                        caller.db.hands['left'] = obj
                        caller.msg(f"You swap {obj.name} to your left hand.")
                        caller.location.msg_contents(f"{caller.name} swaps {obj.name} to their left hand.", exclude=caller)
                    # Offhand item is certainly already in the left hand.
                    caller.msg(f"You wield {obj.name} in your left hand.")
                    caller.location.msg_contents(f"{caller.name} wields {obj.name} in their left hand.", exclude=caller)
                    caller.db.wielding['left'] = obj
                elif obj == left_hand and not inherits_from(obj, 'typeclasses.objects.OffHand'): # Make sure the item is a main hand wield.
                    caller.msg(f"You swap the contents of your hands and wield {obj.name} in your right hand.")
                    caller.location.msg_contents(f"{caller.name} swaps the content of their hands "
                                                    f"and wields {obj.name} in their right hand.", exclude=caller)
                    caller.db.hands['right'] = obj
                    if right_hand:
                        caller.db.hands['right'] = None
                        caller.db.hands['left'] = obj
                    caller.db.wielding['right'] = obj
                elif obj == right_hand and not inherits_from(obj, 'typeclasses.objects.OffHand'): # Make sure the item is a main hand wield.
                    caller.msg(f"You wield {obj.name} in your right hand.")
                    caller.location.msg_contents(f"{caller.name} wields {obj.name} in their right hand.", exclude=caller)
                    caller.db.wielding['right'] = obj
            elif hands_req == 2:
                if obj == left_hand:
                    if right_hand:
                        caller.msg(f"You stow away {right_hand.name}.")
                        caller.location.msg_contents(f"{caller.name} stows away {right_hand}.", exclude=caller)
                        caller.db.hands['right'] = None
                elif obj == right_hand:
                    if left_hand:
                        caller.msg(f"You stow away {left_hand.name}.")
                        caller.location.msg_contents(f"{caller.name} stows away {left_hand}.", exclude=caller)
                        caller.db.hands['left'] = None
                caller.msg(f"You wield {obj.name} in both hands.")
                caller.location.msg_contents(f"{caller.name} wields {obj.name} in both hands.", exclude=caller)
                caller.db.wielding['both'] = obj
        elif obj.location == caller.location:
            caller.msg(f"You must be carrying a weapon to wield it.")
            return

class CmdUnwield(Command):
    """
    Unwield a weapon.
    Usage: unwield
    """

    key = 'unwield'

    def func(self):
        caller = self.caller
        wielding = caller.db.wielding
        left_wield, right_wield, both_wield  = wielding.values()
        
        if left_wield:
            caller.msg(f"You stop wielding {left_wield.name} in your offhand.")
            caller.location.msg_contents(f"{caller.name} stops wielding {left_wield.name} in their offhand.", exclude=caller)
            wielding['left'] = None
        elif right_wield and not left_wield:
            caller.msg(f"You stop wielding {right_wield.name}.")
            caller.location.msg_contents(f"{caller.name} stops wielding {right_wield.name}.", exclude=caller)
            wielding['right'] = None
        else:
            caller.msg(f"You stop wielding {both_wield.name}.")
            caller.location.msg_contents(f"{caller.name} stops wielding {both_wield.name}.", exclude=caller)
            wielding['both'] = None

class CmdLook(Command):
    """
    look at location or object
    Usage:
      look
      look <obj>
      look *<account>
    Observes your location or objects in your vicinity.
    """
    key = "look"
    aliases = ["l", "ls"]
    locks = "cmd:all()"
    
    def func(self):
        """
        Handle the looking.
        """
        caller = self.caller
        if not self.args:
            target = caller.location
            if not target:
                caller.msg("You have no location to look at!")
                return
        else:
            args = self.args.strip()
            if args == 'crowd':
                self.caller.location.crowd(self.caller)
                return
            else:
                target = caller.search(args, location=[caller, caller.location])
                if not target:
                    return
        self.msg((caller.at_look(target), {'type': 'look'}), options=None)

class CmdMatch(Command): #TODO: NOT FINISHED
    """
    Matches object in location or inventory.

    Usage: match <object>
    """
    key = 'match'

    def func(self):
        if not self.args:
            self.caller.msg("Usage: match <object>")
            return
        
        args = self.args.lstrip()

        obj = self.caller.search(args, location=[self.caller.location, self.caller])

        if not obj:
            self.caller.msg(f"Could not find {self.args}.")
            return
        else:
            self.caller.msg(f"Object found {self.args}.")
    pass

class CmdLight(Command):
    key = 'light'

    def parse(self):
        caller = self.caller
        if not self.args:
            caller.msg("Light what?")
            raise InterruptCommand
        else:
            args = self.args.strip()
            obj = caller.search(args, quiet=True)
            obj = obj[0]
            if obj:
                if not inherits_from(obj, 'typeclasses.objects.Lighting'):
                    caller.msg(f"{obj.get_display_name(caller)} cannot be lit!")
                    raise InterruptCommand
                else:
                    self.obj = obj
            else:
                caller.msg(f"{args} not found!")
                raise InterruptCommand

    def func(self):
        caller = self.caller
        obj = self.obj

        obj.ignite(caller)

class CmdStock(Command):
    key = 'stock'
    def func(self):
        room_contents = self.caller.location.contents
        for i in room_contents:
            if i.is_typeclass('typeclasses.characters.Merchant'):
                self.caller.msg(i.merch.return_stock())



def get_arg_type(args):
    arg_type = 0 # Default inventory summary.

    all_list = ['all', '1']
    fav_list = ['fav', 'favor', 'favorite', 'favorites', '2']
    weap_list = ['weap', 'weapon', 'weapons', '3']
    arm_list = ['arm', 'armor', '4']
    cloth_list = ['clo', 'cloth', 'clothing', '5']
    contain_list = ['con', 'cont', 'containers', '6']
    jewel_list = ['jew', 'jewel', 'jewelry', '7']
    relic_list = ['rel', 'relic', 'relics', '8']
    consume_list = ['cons', 'consum', 'consumable', 'consumables', '9']
    quest_list = ['que', 'ques', 'quest', '10']
    craft_list = ['cra', 'craf', 'craft', 'crafting', '11']
    misc_list = ['mis', 'misc', '12']

    if args in all_list: # List the entire inventory, separated by category.
        arg_type = 1
    elif args in fav_list:
        arg_type = 2
    elif args in weap_list:
        arg_type = 3
    elif args in arm_list:
        arg_type = 4
    elif args in cloth_list:
        arg_type = 5
    elif args in contain_list:
        arg_type = 6
    elif args in jewel_list:
        arg_type = 7
    elif args in relic_list:
        arg_type = 8
    elif args in consume_list:
        arg_type = 9
    elif args in quest_list:
        arg_type = 10
    elif args in craft_list:
        arg_type = 11
    elif args in misc_list:
        arg_type = 12
    return arg_type

def get_inv_final_list(filtered_items, arg_type):
    final_list = []
    for item in filtered_items:
        if arg_type == 2 and item.tags.get('favorite'):
            final_list.append(item)
        elif arg_type == 3 and item.tags.get('weapon'):
            final_list.append(item)
        elif arg_type == 4 and item.tags.get('armor'):
            final_list.append(item)
        elif arg_type == 5 and item.tags.get('clothing'):
            final_list.append(item)
        elif arg_type == 6 and item.tags.get('container'):
            final_list.append(item)
        elif arg_type == 7 and item.tags.get('jewelry'):
            final_list.append(item)
        elif arg_type == 8 and item.tags.get('relic'):
            final_list.append(item)
        elif arg_type == 9 and item.tags.get('consumable'):
            final_list.append(item)
        elif arg_type == 10 and item.tags.get('quest'):
            final_list.append(item)
        elif arg_type == 11 and item.tags.get('craft'):
            final_list.append(item)
        elif arg_type == 12 and item.tags.get('misc'):
            final_list.append(item)
    return final_list

def get_category_string(arg_type):
    if arg_type == 0:
        category_string = '|cSummary:|n'
    elif arg_type == 1:
        category_string = '|cAll Items:|n'
    elif arg_type == 2:
        category_string = '|cFavorites:|n'
    elif arg_type == 3:
        category_string = '|cWeapons:|n'
    elif arg_type == 4:
        category_string = '|cArmor:|n'
    elif arg_type == 5:
        category_string = '|cClothing:|n'
    elif arg_type == 6:
        category_string = '|cContainers:|n'
    elif arg_type == 7:
        category_string = '|cJewelry:|n'
    elif arg_type == 8:
        category_string = '|cRelics:|n'
    elif arg_type == 9:
        category_string = '|cConsumables:|n'
    elif arg_type == 10:
        category_string = '|cQuest Items:|n'
    elif arg_type == 11:
        category_string = '|cCrafting Materials:|n'
    elif arg_type == 12:
        category_string = '|cMisc.|n'
    return category_string

def get_all_items(filtered_items, table):
    fav_list = []
    weap_list = []
    arm_list = []
    cloth_list = []
    contain_list = []
    jewel_list = []
    relic_list = []
    consume_list = []
    quest_list = []
    craft_list = []
    misc_list = []

    # Sort all items based on category into appropriate lists.
    for item in filtered_items:
        if item.tags.get('favorite'):
            fav_list.append(item)
        elif item.tags.get('weapon'):
            weap_list.append(item)
        elif item.tags.get('armor'):
            arm_list.append(item)
        elif item.tags.get('clothing'):
            cloth_list.append(item)
        elif item.tags.get('container'):
            contain_list.append(item)
        elif item.tags.get('jewelry'):
            jewel_list.append(item)
        elif item.tags.get('relic'):
            relic_list.append(item)
        elif item.tags.get('consumable'):
            consume_list.append(item)
        elif item.tags.get('quest'):
            quest_list.append(item)
        elif item.tags.get('craft'):
            craft_list.append(item)
        elif item.tags.get('misc'):
            misc_list.append(item)

    # Generate table rows for each populated list based on category.
    if fav_list:
        category_string = get_category_string(2)
        table.add_row(f"{category_string}")
        for item in fav_list:
            table.add_row(f"|C{item.name}|n {item.db.desc or ''}")
    if weap_list:
        category_string = get_category_string(3)
        table.add_row(f"{category_string}")
        for item in weap_list:
            table.add_row(f"|C{item.name}|n {item.db.desc or ''}")
    if arm_list:
        category_string = get_category_string(4)
        table.add_row(f"{category_string}")
        for item in arm_list:
            table.add_row(f"|C{item.name}|n {item.db.desc or ''}")
    if cloth_list:
        category_string = get_category_string(5)
        table.add_row(f"{category_string}")
        for item in cloth_list:
            table.add_row(f"|C{item.name}|n {item.db.desc or ''}")
    if contain_list:
        category_string = get_category_string(6)
        table.add_row(f"{category_string}")
        for item in contain_list:
            table.add_row(f"|C{item.name}|n {item.db.desc or ''}")
    if jewel_list:
        category_string = get_category_string(7)
        table.add_row(f"{category_string}")
        for item in jewel_list:
            table.add_row(f"|C{item.name}|n {item.db.desc or ''}")
    if relic_list:
        category_string = get_category_string(8)
        table.add_row(f"{category_string}")
        for item in relic_list:
            table.add_row(f"|C{item.name}|n {item.db.desc or ''}")
    if consume_list:
        category_string = get_category_string(9)
        table.add_row(f"{category_string}")
        for item in consume_list:
            table.add_row(f"|C{item.name}|n {item.db.desc or ''}")
    if quest_list:
        category_string = get_category_string(10)
        table.add_row(f"{category_string}")
        for item in quest_list:
            table.add_row(f"|C{item.name}|n {item.db.desc or ''}")
    if craft_list:
        category_string = get_category_string(11)
        table.add_row(f"{category_string}")
        for item in craft_list:
            table.add_row(f"|C{item.name}|n {item.db.desc or ''}")
    if misc_list:
        category_string = get_category_string(12)
        table.add_row(f"{category_string}")
        for item in misc_list:
            table.add_row(f"|C{item.name}|n {item.db.desc or ''}")
    string = f"|wYou are carrying:\n{table}"
    return string