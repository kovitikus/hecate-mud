temporary_zones =  {
    'forest': {
        'room_keys': [
            'a sacred grove of ancient wood', 'a sparsely-populated fledgling forest', 
                'a cluster of conifer trees'
        ]
    },
    'sewer': {
        'room_keys': [
            'a poorly-maintained sewage tunnel', 'a sewer tunnel constructed of ancient brick',
            'a wide walkway along sewage'
        ]
    },
    'cave': {
        'room_keys': [
            'an uncertain rock bridge', 'a wide opening between', 'a damp rock shelf'
        ]
    },
    'alley': {
        'room_keys': [
            'a dark alleyway', 'a filthy alleyway', 'a narrow alleyway'
        ]
    }
}
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
    ],
    'testing_zone': [
        { # Hecate's Haven
            'coords': {'x': 0, 'y': 0},
            'exits': ['n', 'e', 's', 'w'], 
            'key': "Hecate's Haven",
            'desc': ("You are in a well-constructed room with walls made of red granite rock, "
                "masterfully crafted from various shapes. Aisles, featuring a worn-in deep crimson "
                "carpet, connect all four exits to the center of the room. Four large round "
                "sturdy oak tables, surrounded by various chairs, decorate the northern half of "
                "room. Dominating the southwest corner of the room is a well-worn heavy oak bar "
                "that runs from the western wall into a smooth-cornered turn to end against "
                "the southern wall and is surrounded by stools. "
                "In the southeast quarter, a lounge features a polished large black harpsichord "
                "tucked into the corner, adjacent to a raised limestone platform serving as a "
                "stage. Along the southern half of the middle aisle and against the eastern wall "
                "rests a heavily padded L-shaped couch. Just in front of the couch sits a "
                "low-lying table."),
            'static_sentients': ['hoff'],
            'tags': [('hecates_haven', 'rooms')]
        },
        { # Shopper's Paradise
            'coords': {'x': -1, 'y': 0},
            'exits': ['e', 's'], 
            'key': "Shopper's Paradise",
            'desc': ("You are in a room stuffed to the ceiling with ridiculous amounts of "
                "merchandise. Running parallel against the western wall stands a magnificent "
                "translucent ruby counter, covered in racks and jars that house a plethora of "
                "curious wonders. Surrounding you are shelves and various containers filled with "
                "an assortment of objects and supplies. Volund, the proprietor of this "
                "establishment, appears busy with obsessively sorting and counting his inventory.")
        },
        { # Back Alley
            'coords': {'x': -1, 'y': 1},
            'exits': ['n', 'e'], 
            'key': "a dark alley behind a shop",
            'desc': ("You are in a dark and dirty back alley. Discarded trash is strewn about. "
                "In the southwest corner you see a mucky ladder leading down into a sewer, "
                "emenating a vile stench to through-out the alley. A few belligerent thugs are "
                "causing a ruckus halfway down the alley.")
        },
        { # Training Yard
            'coords': {'x': 0, 'y': 1},
            'exits': ['n', 'e', 'w'], 
            'key': "a training yard",
            'desc': ("You are at a training yard paved with cobblestones as walkways and dirt for "
                "fighting on. A thin layer of sand covers everything here. A never-ending supply "
                "of slaves are locked up in a cage against the southern wall. Several of the "
                "slaves are shackled to the southern wall, ready to fight and die. Benches run "
                "under an ivy-covered pergola along the northern wall. Combatants of various skill "
                "levels and weapons train here under the hot sun, watched over by the "
                "Doctore Oenomaus and several other trainers; each a master of different weapons.")
        },
        { # Apothecary's Shop
            'coords': {'x': 1, 'y': 1},
            'exits': ['n', 'w'], 
            'key': "Apothecary's Shop",
            'desc': ("You are amongst a vast array of plants, spices, minerals, and animal "
                "products. Behind a counter crafted from flowery vines stands Kerra the apothecary. "
                "North of the counter are three rows of various plants. All along the southern wall "
                "hangs shelves that house a multitude of jars, each containing some form of animal "
                "product. The northwestern corner of the room is stacked high with spices, "
                "minerals, and cured plants. Various incense burners are hanging from the ceiling, "
                "filling the room with a sickly-sweet aroma that mixes with an earthy scent.")
        },
        { # Kitchen
            'coords': {'x': 1, 'y': 0},
            'exits': ['s', 'w'], 
            'key': "a large noisy kitchen",
            'desc': ("You are inside a large noisy kitchen lined with white ceramic tiles. Busy "
                "people are hurriedly completing their tasks whilst communicating loudly. Pots and "
                "pans are hanging on hooks all along the walls. Four large ovens are stacked in a "
                "set of two against the northeast wall. A double sink is set in both the southeast "
                "and northwest corners of the room. Straight down the middle of the room rests a "
                "solid steel island, covered in various items being prepared. Ten stove-top burners "
                "line the eastern wall. Against the northern wall sets various bags of grain, rice, "
                "flour, and sugar. A whole cow hangs from the ceiling in the southwest corner, "
                "ready to be butchered.")
        },
        { # Road
            'coords': {'x': 0, 'y': -1},
            'exits': ['e', 's', 'w'], 
            'key': "a bustling cobblestone street",
            'desc': ("You are surrounded by large swarths of people in every direction. Centered "
                "in the middle of the street is a towering bronze statue of 10 feet; featuring a "
                "heavily armored knight plunging his bastard sword into the chest of a kneeling "
                "opponent, red liquid continuously spurts out from the statue’s chest and splashes "
                "into a basin built into the foundation. Surrounding the statue are ornate marble "
                "benches, each about 8 feet in length. Above the inn’s doorway hangs a glass "
                "mosaic street lamp set alight by burning oil. Moving amongst the crowd are people "
                "from all walks of life; from peasants, prostitutes, and workers to lords, ladies, "
                "scholars, priests, knights, and hired guards.")
        },
    ]
}
