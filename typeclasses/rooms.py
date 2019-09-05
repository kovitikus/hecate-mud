"""
Room

Rooms are simple containers that has no location of their own.

"""
from collections import defaultdict

from evennia import DefaultRoom
from evennia.utils import inherits_from
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
        You arrive at <destination name>. <Person/NPC> <is/are> here. You see <exit name> to the 
        <exit direction>, and <exit name> to the <exit direction>.
        """
        if not looker:
            return
        # Get and identify all visible objects.
        visible = (con for con in self.contents if con != looker and
                   con.access(looker, "view"))
        exits, destinations, characters = [], [], []
        for con in visible:
            key = con.get_display_name(looker)
            if con.destination:
                exits.append(key)
                destinations.append(con.destination.get_display_name(looker))
            elif inherits_from(con, "typeclasses.characters.Character"):
                characters.append(f"|c{key}|n")

        short_desc = f"You arrive at {self.get_display_name(looker)}."
        if characters:
            short_desc = f"{short_desc} {list_to_string(characters)} {'is' if len(characters) == 1 else 'are'} here."
        
        if exits:
            print(f"Exits: {exits}")
            num = 1
            exits_len = len(exits)
            exits_string = f"You see "
            for _ in exits:
                if exits_len == 1:
                    exits_string += f"|c{destinations[num - 1]}|n to the |c{exits[num - 1]}|n."
                elif exits_len == num:
                    exits_string += f"and |c{destinations[num - 1]}|n to the |c{exits[num - 1]}|n."
                else:
                    exits_string += f"|c{destinations[num - 1]}|n to the |c{exits[num - 1]}|n, "
                num += 1
            short_desc = f"{short_desc} {exits_string}"
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
        exits, characters, destinations, things = [], [], [], defaultdict(list)
        for con in visible:
            key = con.get_display_name(looker)
            if con.destination:
                exits.append(key)
                destinations.append(con.destination.name)
            elif inherits_from(con, "typeclasses.characters.Character"):
                characters.append(f"|c{key}|n")
            else:
                # things can be pluralized
                things[key].append(con)
        # get description, build string
        location_name = f"    You see {self.get_display_name(looker)}."
        # if self.db.desc:
        #     location_desc = self.db.desc
        if exits:
            num = 1
            exits_len = len(exits)
            exits_string = "    You see "
            for _ in exits:
                if exits_len == 1:
                    exits_string += f"|c{destinations[num - 1]}|n to the |c{exits[num - 1]}|n."
                elif exits_len == num:
                    exits_string += f"and |c{destinations[num - 1]}|n to the |c{exits[num - 1]}|n."
                else:
                    exits_string += f"|c{destinations[num - 1]}|n to the |c{exits[num - 1]}|n, "
                num += 1
        if characters or things:
            # handle pluralization of things (never pluralize characters)
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
        if characters:
            string = f"{string}\n    {list_to_string(characters)} {'is' if len(characters) == 1 else 'are'} here."

        return string
