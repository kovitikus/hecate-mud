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
