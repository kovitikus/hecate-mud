from evennia import Command as BaseCommand
from typeclasses import combat_handler
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
        
        damage = 5
        attacker = self.caller
        target = self.caller.search(self.args)
        if not target:
            self.caller.msg('That target does not exist!')
            return
        if not target.attributes.has('hp'):
            self.caller.msg('You cannot attack that target!')
            return
        
        now = time.time()
        
        lastcast = self.caller.db.stave_bash
        cooldown = lastcast + 3
        time_remaining = cooldown - now

        if time_remaining > 0:
            if time_remaining >= 2:
                message = f"You need to wait {int(time_remaining)} more seconds."
            elif time_remaining >= 1 and time_remaining < 2:
                message = f"You need to wait {int(time_remaining)} more second."
            elif time_remaining < 1:
                message = f"You are in the middle of something."
            self.caller.msg(message)
            return

        roll = random.randint(1, 100)
        success = random.randint(5, 95)
        if roll > success:
            self.caller.msg(f'[Success: {success} Roll: {roll}] You bash {target} with your stave!')
            target.db.hp -= damage
        else:
            self.caller.msg(f'[Success: {success} Roll: {roll}] You miss {target} with your stave!')

        self.caller.db.stave_bash = now