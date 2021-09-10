from evennia.utils.utils import random
from evennia.utils.search import search_object_by_tag

#==[Quantity Objects]==============================================================================#
"""
These are objects which have no individually unique attribute values. Such as fuel or hunger.

These objects my still include attributes unique to the type of object, but all spawned objects
are identical to each other.
"""
QUANTITY_OBJECT = {
    'prototype_key': 'quantity_object',
    'prototype_desc': 'Identical objects which have no unique individual attribute values.',
    'prototype_tags': 'quantity_object',
    'typeclass': 'items.objects.Object',
    'tags': [('quantity', 'groupable', None)],
    'attrs': [('quantity', 1, None, None)]
}

ROCK = {
    'prototype_parent': 'quantity_object',
    'prototype_key': 'rock',
    'key': 'a rock',
    'plural_key': 'rocks',
    'singular_key': 'a rock',
    'desc': 'A good way to get stoned.'
}

#==[Currency]======================================================================================#
COIN = {
    'prototype_key': 'coin',
    'prototype_desc': 'Coins such as platinum, gold, silver, and copper.',
    'prototype_tags': 'coin',
    'typeclass': 'items.objects.Coin',
}

PLAT_COIN = {
    'prototype_parent': 'coin',
    'prototype_key': 'plat_coin',
    'key': 'a platinum coin',
    'plural_key': 'platinum coins',
    'singular_key': 'platinum coin'
}

GOLD_COIN = {
    'prototype_parent': 'coin',
    'prototype_key': 'gold_coin',
    'key': 'a gold coin',
    'plural_key': 'gold coins',
    'singular_key': 'gold coin'
}

SILVER_COIN = {
    'prototype_parent': 'coin',
    'prototype_key': 'silver_coin',
    'key': 'a silver coin',
    'plural_key': 'silver coins',
    'singular_key': 'silver coin'
}

COPPER_COIN = {
    'prototype_parent': 'coin',
    'prototype_key': 'copper_coin',
    'key': 'a copper coin',
    'plural_key': 'copper coins',
    'singular_key': 'copper coin'
}

COIN_PILE = { # A mix of various coin types and values.
    'prototype_parent': 'coin',
    'prototype_key': 'coin_pile',
    'key': 'a pile of coins',
    'plural_key': 'a pile of coins',
    'singular_key': 'a pile of coins'
}

#==[Inventory Objects]=============================================================================#
"""
Inventory objects are objects that have unique properties that must be preserved when combining.
When grouped, these objects are added to the inventory of a pseudo-container object, typically
referred to as 'a pile of various items'.
"""
INVENTORY_OBJECT = {
    'prototype_key': 'inventory_object',
    'tags': [('inventory', 'groupable', None)]
}
#==[Food]==========================================================================================#

FOOD = {
    'prototype_parent': 'inventory_object',
    'prototype_key': 'food',
    'prototype_desc': 'Food items.',
    'prototype_tags': 'food',
    'typeclass': 'items.objects.Object',
    'tags': [('food', 'consumable', None)]
}

RASPBERRY_CAKE = {
    'prototype_parent': 'food',
    'key': 'raspberry cake',
    'price': {'plat': 0, 'gold': 0, 'silver': 0, 'copper': 10},
    'hunger': 10
}

BEEF_STEAK = {
    'prototype_parent': 'food',
    'key': 'beef steak',
    'price': {'plat': 0, 'gold': 0, 'silver': 0, 'copper': 50},
    'hunger': 25
}

MILLET_PORRIDGE = {
    'prototype_parent': 'food',
    'key': 'millet porridge',
    'price': {'plat': 0, 'gold': 0, 'silver': 0, 'copper': 4},
    'hunger': 15
}

BARLEY_PORRIDGE = {
    'prototype_parent': 'food',
    'key': 'barley porridge',
    'price': {'plat': 0, 'gold': 0, 'silver': 0, 'copper': 4},
    'hunger': 15
}

STEWED_BEETROOT = {
    'prototype_parent': 'food',
    'key': 'stewed beetroot',
    'price': {'plat': 0, 'gold': 0, 'silver': 0, 'copper': 4},
    'hunger': 15
}

BOILED_MUTTON_AND_PEAS = {
    'prototype_parent': 'food',
    'key': 'boiled mutton and peas',
    'price': {'plat': 0, 'gold': 0, 'silver': 0, 'copper': 11},
    'hunger': 25
}

#==[Drink]=========================================================================================#

DRINK = {
    'prototype_parent': 'inventory_object',
    'prototype_key': 'drink',
    'prototype_desc': 'Drink items.',
    'prototype_tags': 'drink',
    'typeclass': 'items.objects.Object',
    'tags': [('drink', 'consumable', None)]
}

BLACK_TEA = {
    'prototype_parent': 'drink',
    'key': 'black tea',
    'price': {'plat': 0, 'gold': 0, 'silver': 0, 'copper': 3},
    'thirst': 5
}

WATER = {
    'prototype_parent': 'drink',
    'key': 'water',
    'price': {'plat': 0, 'gold': 0, 'silver': 0, 'copper': 1},
    'thirst': 5
}

#==[Lighting]======================================================================================#

LIGHTING = {
    'prototype_key': 'lighting',
    'key': 'lighting',
    'typeclass': 'items.objects.Lighting'
}

TORCH = {
    'prototype_parent': ('lighting', 'inventory_object'),
    'key': 'torch',
    'typeclass': 'items.objects.Torch'
}

CRUDELY_MADE_TORCH = {
    'prototype_parent': 'lighting',
    'prototype_key': 'crudely-made torch',
    'key': 'crudely-made torch',
    'typeclass': 'items.objects.Torch',
    'price': {'plat': 0, 'gold': 0, 'silver': 0, 'copper': 10},
    'fuel': 90,
    'burn_rate': 30
}

#==[Containers]====================================================================================#

INVENTORY_CONTAINER = {
    'prototype_key': 'inventory_container',
    'key': 'inventory_container',
    'typeclass': 'items.objects.InventoryContainer'
}

INVENTORY_BAG = {
    'prototype_parent': 'inventory_container',
    'key': lambda: generate_random_bag_key(),
    'home': lambda: trash_bin_dbref()
}
# Bags
# Satchels
# Sacks
# Backpacks

#==[Misc]==========================================================================================#

BAIT = {
    'prototype_key': 'bait',
    'prototype_desc': 'Fishing bait',
    'prototype_tags': 'bait',
    'typeclass': 'items.objects.Object',
    'tags': [('bait', 'fishing', None)]
}

FOUL_SMELLING_BAIT = {
    'prototype_parent': 'bait',
    'prototype_key': 'foul-smelling bait',
    'key': 'foul-smelling bait',
    'lure': 1,
    'price': {'plat': 0, 'gold': 0, 'silver': 0, 'copper': 2}
}

#==[Helper Functions]==============================================================================#

def generate_random_bag_key():
    color = ('red', 'blue', 'green', 'yellow', 'black')
    adjective = ('tattered', 'worn', 'pristine', 'well-crafted', 'frayed')
    # a tattered red bag
    # a pristine yellow bag
    bag_key = f"a {random.choice(adjective)} {random.choice(color)} bag"
    return bag_key

def trash_bin_dbref():
    trash_bin = search_object_by_tag(key='trash_bin', category='rooms')[0]
    return trash_bin.dbref
