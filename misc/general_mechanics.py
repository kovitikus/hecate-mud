import time, datetime, random

from evennia import utils, search_script
from evennia.utils import gametime, inherits_from
from evennia.prototypes.prototypes import search_prototype

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
    if inherits_from(owner, 'mobs.mobs.DefaultMob'):
        owner.mob.check_for_target()

def roll_die(sides=100):
    roll = random.randint(1, sides)
    return roll

def return_proto_dic(prototype):
    proto_dic = search_prototype(prototype)
    proto_dic = proto_dic[0]
    name = proto_dic['key']
    attrs = proto_dic['attrs']
    attr_dic = {'key': name}
    for i in attrs:
        attr_dic[i[0]] = i[1]
    return attr_dic

def all_same(items):
    return all(x == items[0] for x in items)

def objects_to_strings(object_list):
    string_list = []
    for i in object_list:
        string_list.append(i.name)
    return string_list
def objects_to_display_names(objects, looker):
    string_list = []
    for i in objects:
        string_list.append(i.get_display_name(looker))
    return string_list

def comma_separated_string_list(string_list):
    num = 1
    list_len = len(string_list)
    formatted_string = ''
    for i in string_list:
        if list_len == num:
            formatted_string = f"{formatted_string} and {i}"
        elif num == 1:
            formatted_string = f"{formatted_string}{i},"
        else:
            formatted_string = f"{formatted_string} {i},"
        num += 1
    return formatted_string
