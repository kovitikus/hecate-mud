
from evennia.utils.utils import variable_from_module

class StatHandler:
    def __init__(self, owner):
        self.owner = owner
        self.main_class_dict = variable_from_module("characters.character_classes", variable='main_classes')
        self.default_character_base_health = variable_from_module("world.hecate_settings",
            variable='DEFAULT_CHARACTER_BASE_HEALTH')
        self.default_character_base_energy = variable_from_module("world.hecate_settings",
            variable='DEFAULT_CHARACTER_BASE_ENERGY')

    def set_base_health(self):
        """
        This method retrieves the base health of a character (owner) and then subsequently sets
        the returned base health value to the character's health dictionary attribute.
        """
        owner = self.owner
        base_health = self.calculate_base_health()
        if not base_health:
            owner.msg("|rWARNING! Could not set the character base health with the stat handler!|n")
            return

        char_health_dict = owner.attributes.get('health', None)
        if char_health_dict:
            owner.db.health['base_health'] = base_health
    def calculate_base_health(self):
        """
        Checks the hecate_settings module for the default base health and then adds to that the class
        choice base health value.

        Returns:
            base_health (int): The final base health value for the character (owner).
        """
        owner = self.owner
        base_health = self.default_character_base_health
        char_class = None

        # Aquire and add the character class base health value.
        if owner.tags.get(category='char_class'):
            char_class = owner.tags.get(category='char_class')
            char_class_dict = self.main_class_dict.get(char_class, None)
            if char_class_dict:
                class_base_health_bonus = char_class_dict.get('base_health_bonus', 0)
                base_health += class_base_health_bonus

        return int(base_health)

    def set_max_health(self):
        """
        This method calls upon another to calculate the maximum health of a character and then
        subsequently sets the returned maximum health value to the character's health dictionary attribute.
        """
        owner = self.owner
        max_health = self.calculate_max_health()
        if not max_health:
            owner.msg("|rWARNING! Could not set the character max health with the stat handler!|n")
            return
        char_health_dict = owner.attributes.get('health', None)
        if char_health_dict:
            owner.db.health['max_health'] = max_health
        else:
            owner.msg("|rWARNING! Could not find the character health dictionary attribute|n "
                "|rwith the stat handler!|n")
    def calculate_max_health(self):
        owner = self.owner
        max_health = 0
        vigor_health_multiplier = 0.002 # 0.2%
        tenacity_health_multiplier = 0.01 # 1%

        base_health = owner.attributes.get('health').get('base_health')
        vigor = owner.attributes.get('stats').get('vigor')
        tenacity = owner.attributes.get('stats').get('tenacity')

        bonus_vigor_health = base_health * (vigor * vigor_health_multiplier)
        bonus_tenacity_health = base_health * (tenacity * tenacity_health_multiplier)
        max_health = base_health + bonus_vigor_health + bonus_tenacity_health

        return int(max_health)

    def set_base_energy(self):
        """
        This method retrieves the base energy of a character (owner) and then subsequently sets
        the returned base energy value to the character's energy dictionary attribute.
        """
        owner = self.owner
        base_energy = self.calculate_base_energy()
        if not base_energy:
            owner.msg("|rWARNING! Could not set the character base energy with the stat handler!|n")
            return

        char_energy_dict = owner.attributes.get('energy', None)
        if char_energy_dict:
            owner.db.energy['base_energy'] = base_energy
    def calculate_base_energy(self):
        """
        Checks the hecate_settings module for the default base energy and then adds to that the class
        choice base energy value.

        Returns:
            base_energy (int): The final base energy value for the character (owner).
        """
        owner = self.owner
        base_energy = self.default_character_base_energy
        char_class = None

        # Aquire and add the character class base energy value.
        if owner.tags.get(category='char_class'):
            char_class = owner.tags.get(category='char_class')
            char_class_dict = self.main_class_dict.get(char_class, None)
            if char_class_dict:
                class_base_energy_bonus = char_class_dict.get('base_energy_bonus', 0)
                base_energy += class_base_energy_bonus

        return int(base_energy)

    def set_max_energy(self):
        """
        This method calls upon another to calculate the maximum energy of a character and then
        subsequently sets the returned maximum energy value to the character's energy dictionary attribute.
        """
        owner = self.owner
        max_energy = self.calculate_max_energy()
        if not max_energy:
            owner.msg("|rWARNING! Could not set the character max energy with the stat handler!|n")
            return
        char_energy_dict = owner.attributes.get('energy', None)
        if char_energy_dict:
            owner.db.energy['max_energy'] = max_energy
        else:
            owner.msg("|rWARNING! Could not find the character energy dictionary attribute|n "
                "|rwith the stat handler!|n")
    def calculate_max_energy(self):
        owner = self.owner
        max_energy = 0
        vigor_energy_multiplier = 0.01 # 1%
        tenacity_energy_multiplier = 0.002 # 0.2%

        base_energy = owner.attributes.get('energy').get('base_energy')
        vigor = owner.attributes.get('stats').get('vigor')
        tenacity = owner.attributes.get('stats').get('tenacity')

        bonus_vigor_energy = base_energy * (vigor * vigor_energy_multiplier)
        bonus_tenacity_energy = base_energy * (tenacity * tenacity_energy_multiplier)
        max_energy = base_energy + bonus_vigor_energy + bonus_tenacity_energy

        return int(max_energy)
