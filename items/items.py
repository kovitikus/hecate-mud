from evennia import DefaultObject
from evennia import TICKER_HANDLER as tickerhandler
from evennia.utils import create
from evennia.utils import logger
from evennia.utils import ansi
from evennia.utils.utils import inherits_from

from misc.generic_str import article
from misc import general_mechanics as gen_mec

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

class Coin(Object):
    def at_object_creation(self):
        self.tags.add('stackable')
        self.tags.add('quantity', category='stack')
        self.tags.add('coin', category='currency')
        self.attributes.add('coin', {'plat': 0, 'gold': 0, 'silver': 0, 'copper': 0})
    def return_appearance(self, looker, **kwargs):
        if self.attributes.has('coin'):
            currency = gen_mec.return_currency(self)
            looker.msg(f"You see {self.get_display_name(looker)} worth {currency}.")

class InventoryContainer(Container):
    def at_object_creation(self):
        self.tags.add('inventory_container', category='container')
        self.attributes.add('max_slots', 50)

class StackQuantity(Object):
    # Stacking objects which have no unique attributes, such as coin.
    # Only accepts objects tagged with ('quantity', category='stack').
    # Objects added to this stack are destroyed and a counter on the stack object is increased.
    # Objects removed from this stack are created and a counter on the stack object is decreased.
    def at_object_creation(self):
        self.attributes.add('quantity', 0)
    def return_appearance(self, looker, **kwargs):
        if self.attributes.has('coin'):
            currency = gen_mec.return_currency(self)
            looker.msg(f"You see {self.get_display_name(looker)} worth {currency}.")

class StackInventory(Object):
    # Stacking objects that have unique attributes and must be preserved.
    # Only accepts objects tagged with ('inventory', category='stack').
    # Objects added to this stack are stored in the contents of the stack object.
    # Objects removed from this stack are pulled from the contents of the stack object.
    def at_object_creation(self):
        self.attributes.add('quantity', 0)
    def return_appearance(self, looker, **kwargs):
        inventory = self.contents
        msg = f"You see {self.get_display_name(looker)}.\n"
        msg = f"{msg}It consists of:\n"
        for i in inventory:
            msg = f"{msg}    {i.get_display_name(looker)}\n"
        looker.msg(msg)

class Lighting(Object):
    pass

class Torch(Lighting):
    def at_object_creation(self):
        self.attributes.add('fuel', 100)
        # Torches burn at the rate of 10 fuel per minute, or 5 fuel every 30 seconds.

        self.tags.add('stackable')
        self.tags.add('inventory', category='stack')

    def ignite(self, lighter):
        room, held_by = self.find_location()
        
        lighter.msg(f"You light {self.name}, igniting it.")
        room.msg_contents(f"{lighter.get_display_name(self)} lights {self.name}, igniting it.", exclude=lighter)

        tickerhandler.add(30, self.on_burn_tick, persistent=True)

    def on_burn_tick(self):
        fuel = self.attributes.get('fuel')
        room, held_by = self.find_location()
        burn_rate = 25

        if fuel <= 0:
            self.death(room, held_by)
            return
        
        if inherits_from(held_by, "typeclasses.characters.Character"):
            held_by.msg(f"Your {self.name} flickers.")
            room.msg_contents(f"{held_by.name}'s {self.name} flickers.", exclude=held_by)
        else:
            room.msg_contents(f"{self.name} flickers.")
        self.db.fuel -= burn_rate
            

    def death(self, room, held_by):
        tickerhandler.remove(30, self.on_burn_tick, persistent=True)
        if inherits_from(held_by, "typeclasses.characters.Character"):
            held_by.msg(f"Your {self.name} torch dies out and it collapses into a tiny pile of ash.")
            room.msg_contents(f"{held_by.name}'s {self.name} dies out and it collapses into a tiny pile of ash.", exclude=held_by)
        else:
            room.msg_contents(f"{self.name} dies out and it collapses into a tiny pile of ash.")
        self.delete()



    def find_location(self):
        #Check to see if the torch is in the hands (inventory) of player
        # or if the torch is in a a room.
        held_by = self.location
        room = None

        if inherits_from(held_by, 'typeclasses.characters.Character'):
            room = held_by.location
        elif inherits_from(held_by, 'typeclasses.rooms.Room'):
            room = held_by
        return room, held_by
