"""
Commands

Commands describe the input the account can do to the game.

"""

from evennia import Command as BaseCommand
from evennia import InterruptCommand
from evennia.utils.evmenu import EvMenu
from world import skillsets, attack_desc
from typeclasses.objects import ObjHands


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

class CmdLearnSkill(Command):
    key = 'learn'
    """
    Usage: learn <skillset> <skill>
    """

    def parse(self):
        caller = self.caller
        args = self.args.lstrip()
        try:
            self.skillset, self.skill = args.split(" ", 1)
        except ValueError:
            caller.msg("Usage: learn <skillset> <skill>")
            raise InterruptCommand

        if self.skillset not in skillsets.VIABLE_SKILLSETS:
            caller.msg(f"{self.skillset} is not a viable skillset!")
            raise InterruptCommand
        if self.skill not in skillsets.VIABLE_SKILLS:
            caller.msg(f"{self.skill} is not a viable skill of {self.skillset}!")
            raise InterruptCommand

    def func(self):
        caller = self.caller
        if not self.args:
            caller.msg('Usage: learn <skillset> <skill>')
            return

        skillsets.learn_skill(self.caller, self.skillset, self.skill)

class CmdGrantSP(Command):
    key = '@grant-sp'
    '''
    Usage: @grant-sp <person> <number> <skill>
    '''
    def parse(self):
        caller = self.caller
        args = self.args.lstrip()
        try:
            self.person, self.number, self.skill = args.split(" ", 2)
        except ValueError:
            caller.msg("Requires 3 arguments. Usage: @grant-sp <person> <number> <skill>")
            raise InterruptCommand

        self.char = caller.search(self.person)
        if not self.char:
            raise InterruptCommand

        try:
            self.number = int(self.number)
        except ValueError:
            caller.msg("The number must be an integer.")
            raise InterruptCommand

        for i in skillsets.VIABLE_SKILLSETS:
            if not self.skill == i:
                caller.msg(f"{self.skill} is not a viable skillset!")
                raise InterruptCommand
    
    def func(self):
        caller = self.caller
        char = self.char
        num = self.number
        skill = self.skill
        skill = char.attributes.get(skill)
        skill['total_sp'] += num
        caller.msg(f'Granted {char} {num} skillpoints in {self.skill}.')

class CmdTest(Command):
    key = 'testy'

    def func(self):
        caller = self.caller
        attacker = caller
        target = 'rat'
        damage_type = 'bruise'
        damage_tier = 2
        body_part = 'head'
        attacker_desc, target_desc = attack_desc.create_attack_desc(attacker, target, damage_type, damage_tier, body_part)
        caller.msg(attacker_desc)
        caller.msg(target_desc)

class CmdInventory(Command):
    """
    Shows your inventory.

    Usage:
      inventory
      inv
      i
    """
    key = "inventory"
    aliases = ["inv", "i"]
    locks = "cmd:all()"
    arg_regex = r"$"

    def func(self):
        """check inventory"""

        caller = self.caller
        items = caller.contents

        # Remove hands and append all other items to a new list.
        filtered_items = []
        for i in items:
            if not i.is_typeclass('typeclasses.objects.ObjHands'):
                filtered_items.append(i)

        if not filtered_items:
            string = "Your inventory is empty."
        else:
            table = self.styled_table(border="header")
            for item in filtered_items:
                table.add_row(f"|C{item.name}|n {item.db.desc or ''}")
            string = f"|wYou are carrying:\n{table}"
        caller.msg(string)

class CmdInhand(Command):
    key = 'inhand'
    aliases = 'inh'
    
    def func(self):
        caller = self.caller

        left_wield, right_wield, both_wield  = caller.db.wielding.values()

        left_hand, right_hand = get_hands(caller)

        left_cont = left_hand.contents
        right_cont = right_hand.contents

        if left_cont:
            left_item = left_cont[0]
            left_item = left_item.name
        else:
            left_item = 'nothing'

        if right_cont:
            right_item = right_cont[0]
            right_item = right_item.name
        else:
            right_item = 'nothing'

        if left_item and right_item == 'nothing':
            caller.msg(f"Your hands are empty.")
            return
        
        if left_wield and right_wield:
            caller.msg(f"You are wielding {left_item} in your left hand and {right_item} in your right hand.")
        elif right_wield:
            caller.msg(f"You are holding {left_item} in your left hand and wielding {right_item} in your right hand.")
        elif both_wield:
            caller.msg(f"You are wielding {right_item} in both hands.")
        else:
            caller.msg(f"You are holding {left_item} in your left hand and {right_item} in your right hand.")

