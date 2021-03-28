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
        'goto': (_call_instance, {'instance': 'random'})},
        {'desc': "Forest",
        'goto': (_call_instance, {'instance': 'forest'})},
        {'desc': "Sewer",
        'goto': (_call_instance, {'instance': 'sewer'})},
        {'desc': "Cave",
        'goto': (_call_instance, {'instance': 'cave'})},
        {'desc': "Alleyway",
        'goto': (_call_instance, {'instance': 'alley'})})
    return text, options

def _call_instance(caller, raw_string, **kwargs):
    instance = kwargs.get('instance')
    caller.instance.set_origin_room(caller.location)
    caller.instance.instance_menu(instance)
    return 'end_menu'

def end_menu(caller, raw_string, **kwargs):
    text = None
    options = None
    return text, options
