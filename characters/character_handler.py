from evennia.utils.utils import variable_from_module

class CharacterHandler():
    """
    This handler contains general behaviors, tasks, and mechanics of the character class.
    """
    def __init__(self, owner):
        self.owner = owner
        self.main_class_dic = variable_from_module("characters.character_classes", variable='main_classes')

    def add_char_class(self, char_class_choice):
        """
        Responsible for properly adding a character class to a character.

        It uses the information contained within characters.character_classes
        """
        owner = self.owner
        if owner.tags.get(category='char_class'):
            owner.msg("You've already got a character class!")
            return
        
        # Pull the proper dictionary from the char_classes dictionary.
        char_class_dic = self.main_class_dic[char_class_choice]
        char_armor_type = char_class_dic.get('char_armor_type')

        owner.tags.add(char_class_choice, category='char_class')
        owner.tags.add(char_armor_type, category='char_armor_type')

        for skillset in char_class_dic['skillsets']:
            owner.skill.learn_skillset(skillset)

    def init_char_stats(self):
        """
        Documentation:
            https://github.com/kovitikus/hecate/blob/master/docs/hecate/character_statistics.md
        """
        owner = self.owner

        starting_stats = {'vigor': 115, 'tenacity': 115, 'celerity': 115, 'awareness': 115,
            'aptitude': 115, 'sanity': 115}

        owner.attributes.add('stats', starting_stats)
        owner.attributes.add('hp', {'max_hp': 100, 'current_hp': 100})
        owner.attributes.add('energy', {'max_energy': 100, 'current_energy': 100})
        owner.attributes.add('armor', 0)
        owner.attributes.add('hunger', 0)
        owner.attributes.add('thirst', 0)
        owner.attributes.add('resistances', {'fire': 0, 'ice': 0, 'light': 0, 'shadow': 0,
            'poison': 0, 'arcane': 0})
