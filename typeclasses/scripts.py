from evennia import DefaultScript
from evennia.utils.utils import lazy_property

from mobs.mob_spawn_handler import MobSpawnHandler

class Script(DefaultScript):
    @lazy_property
    def spawn(self):
        return MobSpawnHandler(self)
