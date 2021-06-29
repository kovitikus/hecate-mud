from evennia import create_object

from characters import character_adjectives


def main(caller, raw_string, **kwargs):
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

def enter_name(caller, raw_string, **kwargs):
    # Check for a previous name.
    text = "Enter your character's name."
    
    options = {"key": "_default",
                "goto": _set_name}
    return text, options

def _set_name(caller, raw_string, **kwargs):
    inp = raw_string.strip()
    caller.ndb._menutree.char_name = inp
    caller.msg(f"You have chosen the name: {inp}")
    return 'main'

def appearance(caller, raw_string, **kwargs):
    get = caller.ndb._menutree.char_appearance.get
    text = "Please choose."
    options = (
    {"key": ("1", "figure"),
    "desc": f"Set your character's figure.\nGender: |c{get('gender')}|n Height: |c{get('height')}|n Build: |c{get('build')}|n\n",
    "goto": "gender"},

    {"key": ("2", "face"),
    "desc": f"Set your character's facial attributes.\nFace Shape: |c{get('face')}|n Eye Color: |c{get('eye_color')}|n Nose: |c{get('nose')}|n Lips: |c{get('lips')}|n Chin: |c{get('chin')}|n Skin Color: |c{get('skin_color')}|n\n",
    "goto": "face"},

    {"key": ("3", "hair"),
    "desc": f"Set your character's hair.\nLength: |c{get('hair_length')}|n Color: |c{get('hair_color')}|n Texture: |c{get('hair_texture')}|n Style: |c{get('hair_style')}|n\n",
    "goto": "hair_length"},

    {"key": ("4", "back", "main"),
    "desc": "Back to main menu.",
    "goto": "main"})
    return text, options

def gender(caller, raw_string, **kwargs):
    text = "Choose your gender."
    options = []
    for g in character_adjectives._FIGURE['gender']:
        options.append({"desc": f"{g}",
                        "goto": (_set_gender, {'gender': f'{g}'})})
    return text, options
def _set_gender(caller, raw_string, **kwargs):
    caller.ndb._menutree.char_appearance['gender'] = kwargs.get('gender')
    return 'height'

def height(caller, raw_string, **kwargs):
    text = 'Choose your height.'
    options = []
    for g in character_adjectives._FIGURE['height']:
        options.append({"desc": f"{g}",
                        "goto": (_set_height, {'height': f'{g}'})})
    return text, options
def _set_height(caller, raw_string, **kwargs):
    caller.ndb._menutree.char_appearance['height'] = kwargs.get('height')
    return 'build'

def build(caller, raw_string, **kwargs):
    text = 'Choose your build.'
    options = []
    for g in character_adjectives._FIGURE['build']:
        options.append({"desc": f"{g}",
                        "goto": (_set_build, {'build': f'{g}'})})
    return text, options
def _set_build(caller, raw_string, **kwargs):
    caller.ndb._menutree.char_appearance['build'] = kwargs.get('build')
    return 'appearance'

def face(caller, raw_string, **kwargs):
    text = 'Choose an adjective that describes your face.'
    options = []
    for g in character_adjectives._FACIAL['face']:
        options.append({"desc": f"{g}",
                        "goto": (_set_face, {'face': f'{g}'})})
    return text, options
def _set_face(caller, raw_string, **kwargs):
    caller.ndb._menutree.char_appearance['face'] = kwargs.get('face')
    return 'eye_color'

def eye_color(caller, raw_string, **kwargs):
    text = 'Choose your eye color.'
    options = []
    for g in character_adjectives._FACIAL['eye_color']:
        options.append({"desc": f"{g}",
                        "goto": (_set_eye_color, {'eye_color': f'{g}'})})
    return text, options
def _set_eye_color(caller, raw_string, **kwargs):
    caller.ndb._menutree.char_appearance['eye_color'] = kwargs.get('eye_color')
    return 'nose'

def nose(caller, raw_string, **kwargs):
    text = 'Choose and adjective that describes your nose.'
    options = []
    for g in character_adjectives._FACIAL['nose']:
        options.append({"desc": f"{g}",
                        "goto": (_set_nose, {'nose': f'{g}'})})
    return text, options
def _set_nose(caller, raw_string, **kwargs):
    caller.ndb._menutree.char_appearance['nose'] = kwargs.get('nose')
    return 'lips'

