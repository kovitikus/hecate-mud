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

    def initialize_equipment_attribute(self):
        owner = self.owner
        equip_dict = {'Head': None, 'Neck': None, 'Shoulders': None, 'Chest': None, 'Arms': None,
            'Hands': None, 'Fingers': None, 'Waist': None, 'Thighs': None, 'Calves': None,
            'Feet': None, 'Inventory Container': None}
        owner.attributes.add('equipment', equip_dict)

    def generate_starting_equipment(self):
        owner = self.owner
        if owner.attributes.has('equipment'):
            if owner.db.equipment['Inventory Container'] == None:
                basic_bag = spawn('inventory_bag')
                if basic_bag:
                    basic_bag = basic_bag[0]
                    basic_bag.move_to(owner)
                    owner.db.equipment['Inventory Container'] = basic_bag
                    owner.db.inventory_slots['max_slots'] = basic_bag.db.max_slots
    
    def list_equipment(self):
        owner = self.owner
        owner_possessive = generic_str.possessive(owner.key)

        if owner.attributes.has('equipment'):
            equip_dict = owner.attributes.get('equipment')
        else:
            owner.msg("You have no equipment!")
            return

        equipment_header = EvCell(f"{owner_possessive} Equipment", align='c', width=25)
        equipment_table = EvTable(border=None, pad_width=0)
        
        for key, value in equip_dict.items():
            equipment_table.add_row(f"{key} ", f"{value}")

        equipment_table.reformat_column(0, fill_char='.')
        equipment_table.reformat_column(1, pad_left=1, width=20)

        owner.msg(f"{equipment_header}\n{equipment_table}")
