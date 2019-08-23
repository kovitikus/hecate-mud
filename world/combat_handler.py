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
    
    def success_calc(self, target, skillset, skill):
        """
        Only whole numbers (rounded down) are used to determine the offensive RB.
        TODO: ADD A ROUND DOWN!!
        """
        a_skillset = self.owner.attributes.get(skillset)
        a_skill = a_skillset.get(skill)
        a_rb = a_skill.get('rb')

        t_rb = 0

        if a_rb > t_rb:
            bonus = a_rb - t_rb
            success = 50 - bonus
        elif t_rb > a_rb:
            loss = t_rb - a_rb
            success = 50 + loss
        else:
            success = 50

        return success
    
    def defense_rb(self, skillset):
        owner = self.owner

        """Weapon Rank Bonus"""
        weap_dic = owner.db.def_skills.get('weapon')
        weap_high_def = weap_dic.get('high')
        weap_mid_def = weap_dic.get('mid')
        weap_low_def = weap_dic.get('low')
        weap_high_rb = 0.0
        weap_mid_rb = 0.0
        weap_low_rb = 0.0

        if weap_high_def.get(skillset):
            weap_high_dic = weap_high_def.get(skillset)
            weap_high_dic_values = weap_high_dic.values()
            for rb in weap_high_dic_values:
                if rb > weap_high_rb:
                    weap_high_rb = rb

        if weap_mid_def.get(skillset):
            weap_mid_dic = weap_mid_def.get(skillset)
            weap_mid_dic_values = weap_mid_dic.values()
            for rb in weap_mid_dic_values:
                if rb > weap_mid_rb:
                    weap_mid_rb = rb

        if weap_low_def.get(skillset):
            weap_low_dic = weap_low_def.get(skillset)
            weap_low_dic_values = weap_low_dic.values()
            for rb in weap_low_dic_values:
                if rb > weap_low_rb:
                    weap_low_rb = rb
        

        """Dodge Rank Bonus"""
        dodge_dic = owner.db.def_skills.get('dodge')
        dodge_high_def = dodge_dic.get('high')
        dodge_mid_def = dodge_dic.get('mid')
        dodge_low_def = dodge_dic.get('low')
        dodge_high_rb = 0.0
        dodge_mid_rb = 0.0
        dodge_low_rb = 0.0

        if dodge_high_def.get(skillset):
            dodge_high_dic = dodge_high_def.get(skillset)
            dodge_high_dic_values = dodge_high_dic.values()
            for rb in dodge_high_dic_values:
                if rb > dodge_high_rb:
                    dodge_high_rb = rb

        if dodge_mid_def.get(skillset):
            dodge_mid_dic = dodge_mid_def.get(skillset)
            dodge_mid_dic_values = dodge_mid_dic.values()
            for rb in dodge_mid_dic_values:
                if rb > dodge_mid_rb:
                    dodge_mid_rb = rb

        if dodge_low_def.get(skillset):
            dodge_low_dic = dodge_low_def.get(skillset)
            dodge_low_dic_values = dodge_low_dic.values()
            for rb in dodge_low_dic_values:
                if rb > dodge_low_rb:
                    dodge_low_rb = rb

    
        """Shield Rank Bonus"""
        shield_dic = owner.db.def_skills.get('shield')
        shield_high_def = shield_dic.get('high')
        shield_mid_def = shield_dic.get('mid')
        shield_low_def = shield_dic.get('low')
        shield_high_rb = 0.0
        shield_mid_rb = 0.0
        shield_low_rb = 0.0

        if shield_high_def.get(skillset):
            shield_high_dic = shield_high_def.get(skillset)
            shield_high_dic_values = shield_high_dic.values()
            for rb in shield_high_dic_values:
                if rb > shield_high_rb:
                    shield_high_rb = rb

        if shield_mid_def.get(skillset):
            shield_mid_dic = shield_mid_def.get(skillset)
            shield_mid_dic_values = shield_mid_dic.values()
            for rb in shield_mid_dic_values:
                if rb > shield_mid_rb:
                    shield_mid_rb = rb

        if shield_low_def.get(skillset):
            shield_low_dic = shield_low_def.get(skillset)
            shield_low_dic_values = shield_low_dic.values()
            for rb in shield_low_dic_values:
                if rb > shield_low_rb:
                    shield_low_rb = rb


        """
        Calculate Layering
        First Highest RB gets 100%
        Second Highest RB gets 50%
        Third Highest RB gets 33%
        """

        """High Layer"""
        # weap_high_rb, dodge_high_rb, shield_high_rb
        h_rb = [weap_high_rb, dodge_high_rb, shield_high_rb]
        h_rb.sort(reverse=True)
        h_layer1 = h_rb[0] * 1
        h_layer2 = h_rb[1] * 0.5
        h_layer3 = h_rb[2] * 0.33
        high_def_rb = (h_layer1 + h_layer2 + h_layer3)

        """Mid Layer"""
        # weap_mid_rb, dodge_mid_rb, shield_mid_rb
        m_rb = [weap_mid_rb, dodge_mid_rb, shield_mid_rb]
        m_rb.sort(reverse=True)
        m_layer1 = m_rb[0] * 1
        m_layer2 = m_rb[1] * 0.5
        m_layer3 = m_rb[2] * 0.33
        mid_def_rb = (m_layer1 + m_layer2 + m_layer3)

        """Low Layer"""
        # weap_low_rb, dodge_low_rb, shield_low_rb
        l_rb = [weap_low_rb, dodge_low_rb, shield_low_rb]
        l_rb.sort(reverse=True)
        l_layer1 = l_rb[0] * 1
        l_layer2 = l_rb[1] * 0.5
        l_layer3 = l_rb[2] * 0.33
        low_def_rb = (l_layer1 + l_layer2 + l_layer3)

        # Assign the values to the character.
        def_rb = owner.db.def_rb
        def_rb['high'] = high_def_rb
        def_rb['mid'] = mid_def_rb
        def_rb['low'] = low_def_rb

    def attack(self, target, skillset, skill, weapon, damage_type):
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
        success = self.success_calc(target, skillset, skill)

        # Make sure that the success is never below 5 or above 95 and always 5 if the target is unconscious.
        if success < 5 or target.db.ko == True:
            success = 5
        elif success > 95:
            success = 95
        
        #temp values
        damage_tier = 0
        body_part = 'head'

        # a_desc, t_desc = build_skill_str.create_attack_desc(self.owner, target, damage_type, damage_tier, body_part)
        # outcome = a_desc
        # weapon = 'quarterstave'

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