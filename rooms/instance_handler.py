import random, time
from datetime import datetime

from evennia import GLOBAL_SCRIPTS
from evennia.utils import logger
from evennia.utils.search import search_object
from evennia.utils.create import create_object
from evennia.utils.utils import variable_from_module


class InstanceHandler:
    def __init__(self, owner):
        self.owner = owner
        self.randomize_room_type = False
        self.static_zones = variable_from_module("rooms.zones", variable='static_zones')

        # The instance ledger is set in server.conf.settings
        self.ledger = GLOBAL_SCRIPTS.instance_ledger

    # The instance handler should check for currently owned instances of the same request.
    # If an instance conflict is found, the player is prompted to choose between the old instance and new.

    # Need to generate 3-5 new rooms. Exits never connect back to previous rooms > 1 room prior.
    # Room location will be set to none and typeclass will be Room.

    # A portal will open in the owner's current location, leading to the first room.
    # Another portal is added to the final room that returns to the original location.

#-------------
# Instance Options
    # Called by rooms.instance_menu
    def set_room_type(self, room_type):
        if room_type == 'random':
            self.randomize_room_type = True
        else:
            self.randomize_room_type = False
            self.room_type = room_type
            
        self._generate_instance()

#-------------
# Instance Creation
    def _generate_instance(self):
        # Save the data to the handler.
        self.used_coords = []
        self.rooms_list = []
        self.exits_list = []

        self._set_origin_room()
        self._set_time()
        self._set_instance_id()
        self._get_room_qty()
        self._generate_rooms()
        self._generate_exits()
        self._save_instance()
        self._create_log_string()

    def _generate_rooms(self):
        for _ in range(1, self.room_qty + 1):
            if self.randomize_room_type:
                self._get_room_type()
            self._get_room_key()

            self.room = create_object(typeclass='rooms.rooms.Room', key=self.room_key)
            self.room.tags.add(self.instance_id, category='instance_id')
            self.room.tags.add(self.room_type, category='zone_type')
            self.room.tags.add('instance_spawn_testing', category='zone_id')
            self.room.tags.add('has_spawn')
            self.rooms_list.append(self.room)

    def _generate_exits(self):
        for num, room in enumerate(self.rooms_list, start=1):
            if num == 1:
                # Generate a portal in origin room that leads to first room of the instance.
                portal_to_instance = create_object(typeclass='travel.exits.Exit', key=room.name,
                    location=self.origin_room, aliases=['port', 'portal'],
                    tags=[('portal', 'exits'), ('enter_instance', 'exits')], destination=room)
                self.exits_list.append(portal_to_instance)

                # Room 1 Coordinates
                current_room_coords = {'x': 0, 'y': 0}
                room.attributes.add('coords', current_room_coords)
                self.used_coords.append(current_room_coords)

                # Decide next room's coordinates.
                self._generate_new_room_coords(current_room_coords)

                # The first room only requires 1 exit.
                exit_to_next_room = create_object(typeclass='travel.exits.Exit', key='temp',
                                        location=room)
                exit_to_next_room.tags.add(self.dir_choice, category='card_dir')
                self.exits_list.append(exit_to_next_room)

                # Store this iteration's objects for the next room.
                prev_room = room
                prev_room_exit = exit_to_next_room

            elif num > 1 and num < len(self.rooms_list): # All rooms between first and last.
                # Connect the previous room to this room.
                prev_room_exit.destination = room
                prev_room_exit.key = room.name

                exit_to_previous_room = create_object(typeclass='travel.exits.Exit', key=prev_room.name,
                                        location=room, destination=prev_room)
                exit_to_previous_room.tags.add(self._opposite_card_dir(self.dir_choice), category='card_dir')
                self.exits_list.append(exit_to_previous_room)
                
                # Room Coordinates
                current_room_coords = self.next_room_coords
                room.attributes.add('coords', current_room_coords)
                self.used_coords.append(current_room_coords)

                # Decide next room's coordinates.
                self._generate_new_room_coords(current_room_coords)

                exit_to_next_room = create_object(typeclass='travel.exits.Exit', key='temp',
                                        location=room)
                exit_to_next_room.tags.add(self.dir_choice, category='card_dir')
                self.exits_list.append(exit_to_next_room)

                # Store this iteration's objects for the next room.
                prev_room = room
                prev_room_exit = exit_to_next_room
            
            elif num == len(self.rooms_list):
                # Connect the previous room to this room.
                prev_room_exit.destination = room
                prev_room_exit.key = room.name

                # The final room requires an exit back to previous room.
                exit_to_previous_room = create_object(typeclass='travel.exits.Exit', key=prev_room.name,
                                        location=room, destination=prev_room)
                exit_to_previous_room.tags.add(self._opposite_card_dir(self.dir_choice), category='card_dir')
                self.exits_list.append(exit_to_previous_room)

                # Room Coordinates
                current_room_coords = self.next_room_coords
                room.attributes.add('coords', current_room_coords)
                self.used_coords.append(current_room_coords)

                # Create a portal that returns back to the location the instance was generated from.
                portal_to_origin = create_object(typeclass='travel.exits.Exit', key=self.origin_room.name,
                                    location=room, aliases=['port', 'portal'],
                                    tags=[('portal', 'exits'), ('exit_instance', 'exits')], 
                                    destination=self.origin_room)
                self.exits_list.append(portal_to_origin)

        for exit in self.exits_list:
            exit.tags.add(self.instance_id, category='instance_id')

    def _generate_new_room_coords(self, current_room_coords):
        """
        Picks a random cardinal direction and uses it to generate a new set of 
        random x, y coordinates. Tests the new coordinates to ensure that they aren't already in use.
        When results aren't already in the self.used_coords list, they are set to the handler.

        Arguments:
            current_room_coords (dictionary): A dictionary consisting of an x key and y key
                both containing an integar.
        
        Sets:
            self.next_room_coords (dictionary): A dictionary consisting of an x key and y key
                both containing an integar.
            self.dir_choice (string): A cardinal direction used to determine the exit direction
                of the current room to the new room.

        Example:
            https://gist.github.com/kovitikus/f231899a6111f508675596fd8599182f
        """
        free_space = False
        card_dirs = ['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw']

        while free_space == False:
            dir_choice = random.choice(card_dirs)

            test_coords = self._card_dir_to_coords(current_room_coords, dir_choice)

            if test_coords not in self.used_coords:
                self.next_room_coords = test_coords
                self.dir_choice = dir_choice
                free_space = True
            else:
                card_dirs.remove(dir_choice)

    def _save_instance(self):
        # Save to ledger.
        if not self.ledger.attributes.has('instances'):
            self.ledger.attributes.add('instances', {})
        self.ledger.db.instances[self.instance_id] = {}
        self.ledger.db.instances[self.instance_id]['creator'] = self.owner
        self.ledger.db.instances[self.instance_id]['epoch_creation'] = self.epoch_creation
        self.ledger.db.instances[self.instance_id]['epoch_expiration'] = self.epoch_expiration
        self.ledger.db.instances[self.instance_id]['rooms'] = self.rooms_list
        self.ledger.db.instances[self.instance_id]['exits'] = self.exits_list

        # Save to object that generated this instance.
        if not self.owner.attributes.has('instances'):
            self.owner.attributes.add('instances', {})
        self.owner.db.instances[self.instance_id] = {}
        self.owner.db.instances[self.instance_id]['epoch_creation'] = self.epoch_creation
        self.owner.db.instances[self.instance_id]['epoch_expiration'] = self.epoch_expiration
        self.owner.db.instances[self.instance_id]['rooms'] = self.rooms_list
        self.owner.db.instances[self.instance_id]['exits'] = self.exits_list

    def _create_log_string(self):
        border = "======================================================"
        instance_type = f"Instance Type: {'random' if self.randomize_room_type else self.room_type}"
        creation_time = f"Creation Time: {self.creation_time}"
        creator = f"Creator: {self.owner.name}"
        epoch_create = f"Epoch Creation: {self.epoch_creation}"
        epoch_expire = f"Epoch Expiration: {self.epoch_expiration}"
        room_count = f"Room Count: {len(self.rooms_list)}"
        log_str = f"{border}\n{instance_type}\n{creation_time}\n{creator}\n"
        log_str = f"{log_str}\n{epoch_create}\n{epoch_expire}\n{room_count}\n"

        self.ledger.db.instances[self.instance_id]['log_str'] = log_str
        self.owner.db.instances[self.instance_id]['log_str'] = log_str
        logger.log_file(log_str, filename='instances.log')

