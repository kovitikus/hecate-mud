from evennia import DefaultCharacter
from world import skillsets
from world.combat_handler import CombatHandler
from evennia.utils.utils import lazy_property
from evennia.utils.search import search_object

class DefaultMob(DefaultCharacter):
    def at_object_creation(self):
        self.db.hp = 100
        self.db.ko = False
        self.db.approached = []
        
class Rat(DefaultMob):
    @lazy_property
    def combat(self):
        return CombatHandler

    def get_target(self):
        visible = (targs for targ in self.location.contents if targ.has_account)
        for targ in visible:
            key = targ.key
        


    rat_skills = {'claw': {'damage_type': 'slash', 'difficulty': 'easy', 'attack_range': 'melee', 'default_aim': 'mid'},
                    'bite': {'damage_type': 'slash', 'difficulty': 'easy', 'attack_range': 'melee', 'default_aim': 'high'}}
    def at_object_creation(self):
        pass
    def claw(self):
        rb = skillsets.easy_rb
        combat.attack
        pass
    def bite(self):
        pass