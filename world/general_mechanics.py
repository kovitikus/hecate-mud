import time, datetime, random
from evennia import utils, search_script
from evennia.utils import gametime, inherits_from
from typeclasses.rooms import Room
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
    if inherits_from(owner, 'typeclasses.mobs.DefaultMob'):
        owner.mob.check_for_target()

def roll_die(sides=100):
    roll = random.randint(1, sides)
    return roll

def return_currency(owner):
    if owner.attributes.has('coin'):
        coin_dic = owner.attributes.get('coin')
        string = f"{coin_dic['plat']}p {coin_dic['gold']}g {coin_dic['silver']}s {coin_dic['copper']}c"
        return string

def add_coin(owner, plat=0, gold=0, silver=0, copper=0):
    if owner.attributes.has('coin'):
        coin_dic = owner.attributes.get('coin')
        plat_dic = coin_dic['plat']
        gold_dic = coin_dic['gold']
        silver_dic = coin_dic['silver']
        copper_dic = coin_dic['copper']
    
        total_copper = copper + copper_dic
        total_silver = silver + silver_dic
        total_gold = gold + gold_dic
        total_plat = plat + plat_dic

        if total_copper > 999:
            total_silver += int(convert_coin(copper=total_copper, result_type=silver))
            total_copper = 999

        if total_silver > 999:
            total_gold += int(convert_coin(silver=total_silver, result_type=gold))
            total_silver = 999
        
        if total_gold > 999:
            total_plat += int(convert_coin(gold=total_gold, result_type=plat))
            total_gold = 999

        coin_dic['copper'] = total_copper
        coin_dic['silver'] = total_silver
        coin_dic['gold'] = total_gold
        coin_dic['plat'] = total_plat

def remove_coin(owner, plat=0, gold=0, silver=0, copper=0):
    if owner.attributes.has('coin'):
        coin_dic = owner.attributes.get('coin')
        plat_dic = coin_dic['plat']
        gold_dic = coin_dic['gold']
        silver_dic = coin_dic['silver']
        copper_dic = coin_dic['copper']

        total_copper = copper_dic - copper
        total_silver = silver_dic - silver
        total_gold = gold_dic - gold
        total_plat = plat_dic - plat

        if total_copper > 999:
            total_silver += int(convert_coin(copper=total_copper, result_type=silver))
            total_copper = 999

        if total_silver > 999:
            total_gold += int(convert_coin(silver=total_silver, result_type=gold))
            total_silver = 999
        
        if total_gold > 999:
            total_plat += int(convert_coin(gold=total_gold, result_type=plat))
            total_gold = 999

        coin_dic['copper'] = total_copper
        coin_dic['silver'] = total_silver
        coin_dic['gold'] = total_gold
        coin_dic['plat'] = total_plat

def convert_coin(plat=0, gold=0, silver=0, copper=0, result_type='copper'):
    if result_type == 'plat':
        plat = (copper / 1_000_000_000) + (silver / 1_000_000) + (gold / 1_000)
        return plat

    elif result_type == 'gold':
        gold = (copper / 1_000_000) + (silver / 1_000) + (plat * 1_000)
        return gold
        
    elif result_type == 'silver':
        silver = (copper / 1_000) + (gold * 1_000) + (plat * 1_000_000)
        return silver
        
    else:
        copper = (silver * 1_000) + (gold * 1_000_000) + (plat * 1_000_000_000)
        return copper

def return_proto_dic(prototype):
    proto_dic = search_prototype(prototype)
    proto_dic = proto_dic[0]
    name = proto_dic['key']
    attrs = proto_dic['attrs']
    attr_dic = {'key': name}
    for i in attrs:
        attr_dic[i[0]] = i[1]
    return attr_dic

def group_objects(objects, obj_loc):
    msg = ''
    inv_stack_objects = []
    qty_stack_objects = []
    stacked_obj_names = []

    for obj in objects:
        if not obj.tags.has('stackable'):
            msg = f"{obj} cannot be grouped!"
            return msg
    
    for obj in objects:
        if obj.tags.has('quantity', category='stack'):
            qty_stack_objects.append(obj)
        elif obj.tags.has('inventory', category='stack'):
            inv_stack_objects.append(obj)

    if len(qty_stack_objects) > 1:
        if qty_stack_objects[0].is_typeclass('typeclasses.objects.Coin', exact=True):
            qty_stack = utils.create.create_object(key=f'a pile of coins.', 
                    typeclass='typeclasses.objects.StackQuantity', 
                    location=obj_loc)
            if qty_stack:
                for coin in qty_stack_objects:
                    plat = coin.db.coin['plat']
                    gold = coin.db.coin['gold']
                    silver = coin.db.coin['silver']
                    copper = coin.db.coin['copper']
                    add_coin(qty_stack, plat=plat, gold=gold, silver=silver, copper=copper)
                    stacked_obj_names.append(coin.name)
                stacked_obj_names = comma_separated_string_list(stacked_obj_names)
                msg = f"You group together {stacked_obj_names}."
                return msg
                


    return msg

def objects_to_strings(object_list):
    string_list = []
    for i in object_list:
        string_list.append(i.name)
    return string_list

def comma_separated_string_list(string_list):
    num = 0
    list_len = len(string_list)
    formatted_string = ''
    for i in string_list:
        if list_len == num:
            formatted_string = f"{formatted_string} and {i}"
        if num == 0:
            formatted_string = f"{formatted_string}{i},"
        else:
            formatted_string = f"{formatted_string} {i},"
        num += 1
    return formatted_string
