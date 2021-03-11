from evennia import CmdSet

from travel import travel_cmds

class TravelCmdSet(CmdSet):
    key = "card_dir"
    def at_cmdset_creation(self):
        self.add(travel_cmds.CmdNorth())
        self.add(travel_cmds.CmdNortheast())
        self.add(travel_cmds.CmdEast())
        self.add(travel_cmds.CmdSoutheast())
        self.add(travel_cmds.CmdSouth())
        self.add(travel_cmds.CmdSouthwest())
        self.add(travel_cmds.CmdWest())
        self.add(travel_cmds.CmdNorthwest())
        self.add(travel_cmds.CmdAbandonFailedTraveller())
