"""
Account

The Account represents the game "account" and each login has only one
Account object. An Account is what chats on default channels but has no
other in-game-world existence. Rather the Account puppets Objects (such
as Characters) in order to actually participate in the game world.


Guest

Guest accounts are simple low-level accounts that are created/deleted
on the fly and allows users to test the game without the commitment
of a full registration. Guest accounts are deactivated by default; to
activate them, add the following line to your settings file:

    GUEST_ENABLED = True

You will also need to modify the connection screen to reflect the
possibility to connect with a guest account. The setting file accepts
several more options for customizing the Guest account system.

"""
from django.conf import settings

from evennia import DefaultAccount, DefaultGuest
from evennia.utils.create import create_object
from evennia.utils import class_from_module, create, logger
from evennia.comms.models import ChannelDB
from evennia.server.throttle import Throttle
from evennia.server.signals import (SIGNAL_ACCOUNT_POST_CREATE, SIGNAL_OBJECT_POST_PUPPET,
                                    SIGNAL_OBJECT_POST_UNPUPPET)

CREATION_THROTTLE = Throttle(limit=2, timeout=10 * 60)
LOGIN_THROTTLE = Throttle(limit=5, timeout=5 * 60)
_MULTISESSION_MODE = settings.MULTISESSION_MODE


class Account(DefaultAccount):
    def at_account_creation(self):
        """
        This is called once, the very first time the account is created
        (i.e. first time they register with the game). It's a good
        place to store attributes all accounts should have, like
        configuration values etc.
        """
        # set an (empty) attribute holding the characters this account has
        lockstring = (
            "attrread:perm(Admins);attredit:perm(Admins);" "attrcreate:perm(Admins);"
        )
        self.attributes.add("_playable_characters", [], lockstring=lockstring)
        self.attributes.add("_saved_protocol_flags", {}, lockstring=lockstring)
        self.tags.add("new_account")
        self.attributes.add('abandon_failed_traveller', False)

    def create_character(self, *args, **kwargs):
        character, errs = super().create_character(*args, **kwargs)
        if character:
            character.instance.generate_ooc_rooms()
        return character, errs

class Guest(DefaultGuest):
    """
    This class is used for guest logins. Unlike Accounts, Guests and their
    characters are deleted after disconnection.
    """
    pass
