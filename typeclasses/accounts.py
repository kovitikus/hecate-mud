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

    @classmethod
    def create(cls, *args, **kwargs):
        """
        Creates an Account (or Account/Character pair for MULTISESSION_MODE<2)
        with default (or overridden) permissions and having joined them to the
        appropriate default channels.
        Kwargs:
            username (str): Username of Account owner
            password (str): Password of Account owner
            email (str, optional): Email address of Account owner
            ip (str, optional): IP address of requesting connection
            guest (bool, optional): Whether or not this is to be a Guest account
            permissions (str, optional): Default permissions for the Account
            typeclass (str, optional): Typeclass to use for new Account
            character_typeclass (str, optional): Typeclass to use for new char
                when applicable.
        Returns:
            account (Account): Account if successfully created; None if not
            errors (list): List of error messages in string form
        """

        account = None
        errors = []

        username = kwargs.get("username")
        password = kwargs.get("password")
        email = kwargs.get("email", "").strip()
        guest = kwargs.get("guest", False)

        permissions = kwargs.get("permissions", settings.PERMISSION_ACCOUNT_DEFAULT)
        typeclass = kwargs.get("typeclass", cls)

        ip = kwargs.get("ip", "")
        if ip and CREATION_THROTTLE.check(ip):
            errors.append(
                "You are creating too many accounts. Please log into an existing account."
            )
            return None, errors

        # Normalize username
        username = cls.normalize_username(username)

        # Validate username
        if not guest:
            valid, errs = cls.validate_username(username)
            if not valid:
                # this echoes the restrictions made by django's auth
                # module (except not allowing spaces, for convenience of
                # logging in).
                errors.extend(errs)
                return None, errors

        # Validate password
        # Have to create a dummy Account object to check username similarity
        valid, errs = cls.validate_password(password, account=cls(username=username))
        if not valid:
            errors.extend(errs)
            return None, errors

        # Check IP and/or name bans
        banned = cls.is_banned(username=username, ip=ip)
        if banned:
            # this is a banned IP or name!
            string = (
                "|rYou have been banned and cannot continue from here."
                "\nIf you feel this ban is in error, please email an admin.|x"
            )
            errors.append(string)
            return None, errors

        # everything's ok. Create the new account.
        try:
            try:
                account = create.create_account(
                    username, email, password, permissions=permissions, typeclass=typeclass
                )
                logger.log_sec(f"Account Created: {account} (IP: {ip}).")

            except Exception as e:
                errors.append(
                    "There was an error creating the Account. If this problem persists, contact an admin."
                )
                logger.log_trace()
                return None, errors

            # This needs to be set so the engine knows this account is
            # logging in for the first time. (so it knows to call the right
            # hooks during login later)
            account.db.FIRST_LOGIN = True

            # Record IP address of creation, if available
            if ip:
                account.db.creator_ip = ip

            # join the new account to the public channel
            pchannel = ChannelDB.objects.get_channel(settings.DEFAULT_CHANNELS[0]["key"])
            if not pchannel or not pchannel.connect(account):
                string = f"New account '{account.key}' could not connect to public channel!"
                errors.append(string)
                logger.log_err(string)

            if account and settings.MULTISESSION_MODE < 2:
                # Load the appropriate Character class
                character_typeclass = 'characters.characters.OOC_Character'
                # character_home = kwargs.get("home")
                Character = class_from_module(character_typeclass)
                name = account.key
                possessive = '\'' if name[-1] == 's' else '\'s'
                homeroom = create_object(
                    typeclass='rooms.rooms.OOC_Quarters',
                    key=f"{name}{possessive} Quarters"
                )

                # Create the character
                character, errs = Character.create(
                    account.key,
                    account,
                    ip=ip,
                    typeclass=character_typeclass,
                    permissions=permissions,
                    home=homeroom,
                )
                errors.extend(errs)

                if character:
                    # Update playable character list
                    if character not in account.characters:
                        account.db._playable_characters.append(character)

                    # We need to set this to have @ic auto-connect to this character
                    account.db._last_puppet = character

        except Exception:
            # We are in the middle between logged in and -not, so we have
            # to handle tracebacks ourselves at this point. If we don't,
            # we won't see any errors at all.
            errors.append("An error occurred. Please e-mail an admin if the problem persists.")
            logger.log_trace()

        # Update the throttle to indicate a new account was created from this IP
        if ip and not guest:
            CREATION_THROTTLE.update(ip, "Too many accounts being created.")
        SIGNAL_ACCOUNT_POST_CREATE.send(sender=account, ip=ip)
        return account, errors

class Guest(DefaultGuest):
    """
    This class is used for guest logins. Unlike Accounts, Guests and their
    characters are deleted after disconnection.
    """
    pass
