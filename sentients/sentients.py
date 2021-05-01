MERCHANT = {
    'prototype_key': 'merchant',
    'key': 'merchant',
    'typeclass': 'characters.characters.Character',
    'tags': ('merchant', 'sentients'),
    'stock': {}
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
