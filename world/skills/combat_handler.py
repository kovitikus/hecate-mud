from world.skills import skillsets
from world.skills import build_skill_str
from world import general_mechanics as gen_mec
import random

class CombatHandler:
    def __init__(self, owner):
        self.owner = owner
        self.approached_list = self.get_approached()
        self.has_approached_attr = True if owner.attributes.has('approached') else False

    def approach(self, target):
        owner = self.owner

        owner_app = self.approached_list
        t_app = target.combat.approached_list

        owner_name = owner.key
        t_name = target.key

        if target in owner_app: # Owner is already approached to the target.
            owner.msg(f"You are already approached to {t_name}!")
            return
        if len(owner_app) >= 1: # Cannot approach a new target if currently approached to 1 or more targets.
            owner.msg(f"You are already approached to {owner_app}!")
            target.msg(f"{owner_name} attempts to approach you, but fails.")
            return
        if len(t_app) >= 3: # Target has 3 characters approached to it and cannot gain more.
            owner.msg(f"{t_app} are already approached to that target!")
            return
        self.add_approached(target)
        target.combat.add_approached(owner)
        owner.msg(f"You approach {t_name}.")
        target.msg(f"{owner_name} approaches you.")
        return

    def get_approached(self):
        owner = self.owner
        approached_list = []
        if self.has_approached_attr:
            approached_list = list(owner.attributes.get('approached'))
        return approached_list

    def add_approached(self, character):
        owner = self.owner
        if self.has_approached_attr:
            owner.db.approached.append(character)
            self.approached_list.append(character)

    def remove_approached(self, character):
        owner = self.owner
        if self.has_approached_attr:
            owner.db.approached.remove(character)
            self.approached_list.remove(character)

    def clear_approached(self):
        owner = self.owner
        if self.has_approached_attr:
            owner.db.approached.clear()
            self.approached_list.clear()

    def retreat(self):
        owner = self.owner
        owner_app = self.approached_list
        owner_name = owner.key

        if len(owner_app) == 0:
            owner.msg(f"You are not approached to anything.")
            return
        for target in owner_app:
            target.combat.remove_approached(owner)
            target.msg(f"{owner_name} retreats from you.")
        owner.msg(f"You retreat.")
        
        self.clear_approached()
    
    def success_calc(self, target, skillset, skill, aim):
        """
        Only whole numbers (rounded down) are used to determine the offensive RS.

        TODO: Add a round down for the final RS. Integers only!
        """
        owner = self.owner
        attack_rank = owner.skill.return_skill_rank(skillset, skill)
        attack_difficulty = skillsets.skillsets[skillset][skill].get('difficulty')
        attack_rs = owner.skill.return_rank_score(attack_rank, attack_difficulty)

        defend_high, defend_mid, defend_low = target.skill.defense_layer_calc(rs_only=True)


        if aim == 'high':
            defend_rs = defend_high
        elif aim == 'mid':
            defend_rs = defend_mid
        elif aim == 'low':
            defend_rs == defend_low

        if attack_rs > defend_rs:
            bonus = attack_rs - defend_rs
            success = 50 - bonus
        elif defend_rs > attack_rs:
            penalty = defend_rs - attack_rs
            success = 50 + penalty
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
        if skillset in skillsets.VIABLE_SKILLSETS:
            if skill in skillsets.skillsets[skillset]:
                weapon_type = skillsets.skillsets[skillset][skill]['weapon']
                return weapon_type

    def attack(self, target, skillset, skill):
        owner = self.owner
        weapon = self.get_weapon_type(skillset, skill)
        damage_type = owner.skill.return_damage_type(skillset, skill)
        aim = owner.skill.return_default_aim(skillset, skill)

        if not gen_mec.check_roundtime(owner):
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
            owner_desc, target_desc, others_desc = build_skill_str.create_attack_desc(owner, target, skillset, skill, weapon, damage_type, damage_tier, body_part, hit, aim)

            owner.msg(f"|430[Success: {success} Roll: {roll}] {owner_desc}|n")
            target.msg(f"|r[Success: {success} Roll: {roll}] {target_desc}|n")
            owner.location.msg_contents(f"{others_desc}", exclude=(owner, target))
            target.combat.take_damage(owner, damage)

        else:
            hit = False
            owner_desc, target_desc, others_desc = build_skill_str.create_attack_desc(owner, target, skillset, skill, weapon, damage_type, damage_tier, body_part, hit, aim)

            owner.msg(f"|430[Success: {success} Roll: {roll}] {owner_desc}|n")
            target.msg(f"|r[Success: {success} Roll: {roll}] {target_desc}|n")
            owner.location.msg_contents(f"{others_desc}", exclude=(owner, target))
        
        gen_mec.set_roundtime(owner)
        if owner.has_account:
            owner.skill.grant_ap(skillset)

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