from evennia import create_object
from world import adjectives

def main(self, raw_string, **kwargs):
    #Initilize values
    attrs = {'gender': None, 'height': None, 'build': None, 'face': None, 'eye_color': None, 'nose': None, 'lips': None,
            'chin': None, 'skin_color': None, 'hair_color': None, 'texture': None, 'length': None, 'style': None}
    prev = kwargs.get('prev')
    if not prev:
        self.ndb._menutree.attr = attrs
        self.ndb._menutree.skills = {}

    # self.ndb._menutree.gender
    # self.ndb._menutree.height
    # self.ndb._menutree.build
    # self.ndb._menutree.face
    # self.ndb._menutree.eye_color
    # self.ndb._menutree.nose
    # self.ndb._menutree.lips
    # self.ndb._menutree.chin
    # self.ndb._menutree.skin
    # self.ndb._menutree.hair_color
    # self.ndb._menutree.texture
    # self.ndb._menutree.length
    # self.ndb._menutree.style

    text = 'Please create your character.'
    options = (
        {"key": ("1", "name"),
        "desc": "Name your character.",
        "goto": "enter_name"},
        {"key": ("2", "appearance", "appear"),
        "desc": "Create your character's appearance.",
        "goto": "appearance"},
        {"key": ("3", "finish", "create"),
        "desc": "Finish and create.",
        "goto": _create_char}
    )
    return text, options

def enter_name(self, raw_string, **kwargs):
    # Check for a previous name.
    prev_entry = kwargs.get("prev_entry")

    if prev_entry:
        text = f"Current Name: {prev_entry}.\nEnter another name or press RETURN to accept."
    else:
        text = "Enter your character's name or press RETURN to abort."
    
    options = {"key": "_default",
                "goto": (_set_name, {"prev_entry": prev_entry})}
    return text, options

def _set_name(self, raw_string, **kwargs):
    inp = raw_string.strip()

    prev_entry = kwargs.get("prev_entry")

    if not inp:
        # A blank input either means OK or Abort
        if prev_entry:
            self.ndb._menutree.name = prev_entry
            self.msg(f"Your character's name has been set to |c{prev_entry}|n.")
            return "main"
        else:
            self.msg("Aborted.")
            return "main"
    else:
        #Re-run old node, but pass in the name given.
        return None, {"prev_entry": inp}

def appearance(self, raw_string, **kwargs):
    text = "Please choose."
    options = (
    {"key": ("1", "gender"),
    "desc": f"Set your character's gender.\n        Currently: |c{self.ndb._menutree.attr.get('gender')}|n",
    "goto": "gender"},
    {"key": ("2", "height"),
    "desc": f"Set your character's height.\n        Currently: |c{self.ndb._menutree.attr.get('height')}|n",
    "goto": "height"},
    {"key": ("3", "build"),
    "desc": f"Set your character's build.\n        Currently: |c{self.ndb._menutree.attr.get('build')}|n",
    "goto": "build"},
    {"key": ("4", "face"),
    "desc": f"Set your character's face type.\n        Currently: |c{self.ndb._menutree.attr.get('face')}|n",
    "goto": "face"},
    {"key": ("5", "eye"),
    "desc": f"Set your character's eye color.\n        Currently: |c{self.ndb._menutree.attr.get('eye_color')}|n",
    "goto": "eye_color"},
    {"key": ("6", "nose"),
    "desc": f"Set your character's nose.\n        Currently: |c{self.ndb._menutree.attr.get('nose')}|n",
    "goto": "nose"},
    {"key": ("7", "lips"),
    "desc": f"Set your character's lips.\n        Currently: |c{self.ndb._menutree.attr.get('lips')}|n",
    "goto": "lips"},
    {"key": ("8", "chin"),
    "desc": f"Set your character's chin.\n        Currently: |c{self.ndb._menutree.attr.get('chin')}|n",
    "goto": "chin"},
    {"key": ("9", "skin"),
    "desc": f"Set your character's skin color.\n        Currently: |c{self.ndb._menutree.attr.get('skin_color')}|n",
    "goto": "skin_color"},
    {"key": ("10", "hair"),
    "desc": f"Set your character's hair color.\n        Currently: |c{self.ndb._menutree.attr.get('hair_color')}|n",
    "goto": "hair_color"},
    {"key": ("11", "texture"),
    "desc": f"Set your character's hair texture.\n        Currently: |c{self.ndb._menutree.attr.get('texture')}|n",
    "goto": "texture"},
    {"key": ("12", "length"),
    "desc": f"Set your character's hair length.\n        Currently: |c{self.ndb._menutree.attr.get('length')}|n",
    "goto": "length"},
    {"key": ("13", "style"),
    "desc": f"Set your character's hair style.\n        Currently: |c{self.ndb._menutree.attr.get('style')}|n",
    "goto": "style"},
    {"key": ("14", "back", "main"),
    "desc": "Back to main menu.",
    "goto": ("main", {'prev': 'prev'})}     
    )
    return text, options

