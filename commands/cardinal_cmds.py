from evennia import Command as BaseCommand

from misc import general_mechanics as gen_mec

class North(BaseCommand):
    """
    Finds an exit object marked with the same cardinal direction and calls its at_traverse hook.
    """

    key = 'n'
    aliases = ['no', 'nor', 'nort', 'north']
    auto_help = False

    def func(self):
        caller = self.caller
        direction = self.key

        success = caller.travel.traverse_cardinal_exit(direction)
        if not success:
            caller.msg("There is no exit to the north.")
            return

class Northeast(BaseCommand):
    """
    Finds an exit object marked with the same cardinal direction and calls its at_traverse hook.
    """

    key = 'ne'
    aliases = ['northe', 'northea', 'northeas', 'northeast']
    auto_help = False

    def func(self):
        caller = self.caller
        direction = self.key

        success = caller.travel.traverse_cardinal_exit(direction)
        if not success:
            caller.msg("There is no exit to the northeast.")
            return

class East(BaseCommand):
    """
    Finds an exit object marked with the same cardinal direction and calls its at_traverse hook.
    """

    key = 'e'
    aliases = ['ea', 'eas', 'east']
    auto_help = False

    def func(self):
        caller = self.caller
        direction = self.key

        success = caller.travel.traverse_cardinal_exit(direction)
        if not success:
            caller.msg("There is no exit to the east.")
            return

class Southeast(BaseCommand):
    """
    Finds an exit object marked with the same cardinal direction and calls its at_traverse hook.
    """

    key = 'se'
    aliases = ['southe', 'southea', 'southeas', 'southeast']
    auto_help = False

    def func(self):
        caller = self.caller
        direction = self.key

        success = caller.travel.traverse_cardinal_exit(direction)
        if not success:
            caller.msg("There is no exit to the southeast.")
            return

class South(BaseCommand):
    """
    Finds an exit object marked with the same cardinal direction and calls its at_traverse hook.
    """

    key = 's'
    aliases = ['so', 'sou', 'sout', 'south']
    auto_help = False

    def func(self):
        caller = self.caller
        direction = self.key

        success = caller.travel.traverse_cardinal_exit(direction)
        if not success:
            caller.msg("There is no exit to the south.")
            return


class Southwest(BaseCommand):
    """
    Finds an exit object marked with the same cardinal direction and calls its at_traverse hook.
    """

    key = 'sw'
    aliases = ['southw', 'southwe', 'southwes', 'southwest']
    auto_help = False

    def func(self):
        caller = self.caller
        direction = self.key

        success = caller.travel.traverse_cardinal_exit(direction)
        if not success:
            caller.msg("There is no exit to the southwest.")
            return

class West(BaseCommand):
    """
    Finds an exit object marked with the same cardinal direction and calls its at_traverse hook.
    """

    key = 'w'
    aliases = ['we', 'wes', 'west']
    auto_help = False

    def func(self):
        caller = self.caller
        direction = self.key

        success = caller.travel.traverse_cardinal_exit(direction)
        if not success:
            caller.msg("There is no exit to the west.")
            return

class Northwest(BaseCommand):
    """
    Finds an exit object marked with the same cardinal direction and calls its at_traverse hook.
    """

    key = 'nw'
    aliases = ['northw','northwe', 'northwes', 'northwest']
    auto_help = False

    def func(self):
        caller = self.caller
        direction = self.key

        success = caller.travel.traverse_cardinal_exit(direction)
        if not success:
            caller.msg("There is no exit to the northwest.")
            return
