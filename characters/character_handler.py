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
