from collections import defaultdict

from evennia import DefaultRoom
from evennia import search_object
from evennia.utils import inherits_from
from evennia.utils.create import create_object
from evennia.utils.utils import list_to_string, lazy_property

from mobs.mob_spawner import MobSpawner


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
        self.attributes.add('crowd', False)


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
        exits, exit_name, characters, destinations, things = [], [], [], [], defaultdict(list)
        for con in visible:
            key = con.get_display_name(looker)
            if con.destination:
                exits.append(con)
                exit_name.append(key)
                destinations.append(con.destination.name)
            elif inherits_from(con, "characters.characters.Character"):
                characters.append(f"|c{key}|n")
            else:
                # things can be pluralized
                things[key].append(con)
        # get description, build string
        location_name = f"    You see |530{self.get_display_name(looker)}|n."
        # if self.db.desc:
        #     location_desc = self.db.desc
        if exits:
            num = 1
            exits_len = len(exits)
            exits_string = "    You see "
            for x in exits:
                x_alias = x.aliases.all()
                if x.tags.get('door', category='exits'):
                    if exits_len == 1:
                        exits_string += (f"|530{exit_name[num - 1]}|n to the "
                                        f"|340{looker.travel.card_dir_name(x.db.card_dir)}|n.")
                    elif exits_len == num:
                        exits_string += f"and |530{exit_name[num - 1]}|n to the |340{looker.travel.card_dir_name(x.db.card_dir)}|n."
                    else:
                        exits_string += f"|530{exit_name[num - 1]}|n to the |340{looker.travel.card_dir_name(x.db.card_dir)}|n, "
                elif x.tags.get('stair', category='exits') or x.tags.get('ladder', category='exits'):
                    if exits_len == 1:
                        exits_string += f"|530{exit_name[num - 1]}|n leading |340{'upwards' if 'u' in x_alias else 'downwards'}|n."
                    elif exits_len == num:
                        exits_string += f"and |530{exit_name[num - 1]}|n leading |340{'upwards' if 'u' in x_alias else 'downwards'}|n."
                    else:
                        exits_string += f"|530{exit_name[num - 1]}|n leading |340{'upwards' if 'u' in x_alias else 'downwards'}|n, "
                else:
                    if exits_len == 1:
                        exits_string += f"|530{destinations[num - 1]}|n to the |340{looker.travel.card_dir_name(x.db.card_dir)}|n."
                    elif exits_len == num:
                        exits_string += f"and |530{destinations[num - 1]}|n to the |340{looker.travel.card_dir_name(x.db.card_dir)}|n."
                    else:
                        exits_string += f"|530{destinations[num - 1]}|n to the |340{looker.travel.card_dir_name(x.db.card_dir)}|n, "
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
            string = f"{string}\n    {list_to_string(thing_strings)} |nlie upon the ground."
        if characters:
            string = f"{string}\n    {list_to_string(characters)} {'is' if len(characters) == 1 else 'are'} here."
        if self.db.crowd and not characters:
            string = f"{string}\n    {self.db.crowd_short_desc}"
        if self.db.crowd and characters:
            string = f"{string} {self.db.crowd_short_desc}"

        return string

    def crowd(self, looker):
        people = ['dock laborers', 'a few beggars', 'boatmen', 'cats', 'ragged dogs', 'children', 'citizens', 'drovers', 'peddlers', 'priests', 'prostitutes', 'refugees', 'sailors', 'servants', 'traders', 'urchins', 'workers', 'fishermen', 'large brown rats', 'constables']
        if self.db.crowd:
            looker.msg(f"You find yourself at the periphery of a terribly thick crowd. You note a moderate number of {list_to_string(people)}.")

class SewerRoom(Room):
    @lazy_property
    def spawn(self):
        return MobSpawner(self)
    def at_object_receive(self, new_arrival, source_location):
        if new_arrival.has_account and not new_arrival.is_superuser:
            self.spawn.spawn_timer()
    def at_object_leave(self, moved_obj, target_location):
        empty_room = False
        if moved_obj.has_account and not moved_obj.is_superuser:
            for obj in self.contents_get():
                if obj.has_account and not obj.is_superuser:
                    return
                else:
                    empty_room = True
            if empty_room:
                self.spawn.destroy_mob()
