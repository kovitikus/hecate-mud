import time

from evennia import GLOBAL_SCRIPTS
from evennia.utils import logger
from evennia.utils.create import create_script
from evennia.utils.search import search_object_by_tag

class RoomHandler:
    def __init__(self, owner):
        self.owner = owner

        # All zones are stored in a single dictionary attribute on the zone_ledger script.
        # This makes it possible to add other attributes, such as total number of occupied zones,
        # while also maintaining a curated dictionary of zones.
        if not GLOBAL_SCRIPTS.zone_ledger.attributes.has('zones'):
            GLOBAL_SCRIPTS.zone_ledger.attributes.add('zones', {})

#-------------
# Called by at_object_receive on the rooms.rooms.Room typeclass
    def set_room_occupied(self, occupant):
        owner = self.owner
        zones = GLOBAL_SCRIPTS.zone_ledger.db.zones
        uid = None

        if not owner.tags.get('occupied', category='rooms'):
            owner.tags.add('occupied', category='rooms')

        if owner.tags.get(category='zone_id'):
            uid = owner.tags.get(category='zone_id')

        if uid is not None:
            # Zone script doesn't exist. Generate a new one.
            if uid not in zones:
                zone_script = create_script(typeclass='typeclasses.scripts.Script', 
                                key=uid, persistent=True, autostart=True)
                zone_script.attributes.add('occupants', [])
                zone_script.attributes.add('rooms', [])
                zone_script.attributes.add('sentients', [])

                # Pass the room's zone_type to the zone_script.
                if owner.tags.get(category='zone_type'):
                    zone_type = owner.tags.get(category='zone_type')
                    zone_script.tags.add(zone_type, category='zone_type')

                # Spawn sentients.
                if owner.tags.get('has_spawn'):
                    zone_script.spawn.start_spawner()

                # Find and add all rooms for this zone.
                zone_objects_list = search_object_by_tag(key=uid, category='zone_id')
                zone_rooms = []
                for i in zone_objects_list:
                    if i.is_typeclass('rooms.rooms.Room'):
                        zone_rooms.append(i)
                zone_script.db.rooms = zone_rooms

                # Add a reference to the zone script to the ledger for later retrieval.
                zones[uid] = zone_script

            # Zone script exists. Update it.
            zone_script = zones.get(uid)
            if zone_script is not None:
                zone_occupants = list(zone_script.db.occupants)
                if occupant not in zone_occupants:
                    zone_script.db.occupants.append(occupant)

#-------------
# Called by at_object_leave on the rooms.rooms.Room typeclass
    def set_room_vacant(self, occupant, target_location):
        owner = self.owner
        zones = GLOBAL_SCRIPTS.zone_ledger.db.zones
        empty_room = False
        empty_zone = False
        static_zone = False

        # Check if this room is void of players.
        for obj in owner.contents_get():
            if obj.has_account:
                empty_room = False
            else:
                empty_room = True
        if empty_room and owner.tags.get('occupied', category='rooms'):
            owner.tags.remove('occupied', category='rooms')

        # Acquire this room's zone identifier.
        if owner.tags.get(category='zone_id'):
            uid = owner.tags.get(category='zone_id')
        else:
            uid = None

        # Acquire target location's zone identifier.
        if target_location.tags.get(category='zone_id'):
            target_location_uid = target_location.tags.get(category='zone_id')
        else:
            target_location_uid = None

        if uid is not None and uid != target_location_uid:
            if uid in zones:
                # Remove the occupant from the zone.
                zone_script = zones[uid]
                if zone_script is not None:
                    if zone_script.attributes.has('occupants'):
                        zone_occupant_list = list(zone_script.db.occupants)
                        if occupant in zone_occupant_list:
                            zone_script.db.occupants.remove(occupant)

                        if zone_script.tags.get('static_zone'):
                            static_zone = True

                        # Check if the zone is empty.
                        zone_occupant_count = len(zone_script.db.occupants)
                        if zone_occupant_count == 0:
                            empty_zone = True
                        if empty_zone and not static_zone:
                            del zones[uid]
                            zone_script.delete()

#----------------
# Black Hole Room Logic
    def black_hole(self, object):
        obj_name = object.name
        deleted = object.delete()
        if deleted:
            log_str = f"{obj_name} has been destroyed!"
            logger.log_file(log_str, filename='black_hole.log')

#-----------------
# Trash Bin Room Logic
    def obj_enter_trash(self, object):
        grace_period = 2_592_000 # seconds = 30 days
        now = time.time() # Current epoch time
        deletion_time = now + grace_period
        object.attributes.add('deletion_time', deletion_time)

        log_str = f"{object.name} pending deletion at {deletion_time} epoch time."
        logger.log_file(log_str, filename='trash_bin.log')
    
    def empty_trash(self):
        now = time.time()
        for obj in self.owner.contents:
            if obj.attributes.has('deletion_time'):
                deletion_time = obj.attributes.get('deletion_time')
                obj_name = obj.name
                if now >= deletion_time:
                    deleted = obj.delete()
                    if deleted:
                        log_str = f"{obj_name} has been destroyed!"
                        logger.log_file(log_str, filename='trash_bin.log')
