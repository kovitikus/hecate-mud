from evennia import DefaultCharacter

class DefaultMob(DefaultCharacter):
    def at_object_creation(self):
        self.db.hp = 100
        self.db.ko = False
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
    def at_object_creation(self):
        pass
    def bite(self):
        pass