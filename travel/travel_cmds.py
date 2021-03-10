from evennia import Command as BaseCommand, InterruptCommand

from misc import general_mechanics as gen_mec

class CmdFollow(BaseCommand):
    """
    Follows a specified target, automatically attempting to travel with them when they traverse an exit.

    Using 'follow' by itself when already following a leader will force your character to stop following.

    Usage:
        follow <target>

    Example:
        > follow alephate
        > follow ale

        > fol
        You stop following Alephate.

    Aliases:
        follo, foll, fol
    """
    key = 'follow'
    aliases = ['follo', 'foll', 'fol']

    def func(self):
        caller = self.caller
        leader = caller.db.leader

        # Check for unfollow.
        if not self.args:
            if leader == None:
                caller.msg("You must specify a target to follow.")
                return
            else:
                caller.msg(f"You stop following {leader.get_display_name(caller)}.")
                leader.msg(f"{caller.get_display_name(leader)} stops following you.")
                caller.location.msg_contents(f"{caller.name} stops following {leader.name}.")
                caller.db.leader = None
                return

        # Find and follow a target.
        args = self.args.strip()
        target = caller.search(args)[0]
        if not target:
            caller.msg(f"Could not find {args}.")
            return
        else:
            caller.db.leader = target
            caller.msg(f"You follow {target.get_display_name(caller)}.")
            target.db.followers.append(target)
            target.msg(f"{caller.get_display_name(target)} follows you.")
            caller.location.msg_contents(f"{caller.name} follows {target.name}.", exclude=[caller, target])

class CmdAbandon(BaseCommand):
    """
    Abandons a specified target, if that target is following you.

    Usage:
        abandon Karen

    Aliases:
        aban, aband, abando
    """
    key = 'abandon'
    aliases = ['aban', 'aband,', 'abando']
    
    def func(self):
        caller = self.caller
        if not self.args:
            caller.msg("You must specify a target to abandon.")
        args = self.args

        target = caller.search(args)[0]
        if not target:
            caller.msg(f"{args} not found. Specify a valid target to abandon.")
        else:
            caller.db.followers.remove(target)

class CmdDisband(BaseCommand):
    """
    Abandons all followers.

    Usage:
        disband

    Aliases:
        dis, disb, disba, disban
    """
    key = 'disband'
    aliases = ['dis', 'disb', 'disba', 'disban']

    def func(self):
        self.caller.db.followers = []

# Exit Commands
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
        abandonfailedtraveler t

    Alias:
        abft, abandonfailedtraveler
    """

    key = 'abandonfailedtraveller'
    aliases = ['abft', 'abandonfailedtraveler']
    

    def func(self):
        abft_on = ['1', 'yes', 'y', 'true', 't']
        abft_off = ['0', 'no', 'n', 'false', 'f']

        if self.args in abft_on:
            self.caller.account.db.abandon_failed_traveller = True
        elif self.args in abft_off:
            self.caller.account.db.abandon_failed_traveller = False
        else:
            self.caller.msg(f"Your request to update {self.key} requires a valid option. Use \"help abft\" for more info.")
