from evennia.utils.utils import delay

class StatusHandler:
    def __init__(self, owner):
        self.owner = owner

#--------------------
# AFK status check
    def afk_check(self):
        owner = self.owner

        # Default AFK timer in seconds. (10 minutes)
        if not owner.attributes.has('afk_timer'):
            owner.attributes.add('afk_timer', 600)

        # Player's AFK time preference, in seconds.
        afk_timer = owner.attributes.get('afk_timer')

        if not owner.attributes.has('afk'):
            owner.attributes.add('afk', False)
        
        if owner.db.afk == True:
            self.afk_off()

        delay(afk_timer, self.afk_on)
 
    #--------------------
    # AFK Helpers
    def afk_on(self):
        owner = self.owner

        # Delay timer expired, player is present.
        owner.db.afk = True
        owner.msg("|yYou are now AFK.|n")

    def afk_off(self):
        owner = self.owner

        # Player was AFK, but has returned to the keyboard.
        owner.db.afk = False
        owner.msg("|yYou are no longer AFK.|n")
