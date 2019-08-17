from evennia import DefaultObject

class Object(DefaultObject):
    pass

class ObjHands(Object):
    pass

class Stave(Object):
    def at_object_creation(self):
        self.attributes.add('wieldable', 2)
