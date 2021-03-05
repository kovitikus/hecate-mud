from evennia.prototypes.spawner import spawn

class EquipmentHandler:
    def __init__(self, owner):
        self.owner = owner

    def generate_equipment(self):
        '''
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
        '''
        owner = self.owner
        if owner.attributes.has('equipment'):
            if owner.db.equipment['inventory_container'] == None:
                basic_bag = spawn('inventory_bag')
                if basic_bag:
                    basic_bag = basic_bag[0]
                    basic_bag.move_to(owner)
                    owner.db.equipment['inventory_container'] = basic_bag
                    owner.db.inventory_slots['max_slots'] = basic_bag.db.max_slots
    
    def list_equipment(self):
        owner = self.owner
        if owner.attributes.has('equipment'):
            equip_dic = owner.attributes.get('equipment')
        else:
            owner.msg("You have no equipment!")
            return

        head = equip_dic.get('head')
        neck = equip_dic.get('neck')
        shoulders = equip_dic.get('shoulders')
        chest = equip_dic.get('chest')
        arms = equip_dic.get('arms')
        hands = equip_dic.get('hands')
        fingers = equip_dic.get('fingers')
        waist = equip_dic.get('waist')
        thighs = equip_dic.get('thighs')
        calves = equip_dic.get('calves')
        feet = equip_dic.get('feet')
        inventory_container = equip_dic.get('inventory_container')

        owner.msg(f"""
        ==== Equipment ====
        Head: {head}
        Neck: {neck}
        Shoulders: {shoulders}
        Chest: {chest}
        Arms: {arms}
        Hands: {hands}
        Fingers: {fingers}
        Waist: {waist}
        Thighs: {thighs}
        Calves: {calves}
        Feet: {feet}
        Inventory Container: {inventory_container}
        """)
