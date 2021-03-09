from evennia import Command as BaseCommand

from misc import general_mechanics as gen_mec

class CmdNorth(BaseCommand):
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

class CmdNortheast(BaseCommand):
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

class CmdEast(BaseCommand):
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

class CmdSoutheast(BaseCommand):
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

class CmdSouth(BaseCommand):
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


class CmdSouthwest(BaseCommand):
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

class CmdWest(BaseCommand):
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

class CmdNorthwest(BaseCommand):
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

# Travel Options
class CmdAbandonFailedTraveller(BaseCommand):
    """
    Turns on or off the ability to abandon any object following you, 
        if that object does not have permission to enter the destination.

    Usage:
        abandonfailedtraveller 1|0|yes|no|y|n|true|false|t|f

    Example:
        abft1
        abftn
        abandonfailedtraveller false
        abft 1
        abft no

    Alias:
        abft 
    """

    key = 'abandonfailedtraveller'
    aliases = 'abft'
    abft_on = ['1', 'yes', 'y', 'true', 't']
    abft_off = ['0', 'no', 'n', 'false', 'f']

    def func(self):
        if self.args in self.abft_on:
            self.caller.account.db.abandon_failed_traveller = True
        elif self.args in self.abft_off:
            self.caller.account.db.abandon_failed_traveller = False
        else:
            self.caller.msg(f"Your request to update {self.key} requires a valid option. Use \"help abft\" for more info.")
