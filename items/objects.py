from evennia import DefaultObject
from evennia import TICKER_HANDLER as tickerhandler
from evennia.utils import create
from evennia.utils import logger
from evennia.utils import ansi
from evennia.utils.utils import inherits_from, lazy_property

from characters.currency_handler import CurrencyHandler
from misc.generic_str import article

class Object(DefaultObject):
    @lazy_property
    def currency(self):
        return CurrencyHandler(self)

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
            coin_str = self.currency.positive_coin_types_to_string()
            looker.msg(f"You see {self.get_display_name(looker)} worth {coin_str}.")

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
            coin_str = self.currency.positive_coin_types_to_string()
            looker.msg(f"You see {self.get_display_name(looker)} worth {coin_str}.")

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
        
        if inherits_from(held_by, "characters.characters.Character"):
            held_by.msg(f"Your {self.name} flickers.")
            room.msg_contents(f"{held_by.name}'s {self.name} flickers.", exclude=held_by)
        else:
            room.msg_contents(f"{self.name} flickers.")
        self.db.fuel -= burn_rate
            

    def death(self, room, held_by):
        tickerhandler.remove(30, self.on_burn_tick, persistent=True)
        if inherits_from(held_by, "characters.characters.Character"):
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

        if inherits_from(held_by, 'characters.characters.Character'):
            room = held_by.location
        elif inherits_from(held_by, 'rooms.rooms.Room'):
            room = held_by
        return room, held_by
