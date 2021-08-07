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
        self.static_zones = variable_from_module("rooms.zones", variable='static_zones')

        # The instance ledger is set in server.conf.settings
        ledger = GLOBAL_SCRIPTS.instance_ledger
        instance_types = ['temporary_instance', 'static_instance']
        for type in instance_types:
            if not ledger.attributes.has(key=type):
                ledger.attributes.add(type, {})
        self.ledger = ledger

#----------------------
# Temporary Instance Generation
    def generate_temporary_instance(self, zone_type):
        """
        Calls upon the methods required to assemble the randomly generated instance.
        This type of instance is temporary and has an expiration set as an epoch timestamp.

        Arguments:
            zone_type (string): A type of zone, which determines the room's description and 
                which sentients occupy the zone. Such as forest, sewer, caves, etc.
        """
        owner = self.owner
        instance_type = 'temporary_instance'

        creation_time, epoch_creation, epoch_expiration = self._set_time(instance_type)
        instance_id = f"{owner.dbid}_{creation_time}"

        rooms_list = self._generate_rooms(zone_type, instance_id)
        exits_list = self._generate_exits(rooms_list)

        for exit in exits_list:
            exit.tags.add(instance_id, category='instance_id')

        self._save_instance(instance_type, instance_id, zone_type, creation_time, epoch_creation,
            epoch_expiration, rooms_list, exits_list)

    def _generate_rooms(self, zone_type, instance_id):
        rooms_list = []
        min_room_qty = 6
        max_room_qty = 11

        room_qty = random.randrange(min_room_qty, max_room_qty)

        for _ in range(1, room_qty + 1):
            room = create_object(typeclass='rooms.rooms.Room', key=self._generate_room_key(zone_type))
            room.tags.add(instance_id, category='instance_id')
            room.tags.add(zone_type, category='zone_type')
            room.tags.add('instance_spawn_testing', category='zone_id')
            room.tags.add('has_spawn')
            rooms_list.append(room)

        return rooms_list

    def _generate_exits(self, rooms_list):
        exits_list = []
        used_coords = []
        origin_room = self.owner.location
        for num, room in enumerate(rooms_list, start=1):
            if num == 1:
                # Generate a portal in origin room that leads to first room of the instance.
                portal_to_instance = create_object(typeclass='travel.exits.Exit', key=room.name,
                    location=origin_room, aliases=['port', 'portal'],
                    tags=[('portal', 'exits'), ('enter_instance', 'exits')], destination=room)
                exits_list.append(portal_to_instance)

                # Room 1 Coordinates
                current_room_coords = {'x': 0, 'y': 0}
                room.attributes.add('coords', current_room_coords)
                used_coords.append(current_room_coords)

                # Decide next room's coordinates.
                dir_choice, next_room_coords = self._generate_new_room_coords(current_room_coords, used_coords)

                # The first room only requires 1 exit.
                exit_to_next_room = create_object(typeclass='travel.exits.Exit', key='temp',
                                        location=room)
                exit_to_next_room.tags.add(dir_choice, category='card_dir')
                exits_list.append(exit_to_next_room)

                # Store this iteration's objects for the next room.
                prev_room = room
                prev_room_exit = exit_to_next_room

            elif num > 1 and num < len(rooms_list): # All rooms between first and last.
                # Connect the previous room to this room.
                prev_room_exit.destination = room
                prev_room_exit.key = room.name

                exit_to_previous_room = create_object(typeclass='travel.exits.Exit', key=prev_room.name,
                                        location=room, destination=prev_room)
                exit_to_previous_room.tags.add(self._opposite_card_dir(dir_choice), category='card_dir')
                exits_list.append(exit_to_previous_room)
                
                # Room Coordinates
                current_room_coords = next_room_coords
                room.attributes.add('coords', current_room_coords)
                used_coords.append(current_room_coords)

                # Decide next room's coordinates.
                dir_choice, next_room_coords = self._generate_new_room_coords(current_room_coords, used_coords)

                exit_to_next_room = create_object(typeclass='travel.exits.Exit', key='temp',
                                        location=room)
                exit_to_next_room.tags.add(dir_choice, category='card_dir')
                exits_list.append(exit_to_next_room)

                # Store this iteration's objects for the next room.
                prev_room = room
                prev_room_exit = exit_to_next_room
            
            elif num == len(rooms_list):
                # Connect the previous room to this room.
                prev_room_exit.destination = room
                prev_room_exit.key = room.name

                # The final room requires an exit back to previous room.
                exit_to_previous_room = create_object(typeclass='travel.exits.Exit', key=prev_room.name,
                                        location=room, destination=prev_room)
                exit_to_previous_room.tags.add(self._opposite_card_dir(dir_choice), category='card_dir')
                exits_list.append(exit_to_previous_room)

                # Room Coordinates
                current_room_coords = next_room_coords
                room.attributes.add('coords', current_room_coords)
                used_coords.append(current_room_coords)

                # Create a portal that returns back to the location the instance was generated from.
                portal_to_origin = create_object(typeclass='travel.exits.Exit', key=origin_room.name,
                                    location=room, aliases=['port', 'portal'],
                                    tags=[('portal', 'exits'), ('exit_instance', 'exits')], 
                                    destination=origin_room)
                exits_list.append(portal_to_origin)
        return exits_list

