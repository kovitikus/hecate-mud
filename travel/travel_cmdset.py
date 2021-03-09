from evennia import CmdSet

from travel import travel_cmds

class travelCmdSet(CmdSet):
    key = "card_dir"
    def at_cmdset_creation(self):
        self.add(travel_cmds.North())
        self.add(travel_cmds.Northeast())
        self.add(travel_cmds.East())
        self.add(travel_cmds.Southeast())
        self.add(travel_cmds.South())
        self.add(travel_cmds.Southwest())
        self.add(travel_cmds.West())
        self.add(travel_cmds.Northwest())