def _set_appearance(self, raw_string, **kwargs):
    prev = kwargs.get('prev_node')
    choice = kwargs.get('choice')

    if prev == 'gender':
        self.ndb._menutree.attr['gender'] = choice
        return 'appearance'
    if prev == 'height':
        self.ndb._menutree.attr['height'] = choice
        return 'appearance'
    if prev == 'build':
        self.ndb._menutree.attr['build'] = choice
        return 'appearance'
    if prev == 'face':
        self.ndb._menutree.attr['face'] = choice
        return 'appearance'
    if prev == 'eye_color':
        self.ndb._menutree.attr['eye_color'] = choice
        return 'appearance'
    if prev == 'nose':
        self.ndb._menutree.attr['nose'] = choice
        return 'appearance'
    if prev == 'lips':
        self.ndb._menutree.attr['lips'] = choice
        return 'appearance'
    if prev == 'chin':
        self.ndb._menutree.attr['chin'] = choice
        return 'appearance'
    if prev == 'skin_color':
        self.ndb._menutree.attr['skin_color'] = choice
        return 'appearance'
    if prev == 'hair_color':
        self.ndb._menutree.attr['hair_color'] = choice
        return 'appearance'
    if prev == 'texture':
        self.ndb._menutree.attr['texture'] = choice
        return 'appearance'
    if prev == 'length':
        self.ndb._menutree.attr['length'] = choice
        return 'appearance'
    if prev == 'style':
        self.ndb._menutree.attr['style'] = choice
        return 'appearance'

    return 'appearance'

def gender(self, raw_string, **kwargs):
    text = "Choose your gender."
    options = []
    for g in adjectives._FIGURE['gender']:
        options.append({"desc": f"{g}",
                        "goto": (_set_appearance, {'prev_node': 'gender', 'choice': f'{g}'})})
    return text, options

def height(self, raw_string, **kwargs):
    text = 'Choose your height.'
    options = []
    for g in adjectives._FIGURE['height']:
        options.append({"desc": f"{g}",
                        "goto": (_set_appearance, {'prev_node': 'height', 'choice': f'{g}'})})
    return text, options

def build(self, raw_string, **kwargs):
    text = 'Choose your build.'
    options = []
    for g in adjectives._FIGURE['build']:
        options.append({"desc": f"{g}",
                        "goto": (_set_appearance, {'prev_node': 'build', 'choice': f'{g}'})})
    return text, options

def face(self, raw_string, **kwargs):
    text = 'Choose an adjective that describes your face.'
    options = []
    for g in adjectives._FACIAL['face']:
        options.append({"desc": f"{g}",
                        "goto": (_set_appearance, {'prev_node': 'face', 'choice': f'{g}'})})
    return text, options

def eye_color(self, raw_string, **kwargs):
    text = 'Choose your eye color.'
    options = []
    for g in adjectives._FACIAL['eye_color']:
        options.append({"desc": f"{g}",
                        "goto": (_set_appearance, {'prev_node': 'eye_color', 'choice': f'{g}'})})
    return text, options