#----------------------
# Static Instance Generation
    def generate_static_instance(self, zone_type):
        """
        Takes a list of dictionaries, each dictionary with instructions for a single room and its exits
        and generates them into the world. Coordinates and cardinal directions are required.

        Arguments:
            zone (string): The name of the zone requested. It is passed into here by instance_menu.py
                but the instructions are held in the zones.py module.

        Example:
            https://gist.github.com/kovitikus/b561663ec5c75f1598d50f2cd7b741b7
        """
        rooms_list = []
        exits_list = []
        sentients_list = []
        instructions = self.static_zones[zone_type]
        instance_id = zone_type
        instance_type = 'static_instance'
        creation_time, epoch_creation, epoch_expiration = self._set_time(instance_type)

        #----------
        # Room Generation
        # Doing this first ensures that each exit's destination room object already exists.
        for dict in instructions:
            room_key = dict['key']
            room_desc = dict.get('desc', f"You see nothing special about {room_key}.")
            tags = dict.get('tags', [])
            tags.append((zone_type, 'zone_id'))

            room = create_object("rooms.rooms.Room", key=room_key, tags=tags,
            attributes=[('coords', dict['coords']), ('desc', room_desc)])

            # Checks to see if the room has any static sentients and if so, calls the spawner.
            static_sentients = dict.get('static_sentients', None) # A list of strings.
            if static_sentients:
                for sentient in static_sentients:
                    sentient_obj = room.spawn.static_sentient(sentient, room)
                    sentients_list.append(sentient_obj)

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
                    exits_list.append(exit_obj)

        self._save_instance(instance_type, instance_id, zone_type, creation_time, epoch_creation,
            epoch_expiration, rooms_list, exits_list, sentients_list=sentients_list)

