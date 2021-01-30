from evennia.utils.evtable import EvTable
from world import general_mechanics as gen_mec

class InventoryHandler():
    def __init__(self, owner):
        self.owner = owner

        self.inventory_contents = owner.contents

    def inhand(self):
        owner = self.owner

        main_wield, off_wield, both_wield  = owner.db.wielding.values()
        main_hand, off_hand = owner.db.hands.values()
        main_desc, off_desc = owner.db.hands_desc.values()

        if off_hand:
            off_item = off_hand.name
        else:
            off_item = 'nothing'

        if main_hand:
            main_item = main_hand.name
        else:
            main_item = 'nothing'

        if not off_hand and not main_hand:
            owner.msg(f"Your hands are empty.")
            return
        
        
        if off_wield and not main_wield:
            owner.msg(f"You are holding {main_item} in your {main_desc} hand and wielding {off_item} in your {off_desc} hand .")
        elif main_wield and not off_wield:
            owner.msg(f"You are wielding {main_item} in your {main_desc} hand and holding {off_item} in your {off_desc} hand.")
        elif off_wield and main_wield:
            owner.msg(f"You are wielding {main_item} in your {main_desc} hand and {off_item} in your {off_desc} hand.")
        elif both_wield:
            owner.msg(f"You are wielding {both_wield.name} in both hands.")
        else:
            owner.msg(f"You are holding {main_item} in your {main_desc} hand and {off_item} in your {off_desc} hand.")

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
                # Show items in hands.
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
