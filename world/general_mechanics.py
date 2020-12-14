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

def return_obj_coin(obj):
    if obj.attributes.has('coin'):
        return obj.db.coin['plat'], obj.db.coin['gold'], obj.db.coin['silver'], obj.db.coin['copper']

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
    stacked_obj_names = comma_separated_string_list(objects_to_strings(objects))

    # Check of every object in list is stackable. Abort if not.
    for obj in objects:
        if not obj.tags.get('stackable'):
            msg = f"{obj} is not able to be grouped!"
            return msg
    
    # Check if all objects in the list have the same name.
    same_name = all_same(objects_to_strings(objects))

    # Sort objects into quantity or inventory stack type lists.
    for obj in objects:
        if obj.tags.get('quantity', category='stack'):
            qty_stack_objects.append(obj)
        elif obj.tags.get('inventory', category='stack'):
            inv_stack_objects.append(obj)

    # Quantity Stackables
    if len(qty_stack_objects) > 1:
        are_coins = False
        #Check to see if all quantity stack objects are coins.
        for obj in qty_stack_objects:
            if obj.is_typeclass('typeclasses.objects.Coin', exact=True):
                are_coins = True
            else:
                msg = "You can't group coins with non-coins!"
                return msg
        if are_coins:
            stack_coins(obj_loc, qty_stack_objects, stacked_obj_names)
            msg = f"You group together {stacked_obj_names}."
            return msg

    # Inventory Stackables
    if len(inv_stack_objects) > 1:
        inv_quantity = 0
        if same_name:
            inv_stack = utils.create.create_object(key=f'a pile of {inv_stack_objects[0].name}es', 
                typeclass='typeclasses.objects.StackInventory', 
                location=obj_loc)
            if inv_stack:
                for obj in inv_stack_objects:
                    obj.move_to(inv_stack, quiet=True, move_hooks=False)
                    inv_quantity += 1
                inv_stack.db.quantity = inv_quantity
                msg = f"You group together some {inv_stack_objects[0].name}es into a pile."
                return msg

def ungroup_objects(obj, obj_loc):
    if obj.is_typeclass('typeclasses.objects.StackQuantity'):
        if obj.tags.get('coin', category='currency'):
            plat, gold, silver, copper = return_obj_coin(obj)
            multi_coin = 0
            for x in [plat, gold, silver, copper]:
                if x > 0:
                    multi_coin += 1
            if multi_coin >= 2:
                if plat > 0:
                    plat_pile = utils.create.create_object(key='a pile of platinum coins', location=obj_loc,
                                                typeclass='typeclasses.objects.Coin')
                    if plat_pile:
                        plat_pile.db.coin['plat'] = plat
                        obj.db.coin['plat'] = 0
                if gold > 0:
                    gold_pile = utils.create.create_object(key='a pile of gold coins', location=obj_loc,
                                                typeclass='typeclasses.objects.Coin')
                    if gold_pile:
                        gold_pile.db.coin['gold'] = gold
                        obj.db.coin['gold'] = 0
                if silver > 0:
                    silver_pile = utils.create.create_object(key='a pile of silver coins', location=obj_loc,
                                                typeclass='typeclasses.objects.Coin')
                    if silver_pile:
                        silver_pile.db.coin['silver'] = silver
                        obj.db.coin['silver'] = 0
                if copper > 0:
                    copper_pile = utils.create.create_object(key='a pile of copper coins', location=obj_loc,
                                                typeclass='typeclasses.objects.Coin')
                    if copper_pile:
                        copper_pile.db.coin['copper'] = copper
                        obj.db.coin['copper'] = 0
                msg = f"You ungroup {obj.name} into separate piles of coins."
                obj.delete()
                return msg
    elif obj.is_typeclass('typeclasses.objects.StackInventory'):
        stack_contents = obj.contents
        for x in stack_contents:
            x.move_to(obj_loc, quiet=True, move_hooks=False)
        msg = f"You ungroup {obj.name}, producing {comma_separated_string_list(objects_to_strings(stack_contents))}."
        obj.delete()
        return msg

def split_pile(split_type, pile, obj_loc, quantity=0, qty_obj=None):
    pile_name = pile.name

    if split_type == 'default':
        # This condition splits the pile as evenly as possible into 2 piles.
        # The original pile always contains the higher quantity of items, if not evenly split.
        pass
    elif split_type == 'from':
        if pile.is_typeclass('typeclasses.objects.StackQuantity'):
            # This is a pile of coins, or other similar pile.
            if pile.tags.get('coin', category='currency'):
                currency = pile.attributes.get('coin')
                coin_type = currency.get(qty_obj)
                if coin_type >= quantity:
                    currency[coin_type] -= quantity
                    # We also have to determine here if the coin pile has homogenized and change its description.

                    # Now we need to make a new coin pile with the value of the
                    # new coins split from the original.

                else:
                    # There's not enough coin in the pile to execute the action.
                    msg = f"{pile.name} doesn't container {quantity} of {qty_obj}!"
                    return msg
            pass
        elif pile.is_typeclass('typeclasses.objects.StackInventory'):
            # Object has contents
            qty_obj_names = []

            qty_objects = pile.search(qty_obj, location=pile, quiet=True)
            # Check that there are enough objects in the pile to meet requirements.
            if len(qty_objects) >= quantity:
                num = 1
                while num <= quantity:
                    obj = qty_objects.pop
                    qty_obj_names.append(obj.name)
                    obj.move_to(obj_loc, quiet=True, move_hooks=False)
                    num += 1

                msg = f"You split"
                if all_same(qty_obj_names):
                    msg = f"{msg} {quantity} {qty_obj_names[0]}"
                else:
                    msg = f"{msg} {comma_separated_string_list(qty_obj_names)}"
                msg= f"{msg} from {pile_name}."
            else:
                msg = f"There aren't {quantity} of {qty_obj} in {pile.name}!"
                return msg

            # Check if the pile has 1 or less objects remaining.
            if len(pile.contents) == 1:
                obj = pile.contents
                obj.move_to(obj_loc, quiet=True, move_hooks=False)
            if len(pile.contents) == 0:
                pile.delete()
    return msg

    
def all_same(items):
    return all(x == items[0] for x in items)

                
def stack_coins(obj_loc, qty_stack_objects, stacked_obj_names):
    qty_stack = utils.create.create_object(key=f'a pile of coins', 
            typeclass='typeclasses.objects.StackQuantity', 
            location=obj_loc)
    if qty_stack:
        qty_stack.attributes.add('coin', {'plat': 0, 'gold': 0, 'silver': 0, 'copper': 0})
        qty_stack.tags.add('coin', category='currency')
        for obj in qty_stack_objects:
            plat, gold, silver, copper = return_obj_coin(obj)
            add_coin(qty_stack, plat=plat, gold=gold, silver=silver, copper=copper)
            obj.delete()
        return qty_stack



def objects_to_strings(object_list):
    string_list = []
    for i in object_list:
        string_list.append(i.name)
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