#----------------------
# Instance Save and Destroy
    def _save_instance(self, instance_type, instance_id, zone_type, creation_time, epoch_creation,
        epoch_expiration, rooms_list, exits_list, sentients_list=None):
        """
        This method saves the instance data to the instance ledger (global script). It also stores the
        data in a log string, which is saved to a log file.

        Arguments:
            instance_type (string): One of static_instance or temporary_instance.
            instance_id (string): The unique identifier for this instance. Temporary instances
                have an ID generated from a timestamp, while static instances have a static ID based
                on the zone's name.
            zone_type (string): The type of zone used to generate the instance. Such as forest, caves,
                sewer, etc.
            creation_time (string): The human-readable instance creation timestamp.
            epoch_creation (float): The epoch variation of the instance's creation timestamp.
            epoch_expiration (float): The timestamp used to determine when the instance will automatically
                be destroyed. This is set to 0 if the instance is static.
            rooms_list (list): A list of room objects that were generated for this instance.
            exits_list (list); A list of exit objects that were generated for this instance.
        """
        owner = self.owner
        if sentients_list is None:
            sentients_list = []

        log_str = self._create_log_string(instance_type, instance_id, zone_type, creation_time,
            epoch_creation, epoch_expiration, rooms_list)
        logger.log_file(log_str, filename=f'{instance_type}.log')

        # Save to ledger.
        ledger_dict = self.ledger.attributes.get(key=instance_type)
        ledger_dict[instance_id] = {}
        ledger_dict[instance_id]['creator'] = owner
        ledger_dict[instance_id]['creation_time'] = creation_time
        ledger_dict[instance_id]['epoch_creation'] = epoch_creation
        ledger_dict[instance_id]['epoch_expiration'] = epoch_expiration
        ledger_dict[instance_id]['rooms'] = rooms_list
        ledger_dict[instance_id]['exits'] = exits_list
        ledger_dict[instance_id]['sentients'] = sentients_list
        ledger_dict[instance_id]['log_str'] = log_str

        # Save to object that generated this instance.
        if instance_type == 'temporary_instance':
            if not owner.attributes.get(key=instance_type):
                owner.attributes.add(instance_type, {})
            ledger_dict = owner.attributes.get(key=instance_type)
            ledger_dict[instance_id] = {}
            ledger_dict[instance_id]['epoch_creation'] = epoch_creation
            ledger_dict[instance_id]['epoch_expiration'] = epoch_expiration
            ledger_dict[instance_id]['rooms'] = rooms_list
            ledger_dict[instance_id]['exits'] = exits_list
            ledger_dict[instance_id]['sentients'] = sentients_list
            ledger_dict[instance_id]['log_str'] = log_str

    def destroy_instance(self, instance_type, instance_id):
        # Get the proper instance dictionary type.
        ledger_dict = self.ledger.attributes.get(key=instance_type)
        # Make sure the instance_id exists on the ledger.
        if not instance_id in ledger_dict:
            err_msg = f"destroy_instance could not find instance_id: {instance_id}"
            logger.log_file(err_msg, filename='instance_errors.log')
            self.owner.msg('|rCRITICAL ERROR! destroy_instance could not find the instance_id!|n')
            return
        else:
            instance_dict = ledger_dict[instance_id]

        # Delete all sentients.
        sentients_list = instance_dict['sentients']
        for sentient in sentients_list:
            # Delete all objects in the sentient's inventory.
            for item in sentient.contents:
                item.delete()
            sentient.delete()
        if len(sentients_list) == 0:
            del ledger_dict[instance_id]['sentients']

        # Delete all exits.
        exits_list = instance_dict['exits']
        for exit in exits_list:
            exit.delete()
        if len(exits_list) == 0:
            del ledger_dict[instance_id]['exits']

        # Delete all rooms.
        rooms_list = instance_dict['rooms']
        for room in rooms_list:
            # Delete all objects in the room.
            for item in room.contents:
                item.delete()
            room.delete()
        if len(rooms_list) == 0:
            del ledger_dict[instance_id]['rooms']

        # Remove the instance from the creator object.
        if instance_type == 'temporary_instance':
            creator = instance_dict['creator']
            creator_dict = creator.attributes.get(instance_type)
            del creator_dict[instance_id]
        # Exits and Rooms are deleted, remove the instance from the ledger.
        del ledger_dict[instance_id]

