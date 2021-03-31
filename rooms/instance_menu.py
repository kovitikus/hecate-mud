"""
=========[Instance Menu]=========

1 - Generate a random type of instance.
2 - Generate a forest.
3 - Generate a sewer.
4 - Generate a cave.
5 - Generate an alleyway.

=================================
"""

def start_menu(caller, raw_string, **kwargs):
    text = f"Choose the type of instance to generate."
    options = (
        {'desc': "Random",
        'goto': (_call_instance, {'room_type': 'random'})},
        {'desc': "Forest",
        'goto': (_call_instance, {'room_type': 'forest'})},
        {'desc': "Sewer",
        'goto': (_call_instance, {'room_type': 'sewer'})},
        {'desc': "Cave",
        'goto': (_call_instance, {'room_type': 'cave'})},
        {'desc': "Alleyway",
        'goto': (_call_instance, {'room_type': 'alley'})})
    return text, options

def _call_instance(caller, raw_string, **kwargs):
    instance = kwargs.get('room_type')
    caller.instance.set_room_type(instance)
    return 'end_menu'

def end_menu(caller, raw_string, **kwargs):
    text = None
    options = None
    return text, options
