from evennia import DefaultObject
from evennia.utils import create
from evennia.utils import logger
from evennia.utils import ansi
from evennia.utils.utils import inherits_from
from world.generic_str import article

class Object(DefaultObject):
    def get_numbered_name(self, count, looker, **kwargs):
        """
        Return the numbered (singular, plural) forms of this object's key. This is by default called
        by return_appearance and is used for grouping multiple same-named of this object. Note that
        this will be called on *every* member of a group even though the plural name will be only
        shown once. Also the singular display version, such as 'an apple', 'a tree' is determined
        from this method.
        Args:
            count (int): Number of objects of this type
            looker (Object): Onlooker. Not used by default.
        Kwargs:
            key (str): Optional key to pluralize, if given, use this instead of the object's key.
        Returns:
            singular (str): The singular form to display.
            plural (str): The determined plural form of the key, including the count.
        """
        key = kwargs.get("key", self.key)
        key = ansi.ANSIString(key)  # this is needed to allow inflection of colored names
        singular = key
        plural = key
        return singular, plural
    pass

class Staves(Object):
    def at_object_creation(self):
        self.attributes.add('wieldable', 2)
        self.attributes.add('skillset', 'staves')
        self.tags.add('staves', category='skillset')

class Swords(Object):
    def at_object_creation(self):
        self.attributes.add('wieldable', 1)
        self.attributes.add('skillset', 'swords')
        self.tags.add('swords', category='skillset')

class OffHand(Object):
    def at_object_creation(self):
        self.attributes.add('wieldable', 1)

class Shields(OffHand):
    def at_object_creation(self):
        self.attributes.add('skillset', 'shields')
        self.tags.add('shields', category='skillset')

class Chest(Object):
    def at_object_creation(self):
        self.tags.add('chest', category='equipment')

class Container(Object):
    pass

class InventoryContainer(Container):
    def at_object_creation(self):
        self.tags.add('inventory_container', category='container')
        self.attributes.add('max_slots', 50)

class Lighting(Object):
    pass

class Torch(Lighting):
    def at_object_creation(self):
        self.attributes.add('fuel', 100)
        # Torches burn at the rate of 10 fuel per minute, or 5 fuel every 30 seconds.

    def ignite(self, lighter):
        room, held_by = self.find_location()
        if held_by == 'character':
            lighter.msg(f"You light {self.name}, igniting it.")
            room.msg_contents(f"{lighter.get_display_name(self)} lights {self.name}, igniting it.", exclude=lighter)
        elif held_by == 'room':
            room.msg_contents(f"{lighter.get_display_name(self)} lights {self.name}, igniting it.", exclude=lighter)

    def find_location(self):
        #Check to see if the torch is in the hands (inventory) of player
        # or if the torch is in a a room.
        here = self.location
        held_by = None
        room = None

        if inherits_from(here, 'typeclasses.characters.Character'):
            held_by = 'character'
            room = here.location
        elif inherits_from(here, 'typeclasses.rooms.Room'):
            held_by = 'room'
            room = here
        return room, held_by