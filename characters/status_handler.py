import inflect

from evennia.utils.utils import delay

_INFLECT = inflect.engine()

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


    def can_attack(self, required_weapon):
        owner = self.owner
        can_attack = True
        err_msg = ''

        if not owner.db.standing:
            can_attack = False
            err_msg = "You must be standing to attack!"

        main_wield, off_wield, both_wield = owner.db.wielding.values()
        weapon_tags = [
            main_wield.tags.get(category='weapon'),
            off_wield.tags.get(category='weapon'),
            both_wield.tags.get(category='weapon')
        ]

        if required_weapon not in weapon_tags:
            wielding = owner.equip.wield(required_weapon)
            if not wielding:
                can_attack = False
                err_msg = f"You do not have {_INFLECT.a(required_weapon)} wielded!"

        return can_attack, err_msg

    def can_be_attacked(self):
        owner = self.owner
        can_be_attacked = True
        err_msg = ''

        return can_be_attacked, err_msg

    def can_be_damaged(self):
        owner = self.owner
        can_be_damaged = True
        err_msg = ''

        invulnerable = owner.attributes.get("invulnerable", default=False)
        invincible = owner.attributes.get("invincible", default=False)
        if invulnerable or invincible:
            can_be_damaged = False

        return can_be_damaged, err_msg

    def get_status(self, status=None):
        """
        Returns the requested status effects of the owner, based on the kwarg provided.
        Prefers to check this handler's self.status property.

        Keyword Arguments:
            status (string): Name of the status requested.

        Returns:
            dict or None:
                Returns the single dictionary requested by the status kwarg.
                If set to none, return the dictionary of all statuses on the owner.
        """
        if self.status is None:
            # This is the first time the get_status() method has been called by this handler's owner.
            # Retrieves the current database copy of the owner's status.
            # Saves it to this StatusHandler.

            # (key: Status Name / value (dict): Status Details)
            #---
            # body_recovery_cd: {seconds: 10.1}
            # mind_recovery_cd: {seconds: 2.3}
            # shrine_of_hecates_light: {tenacity: 3, awareness: 5, light_magic_pwr: 10, length: utils.delay}
            self.status = dict(self.owner.attributes.get('status'))
                # dict() method breaks the _SaverDict
                # https://www.evennia.com/docs/latest/Attributes.html#retrieving-mutable-objects

        if status is None: # The kwarg of this method.
            # Returns a dictionary of the owner's status effects.
            # Retrieved from the StatusHandler.

            # (key: Status Name / value (dict): Status Details)
            #---
            return self.status
        else:
            # Returns a single status details dictionary.

            # (key: Status Detail / value: Value)
            #---
            # (body_recovery_cd): 3.8
            # (damage_over_time_tickrate): 7.2
            return self.status.get(status, None)

    def set_status(self, status_name, status_effect, value):
        status_dict = self.status.get(status_name, None)
        if status_dict is None:
            return "Status not found."

        effect_dict = self.status.get(status_effect, None)
        if effect_dict is None:
            return "Status effects not found."

        self.status[status_name][status_effect] = value
        self._save_status()

    def _save_status(self):
        self.owner.db.status = self.status

    def check_ko(self):
        msg = ''
        ko = False
        if self.status['ko'] == True:
            ko = True
            msg("You can't do that while unconscious!")
        return msg, ko
