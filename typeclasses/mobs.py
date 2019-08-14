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
        self.db.hp = 100
        self.db.ko = False
        self.db.approached = []

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
            print(target)
            return target

        # If approached is empty, find new target and approach it.
        visible = []
        print('Location: ', self.location)
        print('Location contents: ', self.location.contents)
        for targ in self.location.contents:
            if targ.has_account:
                if targ != self:
                    visible.append(targ)
        print('Visible list: ', visible)
        t_len = len(visible)
        
        # Pick target from visible targets.
        rand_targ = random.randrange(t_len)
        print('Random target number: ', rand_targ)
        target = visible[rand_targ - 1]
        # self.combat.approach(self, target)
        print('Target is: ', target)
        return target

    def claw(self):
        target = self.get_target()
        print('Target is: ', target)
        damage_type = self.rat_skills['claw']['damage_type']
        skillset = 'rat'
        skill = 'claw'

        self.combat.attack(target, damage_type, skillset, skill)
        utils.delay(3, self.claw)

    def bite(self):
        pass