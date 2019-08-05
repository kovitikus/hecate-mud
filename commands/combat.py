from evennia import Command as BaseCommand
from evennia import utils
from evennia import create_script
import time
import random

class CmdStaveBash(BaseCommand):
    '''
    Use your staff to bash an enemy.

    Usage:
        bash <target>
    '''
    key = 'bash'
    help_category = 'combat'

    def func(self):
        if not self.args:
            self.caller.msg('Usage: bash <target>')
            return
        target = self.caller.search(self.args)
        if not target:
            self.caller.msg('That target does not exist!')
            return
        if not target.attributes.has('hp'):
            self.caller.msg('You cannot attack that target!')
            return
        self.caller.combat.attack(target)