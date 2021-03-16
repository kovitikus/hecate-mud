from evennia.utils.utils import delay

class StatusHandler:
    afk_delay = None

    def __init__(self, owner):
        self.owner = owner

#--------------------
# AFK status check - https://i.imgur.com/U2EiL7F.png
    #-----------
    # afk_check is called from the Command typeclass at_pre_cmd method.
    def afk_check(self):
        owner = self.owner

        # Player's AFK timer in seconds. 
        # Set by commands.command.CmdAFKTimer
        if not owner.attributes.has('afk_timer'):
            owner.attributes.add('afk_timer', 600) #10 minutes
        afk_timer = owner.attributes.get('afk_timer')

        if not owner.attributes.has('afk'):
            owner.attributes.add('afk', False)
        
        if owner.db.afk == True:
            self.afk_off()
        
        if self.afk_delay is not None:
            self.afk_delay.cancel()

        self.afk_delay = delay(afk_timer, self.afk_on)
 
    #--------------------
    # AFK Helpers
    def afk_on(self):
        owner = self.owner

        # Delay timer expired, player is unresponsive.
        owner.db.afk = True
        owner.msg("|yYou are now AFK.|n")

    def afk_off(self):
        owner = self.owner

        # Player was AFK, but has returned to the keyboard.
        owner.db.afk = False
        owner.msg("|yYou are no longer AFK.|n")
