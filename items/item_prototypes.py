from evennia.utils.utils import random
from evennia.utils.search import search_object_by_tag

FOOD = {
    'prototype_key': 'food',
    'prototype_desc': 'Food items.',
    'prototype_tags': 'food',
    'typeclass': 'items.objects.Object',
    'tags': ('food', 'consumable')
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

DRINK = {
    'prototype_key': 'drink',
    'prototype_desc': 'Drink items.',
    'prototype_tags': 'drink',
    'typeclass': 'items.objects.Object',
    'tags': ('drink', 'consumable')
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

LIGHTING = {
    'prototype_key': 'lighting',
    'key': 'lighting',
    'typeclass': 'items.objects.Lighting'
}

TORCH = {
    'prototype_parent': 'lighting',
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

BAIT = {
    'prototype_key': 'bait',
    'prototype_desc': 'Fishing bait',
    'prototype_tags': 'bait',
    'typeclass': 'items.objects.Object',
    'tags': ('bait', 'fishing')
}

FOUL_SMELLING_BAIT = {
    'prototype_parent': 'bait',
    'prototype_key': 'foul-smelling bait',
    'key': 'foul-smelling bait',
    'lure': 1,
    'price': {'plat': 0, 'gold': 0, 'silver': 0, 'copper': 2}
}

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

# Bags
# Satchels
# Sacks
# Backpacks
