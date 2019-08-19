from evennia import DefaultObject

class Object(DefaultObject):
    pass

class ObjHands(Object):
    def return_appearance(self, looker, **kwargs):
        looker.msg(f"You see nothing spectacular about your {self.key}.")

class Staves(Object):
    def at_object_creation(self):
        self.attributes.add('wieldable', 2)
