from evennia.utils.utils import inherits_from

from misc import general_mechanics as gen_mec

# Handles the traversal of objects to/from other objects.
class TravelHandler:
    def __init__(self, owner):
        self.owner = owner

#---------------------
# General Methods
    def open_environment_exit(self, exit):
        """
        This method is critical in determing the appearance of an exit within the room.
        Outdoor areas have exits that are technically just a continuation into the next room.
        Exits that are occupied by obstacles, such as a door, will not appear as the destination 
        room's name.
        """
        if exit.tags.get('door', category='exits') or \
            exit.tags.get('stair', category='exits') or \
            exit.tags.get('ladder', category='exits'):
            return False
        else:
            return True

    def find_exit_by_card_dir(self):
        for x in self.owner.location.contents:
            if x.tags.get(category='card_dir') == self.direction:
                self.exit_obj = x
                break
            else:
                self.exit_obj = None

    def find_exit_by_destination(self, destination):
        for x in self.owner.location.contents:
            if x.destination == destination:
                self.exit_obj = x
                break
            else:
                self.exit_obj = None

    def card_dir_name(self, card_dir):
        if card_dir == 'n':
            card_dir = 'north'
        elif card_dir == 'ne':
            card_dir = 'northeast'
        elif card_dir == 'e':
            card_dir = 'east'
        elif card_dir == 'se':
            card_dir = 'southeast'
        elif card_dir == 's':
            card_dir = 'south'
        elif card_dir == 'sw':
            card_dir = 'southwest'
        elif card_dir == 'w':
            card_dir = 'west'
        elif card_dir == 'nw':
            card_dir = 'northwest'
        elif card_dir == 'up':
            card_dir = 'upwards'
        elif card_dir == 'down':
            card_dir == 'downwards'
        return card_dir

    # Generate a string from a list of exits.
    def exits_to_string(self, exits):
        owner = self.owner
        exit_str = ''
        exit_str_list = []

        if len(exits) > 0:
            if len(exits) == 1:
                single_exit = True
            else:
                single_exit = False
        else:
            # No exits were found.
            self.no_exit_str = "There are no obvious exits."
            exit_str = False
            return exit_str

        def _exit_str_gen(exit):
            exit_card_dir = exit.tags.get(category='card_dir')
            if exit_card_dir is not None: # Exit has a cardinal direction.
                if self.open_environment_exit(exit):
                    return (f"|310{exit.destination.get_display_name(owner)}|n to the "
                            f"|340{self.card_dir_name(exit_card_dir)}|n")
                else:
                    return (f"|310{exit.get_display_name(owner)}|n to the "
                            f"|340{self.card_dir_name(exit_card_dir)}|n")
            else: # Exit has no cardinal direction.
                if self.open_environment_exit(exit):
                    return f"|310{exit.destination.get_display_name(owner)}|n"
                else:
                    return f"|310{exit.get_display_name(owner)}|n"

        if single_exit:
            exit_str = _exit_str_gen(exits[0])
        else: # 2 or more exits.
            for i in exits:
                exit_str = _exit_str_gen(i)
                exit_str_list.append(exit_str)
            exit_str = gen_mec.comma_separated_string_list(exit_str_list)
        return exit_str

#-------------------
# Cardinal Exit Traversal
    def traverse_cardinal_exit(self, direction):
        owner = self.owner
        self.direction = direction
        self.exit_obj = None

        # Determine if there are party members to add to the traveller list.
        x = None
        if owner.attributes.has('followers'): 
            if len(owner.db.followers) > 0:
                x = list(owner.db.followers)
        if x is not None:
            self.travellers = [owner, *x]
        else:
            self.travellers = [owner, ]
        

        # This option allows the player to abandon a party member if they fail to traverse with the rest of the party.
        # Its value is set by the player via the 'abandonfailedtraveller' or 'abft' command in the travel_cmds.py module.
        self.abandon_failed_traveller = owner.account.db.abandon_failed_traveller

        self.find_exit_by_card_dir()

        if self.exit_obj:
            self.check_traveller_access()
        else:
            return False

        if self.all_travellers_cleared:
            self.traverse_exit()
            return True
        else:
            return False

