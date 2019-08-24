from evennia import utils
from world import skillsets
from world import build_skill_str
import time
import random

class CombatHandler:
    def __init__(self, owner):
        self.owner = owner

    def approach(self, attacker, target):
        a_app = attacker.attributes.get('approached')
        t_app = target.attributes.get('approached')
        a_name = attacker.key
        t_name = target.key

        if target in a_app:
            attacker.msg(f"You are already approached to {t_name}!")
            return
        if len(a_app) >= 1:
            attacker.msg(f"You are already approached to {a_app}!")
            target.msg(f"{a_name} attempts to approach you, but fails.")
            return
        if len(t_app) >= 3:
            attacker.msg(f"{t_app} are already approached to that target!")
            return
        a_app.append(target)
        t_app.append(attacker)
        attacker.msg(f"You approach {t_name}.")
        target.msg(f"{a_name} approaches you.")
        return

    def retreat(self, attacker):
        a_app = attacker.attributes.get('approached')
        a_name = attacker.key

        if len(a_app) == 0:
            attacker.msg(f"You are not approached to anything.")
            return
        for t in a_app:
            t.db.approached.remove(attacker)
            t.msg(f"{a_name} retreats from you.")
        attacker.msg(f"You retreat.")
        
        a_app.clear()
    
    def success_calc(self, target, skillset, skill, aim):
        """
        Only whole numbers (rounded down) are used to determine the offensive RB.

        TODO: Add a round down for the final RB. Integers only!
        """
        owner = self.owner
        a_skillset = owner.attributes.get(skillset)
        a_skill = a_skillset.get(skill)
        a_rb = a_skill.get('rb')

        defen_high = target.db.def_rb['high']
        defen_mid = target.db.def_rb['mid']
        defen_low = target.db.def_rb['low']


        if aim == 'high':
            t_rb = defen_high
        elif aim == 'mid':
            t_rb = defen_mid
        elif aim == 'low':
            t_rb == defen_low

        if a_rb > t_rb:
            bonus = a_rb - t_rb
            success = 50 - bonus
        elif t_rb > a_rb:
            loss = t_rb - a_rb
            success = 50 + loss
        else:
            success = 50

        return success

    def attack(self, target, skillset, skill, weapon, damage_type, aim):
        attacker = self.owner

        if self.owner.db.ko == True:
            self.owner.msg("You can't do that while unconscious!")
            return

        damage = 20

        # Create cooldown attribute if non-existent.
        if not self.owner.attributes.has('attack_cd'):
            self.owner.db.attack_cd = 0

        # Calculate current time, total cooldown, and remaining time.
        now = time.time()
        lastcast = self.owner.attributes.get('attack_cd')
        cooldown = lastcast + 3
        time_remaining = cooldown - now

        # Inform the attacker that they are in cooldown and exit the function.
        if time_remaining > 0 or self.owner.db.busy == True:
            if time_remaining >= 2:
                message = f"You need to wait {int(time_remaining)} more seconds."
            elif time_remaining >= 1 and time_remaining < 2:
                message = f"You need to wait {int(time_remaining)} more second."
            elif time_remaining < 1:
                message = f"You are in the middle of something."
            self.owner.msg(message)
            return

        roll = random.randint(1, 100)
        success = self.success_calc(target, skillset, skill, aim)

        # Make sure that the success is never below 5 or above 95 and always 5 if the target is unconscious.
        if success < 5 or target.db.ko == True:
            success = 5
        elif success > 95:
            success = 95
        
        #temp values
        damage_tier = 0
        body_part = 'head'

        if roll > success:
            hit = True
            attacker_desc, target_desc, others_desc = build_skill_str.create_attack_desc(attacker, target, skillset, skill, weapon, damage_type, damage_tier, body_part, hit)

            self.owner.msg(f"|430[Success: {success} Roll: {roll}] {attacker_desc}|n")
            target.msg(f"|r[Success: {success} Roll: {roll}] {target_desc}|n")
            self.owner.location.msg_contents(f"{others_desc}", exclude=(self.owner, target))
            self.take_damage(target, damage)

        else:
            hit = False
            attacker_desc, target_desc, others_desc = build_skill_str.create_attack_desc(attacker, target, skillset, skill, weapon, damage_type, damage_tier, body_part, hit)

            self.owner.msg(f"|430[Success: {success} Roll: {roll}] {attacker_desc}|n")
            target.msg(f"|r[Success: {success} Roll: {roll}] {target_desc}|n")
            self.owner.location.msg_contents(f"{others_desc}", exclude=(self.owner, target))

        utils.delay(3, self.unbusy)
        self.owner.db.busy = True
        self.owner.db.attack_cd = now

    def take_damage(self, target, damage):
        t_name = target.key
        location = target.location
        targ_app = target.attributes.get('approached')
        print('Target\'s approached list is: ', targ_app)
        
        hp = target.attributes.get('hp')
        current_hp = hp['current_hp']
        current_hp -= damage
        target.db.hp['current_hp'] = current_hp

        location.msg_contents(f'{t_name} has {current_hp} health remaining!')
        if current_hp >= 1:
            target.db.ko = False
        elif current_hp <= 0 and target.db.ko != True:
            target.db.ko = True
            location.msg_contents(f'{t_name} falls unconscious!')
        if current_hp <= -100:
            # Check for
            for a in targ_app:
                print('This is a in target\'s approached list: ', a)
                ap_list = a.attributes.get('approached')
                print('This is the approached list of the attacker: ', ap_list)
                if ap_list:
                    ap_list.remove(target)
            if targ_app:
                targ_app.remove(self.owner)
            if not target.has_account:
                okay = target.delete()
                if not okay:
                    location.msg_contents(f'\nERROR: {t_name} not deleted, probably because delete() returned False.')
                else:
                    location.msg_contents(f'{t_name} breathes a final breath and expires.')
            else:
                target.db.hp['current_hp'] = target.db.hp['max_hp']
                location.msg_contents(f"{t_name} dies and is resurrected to max HP.", exclude=target)
                target.msg("You die and are resurrected to full HP.")
                target.db.ko = False
    
    def unbusy(self):
            self.owner.msg('|yYou are no longer busy.|n')
            self.owner.db.busy = False