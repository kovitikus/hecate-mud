import inflect, random

from evennia.utils import utils

_INFLECT = inflect.engine()

class SpawnHandler:
    def __init__(self, owner):
        """
        The owner is the zone script that represents the zone itself.
        Right now this is just a blank script that lives nowhere.
        It only exists so that a single spawn handler can exist to manage the zone.
        Sorta makes the owner useless. Meh.
        The name of the script is set as the same unique identifier of the zone on the ledger.
        """
        self.owner = owner
        self.zone_rooms = list(self.owner.attributes.get('rooms'))
        zone_type = self.owner.attributes.get('zone_type')
        self.mob_pool = utils.variable_from_module("mobs.mobs", variable=zone_type)
    
    def start_spawner(self):
        occupant_count = len(self.owner.attributes.get('occupants'))
        mob_count = len(self.owner.attributes.get('mobs'))

        if occupant_count > 0 and mob_count < (occupant_count * 2): # 2 mobs spawned per character.
            self._find_target()
            self._target_rep()
            self._pick_mob()
            self._generate_mob_key()
        else:
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

    def _pick_mob(self):
        mobs = []
        for k, v in self.mob_pool:
            if self.mob_pool[k].get('difficulty') < self.target_rep:
                mobs.append(k)
        self.mob = random.choice(mobs)

    def _generate_mob_key(self):
        noun = self.mob_pool[self.mob].get('noun')
        adjs = []
        num = 1
        while (f"adj{num}") in self.mob_pool[self.mob]:
            if random.random() < 0.5:
                adjs.append(random.choice(self.mob_pool[self.mob][f"adj{num}"]))
            num += 1
        self.mob_key = _INFLECT.an(f"{' '.join(adjs)}{noun}").strip()
