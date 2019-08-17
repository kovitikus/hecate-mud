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
        desc = self.caller.desc()
        self.msg(desc)

class CmdCharGen(Command):
    key = "chargen"

    def func(self):
        EvMenu(self.caller, "world.chargen", startnode="main", cmd_on_exit="look", cmdset_mergetype="Replace", cmdset_priority=1,
       auto_quit=True, auto_look=True, auto_help=True)

class CmdLearnSkill(Command):
    key = 'learn'
    """
    Usage: learn <skillset> <skill>
    """

    def parse(self):
        args = self.args.lstrip()
        try:
            self.skillset, self.skill = args.split(" ", 1)
        except ValueError:
            self.caller.msg("Usage: learn <skillset> <skill>")
            raise InterruptCommand

        if self.skillset not in skillsets.VIABLE_SKILLSETS:
            self.caller.msg(f"{self.skillset} is not a viable skillset!")
            raise InterruptCommand
        if self.skill not in skillsets.VIABLE_SKILLS:
            self.caller.msg(f"{self.skill} is not a viable skill of {self.skillset}!")
            raise InterruptCommand

    def func(self):
        if not self.args:
            self.caller.msg('Usage: learn <skillset> <skill>')
            return

        skillsets.learn_skill(self.caller, self.skillset, self.skill)

class CmdGrantSP(Command):
    key = '@grant-sp'
    '''
    Usage: @grant-sp <person> <number> <skill>
    '''

    def parse(self):
        args = self.args.lstrip()
        try:
            self.person, self.number, self.skill = args.split(" ", 2)
        except ValueError:
            self.caller.msg("Requires 3 arguments. Usage: @grant-sp <person> <number> <skill>")
            raise InterruptCommand

        self.char = self.caller.search(self.person)
        if not self.char:
            raise InterruptCommand

        try:
            self.number = int(self.number)
        except ValueError:
            self.caller.msg("The number must be an integer.")
            raise InterruptCommand

        for i in skillsets.VIABLE_SKILLSETS:
            if not self.skill == i:
                self.caller.msg(f"{self.skill} is not a viable skillset!")
                raise InterruptCommand
    
    def func(self):
        char = self.char
        num = self.number
        skill = self.skill
        skill = char.attributes.get(skill)
        skill['total_sp'] += num
        self.caller.msg(f'Granted {char} {num} skillpoints in {self.skill}.')


class CmdTest(Command):
    key = 'testy'
    def func(self):
        attacker = self.caller
        target = 'rat'
        damage_type = 'bruise'
        damage_tier = 2
        body_part = 'head'
        attacker_desc, target_desc = attack_desc.create_attack_desc(attacker, target, damage_type, damage_tier, body_part)
        self.caller.msg(attacker_desc)
        self.caller.msg(target_desc)

class CmdInventory(Command):
    """
    view inventory
    Usage:
      inventory
      inv
    Shows your inventory.
    """
    key = "inventory"
    aliases = ["inv", "i"]
    locks = "cmd:all()"
    arg_regex = r"$"

    def func(self):
        """check inventory"""
        items = self.caller.contents

        # Remove unwanted items.
        filtered_items = []
        for i in items:
            if not i.is_typeclass('typeclasses.objects.ObjHands'):
                filtered_items.append(i)

        if not filtered_items:
            string = "You are not carrying anything."
        else:
            table = self.styled_table(border="header")
            for item in filtered_items:
                table.add_row(f"|C{item.name}|n {item.db.desc or ''}")
            string = f"|wYou are carrying:\n{table}"
        self.caller.msg(string)

class CmdGet(Command):
    """
    pick up something
    Usage:
      get <obj>
    Picks up an object from your location and puts it in
    your inventory.
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
        self.args = self.args.strip()
        obj = caller.search(self.args, location=(caller.location or caller))
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
        
        # Find the character's hands and assign the hand objects to variables.
        right_hand = caller.search('right hand', location=caller)
        left_hand = caller.search('left hand', location=caller)

        obj.move_to(right_hand, quiet=True)
        caller.msg(f"You pick up {obj.name}.")
        caller.location.msg_contents(f"{caller.name} picks up {obj.name}.", exclude=caller)
        # calling at_get hook method
        obj.at_get(caller)

class CmdInhand(Command):
    key = 'inhand'
    aliases = 'inh'
    def func(self):
        items = self.caller.contents
        for item in items:
            if item.key == 'left hand':
                left_hand = item
            elif item.key == 'right hand':
                right_hand = item
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
            self.caller.msg(f"Your hands are empty.")
            return
        
        self.caller.msg(f"You are holding {left_str} in your left hand and {right_str} in your right hand.")

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
        self.args = self.args.strip()

        items = self.caller.contents
        for item in items:
            if item.key == 'left hand':
                left_hand = item
            elif item.key == 'right hand':
                right_hand = item
        
        obj = caller.search(self.args, location=[left_hand, right_hand, caller],
                            nofound_string=' ',
                            multimatch_string=f"You are carrying more than one {self.args}.")
        # if not obj:
        #     # If the object is not in the character's hands, search their inventory instead.
        #     obj = caller.search(self.args, location=caller,
        #                         nofound_string=' ',
        #                         multimatch_string=f"You are carrying more than one {self.args}.")
        if not obj:
            caller.msg(f"You aren't carrying {self.args}.")
            return

        # Call the object script's at_before_drop() method.
        if not obj.at_before_drop(caller):
            return

        if obj.location == caller:
            caller.msg(f"You pull {obj.name} from your inventory and drop it on the ground.")
            caller.location.msg_contents(f"{caller.name} pulls {obj.name} from their inventory and drops it on the ground.", exclude=caller)
        else:
            caller.msg(f"You drop {obj.name}.")
            caller.location.msg_contents(f"{caller.name} drops {obj.name}.", exclude=caller)
        obj.move_to(caller.location, quiet=True)

        # Call the object script's at_drop() method.
        obj.at_drop(caller)
