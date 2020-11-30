"""
CONSUMABLE CATEGORY
"""
# Food Category
FOOD = {
    'prototype_key': 'food',
    'prototype_desc': 'Food items.',
    'prototype_tags': 'food',
    'typeclass': 'typeclasses.objects.Object',
    'tags': ('food', 'consumable')
}

RASPBERRY_CAKE = {
    'prototype_parent': 'food',
    'key': 'raspberry cake',
    'price': 10,
    'hunger': 10
}

BEEF_STEAK = {
    'prototype_parent': 'food',
    'key': 'beef steak',
    'price': 50,
    'hunger': 25
}

# Drink Category
DRINK = {
    'prototype_key': 'drink',
    'prototype_desc': 'Drink items.',
    'prototype_tags': 'drink',
    'typeclass': 'typeclasses.objects.Object',
    'tags': ('drink', 'consumable')
}

BLACK_TEA = {
    'prototype_parent': 'drink',
    'key': 'black tea',
    'price': 3,
    'thirst': 5
}

WATER = {
    'prototype_parent': 'drink',
    'key': 'water',
    'price': 1,
    'thirst': 5
}

"""
LIGHTING CATEGORY
"""
LIGHTING = {
    'prototype_key': 'lighting',
    'key': 'lighting',
    'typeclass': 'typeclasses.objects.Lighting'
}

TORCH = {
    'prototype_parent': 'lighting',
    'key': 'torch',
    'typeclass': 'typeclasses.objects.Torch'
}



INVENTORY_CONTAINER = {
    'prototype_key': 'inventory_container',
    'key': 'inventory_container',
    'typeclass': 'typeclasses.objects.InventoryContainer'
}


INVENTORY_BAG = {
    'prototype_parent': 'inventory_container',
    'key': lambda: generate_random_bag_key()
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