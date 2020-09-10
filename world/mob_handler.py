import random
            
import time, datetime
from evennia import utils
from evennia.utils import gametime
from typeclasses.rooms import Room

class MobHandler:
    def __init__(self, owner):
        self.owner = owner
    def get_target(self):
        owner = self.owner
        # Set target to first approached if already approached.
        approached = owner.attributes.get('approached')
        app_len = len(approached)
        if app_len >= 1:
            target = approached[0]
            return target

        # If approached is empty, find new target and approach it.
        visible = []
        for targ in owner.location.contents_get(exclude=owner):
            if targ.has_account and not targ.is_superuser:
                    visible.append(targ)
        t_len = len(visible)
        if not t_len:
            return
        
        # Pick random target from visible targets.
        rand_targ = random.randrange(t_len)
        target = visible[rand_targ - 1]
        owner.combat.approach(owner, target)
        return target

    def check_roundtime(self):
        owner = self.owner
        if owner.db.ko == True:
            owner.msg("You can't do that while unconscious!")
            return False

        # Create cooldown attribute if non-existent.
        if not owner.attributes.has('roundtime'):
            owner.db.roundtime = 0

        # Calculate current time, total cooldown, and remaining time.
        now = time.time()
        lastcast = owner.attributes.get('roundtime')
        cooldown = lastcast + 2
        time_remaining = cooldown - now

        # Inform the owner that they are in cooldown and exit the function.
        if time_remaining > 0 or owner.db.busy == True:
            if time_remaining >= 2:
                message = f"You need to wait {int(time_remaining)} more seconds."
            elif time_remaining >= 1 and time_remaining < 2:
                message = f"You need to wait {int(time_remaining)} more second."
            elif time_remaining < 1:
                message = f"You are in the middle of something."
            owner.msg(message)
            return False
        return True

    def set_roundtime(self):
        owner = self.owner
        now = time.time()
        utils.delay(2, self.unbusy, owner, persistent=True)
        owner.db.busy = True
        owner.db.roundtime = now

    def unbusy(self):
        owner = self.owner
        owner.msg('|yYou are no longer busy.|n')
        owner.db.busy = False

    def claw(self):
        owner = self.owner
        target = self.get_target()
        damage_type = 'slash'
        skillset = 'rat'
        skill = 'claw'
        aim = 'mid'
        if target:
            owner.combat.attack(target, skillset, skill, damage_type, aim)
    
    def idle(self):
        pass
