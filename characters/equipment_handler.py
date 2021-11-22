"""
Head - Crown/Helmet/Hat
Neck - Necklace/Amulet
Shoulders - Shoulder Pads
Chest - Chest Armor
Arms - Sleeves
Hands - Pair of Gloves
Fingers - Up to 4 Rings
Waist - Belt/Sash
Thighs - Greaves
Calves - Greaves
Feet - Boots/Shoes/Sandals

Bag - Satchel/Backpack/Sack/Bag - Determines maximum inventory slots.

Weapons - Any weapon can be wielded from the inventory or the ground
        Equipped weapons are used automatically if no other is wielded.
        Shields and other offhands can also be equipped.
        Equipped weapons have 1 slot per type of 2H and 1 slot per offhand type.
        2 slots for 1H weapons for dual wielding.
"""

from evennia.prototypes.spawner import spawn
from evennia.utils.evtable import EvTable, EvCell

from misc import generic_str

class EquipmentHandler:
    def __init__(self, owner):
        self.owner = owner

    def _get_equipment(self):
        equipment = self.equipment
        if equipment is None:
            # Get the equipment from the owner's attributes.
            equipment = self.owner.attributes.get('equipment', default=None)
            if equipment is None:
                # The owner has no equipment attribute, create it.
                self.initialize_equipment_attribute()
                equipment = self.owner.attributes.get('equipment')
        return equipment

    def _set_equipment(self, equipment):
        self.equipment = equipment

    def _save_equipment(self):
        self.owner.db.equipment = self.equipment

    def initialize_equipment_attribute(self):
        owner = self.owner
        equip_dict = {'Head': None, 'Neck': None, 'Shoulders': None, 'Chest': None, 'Arms': None,
            'Hands': None, 'Fingers': None, 'Waist': None, 'Thighs': None, 'Calves': None,
            'Feet': None, 'Inventory Container': None,
            'Main Hand Weapon Slot 1': None, 'Main Hand Weapon Slot 2': None,
            'Off-hand Weapon Slot 1': None, 'Off-hand Weapon Slot 2': None
            }
        owner.attributes.add('equipment', equip_dict)

    def generate_starting_equipment(self):
        owner = self.owner
        if owner.db.equipment['Inventory Container'] is None:
            basic_bag = spawn('inventory_bag')
            if basic_bag:
                basic_bag = basic_bag[0]
                basic_bag.move_to(owner)
                self.equipment['Inventory Container'] = basic_bag
                self._save_equipment
                owner.db.inventory_slots['max_slots'] = basic_bag.db.max_slots
    
    def list_equipment(self):
        owner = self.owner
        owner_possessive = generic_str.possessive(owner.key)

        equip_dict = self.equipment

        equipment_header = EvCell(f"{owner_possessive} Equipment", align='c', width=25)
        equipment_table = EvTable(border=None, pad_width=0)
        
        for key, value in equip_dict.items():
            equipment_table.add_row(f"{key} ", f"{value}")

        equipment_table.reformat_column(0, fill_char='.')
        equipment_table.reformat_column(1, pad_left=1, width=20)

        owner.msg(f"{equipment_header}\n{equipment_table}")

    def wield(self, weapon=None):
        owner = self.owner
        equipment = self.equipment

        # Get the owner's current wielding and hand occupancy status.
        main_wield, off_wield, both_wield = self.get_wielding()
        main_hand, off_hand = owner.inv.get_hands()
        main_desc, off_desc = owner.db.hands_desc.values()

        if weapon is None:
            # Check each equipment slot for a mainhand weapon to wield.
            if equipment['Main Hand Weapon Slot 1'] is not None:
                weapon = equipment['Main Hand Weapon Slot 1']
            elif equipment['Main Hand Weapon Slot 2'] is not None:
                weapon = equipment['Main Hand Weapon Slot 2']
            else:
                owner.msg("No suitable weapon could be found to wield!")
                return
        else:
            weapon = owner.search(weapon,
                nofound_string="You must be holding a weapon to wield it.",
                multimatch_string=f"There are more than one {weapon}.")

        # A weapon object has been found. Perform some additional checks on it.
        if not weapon.tags.get('wieldable'):
            owner.msg("That's not a wieldable item.")
            return
        if weapon in [main_wield, off_wield, both_wield]: # Check for an item already wielded.
            owner.msg(f"You are already wielding {weapon.name}.")
            return

        hands_req = weapon.attributes.get('wieldable')

        if weapon not in [main_hand, off_hand]: # Automagically get the object from the inventory.
            owner.inv.force_item_into_hand(weapon, hand=hands_req)
            """
            Decide which hand to put the item in.

            Preference Order
            -------------------
            Prefer the main hand first when unoccupied.
            If main hand is occupied, use the off hand if it is unoccupied.
            Both hands are occupied, prefer dominate hand if not wielding.
            If both hands are occupied anddominate hand is wielding, prefer offhand if not wielding.
            If both hands are occupied and wielding, use the main hand.
            """
            if (not main_hand) or (off_hand and not main_wield) or (off_hand and off_wield):
                hand = 'main'
            else:
                hand = 'off'

            if main_hand and not main_wield:
                owner.msg(f"You stow away {main_hand.name}.")
                owner.location.msg_contents(f"{owner.name} stows away {main_hand.name}.", exclude=owner)
                owner.db.hands['main'] = None
            owner.msg(f"You get {weapon.name} from your inventory.")
            owner.location.msg_contents(f"{owner.name} gets {weapon.name} from their inventory.", exclude=owner)
            owner.db.hands['main'] = weapon
            # Refresh hand variables before the next check.
            main_hand, off_hand = owner.db.hands.values()

        if weapon in [main_hand, off_hand]:
            if hands_req == 1:
                if weapon.tags.get('off_hand'): #For wielding shields.
                    if weapon == main_hand and not main_wield:
                        owner.inv.off_hand(item=weapon)
                    # Offhand item is certainly already in the off hand.
                    owner.msg(f"You wield {weapon.name} in your {off_desc} hand.")
                    owner.location.msg_contents(f"{owner.name} wields {weapon.name} in their {off_desc} hand.", exclude=owner)
                    owner.db.wielding['off'] = weapon
                # Make sure the item is a main hand wield.
                elif weapon == off_hand and not weapon.tags.get('off_hand'): 
                    owner.msg(f"You swap the contents of your hands and wield {weapon.name} in your {main_desc} hand.")
                    owner.location.msg_contents(f"{owner.name} swaps the content of their hands "
                                                    f"and wields {weapon.name} in their {main_desc} hand.", exclude=owner)
                    owner.db.hands['main'] = weapon
                    if main_hand:
                        owner.db.hands['main'] = None
                        owner.db.hands['off'] = weapon
                    owner.db.wielding['main'] = weapon
                elif weapon == main_hand and not inherits_from(weapon, 'items.objects.OffHand'): # Make sure the item is a main hand wield.
                    owner.msg(f"You wield {weapon.name} in your {main_desc} hand.")
                    owner.location.msg_contents(f"{owner.name} wields {weapon.name} in their {main_desc} hand.", exclude=owner)
                    owner.db.wielding['main'] = weapon
            elif hands_req == 2:
                if weapon == off_hand:
                    if main_hand:
                        owner.msg(f"You stow away {main_hand.name}.")
                        owner.location.msg_contents(f"{owner.name} stows away {main_hand}.", exclude=owner)
                        owner.db.hands['main'] = None
                elif weapon == main_hand:
                    if off_hand:
                        owner.msg(f"You stow away {off_hand.name}.")
                        owner.location.msg_contents(f"{owner.name} stows away {off_hand}.", exclude=owner)
                        owner.db.hands['off'] = None
                owner.msg(f"You wield {weapon.name} in both hands.")
                owner.location.msg_contents(f"{owner.name} wields {weapon.name} in both hands.", exclude=owner)
                owner.db.wielding['both'] = weapon
                owner.db.hands['main'] = weapon
        elif weapon.location == owner.location:
            owner.msg(f"You must be carrying a weapon to wield it.")
            return

    def stop_wielding_item(self, item):
        owner = self.owner
        main_wield, off_wield, both_wield = self.wielding.values()
        for looker in owner.location.contents:
            if looker == owner:
                looker.msg(f"You stop wielding {item.get_display_name(looker)}.")
            else:
                looker.msg(f"{owner.get_display_name(looker)} stops wielding "
                    f"{item.get_display_name(looker)}.")
        if item == main_wield:
            self.set_wielding('main')
        elif item == off_wield:
            self.set_wielding('off')
        elif item == both_wield:
            self.set_wielding('both')

    def get_wielding(self, hand=None):
        """
        Returns the requested wielded status of the owner, based on the kwarg provided.
        """
        if self.wielding is None:
            self.wielding = self.owner.attributes.get('wielding')

        if hand is None:
            return self.wielding.values()
        else:
            return self.wielding.get(hand)

    def set_wielding(self, hand, item=None):
        self.wielding[hand] = item
        self._save_wielding()
    
    def _save_wielding(self):
        self.owner.db.wielding = self.wielding
            
