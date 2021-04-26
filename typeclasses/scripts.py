from evennia import DefaultScript
from evennia.utils.utils import lazy_property

from rooms.spawn_handler import SpawnHandler

class Script(DefaultScript):
    @lazy_property
    def spawn(self):
        return SpawnHandler(self)
