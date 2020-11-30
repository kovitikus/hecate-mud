import time, datetime, random
from evennia import utils
from evennia.prototypes.spawner import spawn
from world import general_mechanics as gen_mec

class MobSpawner:
    def __init__(self, room):
        self.room = room

    def spawn_timer(self):
        # start a timer on the room to check if spawning
        utils.delay(3, self.on_spawn_timer_tick)

    def on_spawn_timer_tick(self):
        # roll the dice and see if a mob will spawn
        roll = gen_mec.roll_die()
        print(f"spawn die roll = {roll}")
        if roll >= 50:
            self.spawn_mob()
        else:
            self.spawn_timer()

    def spawn_mob(self):
        room = self.room

        # Do stuff to determine what mob to spawn based on the character's reputation, etc.

        mob = spawn('rat')
        if len(mob):
            mob = mob[0]
            
        if mob:
            mob.move_to(room, quiet=True)
            room.msg_contents(f"{mob} has entered the room.")
            mob.mob.get_target()
            
    def destroy_mob(self):
        room = self.room
        # Search for all mob typeclasses and disable them.
        for obj in room.get_contents():
            if obj.inherits_from('typeclasses.mobs.DefaultMob'):
                obj.delete()