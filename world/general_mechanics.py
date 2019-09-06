import time
from evennia import utils, search_script
from evennia.utils import gametime
from typeclasses.rooms import Room

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

def set_roundtime(owner):
    now = time.time()
    utils.delay(2, unbusy, owner, persistent=True)
    owner.db.busy = True
    owner.db.roundtime = now

def unbusy(owner):
    owner.msg('|yYou are no longer busy.|n')
    owner.db.busy = False
 
def start_time_cycle():
    gametime.schedule(begin_time, repeat=False, hour=0, min=0, sec=0)

def begin_time():
    change_time = gametime.schedule(time_cycle, repeat=True, min=20, sec=0)
    change_time.attributes.add('day', True)
    change_time.attributes.add('phase', 6)
    change_time.key = 'time_cycle'

def time_cycle():
    change_time = search_script('change_time')
    day = change_time.db.day
    phase = change_time.db.phase

    # Check if it's the end of the final phase of night.
    # Strings are placeholders until better alternatives can be writ.
    if not day and phase == 6:
        change_time.db.day = True
        change_time.db.phase = 1
        string = "The sun rises above the eastern horizon."
    elif day and phase == 1:
        change_time.db.phase = 2
        string = "It's now mid-morning."
    elif day and phase == 2:
        change_time.db.phase = 3
        string = "It's now early-noon."
    elif day and phase == 3:
        change_time.db.phase = 4
        string = "It's now high-noon."
    elif day and phase == 4:
        change_time.db.phase = 5
        string = "It's now mid-afternoon."
    elif day and phase == 5:
        change_time.db.phase = 6
        string = "It's now dusk."
    elif day and phase == 6:
        change_time.db.day = False
        change_time.db.phase = 1
        string = "The sun has set and the moon begins to glow."
    elif not day and phase == 1:
        change_time.db.phase = 2
        string = "It's now early-evening."
    elif not day and phase == 2:
        change_time.db.phase = 3
        string = "It's now late-evening."
    elif not day and phase == 3:
        change_time.db.phase = 4
        string = "It's now midnight."
    elif not day and phase == 4:
        change_time.db.phase = 5
        string = "It's now early-morning."
    elif not day and phase == 5:
        change_time.db.phase = 6
        string = "The break of dawn approaches."

    for room in Room.objects.all():
            room.msg_contents(string)
    

        
