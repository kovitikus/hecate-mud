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
        north_exit = None

        for x in caller.location.contents:
            if x.location is caller.location and x.db.card_dir == 'n':
                north_exit = x
        if north_exit is not None:
            if north_exit.access(caller, "traverse"):
                north_exit.at_traverse(caller, north_exit.destination)
            else:
                # Exit is locked.
                if north_exit.db.err_traverse:
                    # if exit has a better error message, let's use it.
                    caller.msg(north_exit.db.err_traverse)
                else:
                    # No shorthand error message. Call hook.
                    north_exit.at_failed_traverse(caller)
        else:
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
        ne_exit = None

        for x in caller.location.contents:
            if x.location is caller.location and x.db.card_dir == 'ne':
                ne_exit = x
        if ne_exit is not None:
            if ne_exit.access(caller, "traverse"):
                ne_exit.at_traverse(caller, ne_exit.destination)
            else:
                # Exit is locked.
                if ne_exit.db.err_traverse:
                    # if exit has a better error message, let's use it.
                    caller.msg(ne_exit.db.err_traverse)
                else:
                    # No shorthand error message. Call hook.
                    ne_exit.at_failed_traverse(caller)
        else:
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
        east_exit = None

        for x in caller.location.contents:
            if x.location is caller.location and x.db.card_dir == 'e':
                east_exit = x
        if east_exit is not None:
            if east_exit.access(caller, "traverse"):
                east_exit.at_traverse(caller, east_exit.destination)
            else:
                # Exit is locked.
                if east_exit.db.err_traverse:
                    # if exit has a better error message, let's use it.
                    caller.msg(east_exit.db.err_traverse)
                else:
                    # No shorthand error message. Call hook.
                    east_exit.at_failed_traverse(caller)
        else:
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
        se_exit = None

        for x in caller.location.contents:
            if x.location is caller.location and x.db.card_dir == 'se':
                se_exit = x
        if se_exit is not None:
            if se_exit.access(caller, "traverse"):
                se_exit.at_traverse(caller, se_exit.destination)
            else:
                # Exit is locked.
                if se_exit.db.err_traverse:
                    # if exit has a better error message, let's use it.
                    caller.msg(se_exit.db.err_traverse)
                else:
                    # No shorthand error message. Call hook.
                    se_exit.at_failed_traverse(caller)
        else:
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
        south_exit = None

        for x in caller.location.contents:
            if x.location is caller.location and x.db.card_dir == 's':
                south_exit = x
        if south_exit is not None:
            if south_exit.access(caller, "traverse"):
                south_exit.at_traverse(caller, south_exit.destination)
            else:
                # Exit is locked.
                if south_exit.db.err_traverse:
                    # if exit has a better error message, let's use it.
                    caller.msg(south_exit.db.err_traverse)
                else:
                    # No shorthand error message. Call hook.
                    south_exit.at_failed_traverse(caller)
        else:
            caller.msg("There is no exit to the south.")
            return


class Southwest(BaseCommand):
    # TODO: It seems obvious from how expansive this command has come that I do need a handler for this behavior.
    """
    Finds an exit object marked with the same cardinal direction and calls its at_traverse hook.
    """

    key = 'sw'
    aliases = ['southw', 'southwe', 'southwes', 'southwest']
    auto_help = False

    def func(self):
        caller = self.caller
        sw_exit = None

        for x in caller.location.contents:
            if x.db.card_dir == 'sw':
                sw_exit = x
        if sw_exit is not None:
            # Check all objects for access and then executes their traversal.
            travellers = [caller, *list(caller.db.followers)]
            all_travellers_cleared = True
            cleared_travellers = []

            # TODO: This abandon option requires a menu for the player to manage their account options. 
            # It is currently set to false by default in the Account typeclass at_object_creation.
            abandon_failed_traveller = caller.account.db.abandon_failed_traveller

            for obj in travellers:
                if sw_exit.access(obj, "traverse"):
                    cleared_travellers.append(obj)
                else:
                    if abandon_failed_traveller == False:
                        all_travellers_cleared == False
                        caller.msg(f"You failed to traverse the exit. {obj.get_display_name(caller)} does not have permission to enter {sw_exit.get_display_name(caller)}.")
                        obj.msg(f"Your leader, {caller.get_display_name(obj)},has failed to traverse an exit. You do not have permission to enter {sw_exit.get_display_name(obj)}.")
                        break # Abandon the for loop and return from the command immediately.
                    else:
                        # Object does not have access to traverse the exit and will be abandoned.
                        caller.msg(f"Your follower, {obj.get_display_name(caller)}, "
                                    "does not have permission to enter {sw_exit.get_display_name(caller)} and will be abandoned.")
                        obj.msg(f"You do not have permission to enter {sw_exit.get_display_name(obj)} "
                                    "and have been abandoned by your leader, {caller.get_display_name(obj)}.")

                        # Clear this object from the leader's follower list.
                        caller.db.followers.remove(obj)
                        # Clear this object's leader attribute.
                        obj.db.leader = None

                        # Generic error message stuff I copied from ExitCommand that I'm not sure I still need.
                        if sw_exit.db.err_traverse:
                            # if exit has a better error message, let's use it.
                            obj.msg(sw_exit.db.err_traverse)
                        else:
                            # No shorthand error message. Call hook.
                            sw_exit.at_failed_traverse(obj)
            if all_travellers_cleared:
                # Execute the traversal of all traveller objects.
                for obj in travellers:
                    if caller == obj:
                        follower_list = travellers
                        follower_list.remove(caller)
                        follower_list = gen_mec.comma_separated_string_list(gen_mec.objects_to_strings(follower_list))
                        caller.msg(f"You are followed by {follower_list} as you travel to {sw_exit.get_display_name(caller)}.")
                    else:
                        obj.msg(f"You follow {caller.get_display_name(obj)} as they travel to {sw_exit.get_display_name(obj)}.")
                        sw_exit.at_traverse(obj, sw_exit.destination)
            else:
                return

        else:
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
        west_exit = None

        for x in caller.location.contents:
            if x.location is caller.location and x.db.card_dir == 'w':
                west_exit = x
        if west_exit is not None:
            if west_exit.access(caller, "traverse"):
                west_exit.at_traverse(caller, west_exit.destination)
            else:
                # Exit is locked.
                if west_exit.db.err_traverse:
                    # if exit has a better error message, let's use it.
                    caller.msg(west_exit.db.err_traverse)
                else:
                    # No shorthand error message. Call hook.
                    west_exit.at_failed_traverse(caller)
        else:
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
        nw_exit = None

        for x in caller.location.contents:
            if x.location is caller.location and x.db.card_dir == 'nw':
                nw_exit = x
        if nw_exit is not None:
            if nw_exit.access(caller, "traverse"):
                nw_exit.at_traverse(caller, nw_exit.destination)
            else:
                # Exit is locked.
                if nw_exit.db.err_traverse:
                    # if exit has a better error message, let's use it.
                    caller.msg(nw_exit.db.err_traverse)
                else:
                    # No shorthand error message. Call hook.
                    nw_exit.at_failed_traverse(caller)
        else:
            caller.msg("There is no exit to the northwest.")
            return
