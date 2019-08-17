"""
Commands

Commands describe the input the account can do to the game.

"""

from evennia import Command as BaseCommand
from evennia import InterruptCommand
from evennia.utils.evmenu import EvMenu
from world import skillsets, attack_desc
from typeclasses.objects import ObjHands

def get_hands(caller):
    left_hand = caller.search('left hand', location=caller)
    right_hand = caller.search('right hand', location=caller)
    return left_hand, right_hand

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

        left_hand, right_hand = get_hands(caller)

        left_cont = left_hand.contents
        right_cont = right_hand.contents

        left_str = ''
        right_str = ''

        if left_cont:
            for i in left_cont:
                left_str = i.key
        else:
            left_str = 'nothing'
        if right_cont:
            for i in right_cont:
                right_str = i.key
        else:
            right_str = 'nothing'
        if left_str and right_str == 'nothing':
            caller.msg(f"Your hands are empty.")
            return
        
        caller.msg(f"You are holding {left_str} in your left hand and {right_str} in your right hand.")

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

        left_hand, right_hand = get_hands(caller)

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
        
        if obj.location == caller:
            caller.msg(f"You get {obj.name} from your inventory.")
            caller.location.msg_contents(f"{caller.name} gets {obj.name} from their inventory.", exclude=caller)
        elif obj.location == caller.location:
            caller.msg(f"You pick up {obj.name}.")
            caller.location.msg_contents(f"{caller.name} picks up {obj.name}.", exclude=caller)
        elif obj.location in (left_hand, right_hand):
            caller.msg(f"You are already carrying {obj.name}.")
            return

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
        
        if obj.location in (left_hand, right_hand):
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
