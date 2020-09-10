from evennia import utils
from world import skillsets
from world import build_skill_str
from world import general_mechanics as gen_mec
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
        Only whole numbers (rounded down) are used to determine the offensive RS.

        TODO: Add a round down for the final RS. Integers only!
        """
        owner = self.owner
        a_rank = skillsets.return_skill_rank(owner, skillset, skill)
        a_difficulty = skillsets.skillsets[skillset][skill].get('difficulty')
        a_rs = skillsets.return_rank_score(a_rank, a_difficulty)

        defen_high, defen_mid, defen_low = skillsets.defense_layer_calc(target, rs_only=True)


        if aim == 'high':
            t_rs = defen_high
        elif aim == 'mid':
            t_rs = defen_mid
        elif aim == 'low':
            t_rs == defen_low

        if a_rs > t_rs:
            bonus = a_rs - t_rs
            success = 50 - bonus
        elif t_rs > a_rs:
            loss = t_rs - a_rs
            success = 50 + loss
        else:
            success = 50
        success = int(success)
        return success

    def body_part_choice(self, aim):
        high_body = ['head', 'face', 'neck', 'left shoulder', 'right shoulder']
        mid_body = ['chest', 'back', 'left arm', 'left hand', 'right arm', 'right hand', 'waist']
        low_body = ['left thigh', 'left leg', 'left foot', 'right thigh', 'right leg', 'right foot']
        
        if aim == 'high':
            body_part = random.choice(high_body)
        elif aim == 'mid':
            body_part = random.choice(mid_body)
        elif aim == 'low':
            body_part = random.choice(low_body)

        return body_part

    def damage_tier(self, success, roll):
        if roll > success:
            difference = roll - success
            if 1 <= difference <= 10:
                damage_tier = 0
                damage = random.randrange(1, 4)
            elif 11 <= difference <= 30:
                damage_tier = 1
                damage = random.randrange(5, 8)
            elif 31 <= difference <= 50:
                damage_tier = 2
                damage = random.randrange(9, 12)
            elif 51 <= difference <= 70:
                damage_tier = 3
                damage = random.randrange(13, 16)
            elif 71 <= difference <= 100:
                damage_tier = 4
                damage = random.randrange(17, 20)
        elif roll <= success:
            damage_tier = 0
            damage = 0
        return damage_tier, damage

    def get_weapon_type(self, skillset, skill):
        if skillsets.skillsets.get(skillset):
            if skillsets.skillsets[skillset].get(skill):
                weapon_type = skillsets.skillsets[skillset][skill]['weapon']
                return weapon_type

    def attack(self, target, skillset, skill):
        attacker = self.owner
        weapon = self.get_weapon_type(skillset, skill)
        damage_type = skillsets.return_damage_type(skillset, skill)
        aim = skillsets.return_default_aim(skillset, skill)

        if not gen_mec.check_roundtime(attacker):
            return

        # This is where the fun begins.

        roll = random.randint(1, 100)
        success = self.success_calc(target, skillset, skill, aim)

        # Make sure that the success is never below 5 or above 95, and always 5 if the target is unconscious.
        if success < 5 or target.db.ko == True:
            success = 5
        elif success > 95:
            success = 95
        
        damage_tier, damage = self.damage_tier(success, roll)

        # Randomly choose the body part hit, based on where the attack is aimed.
        body_part = self.body_part_choice(aim)

        if roll > success:
            hit = True
            attacker_desc, target_desc, others_desc = build_skill_str.create_attack_desc(attacker, target, skillset, skill, weapon, damage_type, damage_tier, body_part, hit, aim)

            attacker.msg(f"|430[Success: {success} Roll: {roll}] {attacker_desc}|n")
            target.msg(f"|r[Success: {success} Roll: {roll}] {target_desc}|n")
            attacker.location.msg_contents(f"{others_desc}", exclude=(attacker, target))
            target.combat.take_damage(attacker, damage)

        else:
            hit = False
            attacker_desc, target_desc, others_desc = build_skill_str.create_attack_desc(attacker, target, skillset, skill, weapon, damage_type, damage_tier, body_part, hit, aim)

            attacker.msg(f"|430[Success: {success} Roll: {roll}] {attacker_desc}|n")
            target.msg(f"|r[Success: {success} Roll: {roll}] {target_desc}|n")
            attacker.location.msg_contents(f"{others_desc}", exclude=(attacker, target))
        
        gen_mec.set_roundtime(attacker)
        if attacker.has_account:
            skillsets.grant_ap(attacker, skillset)

    def take_damage(self, attacker, damage):
        owner = self.owner
        name = owner.key
        location = owner.location
        owner_app = owner.attributes.get('approached')
        
        hp = owner.attributes.get('hp')
        current_hp = hp['current_hp']
        current_hp -= damage
        owner.db.hp['current_hp'] = current_hp

        location.msg_contents(f'{name} has {current_hp} health remaining!')
        if current_hp >= 1:
            owner.db.ko = False
        elif current_hp <= 0 and owner.db.ko != True:
            owner.db.ko = True
            location.msg_contents(f'{name} falls unconscious!')
        if current_hp <= -100:
            # Check for
            for a in owner_app:
                if a is not None:
                    ap_list = a.attributes.get('approached')
                    if ap_list:
                        ap_list.remove(owner)
            if owner_app:
                owner_app.remove(attacker)
            if not owner.has_account:
                owner.on_death()
            else:
                owner.db.hp['current_hp'] = owner.db.hp['max_hp']
                location.msg_contents(f"{name} dies and is resurrected to max HP.", exclude=owner)
                owner.msg("You die and are resurrected to full HP.")
                owner.db.ko = False

    def heal(self, target):
        owner = self.owner

        if not gen_mec.check_roundtime(owner):
            return 

        heal_rank = owner.db.holy['heal']
        max_hp = target.db.hp['max_hp']
        current_hp = target.db.hp['current_hp']

        if current_hp == max_hp:
            if target == owner:
                owner.msg(f"|cYou are already at full health!|n")
            else:
                owner.msg(f"|c{target.name} is already at full health!|n")
            return

        heal_amount = max_hp / 10
        current_hp += heal_amount
        if current_hp > max_hp:
            current_hp = max_hp
        target.db.hp['current_hp'] = current_hp
        if target == owner:
            owner.msg(f"|cYou heal yourself for {heal_amount} health.|n")
        else:
            owner.msg(f"|cYou heal {target.name} for {heal_amount} health.|n")
        gen_mec.set_roundtime(owner)