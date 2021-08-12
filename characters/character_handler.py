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

    def create_desc(self):
        """
        Dynamically generates a character's description.

        The description is broken up into 3 sections, allowing for some to be ommitted.
        This will become useful in regards to clothing or equipment that may obscure parts
        of a character's description.

        If a character's figure exists, it will always be shown.

        Returns:
            desc (string): The final string that represents the character's description.
        """
        owner = self.owner
        desc = "You see a featureless entity."

        figure = owner.attributes.get('figure', default=None)
        facial = owner.attributes.get('facial', default=None)
        hair = owner.attributes.get('hair', default=None)

        if figure:
            height = figure.get('Height')
            build = figure.get('Build')
            sex = figure.get('Gender')

            # "You see a <height> <build> <gender>."
            gender = ('man' if sex == 'male' else 'woman')
            desc = f"You see a {height} {build} {gender}. "

            # Only add facial and hair descriptions if the character has a figure.
            if facial:
                eye_color = facial.get('Eye Color')
                nose = facial.get('Nose')
                lips = facial.get('Lips')
                chin = facial.get('Chin')
                face = facial.get('Face')
                skin_color = facial.get('Skin Color')

                #   "He has <color> eyes set above an <shape> nose, <shape> lips and a <shape> chin
                #   in a <shape> <color> face."
                gender = ('He' if sex == 'male' else 'She')
                desc = (f"{desc}{gender} has {eye_color} eyes set above a {nose} nose, "
                        f"{lips} lips and a {chin} chin in a {face} {skin_color} face. ")

            if hair:
                length = hair.get('Hair Length')
                texture = hair.get('Hair Texture')
                hair_color = hair.get('Hair Color')
                style = hair.get('Hair Style')

                # "<gender> has <length> <texture> <color> hair <style>."
                if length == 'bald':
                    desc = f"{desc}{gender} is {length}. "
                else:
                    desc = f"{desc}{gender} has {length} {texture} {hair_color} hair {style}. "

        return desc
