from evennia import DefaultScript
from evennia.utils.search import search_object_by_tag
from evennia.utils.utils import lazy_property

from rooms.spawn_handler import SpawnHandler

class Script(DefaultScript):
    @lazy_property
    def spawn(self):
        return SpawnHandler(self)

class TrashCollector(DefaultScript):
    def at_script_creation(self):
        self.interval = 86_400 # 24 hours

    def at_repeat(self):
        trash_bin = search_object_by_tag(key='trash_bin', category='rooms')[0]
        trash_bin.room.empty_trash()
