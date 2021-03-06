import random
from evennia.utils import create

from evennia.utils.create import create_object


class InstanceHandler:
    def __init__(self, owner):
        self.owner = owner

    # The instance handler should check for currently owned instances of the same request.
    # If an instance conflict is found, the player is prompted to choose between the old instance and new.

    # Need to generate 3-5 new rooms. 
    # Room location will be set to none and typeclass will be Room.

    # A portal will open in the owner's current location, leading to the first room.
    # Another portal is added to the final room that returns to the original location.

    def generate_rooms(self):
        # Each instance will, for now, contain a possibility of 3-5 rooms.
        room_qty = random.randrange(3-5)
        # Save the data to the handler.
        self.rooms_list = []
        self.exits_list = []

        for _ in range(1, room_qty):
            # Pick a main theme for the room
            self.get_room_type()
            # Pick a name for the room based on the type.
            self.get_room_key()
            # ^
            self.get_exit_type()
            self.get_exit_key()
            
            # Create the room and save it to the handler.
            self.room = create_object(typeclass=self.room_type, key=self.room_key)
            self.rooms_list.append(self.room)
            # ^
            self.rm_exit = create_object(typeclass=self.exit_type, key=self.exit_key)
            self.exits_list.append(self.rm_exit)
            
            

        # Generate the exits for each room by tracking the current room and the previous room.

    def get_room_type(self):
        room_types = ['forest', 'sewer', 'cave']
        self.room_type = random.choice(room_types)

    def get_room_key(self):
        room_type = self.room_type
        forest = ['a sacred grove of ancient wood', 'a sparsely-populated fledgling forest', 'a cluster of conifer trees']
        sewer = ['a poorly-maintained sewage tunnel', 'a sewer tunnel constructed of ancient brick', 'a wide walkway along sewage']
        cave = ['an uncertain rock bridge', 'a wide opening between', 'a damp rock shelf']

        if room_type == 'forest':
            self.room_key = random.choice(forest)
        elif room_type == 'sewer':
            self.room_key = random.choice(sewer)
        elif room_type == 'cave':
            self.room_key = random.choice(cave)

    def get_exit_type(self):
        exit_types = ['stairs', 'door', 'portal']
        self.exit_type = random.choice(exit_types)

    def get_exit_key(self):
        room_key = self.room_key
        if room_key == 'forest':
        elif room_key == 'sewer':
        elif room_key == 'cave':
