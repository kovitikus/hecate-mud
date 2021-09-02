import sys
from twisted.internet.defer import Deferred
from django.conf import settings
from django.test import TestCase
from mock import Mock, patch
from evennia.server.serversession import ServerSession
from evennia.server.sessionhandler import SESSIONS
from evennia.utils import create
from evennia.utils.idmapper.models import flush_cache

# mocking of evennia.utils.utils.delay
def mockdelay(timedelay, callback, *args, **kwargs):
    callback(*args, **kwargs)
    return Deferred()

# mocking of twisted's deferLater
def mockdeferLater(reactor, timedelay, callback, *args, **kwargs):
    callback(*args, **kwargs)
    return Deferred()

def unload_module(module):
    """
    Reset import so one can mock global constants.
    Args:
        module (module, object or str): The module will
            be removed so it will have to be imported again. If given
            an object, the module in which that object sits will be unloaded. A string
            should directly give the module pathname to unload.
    Example:
        ::
            # (in a test method)
            unload_module(foo)
            with mock.patch("foo.GLOBALTHING", "mockval"):
                import foo
                ... # test code using foo.GLOBALTHING, now set to 'mockval'
    Notes:
        This allows for mocking constants global to the module, since
        otherwise those would not be mocked (since a module is only
        loaded once).
    """
    if isinstance(module, str):
        modulename = module
    elif hasattr(module, "__module__"):
        modulename = module.__module__
    else:
        modulename = module.__name__

    if modulename in sys.modules:
        del sys.modules[modulename]

def _mock_deferlater(reactor, timedelay, callback, *args, **kwargs):
    callback(*args, **kwargs)
    return Deferred()

