import random

from misc import generic_str
from misc import general_mechanics as gen_mec

from skills import skillsets


class CombatHandler:
    def __init__(self, owner):
        self.owner = owner

        self.article = generic_str.article
        self.pronoun = generic_str.pronoun
        self.prop_name = generic_str.proper_name

        self.has_approached_attr = True if owner.attributes.has('approached') else False
        self.approached_list = self.get_approached()

    def attack(self, target, skillset, skill):
        owner = self.owner

        if not gen_mec.check_roundtime(owner):
            return

        # This is where the fun begins.
        self.init_variables(target, skillset, skill)
        self.set_weapon_type()
        self.set_damage_type()
        self.set_attack_aim()
        self.set_body_part()
        self.set_die_roll()
        self.set_success()
        self.set_damage_tier()
        self.set_hit()
        self.create_attack_desc()

        if self.hit:
            target.combat.take_damage(owner, self.damage)
        
        gen_mec.set_roundtime(owner)

        if owner.has_account:
            owner.skill.grant_action_points(skillset)

    def init_variables(self, target, skillset, skill):
        self.target = target
        self.skillset = skillset
        self.skill = skill
    
    def set_weapon_type(self):
        if self.skillset in skillsets.VIABLE_SKILLSETS:
            if self.skill in skillsets.skillsets[self.skillset]:
                self.weapon_type = skillsets.skillsets[self.skillset][self.skill]['weapon']
    
    def set_damage_type(self):
        self.damage_type = self.owner.skill.return_damage_type(self.skillset, self.skill)
    
    def set_attack_aim(self):
        self.attack_aim = self.owner.skill.return_default_aim(self.skillset, self.skill)
    
    def set_body_part(self):
        attack_aim = self.attack_aim
        high_body = ['head', 'face', 'neck', 'left shoulder', 'right shoulder']
        mid_body = ['chest', 'back', 'left arm', 'left hand', 'right arm', 'right hand', 'waist']
        low_body = ['left thigh', 'left leg', 'left foot', 'right thigh', 'right leg', 'right foot']
        
        if attack_aim == 'high':
            self.body_part = random.choice(high_body)
        elif attack_aim == 'mid':
            self.body_part = random.choice(mid_body)
        elif attack_aim == 'low':
            self.body_part = random.choice(low_body)
    
    def set_die_roll(self):
        self.die_roll = gen_mec.roll_die()
    
    def set_success(self):
        """
        Only whole numbers (rounded down) are used to determine the offensive RS.

        TODO: Add a round down for the final RS. Integers only!
        """
        owner = self.owner
        attack_aim = self.attack_aim
        skillset = self.skillset
        skill = self.skill

        attack_rank = owner.skill.return_skill_rank(skillset, skill)
        attack_difficulty = skillsets.skillsets[skillset][skill].get('difficulty')
        attack_rs = owner.skill.return_rank_score(attack_rank, attack_difficulty)

        defend_high, defend_mid, defend_low = self.target.skill.defense_layer_calc(rs_only=True)
        defend_rs = None

        if attack_aim == 'high':
            defend_rs = defend_high
        elif attack_aim == 'mid':
            defend_rs = defend_mid
        elif attack_aim == 'low':
            defend_rs == defend_low

        if attack_rs > defend_rs:
            bonus = attack_rs - defend_rs
            success = 50 - bonus
        elif defend_rs > attack_rs:
            penalty = defend_rs - attack_rs
            success = 50 + penalty
        else:
            success = 50

        # Make sure that the success is never below 5 or above 95, and always 5 if the target is unconscious.
        if success < 5 or self.target.db.ko == True:
            success = 5
        elif success > 95:
            success = 95

        self.success = int(success)
    
    def set_damage_tier(self):
        roll = self.die_roll
        success = self.success

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
        
        self.damage_tier = damage_tier
        self.damage = damage
    
    def set_hit(self):
        if self.die_roll > self.success:
            self.hit = True
        else:
            self.hit = False
    
    def create_attack_desc(self):
        article = self.article
        pronoun = self.pronoun
        prop_name = self.prop_name

        owner = self.owner
        target = self.target
        skillset = self.skillset
        skill = self.skill
        weapon = self.weapon_type
        damage_type = self.damage_type
        body_part = self.body_part
        die_roll = self.die_roll
        success = self.success
        damage_tier = self.damage_tier
        hit = self.hit

        cap = str.capitalize

        wound_tier = {'slash': ['shallow cut', 'cut', 'deep cut', 'severe cut', 'devastating cut'],
                    'pierce': ['faint wound', 'puncture', 'deep puncture', 'severe puncture', 'gaping wound'],
                    'bruise': ['small bruise', 'bruise', 'ugly bruise', 'major bruise', 'fracture']}
        attack_wound = wound_tier[damage_type][damage_tier]

        # owner and target pronouns. Possessive (its, his, her), Singular Subject (it, he, she), Singular Object (it, him, her)
        a_poss, a_sin_sub, a_sin_obj = pronoun(owner)
        t_poss, t_sin_sub, t_sin_obj = pronoun(target)
        
        # TODO: Creatures and other non-proper named entities shouldn't be capitalized except at the beginning of a sentence.
        a_name = prop_name(owner)
        t_name = prop_name(target)
        c_a_name = cap(owner.key)
        c_t_name = cap(target.key)

        # Weapon's article. 'a' or 'an'
        if owner.attributes.has('wielding'):
            wielded = owner.attributes.get('wielding')
            if wielded.get('both'):
                both_weap = wielded.get('both')
                art_weap = article(both_weap.name)
            elif wielded.get('main'):
                main_weap = wielded.get('main')
                art_weap = article(main_weap.name)
            else:
                art_weap = article(weapon)

        if hit:
            owner_outcome = f"{cap(t_sin_sub)} suffers {article(attack_wound)} {attack_wound} to {t_poss} {body_part}."
            target_outcome = f"You suffer {article(attack_wound)} {attack_wound} to your {body_part}."
            others_outcome = f"{c_t_name} suffers {article(attack_wound)} {attack_wound} to {t_poss} {body_part}."
        else:
            self.create_defense_desc(c_a_name, art_weap, t_name)
            owner_outcome = self.owner_outcome
            target_outcome = self.target_outcome
            others_outcome = self.others_outcome

        skillsets = {'staves': 
                        {'leg sweep': 
                            {'owner': f"You sweep your {weapon} at {t_name}\'s legs, {owner_outcome}",
                            'others': f"{c_a_name} sweeps {art_weap} {weapon} at {t_name}\'s legs, {others_outcome}"},
                        'feint': 
                            {'owner': f"You sweep your {weapon} at {target}\'s legs, {owner_outcome}",
                            'others': f"{c_a_name} sweeps {art_weap} {weapon} at {t_name}\'s legs, {others_outcome}"},
                        'end jab': 
                            {'owner': f"You sweep your {weapon} at {target}\'s legs, {owner_outcome}",
                            'others': f"{c_a_name} sweeps {art_weap} {weapon} at {t_name}\'s legs, {others_outcome}"},
                        'swat': 
                            {'owner': f"Using the center of {art_weap} {weapon} as a fulcrum, you swat at {t_name} with one end of the weapon! {owner_outcome}",
                            'target': f"Using the center of {art_weap} {weapon} as a fulcrum, {owner} swats at you with one end of the weapon! {target_outcome}",
                            'others': f"Using the center of {art_weap} {weapon} as a fulcrum, {owner} swats at {t_name} with one end of the weapon! {others_outcome}"},
                        'simple strike': 
                            {'owner': f"You sweep your {weapon} at {t_name}\'s legs, {owner_outcome}",
                            'others': f"{c_a_name} sweeps {art_weap} {weapon} at {t_name}\'s legs, {others_outcome}"},
                        'side strike': 
                            {'owner': f"You sweep your {weapon} at {t_name}\'s legs, {owner_outcome}",
                            'others': f"{c_a_name} sweeps {art_weap} {weapon} at {t_name}\'s legs, {others_outcome}"},
                        'pivot smash': 
                            {'owner': f"You sweep your {weapon} at {t_name}\'s legs, {owner_outcome}",
                            'others': f"{c_a_name} sweeps {art_weap} {weapon} at {t_name}\'s legs, {others_outcome}"},
                        'longarm strike': 
                            {'owner': f"You sweep your {weapon} at {t_name}\'s legs, {owner_outcome}",
                            'others': f"{c_a_name} sweeps {art_weap} {weapon} at {t_name}\'s legs, {others_outcome}"},
                        'parting jab': 
                            {'owner': f"You sweep your {weapon} at {t_name}\'s legs, {owner_outcome}",
                            'others': f"{c_a_name} sweeps {art_weap} {weapon} at {t_name}\'s legs, {others_outcome}"},
                        'parting swat': 
                            {'owner': f"You sweep your {weapon} at {t_name}\'s legs, {owner_outcome}",
                            'others': f"{c_a_name} sweeps {art_weap} {weapon} at {t_name}\'s legs, {others_outcome}"},
                        'parting smash': 
                            {'owner': f"You sweep your {weapon} at {t_name}\'s legs, {owner_outcome}",
                            'others': f"{c_a_name} sweeps {art_weap} {weapon} at {t_name}\'s legs, {others_outcome}"},
                        'defensive sweep': 
                            {'owner': f"You sweep your {weapon} at {t_name}\'s legs, {owner_outcome}",
                            'others': f"{c_a_name} sweeps {art_weap} {weapon} at {t_name}\'s legs, {others_outcome}"},
                        'stepping spin': 
                            {'owner': f"You sweep your {weapon} at {t_name}\'s legs, {owner_outcome}",
                            'others': f"{c_a_name} sweeps {art_weap} {weapon} at {t_name}\'s legs, {others_outcome}"},
                        'snapstrike': 
                            {'owner': f"You sweep your {weapon} at {t_name}\'s legs, {owner_outcome}",
                            'others': f"{c_a_name} sweeps {art_weap} {weapon} at {t_name}\'s legs, {others_outcome}"},
                        'sweep strike': 
                            {'owner': f"You sweep your {weapon} at {t_name}\'s legs, {owner_outcome}",
                            'others': f"{c_a_name} sweeps {art_weap} {weapon} at {t_name}\'s legs, {others_outcome}"},
                        'spinstrike': 
                            {'owner': f"You sweep your {weapon} at {t_name}\'s legs, {owner_outcome}",
                            'others': f"{c_a_name} sweeps {art_weap} {weapon} at {t_name}\'s legs, {others_outcome}"},         
                        'tbash': 
                            {'owner': f"You sweep your {weapon} at {t_name}\'s legs, {owner_outcome}",
                            'others': f"{c_a_name} sweeps {art_weap} {weapon} at {t_name}\'s legs, {others_outcome}"},
                        'whirling block': 
                            {'owner': f"You sweep your {weapon} at {t_name}\'s legs, {owner_outcome}",
                            'others': f"{c_a_name} sweeps {art_weap} {weapon} at {t_name}\'s legs, {others_outcome}"},
                        'pivoting longarm': 
                            {'owner': f"You sweep your {weapon} at {t_name}\'s legs, {owner_outcome}",
                            'others': f"{c_a_name} sweeps {art_weap} {weapon} at {t_name}\'s legs, {others_outcome}"}
                        },
                                                
                    'rat': 
                        {'claw': 
                            {'owner': f"You claw at {t_name} with your front paws! {owner_outcome}",
                            'target': f"{c_a_name} claws at you with {a_poss} front paws! {target_outcome}",
                            'others': f"{c_a_name} claws at {t_name} with {a_poss} front paws! {others_outcome}"},
                        'bite': 
                            {'owner': f"You bite at {t_name} with your teeth! {owner_outcome}",
                            'target': f"{c_a_name} bites at you with {a_poss} teeth! {target_outcome}",
                            'others': f"{c_a_name} bites at {t_name} with {a_poss} teeth! {others_outcome}"}
                        },
                    'spider':
                        {'bite': 
                            {'owner': f"You bite at {t_name} with your teeth! {owner_outcome}",
                            'target': f"{c_a_name} bites at you with {a_poss} teeth! {target_outcome}",
                            'others': f"{c_a_name} bites at {t_name} with {a_poss} teeth! {others_outcome}"}
                        },
                    'snake':
                        {'bite': 
                            {'owner': f"You bite at {t_name} with your teeth! {owner_outcome}",
                            'target': f"{c_a_name} bites at you with {a_poss} teeth! {target_outcome}",
                            'others': f"{c_a_name} bites at {t_name} with {a_poss} teeth! {others_outcome}"}
                        }
                    }

        owner_desc = skillsets[skillset][skill]['owner']
        target_desc = skillsets[skillset][skill]['target']
        others_desc = skillsets[skillset][skill]['others']

        owner.msg(f"|430[Success: {success} Roll: {die_roll}] {owner_desc}|n")
        target.msg(f"|r[Success: {success} Roll: {die_roll}] {target_desc}|n")
        owner.location.msg_contents(f"{others_desc}", exclude=[owner, target])

    def create_defense_desc(self, c_a_name, art_weap, t_name):
        article = self.article

        target = self.target
        aim = self.attack_aim
        weapon = self.weapon_type

        high_skills, mid_skills, low_skills = target.skill.defense_layer_calc(skills_only=True)
        def_skills = []
        miss_chance = 20
        targ_weap = None
        targ_offhand = None
        art_targ_weap = None
        art_targ_offhand = None

        #Get target wielded weapon.
        if target.attributes.get('wielding'):
            targ_wield = target.attributes.get('wielding')
            if targ_wield.get('both'):
                targ_weap = targ_wield['both']
                art_targ_weap = article(targ_weap.name)
            if targ_wield.get('main'):
                targ_weap = targ_wield['main']
                art_targ_weap = article(targ_weap.name)
            if targ_wield.get('off'):
                targ_offhand = targ_wield['off']
                art_targ_offhand = article(targ_offhand.name)


        if aim == 'high':
            skills = high_skills
        elif aim == 'mid':
            skills = mid_skills
        elif aim == 'low':
            skills = low_skills

        layer_count = 0
        for i in skills:
            if i != None:
                layer_count += 1
                def_skills.append(i)
        # TODO: What the heck am I rolling here for? The combat outcome should already be determined. Investigate.
        roll = random.randint(0, 100)

        if roll > miss_chance and layer_count > 0:
            outcome = random.choice(def_skills)
        else:
            outcome = 'miss'

        defense_skills = {'miss':
                            {'owner': "You miss!",
                            'target': f"{c_a_name} misses!",
                            'others': f"{c_a_name} misses!"},
                        'stave mid block':
                            {'owner': f"{t_name} blocks your {weapon} with {art_targ_weap} {targ_weap}!",
                            'target': f"You block {c_a_name}\'s {weapon} with your {targ_weap}!",
                            'others': f"{t_name} blocks {c_a_name}\'s {weapon} with {art_targ_weap} {targ_weap}!"},
                        'stave low block':
                            {'owner': f"{t_name} swings the butt of their {targ_weap} low and blocks your {weapon}!",
                            'target': f"You swing the butt of your {targ_weap} low and block {c_a_name}\'s {weapon}!",
                            'others': f"{t_name} swings the butt of their {targ_weap} low and blocks {c_a_name}\'s {weapon}!"},
                        'stave overhead block':
                            {'owner': f"{t_name} raises their {targ_weap} high and blocks your {weapon}!",
                            'target': f"You raise your {targ_weap} high and block {c_a_name}\'s {weapon}!",
                            'others': f"{t_name} raises their {targ_weap} and blocks {c_a_name}\'s {weapon}!"},
                        'marts dodge':
                            {'owner': f"{t_name} dodges your {weapon}!",
                            'target': f"You dodge {c_a_name}\'s {weapon}!",
                            'others': f"{t_name} dodges {c_a_name}\'s {weapon}!"},
                        'marts duck':
                            {'owner': f"{t_name} squats low and ducks right under your {weapon}!",
                            'target': f"You squat low and duck right under {c_a_name}\'s {weapon}!",
                            'others': f"{t_name} squats low and ducks right under {c_a_name}\'s {weapon}!"},
                        'marts jump':
                            {'owner': f"{t_name} jumps over your {weapon} and you fail to connect!",
                            'target': f"You jump over {c_a_name}\'s {weapon} and {c_a_name} fails to connect!",
                            'others': f"{t_name} jumps over {c_a_name}\'s {weapon} and {c_a_name} fails to connect!"}
                        }

        self.owner_outcome = defense_skills[outcome]['owner']
        self.target_outcome = defense_skills[outcome]['target']
        self.others_outcome = defense_skills[outcome]['others']

    def take_damage(self, attacker, damage):
        owner = self.owner
        name = owner.key
        location = owner.location
        
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
            self.death()

    def death(self):
        """
        Handle the owner's death.

        Removes the owner from any currently approached objects' approached list.
        Clears the owner's approached list.

        If the owner is not puppeted by a player, call its on_death() method.
        Resurrects the character if puppeted by a player. (temporary)
        """
        owner = self.owner
        for char in self.approached_list:
            if char is not None:
                # Request that each approached object remove this owner from its list.
                char.combat.remove_approached(owner)
        self.clear_approached()
        if not owner.has_account:
            owner.on_death()
        else:
            owner.db.hp['current_hp'] = owner.db.hp['max_hp']
            owner.location.msg_contents(f"{owner.name} dies and is resurrected to full health.", exclude=owner)
            owner.msg("You die and are resurrected to full health.")
            owner.db.ko = False

#-------------------------------------------------------------------------------------#

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
