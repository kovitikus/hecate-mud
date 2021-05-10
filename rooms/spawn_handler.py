import inflect, random

from evennia.utils.search import search_object_by_tag
from evennia.utils.create import create_object
from evennia.utils import utils

_INFLECT = inflect.engine()

class SpawnHandler:
    def __init__(self, owner):
        """
        This handler's owner is the zone_script, created by the RoomHandler 
        and stored on the zone_ledger. The zone_script's key is a unique identifier, used to 
        reference it on the zone_ledger. The zone_script represents the zone as a whole and 
        tracks entities within it, as well as zone specific information. The SpawnHandler 
        lives on the zone_script and is a centralized mechanism that handles all spawn for the zone.

        The room list and the zone_type are both set on the zone_script, within the RoomHandler.

        The pool of sentients that spawn in this zone is set in the sentients.py module.

        This module spawns objects that are throw-aways. These objects have their default home
        designated as the black_hole room, which automatically deletes any entity that enters it.
        """
        self.owner = owner
        self.zone_rooms = list(self.owner.attributes.get('rooms'))
        zone_type = self.owner.tags.get(category='zone_type')
        self.sentient_pool = utils.variable_from_module("sentients.sentients", variable=zone_type)
        self.black_hole = search_object_by_tag(key='black_hole', category='rooms')[0]
    
    def start_spawner(self):
        """
        This method is called upon from outside of the handler, within the RoomHandler, during the
        zone_script's initial setup procedures.

        The basic instructions for managing spawning are set within this method by calling upon 
        other handler methods that gather and create data nessecary for a mob to finally be spawned.
        """
        owner = self.owner
        if owner is None:
            return
        start_spawning = True
        occupant_count = len(owner.attributes.get('occupants', []))
        sentient_count = len(owner.attributes.get('sentients', []))

        if sentient_count >= (occupant_count * 2): # 2 hostile sentients spawned per character.
            start_spawning = False

        if start_spawning == True:
            self._find_target()
            self._target_rep()
            self._pick_spawn_room()
            self._pick_sentient()
            self._generate_sentient_key()
            self._spawn_sentient()
            self._idle_spawner()
        elif start_spawning == False:
            self._idle_spawner()

    def _idle_spawner(self):
        """
        This method is called when it is time for the spawning to cease. It then attempts to start
        spawning again once the wait period is over.
        """
        utils.delay(30, self.start_spawner)

    def _find_target(self):
        """
        Grabs the list of current players in the zone and randomly chooses a character to target.

        The target of the spawn determines the difficulty and type of spawn.

        TODO: This desperately needs to be constrained by how many mobs are already targetting
        the current player. Right now, it's set up so there's a max amount of mobs in the zone
        based on the amount of occupants, but theoretically all mobs could end up targetting a
        single player.
        """
        self.target = random.choice(self.owner.attributes.get('occupants'))
    
    def _target_rep(self):
        """
        Here we'd normally check what reputation the target character has for this zone.
        The rep determines the difficulty and types of sentients that can spawn.
        Tier 1 rep is anything from 1-100, tier 2 101-200, etc
        """
        self.target_rep = 20

    def _pick_spawn_room(self):
        """
        Normally this would be some sort of algorithm to find a nearby room (0 to 4 room distance)
        from the target's current location, but for now it's the target's current location.
        """
        self.spawn_room = self.target.location

    def _pick_sentient(self):
        """
        The sentient_pool variable is generated upon the initilization of this module.
        A static pool of sentients are set within sentients.py
        Only sentients with a base_difficulty less than the target's reputation are selected.
        """
        sentient_pool = self.sentient_pool
        sentients = []
        for k in sentient_pool.keys():
            if sentient_pool[k].get('base_difficulty') < self.target_rep:
                sentients.append(sentient_pool[k])
        self.sentient = random.choice(sentients)

    def _generate_sentient_key(self):
        """
        Randomly pulls from the lists of adjectives on the sentient's dictionary.
        Generates a random key for the sentient.
        """
        noun = self.sentient.get('noun')
        adjs = []
        num = 1

        while (f"adj{num}") in self.sentient:
            if random.random() < 0.5:
                adj = random.choice(self.sentient[f"adj{num}"])
                adjs.append(adj)
            num += 1

        self.sentient_key = _INFLECT.an(f"{' '.join(adjs)} {noun}").strip()

    def _spawn_sentient(self):
        """
        Creates the sentient object and spawns it in the predetermined location.
        """
        sentient = create_object(typeclass='characters.characters.Character', key=self.sentient_key,
                            location=self.spawn_room, home=self.black_hole, 
                            tags=[(self.sentient.get('noun'), 'sentients')])
        self.spawn_room.msg_contents(f"{self.sentient_key} has appeared from the shadows.")
        self.owner.db.sentients.append(sentient)
