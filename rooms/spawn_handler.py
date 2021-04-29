import inflect, random

from evennia.utils.search import search_object_by_tag
from evennia.utils.create import create_object
from evennia.utils import utils

_INFLECT = inflect.engine()

class SpawnHandler:
    def __init__(self, owner):
        """
        The owner is the zone script that represents the zone itself.
        The zone script allows a single spawn handler to exist, managing the zone as a whole.
        The name of the script is set as the same unique identifier of the zone on the ledger.
        """
        self.owner = owner
        self.zone_rooms = list(self.owner.attributes.get('rooms'))
        zone_type = self.owner.tags.get(category='zone_type')
        self.mob_pool = utils.variable_from_module("mobs.mobs", variable=zone_type)
        self.black_hole = search_object_by_tag(key='black_hole', category='rooms')[0]
    
    def start_spawner(self):
        owner = self.owner
        if owner is None:
            return
        start_spawning = True
        occupant_count = len(owner.attributes.get('occupants', []))
        mob_count = len(owner.attributes.get('mobs', []))

        if mob_count >= (occupant_count * 2): # 2 mobs spawned per character.
            start_spawning = False

        if start_spawning == True:
            self._find_target()
            self._target_rep()
            self._pick_spawn_room()
            self._pick_mob()
            self._generate_mob_key()
            self._spawn_mob()
            self._idle_spawner()
        elif start_spawning == False:
            self._idle_spawner()

    def _idle_spawner(self):
        utils.delay(30, self.start_spawner)

    def _find_target(self):
        self.target = random.choice(self.owner.attributes.get('occupants'))
    
    def _target_rep(self):
        # Here we'd normally check what reputation the target character has for this zone.
        # The rep determines the difficulty and types of mobs that can spawn.
        # Tier 1 rep is anything from 1-100, tier 2 101-200, etc
        self.target_rep = 20

    def _pick_spawn_room(self):
        # Normally this would be some sort of algorithm to find a nearby room (0 to 4 room distance)
        # from the target's current location, but for now it's the target's current location.
        self.spawn_room = self.target.location

    def _pick_mob(self):
        mob_pool = self.mob_pool
        mobs = []
        for k in mob_pool.keys():
            if mob_pool[k].get('base_difficulty') < self.target_rep:
                mobs.append(mob_pool[k])
        self.mob = random.choice(mobs)

    def _generate_mob_key(self):
        noun = self.mob.get('noun')
        adjs = []
        num = 1
        while (f"adj{num}") in self.mob:
            if random.random() < 0.5:
                adjs.append(random.choice(self.mob[f"adj{num}"]))
            num += 1
        self.mob_key = _INFLECT.an(f"{' '.join(adjs)} {noun}").strip()

    def _spawn_mob(self):
        mob = create_object(typeclass='characters.characters.Character', key=self.mob_key,
                            location=self.spawn_room, home=self.black_hole)
        self.spawn_room.msg_contents(f"{self.mob_key} has appeared from the shadows.")
        self.owner.db.mobs.append(mob)
