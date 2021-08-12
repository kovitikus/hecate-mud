
from evennia.utils.utils import variable_from_module

class StatHandler:
    def __init__(self, owner):
        self.owner = owner
        self.main_class_dic = variable_from_module("characters.character_classes", variable='main_classes')
        self.default_character_base_hp = variable_from_module("world.hecate_settings",
            variable='DEFAULT_CHARACTER_BASE_HP')

    def char_attributes(self):
        '''
        https://github.com/kovitikus/hecate/blob/master/docs/hecate/character_statistics.md
        '''
        pass

    def set_base_hp(self):
        """
        This method retrieves the base HP of a character (owner) and then subsequently sets
        the returned base health value to the character's HP dictionary attribute.
        """
        owner = self.owner
        base_hp = self.calculate_base_hp()
        if not base_hp:
            owner.msg("|rWARNING! Could not set the character base HP with the stat handler!|n")
            return

        char_hp_dict = owner.attributes.get('hp', None)
        if char_hp_dict:
            owner.db.hp['base_hp'] = base_hp

    def calculate_base_hp(self):
        """
        Checks the hecate_settings module for the default base HP and then adds to that the class
        choice base HP value.

        Returns:
            base_hp (int): The final base health value for the character (owner).
        """
        owner = self.owner
        base_hp = self.default_character_base_hp
        char_class = None

        # Aquire and add the character class base HP value.
        if owner.tags.get(category='char_class'):
            char_class = owner.tags.get(category='char_class')
            char_class_dict = self.main_class_dic.get(char_class, None)
            if char_class_dict:
                class_base_hp_bonus = char_class_dict.get('base_hp_bonus', 0)
                base_hp += class_base_hp_bonus

        return int(base_hp)

    def set_max_hp(self):
        """
        This method calls upon another to calculate the maximum HP of a character and then
        subsequently sets the returned maximum health value to the character's HP dictionary attribute.
        """
        owner = self.owner
        max_hp = self.calculate_max_hp()
        if not max_hp:
            owner.msg("|rWARNING! Could not set the character max HP with the stat handler!|n")
            return
        char_hp_dict = owner.attributes.get('hp', None)
        if char_hp_dict:
            owner.db.hp['max_hp'] = max_hp
        else:
            owner.msg("|rWARNING! Could not find the character HP dictionary attribute|n "
                "|rwith the stat handler!|n")
        
    def calculate_max_hp(self):
        owner = self.owner
        max_hp = 0
        vigor_hp_multiplier = 0.2
        tenacity_hp_multiplier = 1.0

        base_hp = owner.attributes.get('hp').get('base_hp')
        vigor = owner.attributes.get('stats').get('vigor')
        tenacity = owner.attributes.get('stats').get('tenacity')

        bonus_vigor_hp = base_hp * (vigor * vigor_hp_multiplier)
        bonus_tenacity_hp = base_hp * (tenacity * tenacity_hp_multiplier)
        max_hp = base_hp + bonus_vigor_hp + bonus_tenacity_hp

        return int(max_hp)
