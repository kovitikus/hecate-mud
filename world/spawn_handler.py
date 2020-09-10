from evennia.prototypes.spawner import spawn

class SpawnHandler:
    def __init__(self, room):
        self.room = room
    def spawn_mob(self, char):
        room = self.room

        # Do stuff to determine what mob to spawn based on the character's reputation, etc.

        mob = spawn('rat')
        if mob:
            mob.move_to(room, quiet=True)
            room.msg_contents(f"{mob} has entered the room.")
            
    def destroy_mob(self):
        room = self.room
        # Search for all mob typeclasses and disable them.
        for obj in room.get_contents():
            if obj.inherits_from('typeclasses.mobs.DefaultMob'):
                obj.delete()