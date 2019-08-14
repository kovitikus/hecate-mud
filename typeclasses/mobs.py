from evennia import DefaultCharacter
from world import skillsets
from world.combat_handler import CombatHandler
from evennia.utils.utils import lazy_property

class DefaultMob(DefaultCharacter):
    def at_object_creation(self):
        self.db.hp = 100
        self.db.ko = False
        self.db.approached = []
        
    def take_damage(self, damage):
        mob = self.key
        location = self.location
        
        self.db.hp -= damage
        hp = self.db.hp
        location.msg_contents(f'{mob} has {hp} health remaining!')
        if hp >= 1:
            self.db.ko = False
        elif hp <= 0 and self.db.ko != True:
            self.db.ko = True
            location.msg_contents(f'{mob} falls unconscious!')
        if hp <= -100:
            okay = self.delete()
            if not okay:
                location.msg_contents(f'\nERROR: {mob} not deleted, probably because delete() returned False.')
            else:
                location.msg_contents(f'{mob} breathes a final breath and expires.')
        return
        
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