#---------------------
# Logic for grouped object movement.
    def check_traveller_access(self):
        self.all_travellers_cleared = True
        self.cleared_travellers = []
        owner = self.owner
        exit_obj = self.exit_obj
        
        for obj in self.travellers:
            if exit_obj.access(obj, "traverse"):
                self.cleared_travellers.append(obj)
            else:
                if self.abandon_failed_traveller == False:
                    self.halt_travel(obj)
                    break # Abandon the for loop and return from the method immediately.
                else:
                    self.abandon_traveller(obj)
                    
    def halt_travel(self, obj):
        owner = self.owner

        self.all_travellers_cleared == False
        owner.msg(f"You failed to traverse the exit. {obj.get_display_name(owner)} "
                    "does not have permission to enter {exit_obj.get_display_name(owner)}.")
        obj.msg(f"Your leader, {owner.get_display_name(obj)},has failed to traverse an exit. "
                    "You do not have permission to enter {exit_obj.get_display_name(obj)}.")

    def abandon_traveller(self, obj):
        owner = self.owner
        exit_obj = self.exit_obj

        # Object does not have access to traverse the exit and will be abandoned.
        owner.msg(f"Your follower, {obj.get_display_name(owner)}, "
                    "does not have permission to enter {exit_obj.get_display_name(owner)} and will be abandoned.")
        obj.msg(f"You do not have permission to enter {exit_obj.get_display_name(obj)} "
                    "and have been abandoned by your leader, {owner.get_display_name(obj)}.")

        # Clear this object from the leader's follower list.
        owner.db.followers.remove(obj)
        # Clear this object's leader attribute.
        obj.db.leader = None

        # Generic error message stuff I copied from ExitCommand that I'm not sure I still need.
        if exit_obj.db.err_traverse:
            # if exit has a better error message, let's use it.
            obj.msg(exit_obj.db.err_traverse)
        else:
            # No shorthand error message. Call hook.
            exit_obj.at_failed_traverse(obj)

    def traverse_exit(self):
        owner = self.owner
        travellers = self.travellers
        exit_obj = self.exit_obj

        # Execute the traversal of all traveller objects.
        for obj in travellers:
            if owner == obj: # String we send to the character who initiated the travel.
                temp_list = travellers
                temp_list.remove(owner)
                if len(temp_list) > 0: # Avoid sending an empty list.
                    temp_list = gen_mec.comma_separated_string_list(gen_mec.objects_to_strings(temp_list))
                    owner.msg(f"You are followed by {temp_list} as you travel to {exit_obj.get_display_name(owner)}.")
            else:
                obj.msg(f"You follow {owner.get_display_name(obj)} as they travel to {exit_obj.get_display_name(obj)}.")
            exit_obj.at_traverse(obj, exit_obj.destination)

