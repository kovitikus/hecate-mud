"""
Command sets

All commands in the game must be grouped in a cmdset.  A given command
can be part of any number of cmdsets and cmdsets can be added/removed
and merged onto entities at runtime.

To create new commands to populate the cmdset, see
`commands/command.py`.

This module wraps the default command sets of Evennia; overloads them
to add/remove commands from the default lineup. You can create your
own cmdsets by inheriting from them or directly from `evennia.CmdSet`.

"""

from evennia import default_cmds

from commands import command
from commands import combat_cmds



class CharacterCmdSet(default_cmds.CharacterCmdSet):
    """
    The `CharacterCmdSet` contains general in-game commands like `look`,
    `get`, etc available on in-game Character objects. It is merged with
    the `AccountCmdSet` when an Account puppets a Character.
    """
    key = "DefaultCharacter"

    def at_cmdset_creation(self):
        """
        Populates the cmdset
        """
        super().at_cmdset_creation()
        #
        # any commands you add below will overload the default ones.
        #
        self.add(command.CmdDesc())
        self.add(command.CmdCharGen())
        self.add(command.CmdLearnSkillset())
        self.add(command.CmdGrantSP())
        self.add(command.CmdTest())
        self.add(command.CmdLook())
        self.add(command.CmdInventory())
        self.add(command.CmdGet())
        self.add(command.CmdInhand())
        self.add(command.CmdStand())
        self.add(command.CmdKneel())
        self.add(command.CmdSit())
        self.add(command.CmdLie())
        self.add(command.CmdDrop())
        self.add(command.CmdStow())
        self.add(command.CmdWield())
        self.add(command.CmdUnwield())
        self.add(combat_cmds.Approach())
        self.add(combat_cmds.Retreat())
        self.add(combat_cmds.CmdStaveSwat())
        self.add(combat_cmds.CmdHeal())
        self.add(command.CmdPut())
        self.add(command.CmdSkills())
        self.add(command.CmdEquip())
        self.add(command.CmdLight())
        self.add(command.CmdStock())
        self.add(command.CmdBuy())
        self.add(command.CmdConvertCoin())
        self.add(command.CmdGroup())
        self.add(command.CmdUngroup())
        self.add(command.CmdAFKTimer())

class AccountCmdSet(default_cmds.AccountCmdSet):
    """
    This is the cmdset available to the Account at all times. It is
    combined with the `CharacterCmdSet` when the Account puppets a
    Character. It holds game-account-specific commands, channel
    commands, etc.
    """
    key = "DefaultAccount"

    def at_cmdset_creation(self):
        """
        Populates the cmdset
        """
        super().at_cmdset_creation()
        #
        # any commands you add below will overload the default ones.
        #


class UnloggedinCmdSet(default_cmds.UnloggedinCmdSet):
    """
    Command set available to the Session before being logged in.  This
    holds commands like creating a new account, logging in, etc.
    """
    key = "DefaultUnloggedin"

    def at_cmdset_creation(self):
        """
        Populates the cmdset
        """
        super().at_cmdset_creation()
        #
        # any commands you add below will overload the default ones.
        #


class SessionCmdSet(default_cmds.SessionCmdSet):
    """
    This cmdset is made available on Session level once logged in. It
    is empty by default.
    """
    key = "DefaultSession"

    def at_cmdset_creation(self):
        """
        This is the only method defined in a cmdset, called during
        its creation. It should populate the set with command instances.

        As and example we just add the empty base `Command` object.
        It prints some info.
        """
        super().at_cmdset_creation()
        #
        # any commands you add below will overload the default ones.
        #
