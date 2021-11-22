import time, random

from evennia.utils.utils import delay
from evennia.prototypes.prototypes import search_prototype

def check_roundtime(owner):  # sourcery skip: remove-redundant-if
    if owner.db.ko == True:
        msg = "You can't do that while unconscious!"
        return msg, False

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
        elif time_remaining >= 1:
            message = f"You need to wait {int(time_remaining)} more second."
        elif time_remaining < 1:
            message = "You are in the middle of something."
        owner.msg(message)
        return False
    return True

def set_roundtime(owner):
    now = time.time()
    delay(2, unbusy, owner, persistent=True)
    owner.db.busy = True
    owner.db.roundtime = now

def unbusy(owner):
    owner.msg('|yYou are no longer busy.|n')
    owner.db.busy = False
    if owner.tags.get(category='sentient_class'):
        owner.sentient.check_for_target()

def roll_die(sides=100):
    return random.randint(1, sides)

def prototype_to_dictionary(prototype):
    """
    Translates a player-provided string into a list of dictionaries, drawn from the pool of prototypes.
    Each dictionary is comprised of a prototype key and its attributes.

    The purpose of this method is to make the internal prototype data easier to work with.

    Arguments:
        prototype (string): This is the user input to search for.

    Returns:
        result_list (list): A list of dictionaries generated, or an empty list.
    """
    result_list = []
    proto_list = search_prototype(prototype)
    for prototype in proto_list:
        common_dict = {'key': prototype['key']}
        # Attributes saved within prototype dictionaries are formatted as a list of tuples.
        attr_list = prototype['attrs']
        for (key, value, category, lock) in attr_list:
            common_dict[key] = value
        result_list.append(common_dict)
    return result_list

def all_same(items):
    return all(x == items[0] for x in items)

def objects_to_strings(object_list):
    return [i.name for i in object_list]
def objects_to_display_names(objects, looker):
    return [i.get_display_name(looker) for i in objects]

def comma_separated_string_list(string_list):
    """
    Formats a list of strings into a single string, with each element properly separated.

    Arguments:
        string_list (list): A list of strings to be formatted.
    
    Returns:
        formatted_string (string): The resulting formatted string.
    """
    num = 1
    list_len = len(string_list)
    formatted_string = ''

    # In case the list only contains 1 string.
    if list_len == 1:
        return str(string_list[0])

    for num, string in enumerate(string_list, start=1):
        if list_len == 2 and num == 1:
            formatted_string = f"{string} "
        elif list_len > 2 and num < list_len:
            formatted_string = f"{formatted_string}{string}, "
        if num == list_len:
            formatted_string = f"{formatted_string}and {string}"
    return formatted_string
