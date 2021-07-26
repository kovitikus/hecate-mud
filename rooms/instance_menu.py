"""
=========[Instance Menu]=========

1 - Generate a random type of instance.
2 - Generate a forest.
3 - Generate a sewer.
4 - Generate a cave.
5 - Generate an alleyway.

=================================
"""

from evennia import GLOBAL_SCRIPTS
from evennia.utils.utils import variable_from_module

zone_list = variable_from_module("rooms.zones", variable='static_zones')
ledger_dict = {}
ledger_dict['temporary_instance'] = GLOBAL_SCRIPTS.instance_ledger.attributes.get('temporary_instance', {})
ledger_dict['static_instance'] = GLOBAL_SCRIPTS.instance_ledger.attributes.get('static_instance', {})


def node_main_menu(caller, raw_string, **kwargs):
    text = (
        f"Main Menu\n\n"
        f"Current Instance Total\n"
        "----------------------\n"
        f"Temporary Instances: {len(ledger_dict['temporary_instance'])}\n"
        f"Static Instances: {len(ledger_dict['temporary_instance'])}"
    )
    options = (
        {'desc': "Create Temporary Instance",
        'goto': 'node_create_temporary_instance'},
        {'desc': "Create Static Instance",
        'goto': 'node_create_static_instance'},
        {'desc': "Manage Temporary Instances",
        'goto': ('node_manage_instances', {'instance_type': 'temporary_instance'})},
        {'desc': "Manage Static Instances",
        'goto': ('node_manage_instances', {'instance_type': 'static_instance'})})
    return text, options

def node_create_temporary_instance(caller, raw_string, **kwargs):
    text = "Choose the type of instance to generate temporarily:"
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
        'goto': 'node_main_menu'})
    return text, options

def node_create_static_instance(caller, raw_string, **kwargs):
    text = f"Choose the static instance to generate:"
    options = []

    for zone in zone_list.keys():
        options.append({'desc': zone.capitalize(),
        'goto': (_call_instance, {'static_instance': True, 'zone_type': zone})})
    options.append({'desc': "Return to main menu.",
                    'goto': 'node_main_menu'})
    return text, options

def node_manage_instances(caller, raw_string, **kwargs):
    instance_type = kwargs['instance_type']
    text = "Instance Management Menu"
    options = []
    for key, value in ledger_dict[instance_type].items():
        options.append({'desc': f"Instance ID: {key}, Creator: {value['creator']}",
                        'goto': ('node_manage_single_instance', 
                        {'instance_type': instance_type, 'instance_id': key})})
    options.append({'desc': "Return to Main Menu.",
                    'goto': 'node_main_menu'})
    return text, options

def node_manage_single_instance(caller, raw_string, **kwargs):
    instance_type = kwargs['instance_type']
    instance_id = kwargs['instance_id']
    instance_dict = ledger_dict[instance_type][instance_id]

    text = (
        f"Managing {instance_id}\n\n"
        f"Instance Type: {instance_type}\n"
        f"Instance ID: {instance_id}\n"
        f"Creator: {instance_dict.get('creator', 'Nobody')}\n"
        f"Creation Time (Epoch): {instance_dict['epoch_creation']}\n"
        f"Expiration Time (Epoch): {instance_dict.get('epoch_expiration', 'Never')}\n"
        f"# of Rooms: {len(instance_dict.get('rooms', []))}\n"
        f"# of Exits: {len(instance_dict.get('exits', []))}\n"
    )
    options = (
        {'desc': "Delete this instance.",
        'goto': ('node_delete_instance_confirmation',
            {'instance_type': instance_type, 'instance_id': instance_id})},
        {'desc': "Return to Instance Management Menu.",
        'goto': 'node_manage_instances'},
        {'desc': "Return to Main Menu.",
        'goto': 'node_main_menu'})
    return text, options

def node_delete_instance_confirmation(caller, raw_string, **kwargs):
    instance_type = kwargs['instance_type']
    instance_id = kwargs['instance_id']
    text = f"Are you certain that want to delete instance: {instance_id}?"
    options = (
        {'desc': "|gYes, of course.|n",
        'goto': (_delete_instance,
            {'delete': True, 'instance_type': instance_type, 'instance_id': instance_id})},
        {'desc': "|rNO! ABORT DELETION!|n",
        'goto': (_delete_instance,
            {'delete': False, 'instance_type': instance_type, 'instance_id': instance_id})})
    return text, options
def _delete_instance(caller, raw_string, **kwargs):
    delete = kwargs['delete']
    instance_type = kwargs['instance_type']
    instance_id = kwargs['instance_id']
    if delete:
        caller.instance.destroy_instance(instance_type, instance_id)
        caller.msg(f"Deletion of {instance_id} was successful. Ta Ta, Farewell.")
    else:
        caller.msg(f"Deletion of {instance_id} successfully aborted! The instance remains.")
    return 'node_main_menu'

def _call_instance(caller, raw_string, **kwargs):
    zone_type = kwargs.get('zone_type')
    if kwargs.get('static_instance', True):
        caller.instance.generate_static_instance(zone_type)
    else:
        caller.instance.set_room_type(zone_type)
    return 'end_menu'

def end_menu(caller, raw_string, **kwargs):
    text = None
    options = None
    return text, options