class CmdGet(Command):
    """
    Pick up something.

    Usage:
      get <obj>
      take <obj>

    Gets an object from your inventory or location and places it in your hands.
    """
    key = "get"
    aliases = ["take",]
    locks = "cmd:all()"
    arg_regex = r"\s|$"

    def func(self):
        """implements the command."""

        caller = self.caller
        if not self.args:
            caller.msg("Get what?")
            return
        args = self.args.strip()

        left_wield, right_wield, both_wield  = caller.db.wielding.values()
        left_hand, right_hand = get_hands(caller)
        left_cont, right_cont = left_hand.contents, right_hand.contents

        if left_cont:
            left_item  = left_cont[0]
        if right_cont:
            right_item = right_cont[0]
        

        obj = caller.search(args, location=[caller.location, caller, left_hand, right_hand])
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
        
        # Check if wielding a single weapon/shield in left hand and stow it.
        if left_wield:
            caller.msg(f"You stop wielding {left_item.name} and stow it away.")
            left_item.move_to(caller, quiet=True)
            caller.db.wielding['left'] = None

        # If both hands have objects, stow the dominate hand.
        if right_cont and left_cont:
            right_item.move_to(caller, quiet=True)
            caller.msg(f"You stow away {right_item.name}.")
            caller.location.msg_contents(f"{caller.name} stows away {right_item.name}.", exclude=caller)

        # Wielding with both hands technically only holds the item in the right hand (for now).
        # So we already know the left hand is free to get items.
        if both_wield:
            caller.msg(f"You stop wielding {both_wield.name}.")
            caller.location.msg_contents(f"{caller.name} stops wielding {both_wield.name}.", exclude=caller)
            caller.db.wielding['both'] = None

        # Decide the location of the item and echo it.
        if obj.location == caller:
            caller.msg(f"You get {obj.name} from your inventory.")
            caller.location.msg_contents(f"{caller.name} gets {obj.name} from their inventory.", exclude=caller)
        elif obj.location == caller.location:
            caller.msg(f"You pick up {obj.name}.")
            caller.location.msg_contents(f"{caller.name} picks up {obj.name}.", exclude=caller)
        elif obj.location in (left_hand, right_hand):
            caller.msg(f"You are already carrying {obj.name}.")
            return

        if right_cont and not left_cont:
            obj.move_to(left_hand, quiet=True)
        else:
            obj.move_to(right_hand, quiet=True)
        
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
    arg_regex = r"\s|$"

    def func(self):
        """Implement command"""

        caller = self.caller
        if not self.args:
            caller.msg("Drop what?")
            return
        args = self.args.strip()

        left_hand, right_hand = get_hands(caller)

        wielding = caller.db.wielding
        left_wield, right_wield, both_wield  = wielding.values()
        
        obj = caller.search(args, location=[left_hand, right_hand, caller, caller.location],
                            nofound_string=f"You can't find {args}.",
                            multimatch_string=f"There are more than one {args}.")
        if not obj:
            return

        # Call the object script's at_before_drop() method.
        if not obj.at_before_drop(caller):
            return

        if obj.location == caller:
            caller.msg(f"You pull {obj.name} from your inventory and drop it on the ground.")
            caller.location.msg_contents(f"{caller.name} pulls {obj.name} from their inventory and drops it on the ground.", exclude=caller)
        elif obj.location in [left_hand, right_hand]:
            # If the dropped object is currently wielded, stop wielding it and drop it.
            if obj in [left_wield, right_wield, both_wield]:
                caller.msg(f"You stop wielding {obj.name} and drop it.")
                caller.location.msg_contents(f"{caller.name} stops wielding {obj.name} and drops it.", exclude=caller)
                wielding['left'], wielding['right'], wielding['both'] = None, None, None
            else:
                caller.msg(f"You drop {obj.name}.")
                caller.location.msg_contents(f"{caller.name} drops {obj.name}.", exclude=caller)
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
      get <obj>
    Picks up an object from your location and puts it in
    your inventory.
    """

    key = 'stow'
    locks = 'cmd:all()'
    arg_regex = r"\s|$"

    def func(self):
        """implements the command."""
        caller = self.caller
        if not self.args:
            caller.msg("Stow what?")
            return
        args = self.args.strip()

        left_hand, right_hand = get_hands(caller)
        wielding = caller.db.wielding
        left_wield, right_wield, both_wield  = wielding.values()
        
        obj = caller.search(args, location=[left_hand, right_hand, caller.location, caller],
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
        
        if obj.location in [left_hand, right_hand]:
            # If the stowed object is currently wielded, stop wielding it and stow it.
            if obj in [left_wield, right_wield, both_wield]:
                caller.msg(f"You stop wielding {obj.name} and stow it away.")
                caller.location.msg_contents(f"{caller.name} stops wielding {obj.name} and stows it away.", exclude=caller)
                wielding['left'], wielding['right'], wielding['both'] = None, None, None
            else:
                caller.msg(f"You stow away {obj.name}.")
                caller.location.msg_contents(f"{caller.name} stows away {obj.name}.", exclude=caller)
        elif obj.location == caller.location:
            caller.msg(f"You pick up {obj.name} and stow it away.")
            caller.location.msg_contents(f"{caller.name} picks up {obj.name} and stows it away.", exclude=caller)
        elif obj.location == caller:
            caller.msg(f"You already have {obj.name} in your inventory.")
            return

        obj.move_to(caller, quiet=True)

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
        left_hand, right_hand = get_hands(caller)
        obj = caller.search(args, location=[caller, left_hand, right_hand],
                            nofound_string="You must be holding a weapon to wield it.",
                            multimatch_string=f"There are more than one {args}.")
        if not obj:
            return
        if obj == caller:
            caller.msg("You can't wield yourself.")
            return
        if not obj.attributes.get('wieldable'):
            caller.msg("That's not a wieldable item.")

        hands_req = obj.attributes.get('wieldable')

        left_cont = left_hand.contents
        right_cont = right_hand.contents

        if left_cont:
            left_item = left_cont[0]
        if right_cont:
            right_item = right_cont[0]


        if obj.location == caller:
            if right_cont:
                caller.msg(f"You stow away {right_item.name}.")
                right_item.move_to(caller, quiet=True)
            caller.msg(f"You get {obj.name} from your inventory.")
            caller.location.msg_contents(f"{caller.name} gets {obj.name} from their inventory.", exclude=caller)
            obj.move_to(right_hand, quiet=True)
            
        if obj.location in [left_hand, right_hand]:
            if hands_req == 1:
                if obj.location == left_hand:
                    caller.msg(f"You swap the contents of your hands and wield {obj.name} in your right hand.")
                    caller.location.msg_contents(f"{caller.name} swaps the content of their hands and wields {obj.name} in their right hand.", exclude=caller)
                    obj.move_to(right_hand, quiet=True)
                    if right_cont:
                        right_item.move_to(left_hand, quiet=True)
                elif obj.location == right_hand:
                    caller.msg(f"You wield {obj.name} in your right hand.")
                    caller.location.msg_contents(f"{caller.name} wields {obj.name} in their right hand.", exclude=caller)
                caller.db.wielding['right'] = obj
            elif hands_req == 2:
                if obj.location == left_hand:
                    if right_cont:
                        caller.msg(f"You stow away {right_item.name}.")
                        caller.location.msg_contents(f"{caller.name} stows away {right_cont}.", exclude=caller)
                        right_item.move_to(caller, quiet=True)
                elif obj.location == right_hand:
                    if left_cont:
                        caller.msg(f"You stow away {left_item.name}.")
                        caller.location.msg_contents(f"{caller.name} stows away {left_cont}.", exclude=caller)
                        left_item.move_to(caller, quiet=True)
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
        obj = None

        for i in wielding.values():
            obj = i

        # left_hand, right_hand = get_hands(caller)
        # obj = caller.search(wielded_obj, location=[left_hand, right_hand])

        if obj:
            caller.msg(f"You stop wielding {obj.name}.")
            caller.location.msg_contents(f"{caller.name} stops wielding {obj.name}.", exclude=caller)
            wielding['left'], wielding['right'], wielding['both'] = None, None, None


class CmdMatch(Command): # NOT FINISHED
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



# Helper Functions
def get_hands(caller):
    left_hand = caller.search('left hand', location=caller)
    right_hand = caller.search('right hand', location=caller)
    return left_hand, right_hand