#-------------
# Helpers
    def _set_origin_room(self):
        self.origin_room = self.owner.location

    def _set_time(self):
        self.creation_time = datetime.now()
        self.epoch_creation = time.time()
        self.epoch_expiration = self.epoch_creation + (3600 * 24) # 3,600s = 1h

    def _set_instance_id(self):
        self.instance_id = f"{self.owner.dbid}_{self.creation_time}"

    def _get_room_qty(self):
        # Each instance will, for now, contain a possibility of 5-10 rooms.
        self.room_qty = random.randrange(6, 11)

    def _get_room_type(self):
        room_types = ['forest', 'sewer', 'cave', 'alley']
        self.room_type = random.choice(room_types)

    def _get_room_key(self):
        room_type = self.room_type
        forest = ['a sacred grove of ancient wood', 'a sparsely-populated fledgling forest', 'a cluster of conifer trees']
        sewer = ['a poorly-maintained sewage tunnel', 'a sewer tunnel constructed of ancient brick', 'a wide walkway along sewage']
        cave = ['an uncertain rock bridge', 'a wide opening between', 'a damp rock shelf']
        alley = ['a dark alleyway', 'a filthy alleyway', 'a narrow alleyway']

        if room_type == 'forest':
            self.room_key = random.choice(forest)
        elif room_type == 'sewer':
            self.room_key = random.choice(sewer)
        elif room_type == 'cave':
            self.room_key = random.choice(cave)
        elif room_type == 'alley':
            self.room_key = random.choice(alley)

    def _opposite_card_dir(self, card_dir):
        if card_dir == 'n':
            opp_dir = 's'
        elif card_dir == 'ne':
            opp_dir = 'sw'
        elif card_dir == 'e':
            opp_dir = 'w'
        elif card_dir == 'se':
            opp_dir = 'nw'
        elif card_dir == 's':
            opp_dir = 'n'
        elif card_dir == 'sw':
            opp_dir = 'ne'
        elif card_dir == 'w':
            opp_dir = 'e'
        elif card_dir == 'nw':
            opp_dir = 'se'
        return opp_dir

    def _card_dir_to_coords(self, current_coords, card_dir):
        """
        Takes a current room's coordinates and decides what the next room's coordinates would be
        based on the cardinal direction provided from the current room.

        Arguments:
            current_cords (dictionary): A dictionary consisting of an x key and y key
                both containing an integar.
            card_dir (string): A string with the cardinal direction. i.e. 'ne'
        
        Returns (dictionary):
            The new x, y coordinates in the same form as the current_cords.

        Cheat Sheet:
            n = x, y - 1
            ne = x + 1, y - 1
            e = x + 1, y
            se = x + 1, y + 1
            s = x, y + 1
            sw = x - 1, y + 1
            w = x - 1, y
            nw = x - 1, y - 1
        """
        if card_dir == 'n':
            new_coords_x = current_coords['x']
            new_coords_y = current_coords['y'] - 1
        elif card_dir == 'ne':
            new_coords_x = current_coords['x'] + 1
            new_coords_y = current_coords['y'] - 1
        elif card_dir == 'e':
            new_coords_x = current_coords['x'] + 1
            new_coords_y = current_coords['y']
        elif card_dir == 'se':
            new_coords_x = current_coords['x'] + 1
            new_coords_y = current_coords['y'] + 1
        elif card_dir == 's':
            new_coords_x = current_coords['x']
            new_coords_y = current_coords['y'] + 1
        elif card_dir == 'sw':
            new_coords_x = current_coords['x'] - 1
            new_coords_y = current_coords['y'] + 1
        elif card_dir == 'w':
            new_coords_x = current_coords['x'] - 1
            new_coords_y = current_coords['y']
        elif card_dir == 'nw':
            new_coords_x = current_coords['x'] - 1
            new_coords_y = current_coords['y'] - 1
        return {'x': new_coords_x, 'y': new_coords_y}

