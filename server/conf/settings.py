r"""
Evennia settings file.

The available options are found in the default settings file found
here:

d:\muddev\evennia\evennia\settings_default.py

Remember:

Don't copy more from the default file than you actually intend to
change; this will make sure that you don't overload upstream updates
unnecessarily.

When changing a setting requiring a file system path (like
path/to/actual/file.py), use GAME_DIR and EVENNIA_DIR to reference
your game folder and the Evennia library folders respectively. Python
paths (path.to.module) should be given relative to the game's root
folder (typeclasses.foo) whereas paths within the Evennia library
needs to be given explicitly (evennia.foo).

If you want to share your game dir, including its settings, you can
put secret game- or server-specific settings in secret_settings.py.

"""

# Use the defaults from Evennia unless explicitly overridden
from evennia.settings_default import *

######################################################################
# Evennia base server config
######################################################################

# This is the name of your game. Make it catchy!
SERVERNAME = "Hecate"
GAME_SLOGAN = "This is where the fun begins."
SEARCH_MULTIMATCH_REGEX = r"(?P<number>[0-9]+) (?P<name>.*)"
SEARCH_MULTIMATCH_TEMPLATE = " {number} {name}{aliases}{info}\n"

######################################################################
# Game Time setup
######################################################################

# You don't actually have to use this, but it affects the routines in
# evennia.utils.gametime.py and allows for a convenient measure to
# determine the current in-game time. You can of course interpret
# "week", "month" etc as your own in-game time units as desired.

# The time factor dictates if the game world runs faster (timefactor>1)
# or slower (timefactor<1) than the real world.
TIME_FACTOR = 1.0
# The starting point of your game time (the epoch), in seconds.
# In Python a value of 0 means Jan 1 1970 (use negatives for earlier
# start date). This will affect the returns from the utils.gametime
# module. If None, the server's first start-time is used as the epoch.
TIME_GAME_EPOCH = None
# Normally, game time will only increase when the server runs. If this is True,
# game time will not pause when the server reloads or goes offline. This setting
# together with a time factor of 1 should keep the game in sync with
# the real time (add a different epoch to shift time)
TIME_IGNORE_DOWNTIMES = True

WEBCLIENT_OPTIONS = {
    "gagprompt": True,  # Gags prompt from the output window and keep them
    # together with the input bar
    "helppopup": False,  # Shows help files in a new popup window
    "notification_popup": False,  # Shows notifications of new messages as
    # popup windows
    "notification_sound": False   # Plays a sound for notifications of new
    # messages
}

######################################################################
# Global Scripts
######################################################################

# Global scripts started here will be available through
# 'evennia.GLOBAL_SCRIPTS.key'. The scripts will survive a reload and be
# recreated automatically if deleted. Each entry must have the script keys,
# whereas all other fields in the specification are optional. If 'typeclass' is
# not given, BASE_SCRIPT_TYPECLASS will be assumed.  Note that if you change
# typeclass for the same key, a new Script will replace the old one on
# `evennia.GLOBAL_SCRIPTS`.
GLOBAL_SCRIPTS = {
    # 'key': {'typeclass': 'typeclass.path.here',
    #         'repeats': -1, 'interval': 50, 'desc': 'Example script'},
    'time_cycle': {
        'typeclass': 'world.time_cycle.TimeCycle',
        'repeats': -1,
        'interval': 1,
        'desc': 'Tracks global timed events.',
        'persistent': True
    },
    'instance_ledger': {
        'typeclass': 'typeclasses.scripts.Script',
        'desc': 'Holds record of all current instances.',
        'persistent': True,
        'attributes': [('instances', {})]
    }
}

######################################################################
# Default Account setup and access
######################################################################

# Different Multisession modes allow a player (=account) to connect to the
# game simultaneously with multiple clients (=sessions). In modes 0,1 there is
# only one character created to the same name as the account at first login.
# In modes 2,3 no default character will be created and the MAX_NR_CHARACTERS
# value (below) defines how many characters the default char_create command
# allow per account.
#  0 - single session, one account, one character, when a new session is
#      connected, the old one is disconnected
#  1 - multiple sessions, one account, one character, each session getting
#      the same data
#  2 - multiple sessions, one account, many characters, one session per
#      character (disconnects multiplets)
#  3 - like mode 2, except multiple sessions can puppet one character, each
#      session getting the same data.
MULTISESSION_MODE = 1
# The maximum number of characters allowed by the default ooc char-creation command
MAX_NR_CHARACTERS = 1

######################################################################
# Settings given in secret_settings.py override those in this file.
######################################################################
try:
    from server.conf.secret_settings import *
except ImportError:
    print("secret_settings.py file not found or failed to import.")


# Modules that contain prototypes for use with the spawner mechanism.
PROTOTYPE_MODULES = [
    "npcs.npc_prototypes",
    "items.item_prototypes",
    "mobs.mob_prototypes"]


# Typeclass and base for all objects (fallback)
BASE_OBJECT_TYPECLASS = "items.objects.Object"
# Typeclass for character objects linked to an account (fallback)
BASE_CHARACTER_TYPECLASS = "characters.characters.Character"
# Typeclass for rooms (fallback)
BASE_ROOM_TYPECLASS = "rooms.rooms.Room"
# Typeclass for Exit objects (fallback).
BASE_EXIT_TYPECLASS = "travel.exits.Exit"