class HecateTest(TestCase):
    """
    Base test for Evennia, sets up a basic environment.
    """

    account_typeclass = settings.BASE_ACCOUNT_TYPECLASS
    object_typeclass = settings.BASE_OBJECT_TYPECLASS
    character_typeclass = settings.BASE_CHARACTER_TYPECLASS
    exit_typeclass = settings.BASE_EXIT_TYPECLASS
    room_typeclass = settings.BASE_ROOM_TYPECLASS
    script_typeclass = settings.BASE_SCRIPT_TYPECLASS

    @patch("evennia.scripts.taskhandler.deferLater", _mock_deferlater)
    def setUp(self):
        """
        Sets up testing environment
        """
        self.backups = (
            SESSIONS.data_out,
            SESSIONS.disconnect,
            settings.DEFAULT_HOME
        )
        SESSIONS.data_out = Mock()
        SESSIONS.disconnect = Mock()

    #---------------
    # Setup Accounts
        self.account = create.create_account(
            "TestAccount",
            email="test@test.com",
            password="testpassword",
            typeclass=self.account_typeclass,
        )
        self.account2 = create.create_account(
            "TestAccount2",
            email="test@test.com",
            password="testpassword",
            typeclass=self.account_typeclass,
        )

    #---------------
    # Setup the same structure in hecate's at_initial_setup module.
        # Default Home
        self.default_home = create.create_object(typeclass=self.room_typeclass, key="default_home", nohome=True)
        self.default_home.db.desc = ("This is the room where objects travel to when their home location isn\'t " 
                    "explicity set in the source code or by a builder, "
                    "and the object\'s current location is destroyed. "
                    "Character typeclasses are not allowed to enter this room in a move_to check.")

        settings.DEFAULT_HOME = "#%i" % self.default_home.id  # we must have a default home

        # Black Hole
        black_hole = create.create_object(typeclass=self.room_typeclass, key='black_hole')
        black_hole.db.desc = ("The room where all objects go to die. It is the default home for "
                            "objects that are considered worthless. Any object entering this room is "
                            "automatically deleted via the at_object_receive method.")
        black_hole.tags.add('black_hole', category='rooms')
        self.black_hole = black_hole

        # Statis Chamber
        statis_chamber = create.create_object(typeclass=self.room_typeclass, key='statis_chamber')
        statis_chamber.db.desc = ("This room holds objects indefinitely. It is the default home for "
                                "objects that are of significant value, unique, or otherwise should "
                                "not be destroyed for any reason.")
        statis_chamber.tags.add('statis_chamber', category='rooms')
        self.statis_chamber = statis_chamber

        # Trash Bin
        trash_bin = create.create_object(typeclass=self.room_typeclass, key='trash_bin')
        trash_bin.db.desc = ("This room holds objects for 90 days, before being sent to black_hole. "
                                "It is the default home for objects of some value and the destination "
                                "of said objects when discarded by players.")
        trash_bin.tags.add('trash_bin', category='rooms')
        self.trash_bin = trash_bin

        # Create the superuser's home room.
        self.main_office = create.create_object(typeclass=self.room_typeclass, key='Main Office')
        self.main_office.tags.add('main_office', category='ooc_room')

        # Create the Common Room. This is where all portals will lead when entering public OOC areas.
        self.common_room = create.create_object(typeclass=self.room_typeclass, key='Common Room')
        self.common_room.tags.add('common_room', category='ooc_room')
        self.common_room.tags.add(category='public_ooc')

        # Connect the main office and common room with exits.
        exit_main_office_common_room = create.create_object(typeclass=self.exit_typeclass, key='a mahogany door', aliases = ['door', ], 
                                        location=self.main_office, destination=self.common_room, tags=[('door', 'exits'), ])
        exit_main_office_common_room.tags.add('n', category='card_dir')
        exit_main_office_common_room.tags.add(category='ooc_exit')

        exit_common_room_main_office = create.create_object(typeclass=self.exit_typeclass, key='a mahogany door', aliases=['door', ],
                                        location=self.common_room, destination=self.main_office, tags=[('door', 'exits'), ])
        exit_common_room_main_office.tags.add('s', category='card_dir')
        exit_common_room_main_office.tags.add(category='ooc_exit')

    #---------------
    # Setup 2 generic rooms.
        self.room1 = create.create_object(self.room_typeclass, key="Room")
        self.room1.db.desc = "room1_desc"

        self.room2 = create.create_object(self.room_typeclass, key="Room")
        self.room2.db.desc = "room2_desc"

    #---------------
    # Setup the characters.
        self.char1 = create.create_object(
            self.character_typeclass, key="Char", location=self.main_office, home=self.main_office
        )
        self.char1.permissions.add("Developer")
        
        self.char2 = create.create_object(
            self.character_typeclass, key="Char2", location=self.common_room, home=self.common_room
        )
        self.char1.account = self.account
        self.account.db._last_puppet = self.char1
        self.char2.account = self.account2
        self.account2.db._last_puppet = self.char2
        self.script = create.create_script(self.script_typeclass, key="Script")
        self.account.permissions.add("Developer")

    #---------------
    # Setup a fake session
        dummysession = ServerSession()
        dummysession.init_session("telnet", ("localhost", "testmode"), SESSIONS)
        dummysession.sessid = 1
        SESSIONS.portal_connect(
            dummysession.get_sync_data()
        )  # note that this creates a new Session!
        session = SESSIONS.session_from_sessid(1)  # the real session
        SESSIONS.login(session, self.account, testmode=True)
        self.session = session

    def tearDown(self):
        def clean_objects(objects):
            for object in objects:
                for obj in object.contents:
                    obj.delete()
                object.delete()

        clean_chars = [self.char1, self.char2]
        clean_objects(clean_chars)

        clean_rooms = [self.main_office, self.common_room, self.room1, self.room2,
            self.black_hole, self.statis_chamber, self.trash_bin, self.default_home]
        clean_objects(clean_rooms)

        flush_cache()
        SESSIONS.data_out = self.backups[0]
        SESSIONS.disconnect = self.backups[1]
        settings.DEFAULT_HOME = self.backups[2]

        del SESSIONS[self.session.sessid]
        self.account.delete()
        self.account2.delete()

        super().tearDown()
