from typeclasses.characters import Character
from world.skills import skillsets
from world.skills.combat_handler import CombatHandler
from world.mobs.mob_handler import MobHandler
from evennia.utils.utils import lazy_property
from evennia.utils.search import search_object
from evennia import utils
from evennia import TICKER_HANDLER as tickerhandler

class DefaultMob(Character):
    def at_object_creation(self):
        super().at_object_creation()
    def on_death(self):
        name = self.key
        location = self.location
        okay = self.delete()
        if not okay:
            location.msg_contents(f'\nERROR: {name} not deleted, probably because delete() returned False.')
        else:
            location.msg_contents(f'{name} breathes a final breath and expires.')
            location.spawn.spawn_timer()
    @lazy_property
    def combat(self):
        return CombatHandler(self)
    @lazy_property
    def mob(self):
        return MobHandler(self)

class Humanoid(DefaultMob):
    def at_object_creation(self):
        super().at_object_creation()

class Creature(DefaultMob):
    def at_object_creation(self):
        super().at_object_creation()
        
class Rat(Creature):
    def at_object_creation(self):
        super().at_object_creation()
        rank = 10
        skillsets.generate_fresh_skillset(self, 'rat', starting_rank=rank)

class Dummy(DefaultMob):
    def revive(self):
        hp = self.attributes.get('hp')
        cur_hp = hp['current_hp']
        max_hp = hp['max_hp']
        if cur_hp <= 0:
            cur_hp = max_hp