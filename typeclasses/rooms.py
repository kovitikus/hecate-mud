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
        exits, users, things, destination = [], [], defaultdict(list), []
        for con in visible:
            key = con.get_display_name(looker)
            if con.destination:
                exits.append(key)
                destination.append(con.destination.name)
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
                    exits_string += f"|c{destination[exit_len - 1]}|n to the |c{exits[exit_len - 1]}|n."
                elif exit_len == num:
                    exits_string += f"and |c{destination[exit_len - 1]}|n to the |c{exits[exit_len - 1]}|n."
                else:
                    exits_string += f"|c{destination[exit_len - 1]}|n to the |c{exits[exit_len - 1]}|n, "
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

    # Calades Rendition
    # def return_appearance(self,looker,**kwarfs):
    #     """
    #     This formats a description. It is the hook a 'look' command
    #     should call
       
    #     args:
    #         looker (object): object doing the looking
    #         **kwargs (dict): Arbitrary, optional arguments for users
    #             overriding the call (unused by default).
    #     """
    #     if not looker:
    #         return ""
    #     # get and identify all objects
    #     visible = (con for con in self.contents if con != looker and
    #                 con.access(looker, "view"))
    #     exits, users, things, destination = [], [], defaultdict(list), []
    #     for con in visible:
    #         key = con.get_display_name(looker, pose=True)
    #         if con.destination:
    #             exits.append(key)
    #             destination.append(con.destination)
    #         elif con.has_account:
    #             users.append("|c%s|n" % key)
    #         else:
    #             # things can be pluralized
    #             things[key].append(con)
    #         # get description, build string
    #     string = "|cYou are located at %s. |n" % self.get_display_name(looker, pose=True)
    #     desc = self.db.desc
    #     if desc:
    #         string += "%s" % desc
    #     if exits:
    #         num = 1
    #         list_len = len(exits)
    #         string += "\n   You see "
    #         for i in exits:
    #             if len(exits) == 1:
    #                 string += f"|w{destination[0]} to the {exits[0]}."
    #             elif num == list_len:
    #                 string += f"|wand {destination[0]} to the {exits[0]}. "
    #             else:
    #                 string += f"|w{destination[num]} to the {exits[num]}, "
    #                 num += 1
    #     if users or things:
    #         # handle pluralization of things (Never pluralize users)
    #         thing_strings = []
    #         for key, itemlist in sorted(things.items()):
    #             nitem = len(itemlist)
    #             if nitem == 1:
    #                 key, _ = itemlist[0].get_numbered_name(nitem, looker, key=key)
    #             else:
    #                 key = [item.get_numbered_name(nitem, looker, key=key)[1] for item in itemlist][0]
    #             thing_strings.append(key)
    #         if len(users) < 1:
    #             string += "\nYou are standing here alone.|n"
    #         else:
    #             string += "\nStanding around here are |n " + list_to_string(users, endsep="and", addquote=False)
    #         if thing_strings:
    #             string += "\nLaying on the ground infront of you is|n " + list_to_string(thing_strings, endsep="and", addquote=False)
 
    #     return string
