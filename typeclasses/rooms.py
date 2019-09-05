"""
Room

Rooms are simple containers that has no location of their own.

"""
from collections import defaultdict

from evennia import DefaultRoom
from evennia.utils.utils import list_to_string


class Room(DefaultRoom):
    """
    Rooms are like any Object, except their location is None
    (which is default). They also use basetype_setup() to
    add locks so they cannot be puppeted or picked up.
    (to change that, use at_object_creation instead)

    See examples/object.py for a list of
    properties and methods available on all Objects.
    """
    def at_object_creation(self):
        if not self.attributes.has('short_desc'):
            self.attributes.add('short_desc', '|rShort Description Not Set!|n')

    def short_desc(self, looker, **kwargs):
        """
        You arrive at <destination name>. You see <exit name> to the <exit direction>, and
        <exit name> to the <exit direction>.
        """
        exits, destinations = [], []
        for con in self.contents:
            if con != self and con.access(self, "view") and con.destination:
                    exits.append(con.get_display_name(looker))
                    destinations.append(con.destination.get_display_name(looker))

        short_desc = f"You arrive at {self.get_display_name(looker)}."
        
        if exits:
            num = 1
            exit_len = len(exits)
            short_desc = f"{short_desc} You see "
            for _ in exits:
                if exit_len == 1:
                    short_desc += f"|c{destinations[exit_len - 1]}|n to the |c{exits[exit_len - 1]}|n."
                elif exit_len == num:
                    short_desc += f"and |c{destinations[exit_len - 1]}|n to the |c{exits[exit_len - 1]}|n."
                else:
                    short_desc += f"|c{destinations[exit_len - 1]}|n to the |c{exits[exit_len - 1]}|n, "
                num += 1
        return short_desc


    def return_appearance(self, looker, **kwargs):
        """
        This formats a description. It is the hook a 'look' command
        should call.
        Args:
            looker (Object): Object doing the looking.
            **kwargs (dict): Arbitrary, optional arguments for users
                overriding the call (unused by default).
        """
        if not looker:
            return ""
        # get and identify all objects
        visible = (con for con in self.contents if con != looker and
                   con.access(looker, "view"))
        exits, users, things, destinations = [], [], defaultdict(list), []
        for con in visible:
            key = con.get_display_name(looker)
            if con.destination:
                exits.append(key)
                destinations.append(con.destination.name)
            elif con.has_account:
                users.append(f"|c{key}|n")
            else:
                # things can be pluralized
                things[key].append(con)
        # get description, build string
        location_name = f"    You see {self.get_display_name(looker)}."
        # if self.db.desc:
        #     location_desc = self.db.desc
        if exits:
            num = 1
            exit_len = len(exits)
            exits_string = "    You see "
            for _ in exits:
                if exit_len == 1:
                    exits_string += f"|c{destinations[exit_len - 1]}|n to the |c{exits[exit_len - 1]}|n."
                elif exit_len == num:
                    exits_string += f"and |c{destinations[exit_len - 1]}|n to the |c{exits[exit_len - 1]}|n."
                else:
                    exits_string += f"|c{destinations[exit_len - 1]}|n to the |c{exits[exit_len - 1]}|n, "
                num += 1
        if users or things:
            # handle pluralization of things (never pluralize users)
            thing_strings = []
            for key, itemlist in sorted(things.items()):
                nitem = len(itemlist)
                if nitem == 1:
                    key, _ = itemlist[0].get_numbered_name(nitem, looker, key=key)
                else:
                    key = [item.get_numbered_name(nitem, looker, key=key)[1] for item in itemlist][0]
                thing_strings.append(key)

        string = f"{location_name}"
        if self.db.desc:
            string = f"{string} {self.db.desc}"
        if exits:
            string = f"{string}\n{exits_string}"
        if things:
            string = f"{string}\n    {list_to_string(thing_strings)} |nlies upon the ground."
        if users:
            string = f"{string}\n    {list_to_string(users)} is here."

        return string