#---------------------------------------------------------------------
# announce_move_from hook on Character typeclass
    # doc str
    def travel_one_way(self, destination):
        if self.exit_obj is None:
            self.owner.location.msg_contents(f"{self.owner.name} teleports to {destination}", exclude=self.owner)
            return True
        elif not hasattr(self.exit_obj, 'destination'):
            self.owner.location.msg_contents(f"{self.owner.name} departs via {self.exit_obj}.", exclude=self.owner)
            return True
    # doc str
    def pick_departure_string(self):
        exit_obj = self.exit_obj

        # Generate a string from the exits list based on the exit type and if a direction exists.
        owner = self.owner

        # Check for special exit typeclasses.
        if exit_obj.tags.get(category='card_dir') is not None:
            if exit_obj.tags.get('door', category='exits'):
                self.depart_door_str()
            elif exit_obj.tags.get('stair', category='exits'):
                self.depart_stair_str()
            elif exit_obj.tags.get('ladder', category='exits'):
                self.depart_ladder_str()
            else:
                self.depart_default_str()
        else:
            # Exit object has no direction and therefore doesn't require typeclass consideration.
            self.self_str = f"You depart by way of |310{exit_obj.get_display_name(owner)}|n"
            self.others_str = f"{owner.name} departs by way of |310{exit_obj.name}|n"

    # Door Strings
    def depart_door_str(self):
        owner = self.owner
        exit_obj = self.exit_obj
        exit_card_dir = exit_obj.tags.get(category='card_dir')

        if exit_card_dir is not None:
            if exit_card_dir in ['up', 'down']:
                self.self_str = (f"You climb |340{self.card_dir_name(exit_card_dir)}|n "
                                    f"through |310{exit_obj.get_display_name(owner)}|n.")
                self.others_str = (f"{owner.name} climbs |340{self.card_dir_name(exit_card_dir)}|n " # upwards, downwards
                                    f"through |310{exit_obj.name}|n.")
            else:
                self.self_str = (f"You depart |340{self.card_dir_name(exit_card_dir)}|n "
                                    f"through |310{exit_obj.get_display_name(owner)}|n.")
                self.others_str = (f"{owner.name} departs |340{self.card_dir_name(exit_card_dir)}|n "
                                    f"through |310{exit_obj.name}|n.")
    # Stair Strings
    def depart_stair_str(self):
        owner = self.owner
        exit_obj = self.exit_obj
        exit_card_dir = exit_obj.tags.get(category='card_dir')

        if exit_card_dir is not None:
            if exit_card_dir in ['up', 'down']:
                self.self_str = (f"You climb |310{exit_obj.get_display_name(owner)}|n "
                            f"|340{self.card_dir_name(exit_card_dir)}|n.")
                self.others_str = (f"{owner.name} climbs |310{exit_obj.name}|n "
                            f"|340{self.card_dir_name(exit_card_dir)}|n.")
            else:
                self.self_str = (f"You climb |310{exit_obj.get_display_name(owner)}|n "
                            f"to the |340{self.card_dir_name(exit_card_dir)}|n.")
                self.others_str = (f"{owner.name} climbs |310{exit_obj.name}|n "
                            f"to the |340{self.card_dir_name(exit_card_dir)}|n.")
    # Ladder Strings
    def depart_ladder_str(self):
        owner = self.owner
        exit_obj = self.exit_obj
        exit_card_dir = exit_obj.tags.get(category='card_dir')

        if exit_card_dir is not None:
            if exit_card_dir in ['up', 'down']:
                self.self_str = (f"You climb |310{exit_obj.get_display_name(owner)}|n "
                            f"|340{self.card_dir_name(exit_card_dir)}|n.")
                self.others_str = (f"{owner.name} climbs |310{exit_obj.name}|n "
                            f"|340{self.card_dir_name(exit_card_dir)}|n.")
            else:
                self.self_str = (f"You climb |310{exit_obj.get_display_name(owner)}|n "
                            f"to the |340{self.card_dir_name(exit_card_dir)}|n.")
                self.others_str = (f"{owner.name} climbs |310{exit_obj.name}|n "
                            f"to the |340{self.card_dir_name(exit_card_dir)}|n.")
                    
    def depart_default_str(self):
        owner = self.owner
        exit_obj = self.exit_obj
        exit_card_dir = exit_obj.tags.get(category='card_dir')

        if exit_card_dir is not None:
            if exit_card_dir in ['up', 'down']:
                self.self_str = (f"You depart |340{self.card_dir_name(exit_card_dir)}|n "
                            f"towards |310{exit_obj.get_display_name(owner)}|n.")
                self.others_str = (f"{owner.name} departs |340{self.card_dir_name(exit_card_dir)}|n "
                            f"towards |310{exit_obj.name}|n.")
            else:
                self.self_str = (f"You depart |340{self.card_dir_name(exit_card_dir)}|n "
                            f"towards |310{exit_obj.get_display_name(owner)}|n.")
                self.others_str = (f"{owner.name} departs |340{self.card_dir_name(exit_card_dir)}|n "
                            f"towards |310{exit_obj.name}|n.")

    # Sends the final string to the specified objects.
    def send_departure_string(self):
        self.owner.msg(self.self_str)
        self.owner.location.msg_contents(self.others_str, exclude=self.owner)