#----------------------
# Helpers
    def _set_time(self, instance_type):
        """
        Sets various timestamps used in saving, managing, and logging the instance.

        Arguments:
            instance_type (string): Determines if this instance will be static or temporary.
                Only temporary instances expire, automatically destroying themselves.

        Returns:
            creation_time (string): A human-readable format of the instance creation time.
            epoch_creation (float): An epoch timestamp.
            epoch_expiration (float): An epoch timestamp. Used to determine when the instance is 
                ready to be destroyed.
        """
        now = datetime.now()
        creation_time = str(now)
        epoch_creation = now.timestamp()
        if instance_type == 'static_instance':
            epoch_expiration = 0
        elif instance_type == 'temporary_instance':
            epoch_expiration = epoch_creation + (3600 * 24) # 3,600 seconds = 1 hour
        
        return creation_time, epoch_creation, epoch_expiration

    def _generate_room_key(self, zone_type):
        """
        Randomly picks a key for a room, based on the type of zone requested.

        Arguments:
            zone_type (string): The type of zone to choose from.

        Returns:
            room_key (string): The randomly chosen room key.
        """
        temporary_zones_dict = variable_from_module('rooms.zones', 'temporary_zones')
        room_keys_list = temporary_zones_dict.get(zone_type).get('room_keys', [])
        room_key = random.choice(room_keys_list)
        return room_key

    def _opposite_card_dir(self, card_dir):
        """
        Determines the cardinal direction of the exit of the connected room that would lead
        back to the cardinal direction passed to this method.

        Arguments:
            card_dir (string): The originating exit's cardinal direction.

        Returns:
            opp_dir (string): The destination exit's cardinal direction.
        """
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

    def _generate_new_room_coords(self, current_room_coords, used_coords):
        """
        Picks a random cardinal direction and uses it to generate a new set of 
        random x, y coordinates. Tests the new coordinates to ensure that they aren't already in use.
        When results aren't already in the used_coords list, they are set to the handler.

        Arguments:
            current_room_coords (dictionary): A dictionary consisting of an x key and y key
                both containing an integar.
            used_coords (list): A list of dictionaries consisting of coordinates already occupied.
        
        Returns:
            dir_choice (string): A cardinal direction used to determine the exit direction
                of the current room to the new room.
            next_room_coords (dictionary): A dictionary consisting of an x key and y key
                both containing an integar.

        Example:
            https://gist.github.com/kovitikus/f231899a6111f508675596fd8599182f
        """
        free_space = False
        card_dirs = ['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw']

        while free_space == False:
            dir_choice = random.choice(card_dirs)

            test_coords = self._card_dir_to_coords(current_room_coords, dir_choice)

            if test_coords not in used_coords:
                next_room_coords = test_coords
                free_space = True
            else:
                card_dirs.remove(dir_choice)
        return dir_choice, next_room_coords

    def _create_log_string(self, instance_type, instance_id, zone_type, creation_time, epoch_creation,
        epoch_expiration, rooms_list):
        border = "======================================================"
        instance_type = f"Instance ID: {instance_id}"
        room_type = f"Zone Type: {zone_type}"
        creation_time = f"Creation Time: {creation_time}"
        creator = f"Creator: {self.owner.name}"
        epoch_create = f"Epoch Creation: {epoch_creation}"
        epoch_expire = f"Epoch Expiration: {str(epoch_expiration)}"
        room_count = f"Room Count: {len(rooms_list)}"
        log_str = f"{border}\n{instance_type}\n{room_type}\n{creation_time}\n{creator}\n"
        log_str = f"{log_str}\n{epoch_create}\n{epoch_expire}\n{room_count}\n"

        return log_str

#----------------------
# Character Enter and Exit: at_after_traverse() on the Exit typeclass.
    # Exit tagged with ('enter_instance', category='exits')
    def enter_instance(self):
        owner = self.owner
        ledger = self.ledger
        # Determine the currently occupied room's instance_id.
        if owner.location.tags.get(category='instance_id'):
            instance_id = self.owner.location.tags.get(category='instance_id')

            # Add character to instance occupant list.
            if ledger.db.temporary_instance[instance_id].get(key='occupants') is None:
                ledger.db.temporary_instance[instance_id]['occupants'] = []
            ledger.db.temporary_instance[instance_id]['occupants'].append(owner)
        else:
            # This instance_id acquisition should NOT fail. If it does, something went wrong.
            err_msg = f"enter_instance could not find instance_id!"
            logger.log_file(err_msg, filename='temporary_instance_errors.log')
            owner.msg('|rCRITICAL ERROR! enter_instance could not find the instance_id!|n')
            return

    # Exit tagged with ('exit_instance', category='exits')
    def exit_instance(self, source_location):
        owner = self.owner
        ledger = self.ledger
        # This is where the instance cleanup is triggered.
        # Must first determine that all ledger occupants have exited.

        if source_location.tags.get(category='instance_id'):
            instance_id = source_location.tags.get(category='instance_id')

            ledger.db.temporary_instance[instance_id]['occupants'].remove(owner)

            if len(ledger.db.temporary_instance[instance_id]['occupants']) == 0:
                self.destroy_instance('temporary_instance', instance_id)
        else:
            # This instance_id acquisition should NOT fail. If it does, something went wrong.
            err_msg = f"exit_instance could not find instance_id!"
            logger.log_file(err_msg, filename='instance_errors.log')
            owner.msg('|rCRITICAL ERROR! exit_instance could not find the instance_id!|n')
            return

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
