from evennia import CmdSet

from commands import cardinal_cmds

class CardinalCmdSet(CmdSet):
    key = "card_dir"
    def at_cmdset_creation(self):
        self.add(cardinal_cmds.North())
        self.add(cardinal_cmds.Northeast())
        self.add(cardinal_cmds.East())
        self.add(cardinal_cmds.Southeast())
        self.add(cardinal_cmds.South())
        self.add(cardinal_cmds.Southwest())
        self.add(cardinal_cmds.West())
        self.add(cardinal_cmds.Northwest())
