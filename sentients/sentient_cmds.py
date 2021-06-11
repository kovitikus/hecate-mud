from evennia import Command as BaseCommand
from evennia import InterruptCommand

#------------------
# Rat Commands
class CmdRatBite(BaseCommand):
    """
    """
    key = 'ratbite'
    def parse(self):
        if not self.args:
            self.caller.msg("Usage: ratbite <target>")
            return
        self.args = self.args.strip()
    
    def func(self):
        caller = self.caller

        if not caller.db.standing:
            caller.msg("You must be standing to attack!")
            return

        target = caller.search(self.args, quiet=True)
        if not target:
            caller.msg('That target does not exist!')
            return
        target = target[0]

        if not target.attributes.has('hp'):
            caller.msg('You cannot attack that target!')
            return

        # Checks have passed, attack the target.
        caller.combat.attack(target, 'rat', 'bite')

class CmdRatClaw(BaseCommand):
    """
    """
    key = 'ratclaw'
    def parse(self):
        if not self.args:
            self.caller.msg("Usage: ratclaw <target>")
            return
        self.args = self.args.strip()
    
    def func(self):
        caller = self.caller

        if not caller.db.standing:
            caller.msg("You must be standing to attack!")
            return

        target = caller.search(self.args, quiet=True)
        if not target:
            caller.msg('That target does not exist!')
            return
        target = target[0]

        if not target.attributes.has('hp'):
            caller.msg('You cannot attack that target!')
            return

        # Checks have passed, attack the target.
        caller.combat.attack(target, 'rat', 'claw')

#------------------
# Spider Commands
class CmdSpiderBite(BaseCommand):
    """
    """
    key = 'spiderbite'
    def parse(self):
        if not self.args:
            self.caller.msg("Usage: spiderbite <target>")
            return
        self.args = self.args.strip()
    
    def func(self):
        caller = self.caller

        if not caller.db.standing:
            caller.msg("You must be standing to attack!")
            return

        target = caller.search(self.args, quiet=True)
        if not target:
            caller.msg('That target does not exist!')
            return
        target = target[0]

        if not target.attributes.has('hp'):
            caller.msg('You cannot attack that target!')
            return

        # Checks have passed, attack the target.
        caller.combat.attack(target, 'spider', 'bite')

#------------------
# Snake Commands
class CmdSnakeBite(BaseCommand):
    """
    """
    key = 'snakebite'
    def parse(self):
        if not self.args:
            self.caller.msg("Usage: snakebite <target>")
            return
        self.args = self.args.strip()
    
    def func(self):
        caller = self.caller

        if not caller.db.standing:
            caller.msg("You must be standing to attack!")
            return

        target = caller.search(self.args, quiet=True)
        if not target:
            caller.msg('That target does not exist!')
            return
        target = target[0]

        if not target.attributes.has('hp'):
            caller.msg('You cannot attack that target!')
            return

        # Checks have passed, attack the target.
        caller.combat.attack(target, 'snake', 'bite')
