from evennia import create_object
from evennia.utils import evtable
from evennia.utils.utils import variable_from_module


adjectives_dic = variable_from_module("characters.character_adjectives", 'character_adjectives')
properties_list = list(adjectives_dic.keys())

def node_main(caller, raw_string, **kwargs):
    text = 'Please create your character.'
    options = (
        {"key": ("1", "name"),
        "desc": "Name your character.",
        "goto": "node_enter_name"},

        {"key": ("2", "appearance", "appear"),
        "desc": "Create your character's appearance.",
        "goto": "node_appearance"},

        {"key": ("3", "class"),
        "desc": "Choose your character's class.",
        "goto": "node_char_class"},

        {"key": ("4", "finish", "create"),
        "desc": "Finish and create.",
        "goto": _create_char}
    )
    return text, options

def node_enter_name(caller, raw_string, **kwargs):
    # Check for a previous name.
    text = "Enter your character's name."
    
    options = {"key": "_default",
                "goto": (_set_name, 
                {'key': 'char_name'})
                }
    return text, options
def _set_name(caller, raw_string, **kwargs):
    inp = raw_string.strip()
    caller.ndb._menutree.choices_dic['char_name'] = inp
    caller.msg(f"You have chosen the name: {inp}")
    return 'node_main'

def node_appearance(caller, raw_string, **kwargs):
    pass

def _set_choices(caller, raw_string, **kwargs):
    key = kwargs['key']
    value = kwargs['value']

    caller.ndb._menutree.choices_dic[key] = value
    caller.msg(f"You have chosen: |y{value}|n")

    pind = properties_list.index(key)
    next_property = properties_list[pind + 1] if pind < len(properties_list) - 1 else None

    if next_property:
        return None, {'next_property': next_property}

    return 'node_main'

# This appearance node is made possible by Griatch. Thanks a ton for all the help.
# https://gist.github.com/Griatch/b51d7f086d7cee45e8061752b6de113b

def node_appearance(caller, raw_string, **kwargs):
    choices_dic = caller.ndb._menutree.choices_dic
    property = kwargs.get('next_property', properties_list[0])

    table1 = evtable.EvTable(table=[["Name:"], [f"|y{choices_dic.get('char_name')}|n"],
                            ["Class:"], [f"|y{choices_dic.get('char_class')}|n"]],
                            border=None)

    text = (
        f"{table1}\n{_char_desc(choices_dic)}\n"
        f"Choose your character's |g{property}|n:"
    )
    options = []

    adjectives = adjectives_dic[property]
    for adj in adjectives:
        options.append({'desc': adj,
                        'goto': (_set_choices,
                                    {'key': property,
                                    'value': adj}
                                )
        })

    return text, options

def _char_desc(choices_dic):
    get = choices_dic.get
    print(choices_dic)
    final_desc = "You see a featureless entity."
    if get('gender') == None or get('height') == None or get('build') == None:
        figure = False
    else:
        figure = True
        gender = 'man' if get('gender') == 'male' else 'woman'
        figure_desc = f"You see a {get('height')} {get('build')} {gender}."

    if get('eye_color') == None or get('nose') == None or get('lips') == None \
        or get('chin') == None or get('face') == None or get('skin_color') == None:
        facial = False
    else:
        facial = True
        gender = 'He' if get('gender') == 'male' else 'She'
        facial_desc = (f"{gender} has {get('eye_color')} eyes set above a {get('nose')} nose, "
            f"{get('lips')} lips and a {get('chin')} chin in a {get('face')} "
            f"{get('skin_color')} face.")
            
    if get('hair_length') == None:
        hair = False
    else:
        gender = 'He' if get('gender') == 'male' else 'She'
        if get('hair_length') == 'bald':
            hair = True
            hair_desc = f"{gender} is {get('hair_length')}."
        else:
            if get('hair_length') == None or get('hair_texture') == None or \
                get('hair_color') == None or get('hair_style') == None:
                hair = False
            else:
                hair = True
                print('Hair else statement was entered properly.')
                hair_desc = (f"{gender} has {get('hair_length')} {get('hair_texture')} "
                            f"{get('hair_color')} hair {get('hair_style')}.")

    if figure:
        final_desc = f"{figure_desc}"
    if facial:
        final_desc = f"{final_desc} {facial_desc}"
    if hair:
        final_desc = f"{final_desc} {hair_desc}"
    return final_desc

def node_char_class(caller, raw_string, **kwargs):
    text = "Choose your character\'s class."
    char_classes = variable_from_module("characters.character_classes", 'main_classes')
    options = []
    for c in char_classes.keys():
        options.append({'desc': f'{c}',
                        'goto': (_set_char_class, {'char_class': f'{c}'})})
    return text, options
def _set_char_class(caller, raw_string, **kwargs):
    caller.ndb._menutree.choices_dic['char_class'] = kwargs.get('char_class')
    return 'node_main'

def _create_char(caller, raw_string, **kwargs):
    get = caller.ndb._menutree.choices_dic.get

    char_name = get('char_name')
    char_class = get('char_class')
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
    new_char = create_object(typeclass="characters.characters.Character", key=char_name, home=None,
    attributes=[('figure', {'gender': gender, 'height': height, 'build': build}),
                ('facial', {'face': face, 'eye_color': eye_color, 'nose': nose, 'lips': lips, 'chin': chin, 'skin_color': skin_color}),
                ('hair', {'hair_color': hair_color, 'texture': hair_texture, 'length': hair_length, 'style': hair_style})])
    caller.db.chars[str(chars_len)] = new_char
    new_char.char.add_char_class(char_class)
    caller.msg("|gChargen completed!|n")
    return "exit"

def exit(caller, raw_string, **kwargs):
    options = None

'''
Character Creation

Choose your character's:
1. Name
2. Appearance
3. Class
4. Create
'''

'''
Character Appearance Menu

You see a very tall ample man. He has grey eyes set above a large nose, full lips and a clefted chin
in a disfigured pale face. He has close-cropped bouncy ginger hair in a bun.

1. Figure
2. Facial
3. Hair
'''
