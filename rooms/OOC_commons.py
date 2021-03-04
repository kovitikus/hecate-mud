#HEADER
from evennia.utils.create import create_object

#CODE
caller.msg("Creating the Common Room.")
common_room = create_object(typeclass="rooms.rooms.OOC_Room", 
                            key='Common Room', report_to=caller)
if DEBUG:
    common_room.delete()
    caller.msg("Common Room deleted!")
    caller.msg("DEBUG COMPLETE!")
