"""
Commands

Commands describe the input the account can do to the game.

"""

from evennia import Command as BaseCommand
from evennia import InterruptCommand
from evennia.utils.evmenu import EvMenu
from world import skillsets


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

class CmdDesc(BaseCommand):
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

    def parse(self):
        args = self.args.lstrip()
        try:
            self.skillset, self.skill = args.split(" ", 1)
        except ValueError:
            self.caller.msg("Invalid usage. Enter two words separated by a space.")
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


