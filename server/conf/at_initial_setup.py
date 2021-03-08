from evennia.utils import create
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
    char1.equip.generate_equipment()

    room = search_object('#2', use_dbref=True)[0]
    room.key = 'Default Home'
    room.db.desc = ('This is the room where objects travel to when their home location isn\'t ' 
                    'explicity set in the source code or by a builder, '
                    'and the object\'s current room is destroyed. '
                    'Player_Character typeclasses are not allowed to enter this room in a move_to check.')

    # Create the superuser's home room.
    rm3 = create_object(typeclass='rooms.rooms.OOC_Room', key='Main Office')
    char1.home = rm3
    rm3.tags.add('main_office', category='ooc_room')
    char1.move_to(rm3)

    # Create the Common Room. This is where all portals will lead when entering public OOC areas.
    rm4 = create_object(typeclass='rooms.rooms.OOC_Room', key='Common Room')
    rm4.tags.add('common_room', category='ooc_room')
    rm4.tags.add(category='public_ooc')

    # Connect the main office and common room with exits.
    exit_rm3_rm4 = create_object(typeclass='rooms.exits.Door', key='north', aliases = ['n', 'nor', 'nort', 'door'], 
                                    location=rm3, destination=rm4, desc='a mahogany door')
    exit_rm3_rm4.tags.add(category='ooc_exit')

    exit_rm4_rm3 = create_object(typeclass='rooms.exits.Door', key='south', aliases=['s', 'sou', 'sout', 'door'],
                                    location=rm4, destination=rm3, desc='a mahogany door')
    exit_rm4_rm3.tags.add(category='ooc_exit')
