from evennia.utils.utils import variable_from_module

class CharacterClassHandler():
    def __init__(self, owner):
        self.owner = owner

    def add_char_class(self, char_class_choice):
        owner = self.owner
        if owner.attributes.has('char_class'):
            owner.msg("You've already got a character class!")
            return
        else:
            owner.attributes.add('char_class', char_class_choice)
        
        char_class_dic = variable_from_module("characters.character_classes", variable=char_class_choice)

        for skillset in char_class_dic['skillsets']:
            owner.skill.learn_skillset(skillset)