def lips(caller, raw_string, **kwargs):
    text = 'Choose an adjective that describes your lips.'
    options = []
    for g in character_adjectives._FACIAL['lips']:
        options.append({"desc": f"{g}",
                        "goto": (_set_lips, {'lips': f'{g}'})})
    return text, options
def _set_lips(caller, raw_string, **kwargs):
    caller.ndb._menutree.char_appearance['lips'] = kwargs.get('lips')
    return 'chin'

def chin(caller, raw_string, **kwargs):
    text = 'Choose an adjective that describes your chin.'
    options = []
    for g in character_adjectives._FACIAL['chin']:
        options.append({"desc": f"{g}",
                        "goto": (_set_chin, {'chin': f'{g}'})})
    return text, options
def _set_chin(caller, raw_string, **kwargs):
    caller.ndb._menutree.char_appearance['chin'] = kwargs.get('chin')
    return 'skin_color'

def skin_color(caller, raw_string, **kwargs):
    text = 'Choose your skin color.'
    options = []
    for g in character_adjectives._FACIAL['skin_color']:
        options.append({"desc": f"{g}",
                        "goto": (_set_skin_color, {'skin_color': f'{g}'})})
    return text, options
def _set_skin_color(caller, raw_string, **kwargs):
    caller.ndb._menutree.char_appearance['skin_color'] = kwargs.get('skin_color')
    return 'appearance'

def hair_length(caller, raw_string, **kwargs):
    text = 'Choose your hair\'s length.'
    options = []
    for g in character_adjectives._HAIR['length']:
        options.append({"desc": f"{g}",
                        "goto": (_set_hair_length, {'hair_length': f'{g}'})})
    return text, options
def _set_hair_length(caller, raw_string, **kwargs):
    hair_length = kwargs.get('hair_length')
    caller.ndb._menutree.char_appearance['hair_length'] = hair_length
    goto_node = 'appearance' if hair_length == 'bald' else 'hair_color'
    return goto_node

def hair_color(caller, raw_string, **kwargs):
    text = 'Choose your hair color.'
    options = []
    for g in character_adjectives._HAIR['hair_color']:
        options.append({"desc": f"{g}",
                        "goto": (_set_hair_color, {'hair_color': f'{g}'})})
    return text, options
def _set_hair_color(caller, raw_string, **kwargs):
    caller.ndb._menutree.char_appearance['hair_color'] = kwargs.get('hair_color')
    return 'hair_texture'

def hair_texture(caller, raw_string, **kwargs):
    text = 'Choose an adjective that describes your hair\'s texture.'
    options = []
    for g in character_adjectives._HAIR['texture']:
        options.append({"desc": f"{g}",
                        "goto": (_set_hair_texture, {'hair_texture': f'{g}'})})
    return text, options
def _set_hair_texture(caller, raw_string, **kwargs):
    caller.ndb._menutree.char_appearance['hair_texture'] = kwargs.get('hair_texture')
    return 'hair_style'

def hair_style(caller, raw_string, **kwargs):
    text = 'Choose your hairstyle.'
    options = []
    for g in character_adjectives._HAIR['style']:
        options.append({"desc": f"{g}",
                        "goto": (_set_hair_style, {'hair_style': f'{g}'})})
    return text, options
def _set_hair_style(caller, raw_string, **kwargs):
    caller.ndb._menutree.char_appearance['hair_style'] = kwargs.get('hair_style')
    return 'appearance'

def _create_char(caller, raw_string, **kwargs):
    char_name = caller.ndb._menutree.char_name
    get = caller.ndb._menutree.char_appearance.get

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
    hair_texture = get('hair_texture')
    hair_length = get('hair_length')
    hair_style = get('hair_style')


    # Check for chars attribute and initilize if none.
    if not caller.attributes.get("chars"):
        caller.db.chars = {}
    chars_len = len(caller.db.chars) + 1
    caller.msg(f"You currently have a total of {chars_len} characters.")

    #Add the new character object to the chars attribute as next number in the character list.
    caller.db.chars[str(chars_len)] = create_object(typeclass="characters.characters.Character", key=char_name, home=None,
    attributes=[('figure', {'gender': gender, 'height': height, 'build': build}),
                ('facial', {'face': face, 'eye_color': eye_color, 'nose': nose, 'lips': lips, 'chin': chin, 'skin_color': skin_color}),
                ('hair', {'hair_color': hair_color, 'texture': hair_texture, 'length': hair_length, 'style': hair_style})])
    caller.msg("|gChargen completed!|n")
    return "exit"

def exit(caller, raw_string, **kwargs):
    options = None
