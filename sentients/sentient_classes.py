MERCHANT = {
    'prototype_key': 'merchant',
    'key': 'merchant',
    'typeclass': 'characters.characters.Character',
    'tags': ('merchant', 'sentient_class'),
    'stock': {}
}

BASIC_SUPPLIES = {
    'prototype_parent': 'merchant',
    'key': 'basic supplies merchant',
    'stock': {'crudely_made_torch': 10, 'foul_smelling_bait': 100}
}

static_sentients = {
    'hoff': {
        'key': "Hoff",
        'typeclass': "characters.characters.Character",
        'tags': ('merchant', 'sentient_class'),
        'attributes': [('stock', {})]
    }
}

# Critters
rat = {
    'adj1': ['vicious', 'slick-coated', 'large', 'red-maned', 'filthy', 'feral', 'matted', 
            'disheveled'],
    'adj2': ['black', 'yellow', 'pale-white'],
    'desc': "You see a 5 foot tall rat standing before you. It looks hungry.",
    'noun': 'rat',
    'health': 100,
    'base_difficulty': 0
}

spider = {
    'adj1': ['vicious', 'slick-coated', 'large', 'red-maned', 'filthy', 'feral'],
    'adj2': ['black', 'yellow', 'pale-white'],
    'desc': "You see a spider, much larger than a domestic one. This spider is about 4 feet tall.",
    'noun': 'spider',
    'health': 100,
    'base_difficulty': 0
}

snake = {
    'adj1': ['vicious', 'large', 'filthy', 'feral'],
    'adj2': ['black', 'yellow', 'pale-white', 'green', 'emerald', 'jade', 'ruby'],
    'desc': "You see a 5 foot tall snake, poised to strike anything that comes within its reach.",
    'noun': 'snake',
    'health': 100,
    'base_difficulty': 0
}

# Humanoids
skeleton = {
    'adj1': ['fragile', 'creaking', 'groaning', 'shambling', 'filthy', 'disheveled'],
    'adj2': ['black', 'yellowed', 'pale-white', 'moss-coated', 'moss-covered', 'soil-stained'],
    'desc': "The bones of what was once a human have been reanimated.",
    'noun': 'skeleton',
    'health': 100,
    'base_difficulty': 0
}

zombie = {
    'adj1': ['shambling', 'rotting', 'putrid', 'decomposing', 'filthy', 'disheveled'],
    'adj2': ['black', 'yellow', 'pale-white'],
    'desc': "You see the rotting corpse of a human, but it's still alive!",
    'noun': 'zombie',
    'health': 100,
    'base_difficulty': 0
}

# Magical
daemon_animus = {
    'adj1': ['shimmering', 'pulsing', 'luminescent'],
    'desc': ("You behold a creature conjured from a powerful ancient ritual. "
            "Its transparent form resembles a sheet of silk draped over a human. "
            "Light passing through this creature becomes distorted by time and space itself. "
            "Pulsing colors escape this unnatural entity, shimmering with magic."),
    'noun': 'daemon animus',
    'health': 100,
    'base_difficulty': 0
}

# Zone Spawn Pools
sewer = {'rat': rat, 'spider': spider, 'snake': snake}

graveyard = {'skeleton': skeleton, 'zombie': zombie}
