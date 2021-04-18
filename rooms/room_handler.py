from evennia import GLOBAL_SCRIPTS
from evennia.settings_default import TIME_ZONE
from evennia.utils.create import create_script
from evennia import search_script

class RoomHandler:
    def __init__(self, owner):
        self.owner = owner
        self.zone_ledger = GLOBAL_SCRIPTS.zone_ledger
    
    def set_room_occupied(self, occupant):
        owner = self.owner
        zone_ledger = self.zone_ledger
        if not owner.tags.get('occupied', category='rooms'):
            owner.tags.add('occupied', category='rooms')

        # Decide the unique identifier which represents the entire zone.
        if owner.tags.get(category='instance_id'):
            uid = owner.tags.get(category='instance_id')
        elif owner.tags.get(category='zone_id'):
            uid = owner.tags.get(category='zone_id')
        else:
            uid = None

        if uid is not None:
            # If this zone isn't already on the ledger, add as the uid.
            if not zone_ledger.attributes.has(uid):
                zone_ledger.attributes.add(uid, {'mobs': [], 'occupants': []})

                # The first time this zone is added to the ledger, generate a script to track mob spawn.
                mob_spawn_script = create_script(typeclass='typeclasses.scripts.Script', 
                                key=uid, persistent=True, autostart=True)
                mob_spawn_script.spawn.start_spawner() # Initiate the MobSpawnHandler

            # Zone is being tracked, add the new occupant
            zone_ledger_uid = zone_ledger.attributes.get(uid)
            zone_occupants = list(zone_ledger_uid['occupants'])
            if occupant not in zone_occupants:
                zone_ledger_uid['occupants'].append(occupant)

    def set_room_vacant(self, occupant):
        owner = self.owner
        zone_ledger = self.zone_ledger
        empty_room = False
        empty_zone = False

        for obj in self.owner.contents_get():
            if obj.has_account:
                empty_room = False
            else:
                empty_room = True
        if empty_room and owner.tags.get('occupied', category='rooms'):
            owner.tags.remove('occupied', category='rooms')

        # Generate the unique identifier for this room, which represents the entire zone.
        if owner.tags.get(category='instance_id'):
            uid = owner.tags.get(category='instance_id')
        elif owner.tags.get(category='zone_id'):
            uid = owner.tags.get(category='zone_id')
        else:
            uid = None

        if uid is not None:
            # Remove the occupant from the zone ledger.
            zone_ledger_uid = zone_ledger.attributes.get(uid)
            zone_occupant_list = list(zone_ledger_uid['occupants'])
            if occupant in zone_occupant_list:
                zone_ledger_uid['occupants'].remove(occupant)
            zone_occupant_count = len(zone_ledger_uid['occupants'])

            # Check if the zone is empty.
            if zone_occupant_count == 0:
                empty_zone = True
            if empty_zone:
                self.zone_ledger.attributes.remove(uid)

                # Clean up the MobSpawner script.
                spawn_script = search_script(uid)[0]
                spawn_script.delete()
