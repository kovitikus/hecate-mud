from evennia import create_object
from evennia.utils import evtable
from evennia.utils.utils import variable_from_module

DEFAULT_STARTING_LOCATION = variable_from_module("world.hecate_settings", "DEFAULT_STARTING_LOCATION")

# Imports the full adjectives dictionary, which consists of:
# Category dictionary -> property key -> adjective list value
adjectives_dic = variable_from_module("characters.character_adjectives", 'character_adjectives')

# Generates a dictionary category keys containing a list of properties as their values
# Assigns the list to the category key, resetting the list per category.
properties_dic = {}
for category in adjectives_dic.keys():
    properties_dic[category] = []
    for key in adjectives_dic[category].keys():
        properties_dic[category].append(key)

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
    """
    Special Thanks:
        This appearance node was made possible by Griatch. Thanks a ton for all the help.
        https://gist.github.com/Griatch/b51d7f086d7cee45e8061752b6de113b
    """
    choices_dic = caller.ndb._menutree.choices_dic
    table1 = evtable.EvTable(table=[["Name:"], [f"|y{choices_dic.get('char_name')}|n"],
                            ["Class:"], [f"|y{choices_dic.get('char_class')}|n"]],
                            border=None)
    text = (f"{table1}\n{_char_desc(choices_dic)}\n\n"
            "Choose an appearance to modify.")
    options = []
    for category in properties_dic.keys():
        options.append({'desc': category.capitalize(),
                        'goto': ('node_properties',
                                    {'category': category})})
    options.append({'desc': "Return to the Main Menu",
                    'goto': 'node_main'})
    return text, options

def node_properties(caller, raw_string, **kwargs):
    category = kwargs['category']
    property = kwargs.get('next_property', properties_dic[category][0])

    text = (f"Choose your character's |g{property}|n:")
    options = []

    adjectives = adjectives_dic[category][property]
    for adjective in adjectives:
        options.append({'desc': adjective,
                        'goto': (_set_choices,
                                    {'category': category,
                                    'property': property,
                                    'adjective': adjective})})
    return text, options

def _set_choices(caller, raw_string, **kwargs):
    category = kwargs['category']
    property = kwargs['property']
    adjective = kwargs['adjective']

    caller.ndb._menutree.choices_dic[property] = adjective
    caller.msg(f"You have chosen: |y{adjective}|n")

    property_index = properties_dic[category].index(property)
    if property_index < len(properties_dic[category]) - 1:
        next_property = properties_dic[category][property_index + 1]
    else:
        next_property = None

    if next_property:
        return None, {'next_property': next_property,
                    'category': category}
    else:
        return 'node_appearance'

def _char_desc(choices_dic):
    get = choices_dic.get
    final_desc = "You see a featureless entity."
    if get('Gender') == None or get('Height') == None or get('Build') == None:
        figure = False
    else:
        figure = True
        gender = 'man' if get('Gender') == 'male' else 'woman'
        figure_desc = f"You see a {get('Height')} {get('Build')} {gender}."

    if get('Eye Color') == None or get('Nose') == None or get('Lips') == None \
        or get('Chin') == None or get('Face') == None or get('Skin Color') == None:
        facial = False
    else:
        facial = True
        gender = 'He' if get('Gender') == 'male' else 'She'
        facial_desc = (f"{gender} has {get('Eye Color')} eyes set above a {get('Nose')} nose, "
            f"{get('Lips')} lips and a {get('Chin')} chin in a {get('Face')} "
            f"{get('Skin Color')} Face.")
            
    if get('Hair Length') == None:
        hair = False
    else:
        gender = 'He' if get('Gender') == 'male' else 'She'
        if get('Hair Length') == 'bald':
            hair = True
            hair_desc = f"{gender} is {get('Hair Length')}."
        else:
            if get('Hair Length') == None or get('Hair Texture') == None or \
                get('Hair Color') == None or get('Hair Style') == None:
                hair = False
            else:
                hair = True
                hair_desc = (f"{gender} has {get('Hair Length')} {get('Hair Texture')} "
                            f"{get('Hair Color')} hair {get('Hair Style')}.")

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
    attributes = [
                ('figure',
                    {'Gender': get('Gender'), 'Height': get('Height'), 'Build': get('Build')}),
                ('facial',
                    {'Face': get('Face'), 'Eye Color': get('Eye Color'), 'Nose': get('Nose'),
                    'Lips': get('Lips'), 'Chin': get('Chin'), 'Skin Color': get('Skin Color')}),
                ('hair',
                    {'Hair Color': get('Hair Color'), 'Hair Texture': get('Hair Texture'),
                    'Hair Length': get('Hair Length'), 'Hair Style': get('Hair Style')})
    ]


    # Check for chars attribute and initilize if none.
    if not caller.attributes.get("chars"):
        caller.db.chars = {}
    chars_len = len(caller.db.chars) + 1
    caller.msg(f"You currently have a total of {chars_len} characters.")

    #Add the new character object to the chars attribute as next number in the character list.
    new_char = create_object(typeclass="characters.characters.Character", key=get('char_name'),
        home=None, attributes=attributes)
    new_char.db.prelogout_location = DEFAULT_STARTING_LOCATION if DEFAULT_STARTING_LOCATION else new_char.home
    caller.db.chars[str(chars_len)] = new_char
    new_char.char.add_char_class(get('char_class'))
    new_char.stats.set_base_health()
    new_char.stats.set_max_health()
    new_char.stats.set_base_energy()
    new_char.stats.set_max_energy()
    caller.msg("|gChargen completed!|n")
    return "exit"

def exit(caller, raw_string, **kwargs):
    options = None
