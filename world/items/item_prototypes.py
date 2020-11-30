from evennia.utils.utils import random

FOOD = {
    'prototype_key': 'food',
    'prototype_desc': 'Food items.',
    'prototype_tags': 'food',
    'typeclass': 'typeclasses.objects.Object',
    'tags': ('food', 'consumable')
}

DRINK = {
    'prototype_key': 'drink',
    'prototype_desc': 'Drink items.',
    'prototype_tags': 'drink',
    'typeclass': 'typeclasses.objects.Object',
    'tags': ('drink', 'consumable')
}

LIGHTING = {
    'prototype_key': 'lighting',
    'key': 'lighting',
    'typeclass': 'typeclasses.objects.Lighting'
}

INVENTORY_CONTAINER = {
    'prototype_key': 'inventory_container',
    'key': 'inventory_container',
    'typeclass': 'typeclasses.objects.InventoryContainer'
}

BAIT = {
    'prototype_key': 'bait',
    'prototype_desc': 'Fishing bait',
    'prototype_tags': 'bait',
    'typeclass': 'typeclasses.objects.Object',
    'tags': ('bait', 'fishing')
}

ITEMS = {
    'raspbery_cake': {
        'prototype_parent': 'food',
        'key': 'raspberry cake',
        'price': 10,
        'hunger': 10
    },

    'beef_steak': {
        'prototype_parent': 'food',
        'key': 'beef steak',
        'price': 50,
        'hunger': 25
    },

    'millet_porridge': {
        'prototype_parent': 'food',
        'key': 'millet porridge',
        'price': 4,
        'hunger': 15
    },

    'barley_porridge': {
        'prototype_parent': 'food',
        'key': 'barley porridge',
        'price': 4,
        'hunger': 15
    },

    'stewed_beetroot': {
        'prototype_parent': 'food',
        'key': 'stewed beetroot',
        'price': 4,
        'hunger': 15
    },

    'boiled_mutton_and_peas': {
        'prototype_parent': 'food',
        'key': 'boiled mutton and peas',
        'price': 11,
        'hunger': 25
    },

    'black_tea': {
        'prototype_parent': 'drink',
        'key': 'black tea',
        'price': 3,
        'thirst': 5
    },

    'water': {
        'prototype_parent': 'drink',
        'key': 'water',
        'price': 1,
        'thirst': 5
    },

    'torch': {
        'prototype_parent': 'lighting',
        'key': 'torch',
        'typeclass': 'typeclasses.objects.Torch'
    },

    'crudely_made_torch': {
        'prototype_parent': 'lighting',
        'prototype_key': 'CRUDELY_MADE_TORCH',
        'key': 'crudely-made torch',
        'typeclass': 'typeclasses.objects.Torch',
        'price': 10,
        'fuel': 90,
        'burn_rate': 30
    },

    'inventory_bag': {
        'prototype_parent': 'inventory_container',
        'key': lambda: generate_random_bag_key()
    },

    'foul_smelling_bait': {
        'prototype_parent': 'bait',
        'prototype_key': 'FOUL_SMELLING_BAIT',
        'key': 'foul-smelling bait',
        'lure': 1,
        'price': 2,
    }
}

def generate_random_bag_key():
    color = ('red', 'blue', 'green', 'yellow', 'black')
    adjective = ('tattered', 'worn', 'pristine', 'well-crafted', 'frayed')
    # a tattered red bag
    # a pristine yellow bag
    bag_key = f"a {random.choice(adjective)} {random.choice(color)} bag"
    return bag_key

# Bags
# Satchels
# Sacks
# Backpacks