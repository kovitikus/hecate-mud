from evennia import DefaultCharacter

class DefaultMob(DefaultCharacter):
    def at_object_creation(self):
        self.db.hp = 100