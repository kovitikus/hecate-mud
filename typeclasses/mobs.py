from typeclasses.characters import Character
from world import skillsets
from world.combat_handler import CombatHandler
from typeclasses.scripts import ScriptMob
from evennia.utils.utils import lazy_property
from evennia.utils.search import search_object
from evennia import utils
from evennia import TICKER_HANDLER as tickerhandler
import random

class DefaultMob(Character):
    def at_object_creation(self):
        super().at_object_creation()
        
    @lazy_property
    def combat(self):
        return CombatHandler(self)
    @lazy_property
    def combat_script(self):
        return ScriptMob(self)

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
        rat_skills = {'claw': rank, 'bite': rank}
        self.attributes.add('rat', rat_skills)
        tickerhandler.add(3, self.claw)


    def get_target(self):
        # Set target to first approached if already approached.
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
        self.combat.approach(self, target)
        return target

    def claw(self):
        target = self.get_target()
        damage_type = 'slash'
        skillset = 'rat'
        skill = 'claw'
        aim = 'mid'
        if target:
            self.combat.attack(target, skillset, skill, damage_type, aim)

    def bite(self):
        pass

class Dummy(DefaultMob):
    def revive(self):
        hp = self.attributes.get('hp')
        cur_hp = hp['current_hp']
        max_hp = hp['max_hp']
        if cur_hp <= 0:
            cur_hp = max_hp