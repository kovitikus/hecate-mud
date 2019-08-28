from evennia import Command as BaseCommand
from evennia import utils
from evennia import InterruptCommand
from world import skillsets
import time
import random

class Approach(BaseCommand):
    """
    Attempt to approach a target. Required for melee combat.

    Usage:
        approach <target> | engage <target>
    """
    key = 'approach'
    aliases = ['app', 'engage', 'en', 'eng']
    def parse(self):
        if not self.args:
            self.caller.msg("Usage: approach <target> | engage <target>")
            raise InterruptCommand
        try:
            self.target = self.caller.search(self.args)
            if not self.target:
                raise ValueError
        except ValueError:
            self.caller.msg(f"{self.target} not found!")
            raise InterruptCommand

    def func(self):
        attacker = self.caller
        target = self.target
        self.caller.combat.approach(attacker, target)

class Retreat(BaseCommand):
    """
    Attempt to approach a target. Required for melee combat.

    Usage:
        retreat | disengage
    """
    key = 'retreat'
    aliases = ['ret', 'disengage', 'dis']

    def func(self):
        attacker = self.caller
        self.caller.combat.retreat(attacker)

class CmdHeal(BaseCommand):
    key = 'heal'
    def parse(self):
        if not self.args:
            self.target = self.caller
        else:
            self.args = self.args.strip()
            self.target = self.caller.search(self.args)
    def func(self):
        target = self.target
        self.caller.combat.heal(target)

class CmdStaveSwat(BaseCommand):
    '''
    Use your staff to swat an enemy.

    Usage:
        swat <target>
    '''
    key = 'swat'
    help_category = 'combat'

    def parse(self):
        if not self.args:
            self.caller.msg('Usage: swat <target>')
            return
        self.args = self.args.strip()

    def func(self):
        caller = self.caller
        both_wield = caller.db.wielding['both']
        if not caller.db.standing:
            caller.msg("You must be standing to attack!")
            return
        if not both_wield or not both_wield.is_typeclass('typeclasses.objects.Staves'):
            caller.msg("You must be wielding a stave to do that!")
            return
        else:
            weapon = both_wield
        target = caller.search(self.args, quiet=True)
        if not target:
            caller.msg('That target does not exist!')
            return
        target = target[0]
        if not target.attributes.has('hp'):
            caller.msg('You cannot attack that target!')
            return

        aim = skillsets.skillsets['staves']['swat']['default_aim']
        damage_type = skillsets.skillsets['staves']['swat']['damage_type']
        caller.combat.attack(target, 'staves', 'swat', weapon, damage_type, aim)