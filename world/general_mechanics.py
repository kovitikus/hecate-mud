import time
from evennia import utils

def check_roundtime(owner):
    if owner.db.ko == True:
        owner.msg("You can't do that while unconscious!")
        return False

    # Create cooldown attribute if non-existent.
    if not owner.attributes.has('roundtime'):
        owner.db.roundtime = 0

    # Calculate current time, total cooldown, and remaining time.
    now = time.time()
    lastcast = owner.attributes.get('roundtime')
    cooldown = lastcast + 3
    time_remaining = cooldown - now

    # Inform the attacker that they are in cooldown and exit the function.
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

def set_roundtime(owner):
    now = time.time()
    utils.delay(3, unbusy, owner, persistent=True)
    owner.db.busy = True
    owner.db.roundtime = now

def unbusy(owner):
    owner.msg('|yYou are no longer busy.|n')
    owner.db.busy = False