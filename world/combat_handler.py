from evennia import utils
import time
import random

class CombatHandler:
    def __init__(self, owner):
        self.owner = owner

    wound_tier = {'slash': ['shallow cut', 'cut', 'deep cut', 'severe cut', 'devastating cut'],
    'pierce': ['faint wound', 'puncture', 'deep puncture', 'severe puncture', 'gaping wound'],
    'bruise': ['small bruise', 'bruise', 'ugly bruise', 'major bruise', 'fracture']}


    def create_attack_desc(self, attacker, target, damage_type, damage_tier, body_part):
        attack_wound = self.wound_tier[damage_type][damage_tier]
        determiner = 'an' if attack_wound[0] in ['a', 'e', 'i', 'o', 'u'] else 'a'

        if not attacker.attributes.has('figure'):
            a_gender_pos = 'its'
            a_gender_sin = 'it'
        elif attacker.db.figure['gender'] == 'male':
            a_gender_pos = 'his'
            a_gender_sin = 'he'
        elif attacker.db.figure['gender'] == 'female':
            a_gender_pos = 'her'
            a_gender_sin = 'she'

        if not target.attributes.has('figure'):
            t_gender_pos = 'its'
            t_gender_sin = 'it'
        elif target.db.figure['gender'] == 'male':
            t_gender_pos = 'his'
            t_gender_sin = 'he'
        elif target.db.figure['gender'] == 'female':
            t_gender_pos = 'her'
            t_gender_sin = 'she'


        attacker_desc = str.capitalize(f"{t_gender_sin} suffers {determiner} {attack_wound} to {t_gender_pos} {body_part}.")
        target_desc = str.capitalize(f"you suffer {determiner} {attack_wound} to your {body_part}.")

        return attacker_desc, target_desc

    def attack(self, target, damage_type):  
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
        if time_remaining > 0:
            if time_remaining >= 2:
                message = f"You need to wait {int(time_remaining)} more seconds."
            elif time_remaining >= 1 and time_remaining < 2:
                message = f"You need to wait {int(time_remaining)} more second."
            elif time_remaining < 1:
                message = f"You are in the middle of something."
            self.owner.msg(message)
            return

        # roll = random.randint(1, 100)
        # success = random.randint(5, 95)
        roll = 100
        success = 0

        #temp values
        damage_tier = 0
        body_part = 'head'

        a_desc, t_desc = self.create_attack_desc(self.owner, target, damage_type, damage_tier, body_part)

        if roll > success:
            self.owner.msg(f"[Success: {success} Roll: {roll}] You bash {target} with your stave! " + a_desc)
            self.take_damage(target, damage)
        else:
            self.owner.msg(f"[Success: {success} Roll: {roll}] You miss {target} with your stave!")
        utils.delay(3, self.unbusy)
        self.owner.db.attack_cd = now

    def take_damage(self, target, damage):
        mob = target.key
        location = target.location
        
        hp = target.db.hp
        hp -= damage
        target.db.hp = hp
        
        location.msg_contents(f'{mob} has {hp} health remaining!')
        if hp >= 1:
            target.db.ko = False
        elif hp <= 0 and target.db.ko != True:
            target.db.ko = True
            location.msg_contents(f'{mob} falls unconscious!')
        if hp <= -100:
            okay = target.delete()
            if not okay:
                location.msg_contents(f'\nERROR: {mob} not deleted, probably because delete() returned False.')
            else:
                location.msg_contents(f'{mob} breathes a final breath and expires.')
        return
    
    def unbusy(self):
            self.owner.msg('|yYou are no longer busy.|n')