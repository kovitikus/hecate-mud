"""
=========[Instance Menu]=========

1 - Generate a random type of instance.
2 - Generate a forest.
3 - Generate a sewer.
4 - Generate a cave.
5 - Generate an alleyway.

=================================
"""

from evennia.utils.utils import variable_from_module


def start_menu(caller, raw_string, **kwargs):
    text = f"Choose the type of instance to generate."
    options = (
        {'desc': "Random Zone",
        'goto': 'node_random_zones'},
        {'desc': "Static Zone",
        'goto': 'node_static_zones'})
    return text, options

def node_random_zones(caller, raw_string, **kwargs):
    text = "Choose the type of zone to generate randomly:"
    options = (
        {'desc': "Random",
        'goto': (_call_instance, {'zone_type': 'random'})},
        {'desc': "Forest",
        'goto': (_call_instance, {'zone_type': 'forest'})},
        {'desc': "Sewer",
        'goto': (_call_instance, {'zone_type': 'sewer'})},
        {'desc': "Cave",
        'goto': (_call_instance, {'zone_type': 'cave'})},
        {'desc': "Alleyway",
        'goto': (_call_instance, {'zone_type': 'alley'})},
        {'desc': "Return to main menu.",
        'goto': 'start_menu'})
    return text, options

def node_static_zones(caller, raw_string, **kwargs):
    zone_list = variable_from_module("rooms.zones", variable='static_zones')
    text = f"Choose the static zone to generate:"
    options = []

    for zone in zone_list.keys():
        options.append({'desc': zone.capitalize(),
        'goto': (_call_instance, {'static_zone': True, 'zone_type': zone})})
    options.append({'desc': "Return to main menu.",
                    'goto': 'start_menu'})
    return text, options

def _call_instance(caller, raw_string, **kwargs):
    zone_type = kwargs.get('zone_type')
    if kwargs.get('static_zone', False):
        caller.instance.generate_static_zone(zone_type)
    else:
        caller.instance.set_room_type(zone_type)
    return 'end_menu'

def end_menu(caller, raw_string, **kwargs):
    text = None
    options = None
    return text, options
