import random
from datetime import datetime

from evennia.utils.create import create_object
from evennia.utils.evmenu import EvMenu


class InstanceHandler:
    randomize_room_type = False

    def __init__(self, owner):
        self.owner = owner

    # The instance handler should check for currently owned instances of the same request.
    # If an instance conflict is found, the player is prompted to choose between the old instance and new.

    # Need to generate 3-5 new rooms. Exits never connect back to previous rooms > 1 room prior.
    # Room location will be set to none and typeclass will be Room.

    # A portal will open in the owner's current location, leading to the first room.
    # Another portal is added to the final room that returns to the original location.

#-------------
# Instance Options
    # Called by rooms.instance_menu
    def instance_menu(self, instance):
        if instance == 'random':
            self.randomize_room_type = True
        else:
            self.randomize_room_type = False
            if instance == 'forest':
                self.room_type = 'forest'
            elif instance == 'sewer':
                self.room_type = 'sewer'
            elif instance == 'cave':
                self.room_type = 'cave'
            elif instance == 'alley':
                self.room_type = 'alley'
            
        self._generate_instance()

#-------------
# Instance Creation
    def _generate_instance(self):
        # Save the data to the handler.
        self.rooms_list = []
        self.exits_list = []

        self.creation_time = datetime.now()
        self.instance_id = f"{self.owner.dbid}_{self.creation_time}"
        self._get_room_qty()

        for _ in range(1, self.room_qty):
            if self.randomize_room_type:
                self._get_room_type()
            self._get_room_key()

            self.room = create_object(typeclass='rooms.rooms.Room', key=self.room_key)
            self.rooms_list.append(self.room)

        for num, room in enumerate(self.rooms_list, start=1):
            self._get_exit_type()
            self._get_exit_key()
            if num == 1:
                # Generate a portal in origin room that leads to first room of the instance.
                portal_to_instance = create_object(typeclass='travel.exits.Exit', key=self.exit_key,
                                            location=self.origin_room, tags=[('portal', 'exits')], 
                                            destination=room)
                self.exits_list.append(portal_to_instance)

                # The first room only requires 1 exit.
                exit_to_next_room = create_object(typeclass='travel.exits.Exit', key=self.exit_key,
                                        location=room, tags=[self.exit_type])
                self.exits_list.append(exit_to_next_room)

                # Store this iteration's objects for the next room.
                prev_room = room
                prev_room_exit = exit_to_next_room

            elif num > 1 and num < len(self.rooms_list):
                exit_to_next_room = create_object(typeclass='travel.exits.Exit', key=self.exit_key,
                                        location=room, tags=[self.exit_type])
                self.exits_list.append(exit_to_next_room)

                exit_to_previous_room = create_object(typeclass='travel.exits.Exit', key=self.exit_key,
                                            location=room, tags=[self.exit_type], destination=prev_room)
                self.exits_list.append(exit_to_previous_room)

                # Connect the previous room to this room.
                prev_room_exit.destination = room

                # Store this iteration's objects for the next room.
                prev_room = room
                prev_room_exit = exit_to_next_room
            
            elif num == len(self.rooms_list):
                # The final room requires an exit back to previous room.
                exit_to_previous_room = create_object(typeclass='travel.exits.Exit', key=self.exit_key,
                                            location=room, tags=[self.exit_type], destination=prev_room)
                self.exits_list.append(exit_to_previous_room)

                # Create a portal that returns back to the location the instance was generated from.
                portal_to_origin = create_object(typeclass='travel.exits.Exit', key=self.exit_key,
                                            location=room, tags=[('portal', 'exits')], destination=self.origin_room)
                self.exits_list.append(portal_to_origin)

        if not self.owner.attributes.has('instances'):
            self.owner.attributes.add('instances', {})
        self.owner.db.instances[self.instance_id] = self.rooms_list

#-------------
# Helpers
    def set_origin_room(self, origin):
        self.origin_room = origin

    def _get_room_qty(self):
        # Each instance will, for now, contain a possibility of 3-5 rooms.
        self.room_qty = random.randrange(3-5)

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

    def _get_exit_type(self):
        exit_types = [('stair', 'exits'), ('door', 'exits'), ('portal', 'exits')]
        self.exit_type = random.choice(exit_types)

    def _get_exit_key(self):
        room_key = self.room_key
        if room_key == 'forest':
            pass
        elif room_key == 'sewer':
            pass
        elif room_key == 'cave':
            pass
        pass
