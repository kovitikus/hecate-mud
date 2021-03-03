import random

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
        self.rooms_list = []

        for _ in range(1, room_qty):
            room_key = self.generate_room_key()
            self.rooms_list.append(create_object(typeclass="typeclasses.rooms.Room", key=room_key))

        # Generate the exits for each room by tracking the current room and the previous room.


    def generate_room_key(self):
        room_type_list = ['forest', 'sewer', 'cave']
        room_type = random.choice(room_type_list)

        forest = ['a sacred grove of ancient wood', 'a sparsely-populated fledgling forest', 'a cluster of conifer trees']
        sewer = ['a poorly-maintained sewage tunnel', 'a sewer tunnel constructed of ancient brick', 'a wide walkway along sewage']
        cave = ['an uncertain rock bridge', 'a wide opening between', 'a damp rock shelf']

        if room_type == 'forest':
            room_key = random.choice(forest)
        elif room_type == 'sewer':
            room_key = random.choice(sewer)
        elif room_type == 'cave':
            room_key = random.choice(cave)
        
        return room_key
