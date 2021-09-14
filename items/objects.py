from evennia import DefaultObject
from evennia import TICKER_HANDLER as tickerhandler
from evennia.utils.utils import inherits_from

from misc import coin

class Object(DefaultObject):
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
        self.tags.add('coin', category='groupable')
        self.tags.add('coin', category='currency')
        self.attributes.add('coin', coin.create_coin_dict())
    def return_appearance(self, looker, **kwargs):
        if self.attributes.has('coin'):
            coin_str = coin.positive_coin_types_to_string(self.db.coin)
            looker.msg(f"You see {self.get_display_name(looker)} worth {coin_str}.")

class InventoryContainer(Container):
    def at_object_creation(self):
        self.tags.add('inventory_container', category='container')
        self.attributes.add('max_slots', 50)

class InventoryGroup(Object):
    # Grouping category for objects that have unique attributes and must be preserved.
    # Only accepts objects tagged with ('inventory', category='groupable').
    # Objects added to this group are stored in the contents of the group object.
    # Objects removed from this group are pulled from the contents of the group object.
    def at_object_creation(self):
        self.attributes.add('quantity', 0)
        self.tags.add('inventory', category='groupable')
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
        self.tags.add('inventory', category='groupable')

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
            room.msg_contents(f"{held_by.name}'s {self.name} dies out and it collapses into a tiny pile of ash.",
                exclude=held_by)
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
