from evennia import Command as BaseCommand
from evennia import utils
from world import skillsets
import time
import random

class CmdStaveBash(BaseCommand):
    '''
    Use your staff to swat an enemy.

    Usage:
        swat <target>
    '''
    key = 'swat'
    help_category = 'combat'

    def func(self):
        if not self.args:
            self.caller.msg('Usage: swat <target>')
            return
        target = self.caller.search(self.args)
        if not target:
            self.caller.msg('That target does not exist!')
            return
        if not target.attributes.has('hp'):
            self.caller.msg('You cannot attack that target!')
            return
        damage_type = skillsets.skillsets['staves']['swat']['damage_type']
        self.caller.combat.attack(target, damage_type, 'staves', 'swat')