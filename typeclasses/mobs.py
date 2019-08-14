from evennia import DefaultCharacter
from world import skillsets
from world.combat_handler import CombatHandler
from typeclasses.scripts import ScriptMob
from evennia.utils.utils import lazy_property
from evennia.utils.search import search_object
from evennia import utils
from evennia import TICKER_HANDLER as tickerhandler
import random

class DefaultMob(DefaultCharacter):
    def at_object_creation(self):
        self.attributes.add('hp', {'max_hp': 100, 'current_hp': 100})
        self.attributes.add('ko', False)
        self.attributes.add('approached', [])

    @lazy_property
    def combat(self):
        return CombatHandler(self)
    @lazy_property
    def combat_script(self):
        return ScriptMob(self)
        
class Rat(DefaultMob):
    
    rat_skills = {'claw': {'damage_type': 'slash', 'difficulty': 'easy', 'attack_range': 'melee', 'default_aim': 'mid'},
                    'bite': {'damage_type': 'slash', 'difficulty': 'easy', 'attack_range': 'melee', 'default_aim': 'high'}}
    def at_object_creation(self):
        super().at_object_creation()
        rank = 10
        rb = skillsets.easy_rb
        rb = rb[rank - 1]
        rat_skills = {'claw': {'rank': rank, 'rb': rb}, 'bite': {'rank': rank, 'rb': rb}}
        self.attributes.add('rat', rat_skills)
        tickerhandler.add(3, self.claw)


    def get_target(self):
        # Set target to first approached.
        approached = self.attributes.get('approached')
        app_len = len(approached)
        if app_len >= 1:
            target = approached[0]
            return target

        # If approached is empty, find new target and approach it.
        visible = []
        for targ in self.location.contents_get(exclude=self):
            if targ.has_account and not targ.is_superuser:
                    visible.append(targ)
        t_len = len(visible)
        if not t_len:
            return
        
        # Pick random target from visible targets.
        rand_targ = random.randrange(t_len)
        target = visible[rand_targ - 1]
        # self.combat.approach(self, target)
        return target

    def claw(self):
        target = self.get_target()
        damage_type = self.rat_skills['claw']['damage_type']
        skillset = 'rat'
        skill = 'claw'
        if target:
            self.combat.attack(target, damage_type, skillset, skill)

    def bite(self):
        pass