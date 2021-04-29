from evennia.utils.utils import lazy_property

from characters.characters import Character
from mobs.mob_handler import MobHandler


class DefaultMob(Character):
    @lazy_property
    def mob(self):
        return MobHandler(self)

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
        self.skill.generate_fresh_skillset('rat', starting_rank=rank)

class Dummy(DefaultMob):
    def revive(self):
        hp = self.attributes.get('hp')
        cur_hp = hp['current_hp']
        max_hp = hp['max_hp']
        if cur_hp <= 0:
            cur_hp = max_hp

sewer = {
    'rat': {
        'adj1': ['vicious', 'slick-coated', 'large', 'red-maned', 'filthy', 'feral'],
        'adj2': ['black', 'yellow', 'pale-white', 'black'],
        'noun': 'rat',
        'health': 100,
        'base_difficulty': 0,
    }
}
