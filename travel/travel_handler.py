from misc import general_mechanics as gen_mec

# Handles the traversal of objects to/from other objects.
class TravelHandler:
    def __init__(self, owner):
        self.owner = owner

    def traverse_cardinal_exit(self, direction):
        owner = self.owner
        self.direction = direction
        self.exit_obj = None
        self.travellers = [owner, *list(owner.db.followers)]
        self.all_travellers_cleared = True
        self.cleared_travellers = []

        # This option allows the player to abandon a party member if they fail to traverse with the rest of the party.
        # Its value is set by the player via the 'abandonfailedtraveler' or 'abft' command in the travel_cmds.py module.
        self.abandon_failed_traveller = owner.account.db.abandon_failed_traveller

        self.find_exit(direction)

        if self.exit_obj:
            self.check_traveller_access()
        else:
            return False

        if self.all_travellers_cleared:
            self.traverse_exit()
            return True

#-------------------------------------------------------------------
    def find_exit(self):
        for x in self.owner.location.contents:
            if x.db.card_dir == self.direction:
                self.exit_obj = x

    def check_traveller_access(self):
        owner = self.owner
        exit_obj = self.exit_obj
        
        for obj in self.travellers:
            if exit_obj.access(obj, "traverse"):
                self.cleared_travellers.append(obj)
            else:
                if self.abandon_failed_traveller == False:
                    self.halt_travel(obj)
                    break # Abandon the for loop and return from the method immediately.
                else:
                    self.abandon_traveller(obj)
                    
    def halt_travel(self, obj):
        owner = self.owner

        self.all_travellers_cleared == False
        owner.msg(f"You failed to traverse the exit. {obj.get_display_name(owner)} "
                    "does not have permission to enter {exit_obj.get_display_name(owner)}.")
        obj.msg(f"Your leader, {owner.get_display_name(obj)},has failed to traverse an exit. "
                    "You do not have permission to enter {exit_obj.get_display_name(obj)}.")

    def abandon_traveller(self, obj):
        owner = self.owner
        exit_obj = self.exit_obj

        # Object does not have access to traverse the exit and will be abandoned.
        owner.msg(f"Your follower, {obj.get_display_name(owner)}, "
                    "does not have permission to enter {exit_obj.get_display_name(owner)} and will be abandoned.")
        obj.msg(f"You do not have permission to enter {exit_obj.get_display_name(obj)} "
                    "and have been abandoned by your leader, {owner.get_display_name(obj)}.")

        # Clear this object from the leader's follower list.
        owner.db.followers.remove(obj)
        # Clear this object's leader attribute.
        obj.db.leader = None

        # Generic error message stuff I copied from ExitCommand that I'm not sure I still need.
        if exit_obj.db.err_traverse:
            # if exit has a better error message, let's use it.
            obj.msg(exit_obj.db.err_traverse)
        else:
            # No shorthand error message. Call hook.
            exit_obj.at_failed_traverse(obj)

    def traverse_exit(self):
        owner = self.owner
        travellers = self.travellers
        follower_list = travellers
        exit_obj = self.exit_obj

        # Execute the traversal of all traveller objects.
        for obj in travellers:
            if owner == obj:
                follower_list.remove(owner)
                follower_list = gen_mec.comma_separated_string_list(gen_mec.objects_to_strings(follower_list))
                owner.msg(f"You are followed by {follower_list} as you travel to {exit_obj.get_display_name(owner)}.")
            else:
                obj.msg(f"You follow {owner.get_display_name(obj)} as they travel to {exit_obj.get_display_name(obj)}.")
                exit_obj.at_traverse(obj, exit_obj.destination)
