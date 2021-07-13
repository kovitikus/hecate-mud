static_zones = {
    'darkshire': [
        { # Encampment
            'coords': {'x': 0, 'y': 0},
            'exits': ['n'], 
            'key': "a makeshift encampment"
        },
        { # Main Gate
            'coords': {'x': 0, 'y': -1},
            'exits': ['n', 's'],
            'key': "a main gate"
        },
        { # Town Square - South
            'coords': {'x': 0, 'y': -2},
            'exits': ['n', 'ne', 'e', 's', 'w', 'nw'],
            'key': "a town square"
        },
        { # Town Square - Southwest
            'coords': {'x': -1, 'y': -2},
            'exits': ['n', 'ne', 'e'],
            'key': "a town square"
        },
        { # Town Square - Southeast
            'coords': {'x': 1, 'y': -2},
            'exits': ['n', 'w', 'nw'],
            'key': "a town square"
        },
        { # Town Square - Middle
            'coords': {'x': 0, 'y': -3},
            'exits': ['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw'],
            'key': "the center of a town square"
        },
        { # Town Square - West
            'coords': {'x': -1, 'y': -3},
            'exits': ['n', 'ne', 'e', 'se', 's'],
            'key': "a town square"
        },
        { # Town Square - East
            'coords': {'x': 1, 'y': -3},
            'exits': ['n', 's', 'sw', 'w', 'nw'],
            'key': "a town square"
        },
        { # Town Square - North
            'coords': {'x': 0, 'y': -4},
            'exits': ['e', 'se', 's', 'sw', 'w'],
            'key': "a town square"
        },
        { # Town Square - Northwest
            'coords': {'x': -1, 'y': -4},
            'exits': ['e', 'se', 's'],
            'key': "a town square"
        },
        { # Town Square - Northeast
            'coords': {'x': 1, 'y': -4},
            'exits': ['s', 'sw', 'w'],
            'key': "a town square"
        }
    ]
}