#------------------------------
# Character Enter and Exit: at_after_traverse() on the Exit typeclass.
    # Exit tagged with ('enter_instance', category='exits')
    def enter_instance(self):
        # Determine the currently occupied room's instance_id.
        if self.owner.location.tags.get(category='instance_id'):
            instance_id = self.owner.location.tags.get(category='instance_id')

            # Add character to instance occupant list.
            if self.ledger.db.instances[instance_id].get('occupants') is None:
                self.ledger.db.instances[instance_id]['occupants'] = []
            self.ledger.db.instances[instance_id]['occupants'].append(self.owner)
        else:
            # This instance_id acquisition should NOT fail. If it does, something went wrong.
            err_msg = f"enter_instance could not find instance_id!"
            logger.log_file(err_msg, filename='instance_errors.log')
            self.owner.msg('|rCRITICAL ERROR! enter_instance could not find the instance_id!|n')
            return

    # Exit tagged with ('exit_instance', category='exits')
    def exit_instance(self, source_location):
        # This is where the instance cleanup is triggered.
        # Must first determine that all ledger occupants have exited.

        if source_location.tags.get(category='instance_id'):
            instance_id = source_location.tags.get(category='instance_id')

            self.ledger.db.instances[instance_id]['occupants'].remove(self.owner)

            if len(self.ledger.db.instances[instance_id]['occupants']) == 0:
                self._destroy_instance(instance_id)
        else:
            # This instance_id acquisition should NOT fail. If it does, something went wrong.
            err_msg = f"exit_instance could not find instance_id!"
            logger.log_file(err_msg, filename='instance_errors.log')
            self.owner.msg('|rCRITICAL ERROR! exit_instance could not find the instance_id!|n')
            return

