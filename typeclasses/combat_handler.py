from evennia import DefaultScript
import random

class CombatHandler(DefaultScript):
    def roll_die(self):
        roll = random.randint(1, 100)
        success = random.randint(0, 95)
        if roll > success:
            hit = True
        else:
            hit = False
        return roll, success, hit

    def bash(self, attacker, target):
        roll, success, hit = roll_die(self)
        if hit:
            attacker.msg(f'[Success: {success} Roll: {roll}] You bash {target} with your stave!')
        else:
            attacker.msg(f'[Success: {success} Roll: {roll}] You miss {target} with your stave!')
        