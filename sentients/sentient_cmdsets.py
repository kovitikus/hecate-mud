from evennia import CmdSet

from sentients import sentient_cmds


class RatCmdSet(CmdSet):
    """
    """
    key = "Rat"

    def at_cmdset_creation(self):
        """
        Populates the cmdset
        """
        self.add(sentient_cmds.CmdRatBite())
        self.add(sentient_cmds.CmdRatClaw())
