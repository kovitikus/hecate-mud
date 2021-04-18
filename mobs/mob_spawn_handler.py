from evennia import utils
from evennia import GLOBAL_SCRIPTS
from evennia.prototypes.spawner import spawn

from misc import general_mechanics as gen_mec

class MobSpawnHandler:
    def __init__(self, owner):
        # The owner is the zone script that stores spawned mob data.
        self.owner = owner

        # This handler lives on the script that was generated the first time this zone was occupied.
        # The name of the script is set as the same unique identifier of the zone on the ledger.
        self.zone_ledger_uid = GLOBAL_SCRIPTS.zone_ledger.attributes.get(owner.key)
    
    def start_spawner(self):
        pass