#-------------------------------------------------------
# announce_move_to hook on Character typeclass
    # doc str
    def find_origin_exit(self, origin, destination):
        exits = []
        for o in destination.contents:
            if o.location is destination and o.destination is origin:
                exits.append(o)
        self.origin_exit = exits[0] if exits else "somewhere"

    # doc str
    def origin_exit_missing_destination(self, origin, location):
        if not hasattr(self.origin_exit, 'destination'):
            if origin:
                location.msg_contents(f"{self.owner.name} arrives from |310{origin.name}|n.", exclude=self.owner)
            return True
        else:
            return False

    # Determine arrival string based on exit type.
    def pick_arrival_string(self, origin):
        # Arrival string direction must be the opposite of the origin_exit cardinal direction.
        # A character walking to the east will arrive in its destination from the west.
        # A character arriving by way of climbing down some stairs from above.
        origin_exit = self.origin_exit
        self.others_str = ''

        if origin_exit.tags.get(category='card_dir'):
            if origin_exit.tags.get('door', category='exits'):
                self.arrive_door_str()
            elif origin_exit.tags.get('stair', category='exits'):
                self.arrive_stair_str()
            elif origin_exit.tags.get('ladder', category='exits'):
                self.arrive_ladder_str()
            else:
                self.arrive_default_str()
        else:
            self.others_str = f"{self.owner.name} arrives."

    # Door Strings
    def arrive_door_str(self):
        origin_exit = self.origin_exit
        origin_exit_card_dir = origin_exit.tags.get(category='card_dir')
        if origin_exit_card_dir in ['up', 'down']:
            self.others_str = (f"{self.owner.name} arrives, climbing |340{self.card_dir_name(origin_exit_card_dir)}|n "
                            f"through |310{origin_exit.name}|n.")
        else:
            self.others_str = (f"{self.owner.name} arrives from |310{origin_exit.name}|n to the "
                            f"|340{self.card_dir_name(origin_exit_card_dir)}|n.")
    # Stair Strings
    def arrive_stair_str(self):
        origin_exit = self.origin_exit
        origin_exit_card_dir = origin_exit.tags.get(category='card_dir')
        if origin_exit_card_dir in ['up', 'down']:
            self.others_str = (f"{self.owner.name} arrives, climbing |310{origin_exit.name}|n "
                                f"|340{self.card_dir_name(origin_exit_card_dir)}|n.")
        else:
            self.others_str = (f"{self.owner.name} arrives from |310{origin_exit.name}|n to the "
                            f"|340{self.card_dir_name(origin_exit_card_dir)}|n.")
    # Ladder Strings
    def arrive_ladder_str(self):
        origin_exit = self.origin_exit
        origin_exit_card_dir = origin_exit.tags.get(category='card_dir')
        if origin_exit_card_dir in ['up', 'down']:
            self.others_str = (f"{self.owner.name} arrives, climbing |310{origin_exit.name}|n "
                                f"|340{self.card_dir_name(origin_exit_card_dir)}|n.")
        else:
            self.others_str = (f"{self.owner.name} arrives from |310{origin_exit.name}|n to the "
                            f"|340{self.card_dir_name(origin_exit_card_dir)}|n.")
    def arrive_default_str(self):
        origin_exit = self.origin_exit
        origin_exit_card_dir = origin_exit.tags.get(category='card_dir')
        if origin_exit_card_dir in ['up', 'down']:
                self.others_str = (f"{self.owner.name} arrives, climbing "
                                    f"|340{self.card_dir_name(origin_exit_card_dir)}|n "
                                    f"from |310{origin_exit.name}|n.")
        else:
            self.others_str = (f"{self.owner.name} arrives from |310{origin_exit.name}|n to the "
                            f"|340{self.card_dir_name(origin_exit_card_dir)}|n.")

    # doc str
    def send_arrival_string(self):
        self.owner.location.msg_contents(self.others_str, exclude=self.owner)

#-------------------------
# at_after_move() hook on Character typeclass
    # Generate a summary description of a location, its occupants, and exits.
    def location_summary(self):
        """
        You arrive at <location name>. <Person/Sentient> <is/are> here. You see <exit name> to the 
        <exit direction>, and <exit name> to the <exit direction>.
        """
        owner = self.owner
        location = owner.location
        characters = []
        exits = []
        char_str = ''
        exit_str = ''
        msg = ''

        if location is None:
            return "You have arrive nowhere."

        # Generate lists of characters and exits in the room.
        for i in location.contents:
            if inherits_from(i, 'characters.characters.Character') and i is not owner:
                characters.append(i)
            elif inherits_from(i, 'travel.exits.Exit'):
                exits.append(i)

        # Parse list of characters.
        if len(characters) > 1:
            char_list = gen_mec.objects_to_display_names(characters, owner)
            temp_list = []
            for i in char_list:
                temp_list.append(f"|c{i}|n")
            char_str = gen_mec.comma_separated_string_list(temp_list)
            char_str = f"{char_str} are here. "
        elif len(characters) == 1:
            char_str = f'|c{characters[0].get_display_name(owner)}|n'
            char_str = f"{char_str} is here. "
        else:
            char_str = False

        # Parse list of exits.
        exit_str = self.exits_to_string(exits)

        # Generate final outgoing message.
        msg = f"You arrive at |310{location.get_display_name(owner)}|n. "
        msg = f"{msg}{'' if char_str == False else char_str}" # Characters string addition.
        if exit_str:
            msg = f"{msg}You see {exit_str}."
        else:
            msg = f"{msg}{self.no_exit_str}"
        return msg

#-------------------------
# return_appearance hook on Room typeclass
    def room_exits(self, exits):
        exit_str = self.exits_to_string(exits)
        if exit_str == False:
                exit_str = "    There are no obvious exits."
        else:
            exit_str = f"    You see {exit_str}."
        return exit_str
