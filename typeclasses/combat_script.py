from evennia import DefaultScript
from evennia import utils
import time
import random

class CombatScript(DefaultScript):

    def at_script_creation(self):
            self.key = "combat_script"
            self.desc = "Handles all combat methods."
            self.persistent = True  # will survive reload

    def attack(self, target):  
        damage = 20
        self.obj.db.stave_bash = 0
        now = time.time()
        lastcast = self.obj.db.stave_bash
        cooldown = lastcast + 3
        time_remaining = cooldown - now

        if time_remaining > 0:
            if time_remaining >= 2:
                message = f"You need to wait {int(time_remaining)} more seconds."
            elif time_remaining >= 1 and time_remaining < 2:
                message = f"You need to wait {int(time_remaining)} more second."
            elif time_remaining < 1:
                message = f"You are in the middle of something."
            self.obj.msg(message)
            return

        # roll = random.randint(1, 100)
        # success = random.randint(5, 95)
        roll = 100
        success = 0

        if roll > success:
            self.obj.msg(f'[Success: {success} Roll: {roll}] You bash {target} with your stave!')
            self.take_damage(target, damage)
        else:
            self.obj.msg(f'[Success: {success} Roll: {roll}] You miss {target} with your stave!')
        utils.delay(3, self.unbusy)
        self.obj.db.stave_bash = now

    def take_damage(self, target, damage):
        mob = target.key
        location = target.location
        
        target.db.hp -= damage
        hp = target.db.hp
        location.msg_contents(f'{mob} has {hp} health remaining!')
        if hp >= 1:
            target.db.ko = False
        elif hp <= 0 and target.db.ko != True:
            target.db.ko = True
            location.msg_contents(f'{mob} falls unconscious!')
        if hp <= -100:
            okay = target.delete()
            if not okay:
                location.msg_contents(f'\nERROR: {mob} not deleted, probably because delete() returned False.')
            else:
                location.msg_contents(f'{mob} breathes a final breath and expires.')
        return
    
    def unbusy(self):
            self.obj.msg('|yYou are no longer busy.|n')