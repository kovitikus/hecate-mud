from evennia import DefaultObject
from evennia.utils import create
from evennia.utils import logger
from world.generic_str import article

class Object(DefaultObject):
    pass

class ObjHands(Object):
    def return_appearance(self, looker, **kwargs):
        looker.msg(f"You see nothing spectacular about your {self.key}.")

class Staves(Object):
    def at_object_creation(self):
        self.attributes.add('wieldable', 2)