#---------------
# Destroy the instance.
    def _destroy_instance(self, instance_id):
        # Make sure the instance_id exists on the ledger.
        if not instance_id in self.ledger.db.instances:
            err_msg = f"destroy_instance could not find instance_id: {instance_id}"
            logger.log_file(err_msg, filename='instance_errors.log')
            self.owner.msg('|rCRITICAL ERROR! destroy_instance could not find the instance_id!|n')
            return

        # Check to make sure there are no orphaned characters or objects remaining in the instance.
        # Any left behind will be sent to their default home, so this is not critical.
        
        # Delete all exits.
        exits_list = list(self.ledger.db.instances[instance_id]['exits'])
        for exit in exits_list:
            self.ledger.db.instances[instance_id]['exits'].remove(exit)
            exit.delete()
        if len(self.ledger.db.instances[instance_id]['exits']) == 0:
            del self.ledger.db.instances[instance_id]['exits']

        # Delete all rooms.
        rooms_list = list(self.ledger.db.instances[instance_id]['rooms'])
        for room in rooms_list:
            self.ledger.db.instances[instance_id]['rooms'].remove(room)
            room.delete()
        if len(self.ledger.db.instances[instance_id]['rooms']) == 0:
            del self.ledger.db.instances[instance_id]['rooms']

        # Remove the instance from the creator object.
        creator = self.ledger.db.instances[instance_id]['creator']
        del creator.db.instances[instance_id]
        # Exits and Rooms are deleted, remove the instance from the ledger.
        del self.ledger.db.instances[instance_id]

