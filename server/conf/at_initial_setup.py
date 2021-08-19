from evennia.utils.create import create_object
from evennia.utils.search import search_object


"""
At_initial_setup module template

Custom at_initial_setup method. This allows you to hook special
modifications to the initial server startup process. Note that this
will only be run once - when the server starts up for the very first
time! It is called last in the startup process and can thus be used to
overload things that happened before it.

The module must contain a global function at_initial_setup().  This
will be called without arguments. Note that tracebacks in this module
will be QUIETLY ignored, so make sure to check it well to make sure it
does what you expect it to.

"""


def at_initial_setup():
    # Search by dbref to find the #1 superuser
    char1 = search_object('#1', use_dbref=True)[0]

    room = search_object('#2', use_dbref=True)[0]
    room.key = 'default_home'
    room.db.desc = ("This is the room where objects travel to when their home location isn\'t " 
                    "explicity set in the source code or by a builder, "
                    "and the object\'s current location is destroyed. "
                    "Character typeclasses are not allowed to enter this room in a move_to check.")

    # Black Hole
    black_hole = create_object(typeclass='rooms.rooms.Room', key='black_hole')
    black_hole.db.desc = ("The room where all objects go to die. It is the default home for "
                        "objects that are considered worthless. Any object entering this room is "
                        "automatically deleted via the at_object_receive method.")
    black_hole.tags.add('black_hole', category='rooms')

    # Statis Chamber
    statis_chamber = create_object(typeclass='rooms.rooms.Room', key='statis_chamber')
    statis_chamber.db.desc = ("This room holds objects indefinitely. It is the default home for "
                            "objects that are of significant value, unique, or otherwise should "
                            "not be destroyed for any reason.")
    statis_chamber.tags.add('statis_chamber', category='rooms')

    # Trash Bin
    trash_bin = create_object(typeclass='rooms.rooms.Room', key='trash_bin')
    trash_bin.db.desc = ("This room holds objects for 90 days, before being sent to black_hole. "
                            "It is the default home for objects of some value and the destination "
                            "of said objects when discarded by players.")
    trash_bin.tags.add('trash_bin', category='rooms')

    # Superuser's equipment generation must take place after the item rooms are generated.
    # The inventory container requires trash_bin to exist.
    char1.equip.generate_starting_equipment()

    # Create the superuser's home room.
    rm3 = create_object(typeclass='rooms.rooms.Room', key='Main Office')
    char1.home = rm3
    rm3.tags.add('main_office', category='ooc_room')
    char1.move_to(rm3, quiet=True, move_hooks=False)

    # Create the Common Room. This is where all portals will lead when entering public OOC areas.
    rm4 = create_object(typeclass='rooms.rooms.Room', key='Common Room')
    rm4.tags.add('common_room', category='ooc_room')
    rm4.tags.add(category='public_ooc')

    # Connect the main office and common room with exits.
    exit_rm3_rm4 = create_object(typeclass='travel.exits.Exit', key='a mahogany door', aliases = ['door', ], 
                                    location=rm3, destination=rm4, tags=[('door', 'exits'), ])
    exit_rm3_rm4.tags.add('n', category='card_dir')
    exit_rm3_rm4.tags.add(category='ooc_exit')

    exit_rm4_rm3 = create_object(typeclass='travel.exits.Exit', key='a mahogany door', aliases=['door', ],
                                    location=rm4, destination=rm3, tags=[('door', 'exits'), ])
    exit_rm4_rm3.tags.add('s', category='card_dir')
    exit_rm4_rm3.tags.add(category='ooc_exit')
