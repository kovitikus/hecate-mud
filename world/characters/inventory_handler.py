from evennia.utils.evtable import EvTable
from world import general_mechanics as gen_mec

class InventoryHandler():
    def __init__(self, owner):
        self.owner = owner

        self.inventory_contents = owner.contents

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

    def get_inventory(self, arg_type):
        owner = self.owner
        items = owner.contents
        main_hand, off_hand = owner.db.hands.values()
        equip_items = owner.db.equipment.values()

        # Remove hands and append all other items to a new list.
        filtered_items = []
        for i in items:
            if i not in [main_hand, off_hand]:
                if i not in equip_items:
                    filtered_items.append(i)

        if not filtered_items:
            string = "Your inventory is empty."
        else:
            # if arg_type == 0:
                # Generate summary
                # Count the number of items in the inventory.
                # Show the maximum number of inventory slots.
                # Show each category that has an item and how many items are in the category
                # Show currency.
            if arg_type == 1:
                table = EvTable(border="header")
                string = self.get_all_items(filtered_items, table)
            else:
                final_list = self.get_inv_final_list(filtered_items, arg_type)

                table = EvTable(border="header")
                for item in final_list:
                    table.add_row(f"|C{item.name}|n {item.db.desc or ''}")
                
                category_string = self.get_category_string(arg_type)

                string = f"|wYou are carrying:\n{category_string}\n{table}"
        # Add currency
        string = f"{string}\n{gen_mec.return_currency(owner)}"
        owner.msg(string)
    
    def get_inv_final_list(self, filtered_items, arg_type):
        final_list = []
        for item in filtered_items:
            if arg_type == 2 and item.tags.get('favorite'):
                final_list.append(item)
            elif arg_type == 3 and item.tags.get('weapon'):
                final_list.append(item)
            elif arg_type == 4 and item.tags.get('armor'):
                final_list.append(item)
            elif arg_type == 5 and item.tags.get('clothing'):
                final_list.append(item)
            elif arg_type == 6 and item.tags.get('container'):
                final_list.append(item)
            elif arg_type == 7 and item.tags.get('jewelry'):
                final_list.append(item)
            elif arg_type == 8 and item.tags.get('relic'):
                final_list.append(item)
            elif arg_type == 9 and item.tags.get('consumable'):
                final_list.append(item)
            elif arg_type == 10 and item.tags.get('quest'):
                final_list.append(item)
            elif arg_type == 11 and item.tags.get('craft'):
                final_list.append(item)
            elif arg_type == 12:
                final_list.append(item)
        return final_list

    def get_category_string(self, arg_type):
        if arg_type == 0:
            category_string = '|cSummary:|n'
        elif arg_type == 1:
            category_string = '|cAll Items:|n'
        elif arg_type == 2:
            category_string = '|cFavorites:|n'
        elif arg_type == 3:
            category_string = '|cWeapons:|n'
        elif arg_type == 4:
            category_string = '|cArmor:|n'
        elif arg_type == 5:
            category_string = '|cClothing:|n'
        elif arg_type == 6:
            category_string = '|cContainers:|n'
        elif arg_type == 7:
            category_string = '|cJewelry:|n'
        elif arg_type == 8:
            category_string = '|cRelics:|n'
        elif arg_type == 9:
            category_string = '|cConsumables:|n'
        elif arg_type == 10:
            category_string = '|cQuest Items:|n'
        elif arg_type == 11:
            category_string = '|cCrafting Materials:|n'
        elif arg_type == 12:
            category_string = '|cMisc.|n'
        return category_string

    def get_all_items(self, filtered_items, table):
        fav_list = []
        weap_list = []
        arm_list = []
        cloth_list = []
        contain_list = []
        jewel_list = []
        relic_list = []
        consume_list = []
        quest_list = []
        craft_list = []
        misc_list = []

        # Sort all items based on category into appropriate lists.
        for item in filtered_items:
            if item.tags.get('favorite'):
                fav_list.append(item)
            elif item.tags.get('weapon'):
                weap_list.append(item)
            elif item.tags.get('armor'):
                arm_list.append(item)
            elif item.tags.get('clothing'):
                cloth_list.append(item)
            elif item.tags.get('container'):
                contain_list.append(item)
            elif item.tags.get('jewelry'):
                jewel_list.append(item)
            elif item.tags.get('relic'):
                relic_list.append(item)
            elif item.tags.get('consumable'):
                consume_list.append(item)
            elif item.tags.get('quest'):
                quest_list.append(item)
            elif item.tags.get('craft'):
                craft_list.append(item)
            else:
                misc_list.append(item)

        # Generate table rows for each populated list based on category.
        if fav_list:
            category_string = self.get_category_string(2)
            table.add_row(f"{category_string}")
            for item in fav_list:
                table.add_row(f"|C{item.name}|n {item.db.desc or ''}")
        if weap_list:
            category_string = self.get_category_string(3)
            table.add_row(f"{category_string}")
            for item in weap_list:
                table.add_row(f"|C{item.name}|n {item.db.desc or ''}")
        if arm_list:
            category_string = self.get_category_string(4)
            table.add_row(f"{category_string}")
            for item in arm_list:
                table.add_row(f"|C{item.name}|n {item.db.desc or ''}")
        if cloth_list:
            category_string = self.get_category_string(5)
            table.add_row(f"{category_string}")
            for item in cloth_list:
                table.add_row(f"|C{item.name}|n {item.db.desc or ''}")
        if contain_list:
            category_string = self.get_category_string(6)
            table.add_row(f"{category_string}")
            for item in contain_list:
                table.add_row(f"|C{item.name}|n {item.db.desc or ''}")
        if jewel_list:
            category_string = self.get_category_string(7)
            table.add_row(f"{category_string}")
            for item in jewel_list:
                table.add_row(f"|C{item.name}|n {item.db.desc or ''}")
        if relic_list:
            category_string = self.get_category_string(8)
            table.add_row(f"{category_string}")
            for item in relic_list:
                table.add_row(f"|C{item.name}|n {item.db.desc or ''}")
        if consume_list:
            category_string = self.get_category_string(9)
            table.add_row(f"{category_string}")
            for item in consume_list:
                table.add_row(f"|C{item.name}|n {item.db.desc or ''}")
        if quest_list:
            category_string = self.get_category_string(10)
            table.add_row(f"{category_string}")
            for item in quest_list:
                table.add_row(f"|C{item.name}|n {item.db.desc or ''}")
        if craft_list:
            category_string = self.get_category_string(11)
            table.add_row(f"{category_string}")
            for item in craft_list:
                table.add_row(f"|C{item.name}|n {item.db.desc or ''}")
        if misc_list:
            category_string = self.get_category_string(12)
            table.add_row(f"{category_string}")
            for item in misc_list:
                table.add_row(f"|C{item.name}|n {item.db.desc or ''}")
        string = f"|wYou are carrying:\n{table}"
        return string
