from evennia.utils.utils import lazy_property

from characters.characters import Character
from sentients.sentient_handler import SentientHandler
from sentients.merchant_handler import MerchantHandler


class Sentient(Character):
    @lazy_property
    def sentient(self):
        return SentientHandler(self)

    def at_object_creation(self):
        super().at_object_creation()

    def on_death(self):
        name = self.name
        location = self.location
        okay = self.delete()
        if not okay:
            location.msg_contents(f"\nERROR: {name} not deleted, probably because delete() " 
                                    "returned False.")
        else:
            location.msg_contents(f"{name} breathes a final breath and expires.")
            location.spawn.spawn_timer()

class Merchant(Sentient):
    @lazy_property
    def merch(self):
        return MerchantHandler(self)
    
    def at_object_creation(self):
        self.attributes.add('stock', [])

MERCHANT = {
    'prototype_key': 'merchant',
    'key': 'merchant',
    'typeclass': 'characters.characters.Merchant',
    'tags': ('merchant', 'sentient')
}

BASIC_SUPPLIES = {
    'prototype_parent': 'merchant',
    'key': 'basic supplies merchant',
    'stock': {'crudely_made_torch': 10, 'foul_smelling_bait': 100}
}

sewer = {
    'rat': {
        'adj1': ['vicious', 'slick-coated', 'large', 'red-maned', 'filthy', 'feral'],
        'adj2': ['black', 'yellow', 'pale-white', 'black'],
        'noun': 'rat',
        'health': 100,
        'base_difficulty': 0,
    }
}
