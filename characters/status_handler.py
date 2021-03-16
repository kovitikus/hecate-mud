class StatusHandler:
    def __init__(self, owner):
        self.owner = owner

    def afk(self):
        self.owner.db.afk = True
        self.owner.msg("|yYou are now AFK.|n")