def nose(self, raw_string, **kwargs):
    text = 'Choose and adjective that describes your nose.'
    options = []
    for g in adjectives._FACIAL['nose']:
        options.append({"desc": f"{g}",
                        "goto": (_set_appearance, {'prev_node': 'nose', 'choice': f'{g}'})})
    return text, options

def lips(self, raw_string, **kwargs):
    text = 'Choose an adjective that describes your lips.'
    options = []
    for g in adjectives._FACIAL['lips']:
        options.append({"desc": f"{g}",
                        "goto": (_set_appearance, {'prev_node': 'lips', 'choice': f'{g}'})})
    return text, options

def chin(self, raw_string, **kwargs):
    text = 'Choose an adjective that describes your chin.'
    options = []
    for g in adjectives._FACIAL['chin']:
        options.append({"desc": f"{g}",
                        "goto": (_set_appearance, {'prev_node': 'chin', 'choice': f'{g}'})})
    return text, options

def skin_color(self, raw_string, **kwargs):
    text = 'Choose your skin color.'
    options = []
    for g in adjectives._FACIAL['skin_color']:
        options.append({"desc": f"{g}",
                        "goto": (_set_appearance, {'prev_node': 'skin_color', 'choice': f'{g}'})})
    return text, options

def hair_color(self, raw_string, **kwargs):
    text = 'Choose your hair color.'
    options = []
    for g in adjectives._HAIR['hair_color']:
        options.append({"desc": f"{g}",
                        "goto": (_set_appearance, {'prev_node': 'hair_color', 'choice': f'{g}'})})
    return text, options

def texture(self, raw_string, **kwargs):
    text = 'Choose an adjective that describes your hair\'s texture.'
    options = []
    for g in adjectives._HAIR['texture']:
        options.append({"desc": f"{g}",
                        "goto": (_set_appearance, {'prev_node': 'texture', 'choice': f'{g}'})})
    return text, options

def length(self, raw_string, **kwargs):
    text = 'Choose your hair\'s length.'
    options = []
    for g in adjectives._HAIR['length']:
        options.append({"desc": f"{g}",
                        "goto": (_set_appearance, {'prev_node': 'length', 'choice': f'{g}'})})
    return text, options

def style(self, raw_string, **kwargs):
    text = 'Choose your hairstyle.'
    options = []
    for g in adjectives._HAIR['style']:
        options.append({"desc": f"{g}",
                        "goto": (_set_appearance, {'prev_node': 'style', 'choice': f'{g}'})})
    return text, options

def _create_char(self, raw_string, **kwargs):
    name = self.ndb._menutree.name
    attr = self.ndb._menutree.attr

    #Figure Attributes
    gender = attr.get('gender')
    height = attr.get('height')
    build = attr.get('build')

    #Facial Attributes
    face = attr.get('face')
    eye_color = attr.get('eye_color')
    nose = attr.get('nose')
    lips = attr.get('lips')
    chin = attr.get('chin')
    skin_color = attr.get('skin_color')

    #Hair Attributes
    hair_color = attr.get('hair_color')
    texture = attr.get('texture')
    length = attr.get('length')
    style = attr.get('style')


    # Check for chars attribute and initilize if none.
    if not self.attributes.get("chars"):
        self.db.chars = {}
    chars_len = len(self.db.chars) + 1
    self.msg("You currently have a total of {chars_len} characters.")

    #Add the new character object to the chars attribute as next number in the character list.
    self.db.chars[str(chars_len)] = create_object(typeclass="typeclasses.characters.Player_Character", key=name, home=None,
    attributes=[('figure', {'gender': gender, 'height': height, 'build': build}),
                ('facial', {'face': face, 'eye_color': eye_color, 'nose': nose, 'lips': lips, 'chin': chin, 'skin_color': skin_color}),
                ('hair', {'hair_color': hair_color, 'texture': texture, 'length': length, 'style': style})])
    self.msg("|gChargen completed!|n")
    return "exit"

def exit(self, raw_string, **kwargs):
    options = None