#----------------------
# Generate OOC Chambers for new accounts.
    def generate_ooc_rooms(self):
        owner = self.owner

        name = owner.key
        possessive = '\'' if name[-1] == 's' else '\'s'
        homeroom = create_object(typeclass='rooms.rooms.Room', key=f"{name}{possessive} Quarters")
        homeroom.db.desc = ("This compact room leaves much to be desired. "
            "It has a bunk large enough for one person and an adjoining basic bathroom facility.")
        homeroom.tags.add(category='ooc_room')
        owner.home = homeroom
        owner.location = homeroom

        portal_room = create_object(typeclass='rooms.rooms.Room', key='Portal Room')
        portal_room.tags.add(category='ooc_room')

        # Make exits connecting the Portal Room with the Workshop
        quarters_to_portal_rm = create_object(typeclass='travel.exits.Exit',
                                    key=f'{portal_room.name}', aliases='portal', 
                                    destination=portal_room, location=homeroom, home=homeroom)
        quarters_to_portal_rm.tags.add('n', category='card_dir')
        quarters_to_portal_rm.tags.add(category='ooc_exit')

        portal_rm_to_quarters = create_object(typeclass='travel.exits.Exit',
                                    key=f"{homeroom.name}", aliases=['quar', 'quart'], 
                                    destination=homeroom, location=portal_room, home=portal_room)
        portal_rm_to_quarters.tags.add('s', category='card_dir')
        portal_rm_to_quarters.tags.add(category='ooc_exit')

        # Connect the portal room to the Common Room
        common_room = search_object('Common Room')[0]
        portal_rm_to_common = create_object(typeclass='travel.exits.Exit',
                                    key=f'{common_room.name}', aliases='common', 
                                    destination=common_room, location=portal_room, home=portal_room)
        portal_rm_to_common.tags.add('n', category='card_dir')
        portal_rm_to_common.tags.add(category='ooc_exit')

#-------------
# Static Zone Generation
    def generate_static_zone(self, zone):
        """
        Takes a list of dictionaries, each dictionary with instructions for a single room and its exits
        and generates them into the world. Coordinates and cardinal directions are required.

        Arguments:
            zone (string): The name of the zone requested. It is passed into here by instance_menu.py
                but the instructions are held in the zones.py module.

        Example:
            https://gist.github.com/kovitikus/b561663ec5c75f1598d50f2cd7b741b7
        """
        instructions = self.static_zones[zone]
        #----------
        # Room Generation
        # Doing this first ensures that each exit's destination room object already exists.
        rooms_list = []
        for dict in instructions:
            room_key = dict['key']
            room_desc = dict.get('desc', f"You see nothing special about {room_key}.")

            room = create_object("rooms.rooms.Room", key=room_key, tags=[(zone, 'zone_id')],
            attributes=[('coords', dict['coords']), ('desc', room_desc)])

            # Checks to see if the room has any static sentients and if so, calls the spawner.
            static_sentients = dict.get('static_sentients', None) # A list of strings.
            if static_sentients:
                for sentient in static_sentients:
                    room.spawn.static_sentient(sentient, room)

            rooms_list.append(room)

        #----------
        # Exit Generation
        for num, dict in enumerate(instructions, start=0):
            # There exists the same number of created rooms as dictionaries in the instructions list.
            # This can be used to match the dictionary entry to the room object.
            current_room = rooms_list[num]
            for card_dir in dict['exits']:
                # First the exit destination's coordinates are calculated and then checked against
                # the list of rooms already generated to find the appropriate destination.
                card_dir_room_coords = self._card_dir_to_coords(dict['coords'], card_dir)
                for room in rooms_list:
                    if room.db.coords == card_dir_room_coords:
                        destination_found = True
                        exit_destination = room
                # Successfully found the exit's destination, create the exit.
                if destination_found:
                    exit_obj = create_object(typeclass='travel.exits.Exit', key=exit_destination.key,
                                            location=current_room, destination=exit_destination)
                    exit_obj.tags.add(card_dir, category='card_dir')
