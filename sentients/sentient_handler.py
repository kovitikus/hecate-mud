import random
            
from evennia import utils

class SentientHandler:
    def __init__(self, owner):
        self.owner = owner
        self.skillsets = utils.utils.variable_from_module('skills.skillsets', 'skillsets')

    def check_for_target(self):
        owner = self.owner
        # Set target to first approached if already approached.
        approached = owner.attributes.get('approached')
        app_len = len(approached)
        if app_len >= 1:
            target = approached[0]
            self.choose_attack(target)
        else:
            self.get_target()

    def get_target(self):
        owner = self.owner
        # If approached is empty, find new target and approach it.
        visible = []
        for targ in owner.location.contents_get(exclude=owner):
            if targ.has_account and not targ.is_superuser:
                    visible.append(targ)
        t_len = len(visible)
        if not t_len:
            self.idle()
            return
        
        # Pick random target from visible targets.
        rand_targ = random.randrange(t_len)
        target = visible[rand_targ - 1]
        owner.combat.approach(target)
        self.check_for_target()

    def choose_attack(self, target):
        owner = self.owner
        skillset = owner.tags.get(category='sentient_class')

        choices = []
        for k in self.skillsets[skillset].keys():
            choices.append(k)
        skill = random.choice(choices)

        skill_command = self.skillsets[skillset][skill].get('uid')

        self.attack(skill_command, target)

    def attack(self, skill_command, target):
        owner = self.owner
        cmd = f"{skill_command} {target}"
        owner.execute_cmd(cmd)
    
    def idle(self):
        utils.delay(5, self.check_for_target)
