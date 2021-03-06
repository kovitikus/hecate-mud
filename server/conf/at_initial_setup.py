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
    char = search_object('#1', use_dbref=True)[0]
    char.equip.generate_equipment()

    room = search_object('#2', use_dbref=True)[0]
    room.key = 'Default Home'
    room.db.desc = ('The place where things go when their home isn\'t' 
                    'explicity set in the source code, by a builder, '
                    'or when an object\'s home is destroyed')

    #Create the superuser's home room.
    room3 = create_object(typeclass='rooms.rooms.Room', key=f'{char.get_display_name()}\'s Office')
