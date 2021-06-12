"""
Commands

Commands describe the input the account can do to the game.

"""
import re

from evennia import TICKER_HANDLER as tickerhandler
from evennia import Command as BaseCommand
from evennia import logger
from evennia import InterruptCommand
from evennia.utils import create, inherits_from
from evennia.utils.evmenu import EvMenu

from skills import skillsets


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
    def at_pre_cmd(self):
        """
        This hook is called before self.parse() on all commands.  If
        this hook returns anything but False/None, the command
        sequence is aborted.
        """
        self.caller.status.afk_check()

class CmdCharGen(Command):
    key = "chargen"

    def func(self):
        caller = self.caller
        EvMenu(caller, "characters.chargen", startnode="main", 
                cmd_on_exit="look", cmdset_mergetype="Replace", 
                cmdset_priority=1, auto_quit=True, auto_look=True, 
                auto_help=True)

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
            caller.msg('Usage: learn <skillset>')
            return

        caller.skill.learn_skillset(caller, self.args)

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
        caller.msg("Command is currently disabled.")
        
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
        result = caller.skill.generate_skill_list()
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

        self.arg_type = get_inventory_arg_type(args)

    def func(self):
        self.caller.inv.get_inventory(self.arg_type)

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
        main_hand, off_hand = caller.db.hands.values()
        hands = [main_hand, off_hand]
        

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
        self.caller.inv.inhand()

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
      get <object>
      get <object> from <container>

    Gets an object from your inventory or location and places it in your hands.
    """
    key = 'get'
    aliases = 'take'
    locks = "cmd:all()"

    def parse(self):
        caller = self.caller

        if not self.args:
            caller.msg("Usage: get <object> | get <object> from <container>")
            raise InterruptCommand
        args = self.args

        if 'from' in args:
            obj_arg = args.split('from', 1)[0].strip()
            container_arg = args.split('from', 1)[1].strip()

            container = caller.search(container_arg, quiet=True)[0]
            if not container:
                caller.msg(f"Could not find {container_arg}.")
                raise InterruptCommand
            else:
                if not container.tags.get('container'):
                    caller.msg(f"You can't get {obj_arg} from {container.name}.")
                    raise InterruptCommand
                self.container = container
                obj = caller.search(obj_arg, location=container, quiet=True)[0]
                if not obj:
                    caller.msg(f"Could not find {obj_arg}.")
                    raise InterruptCommand
                else:
                    self.caller_possess = True if obj.location == caller else False
                    self.obj = obj
        else:
            obj_arg = args.strip()
            obj = caller.search(obj_arg, quiet=True)[0]
            if not obj:
                caller.msg(f"Could not find {obj_arg}.")
                raise InterruptCommand
            else:
                self.caller_possess = True if obj.location == caller else False
                self.container = None
                self.obj = obj

        if caller == obj:
            caller.msg("You can't get yourself.")
            raise InterruptCommand

        if not obj.access(caller, 'get'):
            if obj.db.get_err_msg:
                caller.msg(obj.db.get_err_msg)
            else:
                caller.msg("You can't get that.")
            raise InterruptCommand

    def func(self):
        self.caller.item.get_object(self.obj, self.container, self.caller_possess)

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
    def parse(self):
        caller = self.caller

        if not self.args:
            caller.msg("Drop what?")
            raise InterruptCommand
        args = self.args.strip()

        obj = caller.search(args, quiet=True)[0]
        if not obj:
            caller.msg(f"|rYou are not in possession of {args}.|n")
            raise InterruptCommand
        else:
            self.obj = obj

    def func(self):
        self.caller.item.drop_object(self.obj)

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

    def parse(self):
        caller = self.caller
        if not self.args:
            caller.msg("Stow what?")
            raise InterruptCommand
        args = self.args.strip()

        obj = caller.search(args, location=[caller.location, caller],
                            nofound_string=f"You can't find {args}.",
                            multimatch_string=f"There are more than one {args}.")
        if not obj:
            raise InterruptCommand

        if caller == obj:
            caller.msg("You can't get yourself.")
            raise InterruptCommand
        if obj.location == caller:
            caller.msg(f"You already have {obj.name} in your inventory.")
            raise InterruptCommand

        if not obj.access(caller, 'get'):
            if obj.db.get_err_msg:
                caller.msg(obj.db.get_err_msg)
            else:
                caller.msg("You can't get that.")
            raise InterruptCommand

        # calling at_before_get hook method
        if not obj.at_before_get(caller):
            raise InterruptCommand

        self.obj = obj

    def func(self):
        self.caller.item.stow_object(self.obj)

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

        main_wield, off_wield, both_wield = caller.db.wielding.values()
        main_hand, off_hand = caller.db.hands.values()
        main_desc, off_desc = caller.db.hands_desc.values()

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
        if obj in [main_wield, off_wield, both_wield]: # Check for an item already wielded.
            caller.msg(f"You are already wielding {obj.name}.")
            return

        hands_req = obj.attributes.get('wieldable')

        # main hand is dominate.


        if obj not in [main_hand, off_hand]: # Automagically get the object from the inventory.
            if main_hand and not main_wield:
                caller.msg(f"You stow away {main_hand.name}.")
                caller.location.msg_contents(f"{caller.name} stows away {main_hand.name}.", exclude=caller)
                caller.db.hands['main'] = None
            caller.msg(f"You get {obj.name} from your inventory.")
            caller.location.msg_contents(f"{caller.name} gets {obj.name} from their inventory.", exclude=caller)
            caller.db.hands['main'] = obj
            # Refresh hand variables before the next check.
            main_hand, off_hand = caller.db.hands.values()
            
        
        if obj in [main_hand, off_hand]:
            if hands_req == 1:
                if inherits_from(obj, 'items.objects.OffHand'): #For wielding shields.
                    if obj == main_hand and not main_wield:
                        if off_hand: # If theres any item in the off hand, stow it first.
                            caller.db.hands['off'] = None
                            caller.msg(f"You stow away {off_hand.name}.")
                            caller.location.msg_contents(f"{caller.name} stows away {off_hand.name}.", exclude=caller)
                        # Send the offhand weapon to the off hand.
                        caller.db.hands['main'] = None
                        caller.db.hands['off'] = obj
                        caller.msg(f"You swap {obj.name} to your {off_desc} hand.")
                        caller.location.msg_contents(f"{caller.name} swaps {obj.name} to their {off_desc} hand.", exclude=caller)
                    # Offhand item is certainly already in the off hand.
                    caller.msg(f"You wield {obj.name} in your {off_desc} hand.")
                    caller.location.msg_contents(f"{caller.name} wields {obj.name} in their {off_desc} hand.", exclude=caller)
                    caller.db.wielding['off'] = obj
                elif obj == off_hand and not inherits_from(obj, 'items.objects.OffHand'): # Make sure the item is a main hand wield.
                    caller.msg(f"You swap the contents of your hands and wield {obj.name} in your {main_desc} hand.")
                    caller.location.msg_contents(f"{caller.name} swaps the content of their hands "
                                                    f"and wields {obj.name} in their {main_desc} hand.", exclude=caller)
                    caller.db.hands['main'] = obj
                    if main_hand:
                        caller.db.hands['main'] = None
                        caller.db.hands['off'] = obj
                    caller.db.wielding['main'] = obj
                elif obj == main_hand and not inherits_from(obj, 'items.objects.OffHand'): # Make sure the item is a main hand wield.
                    caller.msg(f"You wield {obj.name} in your {main_desc} hand.")
                    caller.location.msg_contents(f"{caller.name} wields {obj.name} in their {main_desc} hand.", exclude=caller)
                    caller.db.wielding['main'] = obj
            elif hands_req == 2:
                if obj == off_hand:
                    if main_hand:
                        caller.msg(f"You stow away {main_hand.name}.")
                        caller.location.msg_contents(f"{caller.name} stows away {main_hand}.", exclude=caller)
                        caller.db.hands['main'] = None
                elif obj == main_hand:
                    if off_hand:
                        caller.msg(f"You stow away {off_hand.name}.")
                        caller.location.msg_contents(f"{caller.name} stows away {off_hand}.", exclude=caller)
                        caller.db.hands['off'] = None
                caller.msg(f"You wield {obj.name} in both hands.")
                caller.location.msg_contents(f"{caller.name} wields {obj.name} in both hands.", exclude=caller)
                caller.db.wielding['both'] = obj
                caller.db.hands['main'] = obj
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
        main_wield, off_wield, both_wield  = wielding.values()
        
        if off_wield:
            caller.msg(f"You stop wielding {off_wield.name} in your offhand.")
            caller.location.msg_contents(f"{caller.name} stops wielding {off_wield.name} in their offhand.", exclude=caller)
            wielding['off'] = None
        elif main_wield and not off_wield:
            caller.msg(f"You stop wielding {main_wield.name}.")
            caller.location.msg_contents(f"{caller.name} stops wielding {main_wield.name}.", exclude=caller)
            wielding['main'] = None
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
            elif args in ['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw']:
                # Looking at an exit returns the appearance of its destination.
                # https://i.imgur.com/6KFXUMd.png
                target = None
                for exit in self.caller.location.exits:
                    if exit.attributes.has('card_dir'):
                        if exit.db.card_dir == args:
                            target = exit
                if target:
                    msg = target.return_appearance(self.caller)
                else:
                    msg = "There is no exit to look at in that direction!"
                self.caller.msg(msg)
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
                if not inherits_from(obj, 'items.objects.Lighting'):
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
    """
    Usage: stock

    Returns the stock of a merchant in the room.
    """
    key = 'stock'
    def func(self):
        room_contents = self.caller.location.contents
        for i in room_contents:
            if i.tags.get('merchant', category='sentient_class'):
                self.caller.msg(i.merch.return_stock())

class CmdBuy(Command):
    """
    Usage: buy <quantity> <item>

    If the quantity is not specified it defaults to 1.

    Examples:
            > buy 10 torch
            The merchant places 10 torches in front of you.

            > buy tea
            The bartender places a cup of tea in front of you.
    """
    key = 'buy'
    def parse(self):
        if not self.args:
            self.caller.msg("You must specify an item to purchase!")
            raise InterruptCommand
        else:
            self.args = self.args.strip()
            args = self.args
        regex = r"\d"
        if re.search(regex, self.args) is not None:
            args = self.args.split(" ", 1)
            quantity = int(args[0])
            item = args[1]
        else:
            quantity = 1
            item = args

        self.quantity = quantity
        self.item = item

    def func(self):
        caller = self.caller
        room_contents = caller.location.contents
        for i in room_contents:
            if i.tags.get('merchant', category='sentient_class'):
                caller.msg(i.merch.sell_item(caller, self.item, quantity=self.quantity))

class CmdConvertCoin(Command):
    """
    Usage:  convertcoin <amount> <type> to <type>

    Example:
            > convertcoin 1 gold to copper
            1 gold is equel to 1000000 copper
    """
    key = 'convertcoin'
    def parse(self):
        if not self.args:
            self.caller.msg("Usage: convertcoin <amount> <type> to <type>")
            raise InterruptCommand
        else:
            args = self.args.strip()
            args = args.split('to', 1)
            amount = args[0].split(' ', 1)
            self.coin_value = int(amount[0].strip())
            self.coin_type = amount[1].strip()
            self.result_type = args[1].strip()
    def func(self):
        coin_type = self.coin_type
        coin_value = self.coin_value
        result_type = self.result_type

        if coin_type == 'plat':
            result_value = self.caller.currency.convert_coin(plat=coin_value, result_type=result_type)
        elif coin_type == 'gold':
            result_value = self.caller.currency.convert_coin(gold=coin_value, result_type=result_type)
        elif coin_type == 'silver':
            result_value = self.caller.currency.convert_coin(silver=coin_value, result_type=result_type)
        elif coin_type == 'copper':
            result_value = self.caller.currency.convert_coin(copper=coin_value, result_type=result_type)
        self.caller.msg(f"{coin_value} {coin_type} is equal to {result_value} {result_type}")

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

            qty_obj = args[0].strip().split(' ', 1) # qty_obj = ['#', 'object']
            self.quantity = qty_obj[0] # quantity = '#'
            if not self.quantity > 0:
                caller.msg("Quantity must be greater than zero!")
                raise InterruptCommand
            self.qty_obj = qty_obj[1] # qty_obj = 'object'

            self.pile = args[1].strip()
            self.pile_loc = caller.location

        elif 'from' and 'my' in args:
            # split # object from my pile
            self.split_type = 'from'
            args = args.split('from', 1) # args = [' # object', ' my pile']

            qty_obj = args[0].strip().split(' ', 1) # qty_obj = ['#', 'object']
            self.quantity = qty_obj[0] # quantity = '#'
            if not self.quantity > 0:
                caller.msg("Quantity must be greater than zero!")
                raise InterruptCommand
            self.qty_obj = qty_obj[1] # qty_obj = 'object'

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
                msg = caller.item.split_pile(split_type, pile, pile_loc)
            elif split_type == 'from':
                msg = caller.item.split_pile(split_type, pile, pile_loc, self.quantity, self.qty_obj)

        caller.msg(msg)

class CmdInstance(Command):
    """
    Usage:
        instance - Used by itself, the instance command returns a summary of the 
                    character's currenly occupied or most recently occupied instance.

        instance menu - Opens the menu that allows for management of instances,
                        including creation, destruction, and resetting.
    """
    key = 'instance'
    aliases = 'inst'
    inst_summary = True
    inst_menu = False

    def parse(self):
        if self.args:
            self.inst_summary = False

            args = self.args.strip()
            if 'menu' in args:
                self.inst_menu = True

    def func(self):
        caller = self.caller

        if self.inst_summary:
            caller.instance.inst_summary()
        elif self.inst_menu:
            EvMenu(caller, 'rooms.instance_menu', startnode='start_menu')
        else:
            return

class CmdAFKTimer(Command):
    """
    Sets the character's AFK Timer in seconds.
    The default value is 600s (10m).

    Usage:
        afktimer 900
    """
    key = 'afktimer'
    aliases = 'afktime'

    def func(self):
        caller = self.caller

        if not self.args:
            caller.msg("You must enter an integer.")
            return
        else:
            args = self.args.strip()
            try:
                args = int(args)
            except:
                self.caller.msg("The value must be an integer greater than 0.")
                raise ValueError

            if not caller.attributes.has('afk_timer'):
                caller.attributes.add('afk_timer', args)
            else:
                caller.db.afk_timer = args
                caller.msg(f"You set your AFK Timer to {args} seconds.")


def get_inventory_arg_type(args):
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
