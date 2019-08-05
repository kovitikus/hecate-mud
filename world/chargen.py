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
            return ("main", {'prev': 'prev'})
        else:
            self.msg("Aborted.")
            return ("main", {'prev': 'prev'})
    else:
        #Re-run old node, but pass in the name given.
        return None, {"prev_entry": inp}

def appearance(self, raw_string, **kwargs):
    get = self.ndb._menutree.attr.get
    text = "Please choose."
    options = (
    {"key": ("1", "figure"),
    "desc": f"Set your character's figure.\nGender: |c{get('gender')}|n Height: |c{get('height')}|n Build: |c{get('build')}|n\n",
    "goto": "gender"},
    {"key": ("2", "face"),
    "desc": f"Set your character's facial attributes.\nFace Shape: |c{get('face')}|n Eye Color: |c{get('eye_color')}|n Nose: |c{get('nose')}|n Lips: |c{get('lips')}|n Chin: |c{get('chin')}|n Skin Color: |c{get('skin_color')}|n\n",
    "goto": "face"},
    {"key": ("3", "hair"),
    "desc": f"Set your character's hair.\nLength: |c{get('length')}|n Color: |c{get('hair_color')}|n Texture: |c{get('texture')}|n Style: |c{get('style')}|n\n",
    "goto": "length"},
    {"key": ("4", "back", "main"),
    "desc": "Back to main menu.",
    "goto": ("main", {'prev': 'prev'})})
    return text, options

def _set_appearance(self, raw_string, **kwargs):
    prev = kwargs.get('prev_node')
    choice = kwargs.get('choice')
    attr = self.ndb._menutree.attr

    if prev == 'gender':
        attr['gender'] = choice
        return 'height'
    if prev == 'height':
        attr['height'] = choice
        return 'build'
    if prev == 'build':
        attr['build'] = choice
        return 'appearance'
    if prev == 'face':
        attr['face'] = choice
        return 'eye_color'
    if prev == 'eye_color':
        attr['eye_color'] = choice
        return 'nose'
    if prev == 'nose':
        attr['nose'] = choice
        return 'lips'
    if prev == 'lips':
        attr['lips'] = choice
        return 'chin'
    if prev == 'chin':
        attr['chin'] = choice
        return 'skin_color'
    if prev == 'skin_color':
        attr['skin_color'] = choice
        return 'appearance'
    if prev == 'length':
        attr['length'] = choice
        next_node = 'appearance' if choice == 'bald' else 'hair_color'
        return next_node
    if prev == 'hair_color':
        attr['hair_color'] = choice
        return 'length'
    if prev == 'length':
        attr['length'] = choice
        return 'style'
    if prev == 'style':
        attr['style'] = choice
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
    get = self.ndb._menutree.attr.get

    #Figure Attributes
    gender = get('gender')
    height = get('height')
    build = get('build')

    #Facial Attributes
    face = get('face')
    eye_color = get('eye_color')
    nose = get('nose')
    lips = get('lips')
    chin = get('chin')
    skin_color = get('skin_color')

    #Hair Attributes
    hair_color = get('hair_color')
    texture = get('texture')
    length = get('length')
    style = get('style')


    # Check for chars attribute and initilize if none.
    if not self.attributes.get("chars"):
        self.db.chars = {}
    chars_len = len(self.db.chars) + 1
    self.msg(f"You currently have a total of {chars_len} characters.")

    #Add the new character object to the chars attribute as next number in the character list.
    self.db.chars[str(chars_len)] = create_object(typeclass="typeclasses.characters.Player_Character", key=name, home=None,
    attributes=[('figure', {'gender': gender, 'height': height, 'build': build}),
                ('facial', {'face': face, 'eye_color': eye_color, 'nose': nose, 'lips': lips, 'chin': chin, 'skin_color': skin_color}),
                ('hair', {'hair_color': hair_color, 'texture': texture, 'length': length, 'style': style})])
    self.msg("|gChargen completed!|n")
    return "exit"

def exit(self, raw_string, **kwargs):
    options = None
