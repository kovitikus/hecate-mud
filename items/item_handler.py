from evennia.utils.create import create_object

from misc import general_mechanics as gen_mec

'''
This handler decides functions related to items, such as get, put, stacking, etc.
'''

class ItemHandler():
    def __init__(self, owner):
        self.owner = owner

    def get_object(self, obj, container, owner_possess):
        #TODO: Allow auto-stow of items in hand and continue to pick up obj if more than one exists in location.
        owner = self.owner
        main_wield, off_wield, both_wield  = owner.db.wielding.values()
        main_hand, off_hand = owner.db.hands.values()
        use_main_hand, use_off_hand = False, False
        owner_msg = ''
        others_msg = ''
        
        if obj in [main_hand, off_hand]:
            owner.msg(f"You are already carrying {obj.name}.")
            return

        # calling at_before_get hook method
        if not obj.at_before_get(owner):
            return
        
        # TODO: Check for free inventory slots.
        # inventory_dic = dict(owner.db.inventory)
        # if inventory_dic['occupied_slots'] < inventory_dic['max_slots']:
        #     free_slot = True

        # All restriction checks passed, move the object to the owner.
        obj.move_to(owner, quiet=True, move_hooks=False)

        #---------------------------[Hand Logic]---------------------------#
        # Items should prefer an open hand first and foremost.
        # When both hands are occupied, but neither are wielding, prefer the dominate hand.
        # Offhand should be used as a last resort, as this is a shield
        #------------------------------------------------------------------#
        
        if both_wield is not None:
            use_main_hand = False
            use_off_hand = True
            owner_msg = f"You stop wielding {both_wield.name}."
            others_msg = f"{owner.name} stops wielding {both_wield.name}."
            owner.db.wielding['both'] = None

        if main_hand == None:
            use_main_hand = True
        elif off_hand == None:
            use_off_hand = True
        else: # Both hands are full.
            if main_wield and off_wield is not None: # Both hands are wielding, prefer main hand to preserve shield.
                use_main_hand = True
                owner_msg = f"You stop wielding and stow away {main_hand.name}."
                others_msg = f"{owner.name} stops wielding and stows away {main_hand.name}."
                owner.db.wielding['main'] = None
                owner.db.hands['main'] = None
            elif main_wield == None:
                use_main_hand = True
                owner.db.wielding['main'] = None
                owner_msg = f"You stow away {main_hand.name} into your inventory."
                others_msg = f"{owner.name} stows away {main_hand.name} into their inventory."
                owner.db.hands['main'] = None
            elif off_wield == None:
                use_off_hand = True
                owner.db.wielding['off'] = None
                owner_msg = f"You stow away {off_hand.name} into your inventory."
                others_msg = f"{owner.name} stows away {off_hand.name} into their inventory."
                owner.db.hands['off'] = None

        if use_main_hand:
            owner.db.hands['main'] = obj
        elif use_off_hand:
            owner.db.hands['off'] = obj

        # TODO: Add an extra occupied inventory slot count.
        # owner.db.inventory_slots['occupied_slots'] +=1

        # Determine the nature of the object's origin.
        owner_msg = f"{owner_msg}\nYou get {obj.name}"
        others_msg = f"{others_msg}\n{owner.name} gets {obj.name}"
        if owner_possess:
            owner_msg = f"{owner_msg} from your inventory"
            others_msg = f"{others_msg} from their inventory"
        if container is not None:
            owner_msg = f"{owner_msg} from {container.name}"
            others_msg = f"{others_msg} from {container.name}"
        owner_msg = f"{owner_msg}."
        others_msg = f"{others_msg}."
        
        # Send out messages.
        owner.msg(owner_msg)
        owner.location.msg_contents(others_msg, exclude=owner)

        # calling at_get hook method
        obj.at_get(owner)

    def stow_object(self, obj):
        owner = self.owner
        main_hand, off_hand = owner.db.hands.values()
        wielding = owner.db.wielding
        main_wield, off_wield, both_wield  = wielding.values()
        
        if obj in [main_hand, off_hand]:
            # If the stowed object is currently wielded, stop wielding it and stow it.
            if obj in [main_wield, off_wield, both_wield]:
                owner.msg(f"You stop wielding {obj.name} and stow it away.")
                owner.location.msg_contents(f"{owner.name} stops wielding {obj.name} and stows it away.", exclude=owner)
                if obj == off_wield:
                    wielding['off'] = None
                elif obj == main_wield:
                    wielding['main'] = None
                else:
                    wielding['both'] = None
            else:
                owner.msg(f"You stow away {obj.name}.")
                owner.location.msg_contents(f"{owner.name} stows away {obj.name}.", exclude=owner)

            if obj == off_hand:
                owner.db.hands['off'] = None
            else:
                owner.db.hands['main'] = None
        elif obj.location == owner.location:
            owner.msg(f"You pick up {obj.name} and stow it away.")
            owner.location.msg_contents(f"{owner.name} picks up {obj.name} and stows it away.", exclude=owner)
            obj.move_to(owner, quiet=True)

        # calling at_get hook method
        obj.at_get(owner)

    def drop_object(self, obj):
        owner = self.owner
        main_hand, off_hand = owner.db.hands.values()
        wielding = owner.db.wielding
        main_wield, off_wield, both_wield  = wielding.values()

        # Call the object script's at_before_drop() method.
        if not obj.at_before_drop(owner):
            return
        
        if obj in [main_hand, off_hand]:
            # If the object is currently wielded, stop wielding it and drop it.
            if obj in [main_wield, off_wield, both_wield]:
                owner.msg(f"You stop wielding {obj.name} and drop it.")
                owner.location.msg_contents(f"{owner.name} stops wielding {obj.name} and drops it.", exclude=owner)
                if off_wield:
                    wielding['off'] = None
                else:
                    wielding['main'], wielding['both'] = None, None
            else:
                owner.msg(f"You drop {obj.name}.")
                owner.location.msg_contents(f"{owner.name} drops {obj.name}.", exclude=owner)
            if obj == off_hand:
                owner.db.hands['off'] = None
            else:
                owner.db.hands['main'] = None
        elif obj.location == owner:
            owner.msg(f"You pull {obj.name} from your inventory and drop it on the ground.")
            owner.location.msg_contents(f"{owner.name} pulls {obj.name} from their inventory and drops it on the ground.", exclude=owner)
        elif obj.location == owner.location:
            owner.msg(f"{obj.name} is already on the ground.")
            return

        obj.move_to(owner.location, quiet=True)

        # Call the object script's at_drop() method.
        obj.at_drop(owner)


    def group_objects(self, objects, obj_loc):
        msg = ''
        inv_stack_objects = []
        qty_stack_objects = []
        stacked_obj_names = gen_mec.comma_separated_string_list(gen_mec.objects_to_strings(objects))

        # Check of every object in list is stackable. Abort if not.
        for obj in objects:
            if not obj.tags.get('stackable'):
                msg = f"{obj} is not able to be grouped!"
                return msg
        
        # Check if all objects in the list have the same name.
        same_name = gen_mec.all_same(gen_mec.objects_to_strings(objects))

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
                if obj.is_typeclass('items.objects.Coin', exact=True):
                    are_coins = True
                else:
                    msg = "You can't group coins with non-coins!"
                    return msg
            if are_coins:
                self.stack_coins(obj_loc, qty_stack_objects, stacked_obj_names)
                msg = f"You group together {stacked_obj_names}."
                return msg

        # Inventory Stackables
        if len(inv_stack_objects) > 1:
            inv_quantity = 0
            if same_name:
                inv_stack = create_object(key=f'a pile of {inv_stack_objects[0].name}es', 
                    typeclass='items.objects.StackInventory', 
                    location=obj_loc)
                if inv_stack:
                    for obj in inv_stack_objects:
                        obj.move_to(inv_stack, quiet=True, move_hooks=False)
                        inv_quantity += 1
                    inv_stack.db.quantity = inv_quantity
                    msg = f"You group together some {inv_stack_objects[0].name}es into a pile."
                    return msg

    def ungroup_objects(self, obj, obj_loc):
        if obj.is_typeclass('items.objects.StackQuantity'):
            if obj.tags.get('coin', category='currency'):
                plat, gold, silver, copper = obj.currency.return_obj_coin(obj)
                multi_coin = 0
                for x in [plat, gold, silver, copper]:
                    if x > 0:
                        multi_coin += 1
                if multi_coin >= 2:
                    if plat > 0:
                        plat_pile = create_object(key='a pile of platinum coins', location=obj_loc,
                                                    typeclass='items.objects.Coin')
                        if plat_pile:
                            plat_pile.db.coin['plat'] = plat
                            obj.db.coin['plat'] = 0
                    if gold > 0:
                        gold_pile = create_object(key='a pile of gold coins', location=obj_loc,
                                                    typeclass='items.objects.Coin')
                        if gold_pile:
                            gold_pile.db.coin['gold'] = gold
                            obj.db.coin['gold'] = 0
                    if silver > 0:
                        silver_pile = create_object(key='a pile of silver coins', location=obj_loc,
                                                    typeclass='items.objects.Coin')
                        if silver_pile:
                            silver_pile.db.coin['silver'] = silver
                            obj.db.coin['silver'] = 0
                    if copper > 0:
                        copper_pile = create_object(key='a pile of copper coins', location=obj_loc,
                                                    typeclass='items.objects.Coin')
                        if copper_pile:
                            copper_pile.db.coin['copper'] = copper
                            obj.db.coin['copper'] = 0
                    msg = f"You ungroup {obj.name} into separate piles of coins."
                    obj.delete()
                    return msg
        elif obj.is_typeclass('items.objects.StackInventory'):
            stack_contents = obj.contents
            for x in stack_contents:
                x.move_to(obj_loc, quiet=True, move_hooks=False)
            msg = f"You ungroup {obj.name}, producing {gen_mec.comma_separated_string_list(gen_mec.objects_to_strings(stack_contents))}."
            obj.delete()
            return msg

    def split_pile(self, split_type, pile, obj_loc, quantity=0, qty_obj=None):
        pile_name = pile.name

        if split_type == 'default':
            # This condition splits the pile as evenly as possible into 2 piles.
            # The original pile always contains the higher quantity of items, if not evenly split.
            pass
        elif split_type == 'from':
            if pile.is_typeclass('items.objects.StackQuantity'):
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
            elif pile.is_typeclass('items.objects.StackInventory'):
                # Object has contents
                qty_obj_names = []

                qty_objects = pile.search(qty_obj, location=pile, quiet=True)
                # Check that there are enough objects in the pile to meet requirements.
                if len(qty_objects) >= quantity:
                    num = 1
                    while num <= quantity:
                        obj = qty_objects.pop()
                        qty_obj_names.append(obj.name)
                        obj.move_to(obj_loc, quiet=True, move_hooks=False)
                        num += 1

                    msg = f"You split"
                    if gen_mec.all_same(qty_obj_names):
                        msg = f"{msg} {quantity} {qty_obj_names[0]}"
                    else:
                        msg = f"{msg} {gen_mec.comma_separated_string_list(qty_obj_names)}"
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

    def stack_coins(self, obj_loc, qty_stack_objects, stacked_obj_names):
        qty_stack = create_object(key=f'a pile of coins', 
                typeclass='items.objects.StackQuantity', 
                location=obj_loc)
        if qty_stack:
            qty_stack.attributes.add('coin', {'plat': 0, 'gold': 0, 'silver': 0, 'copper': 0})
            qty_stack.tags.add('coin', category='currency')
            for obj in qty_stack_objects:
                plat, gold, silver, copper = qty_stack.currency.return_obj_coin(obj)
                qty_stack.currency.add_coin(qty_stack, plat=plat, gold=gold, silver=silver, copper=copper)
                obj.delete()
            return qty_stack
