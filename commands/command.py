"""
Commands

Commands describe the input the account can do to the game.

"""

from evennia import Command as BaseCommand
from evennia.commands.default.building import ObjManipCommand
from evennia import InterruptCommand
from evennia.utils.evmenu import EvMenu
from evennia.utils import create, inherits_from
from world import skillsets, attack_desc
from world.generic_str import article


class Command(BaseCommand):
    """
    Inherit from this if you want to create your own command styles
    from scratch.  Note that Evennia's default commands inherits from
    MuxCommand instead.

    Note that the class's `__doc__` string (this text) is
    used by Evennia to create the automatic help entry for
    the command, so make sure to document consistently here.

    Each Command implements the following methods, called
    in this order (only func() is actually required):
        - at_pre_cmd(): If this returns anything truthy, execution is aborted.
        - parse(): Should perform any extra parsing needed on self.args
            and store the result on self.
        - func(): Performs the actual work.
        - at_post_cmd(): Extra actions, often things done after
            every command, like prompts.
    """
    pass

class CmdDesc(Command):
    key = "desc"
    def func(self):
        caller = self.caller
        desc = caller.desc()
        self.msg(desc)

class CmdCharGen(Command):
    key = "chargen"

    def func(self):
        caller = self.caller
        EvMenu(caller, "world.chargen", startnode="main", cmd_on_exit="look", cmdset_mergetype="Replace", cmdset_priority=1,
       auto_quit=True, auto_look=True, auto_help=True)

class CmdLearnSkill(Command):
    key = 'learn'
    """
    Usage: learn <skillset> <skill>
    """

    def parse(self):
        caller = self.caller
        args = self.args.lstrip()
        try:
            self.skillset, self.skill = args.split(" ", 1)
        except ValueError:
            caller.msg("Usage: learn <skillset> <skill>")
            raise InterruptCommand

        if self.skillset not in skillsets.VIABLE_SKILLSETS:
            caller.msg(f"{self.skillset} is not a viable skillset!")
            raise InterruptCommand
        if self.skill not in skillsets.VIABLE_SKILLS:
            caller.msg(f"{self.skill} is not a viable skill of {self.skillset}!")
            raise InterruptCommand

    def func(self):
        caller = self.caller
        if not self.args:
            caller.msg('Usage: learn <skillset> <skill>')
            return

        skillsets.learn_skill(self.caller, self.skillset, self.skill)

class CmdGrantSP(Command):
    key = '@grant-sp'
    '''
    Usage: @grant-sp <person> <number> <skillset>
    '''
    def parse(self):
        caller = self.caller
        args = self.args.lstrip()
        try:
            self.person, self.number, self.skillset = args.split(" ", 2)
        except ValueError:
            caller.msg("Requires 3 arguments. Usage: @grant-sp <person> <number> <skillset>")
            raise InterruptCommand

        self.char = caller.search(self.person)
        if not self.char:
            raise InterruptCommand

        try:
            self.number = int(self.number)
        except ValueError:
            caller.msg("The number must be an integer.")
            raise InterruptCommand
        print(f"Viable Skillsets: {skillsets.VIABLE_SKILLSETS}")
        if self.skillset not in skillsets.VIABLE_SKILLSETS:
            caller.msg(f"{self.skillset} is not a viable skillset!")
            raise InterruptCommand
    
    def func(self):
        caller = self.caller
        char = self.char
        num = self.number
        skillset = self.skillset
        skillset = char.attributes.get(skillset)
        skillset['total_sp'] += num
        caller.msg(f'Granted {char} {num} skillpoints in {self.skillset}.')

class CmdTest(Command):
    key = 'testy'

    def func(self):
        caller = self.caller
        attacker = caller
        target = 'rat'
        damage_type = 'bruise'
        damage_tier = 2
        body_part = 'head'
        attacker_desc, target_desc = attack_desc.create_attack_desc(attacker, target, damage_type, damage_tier, body_part)
        caller.msg(attacker_desc)
        caller.msg(target_desc)

class CmdCreate(ObjManipCommand):
    """
    create new objects
    Usage:
      create[/drop] <objname>[;alias;alias...][:typeclass], <objname>...
    switch:
       drop - automatically drop the new object into your current
              location (this is not echoed). This also sets the new
              object's home to the current location rather than to you.
    Creates one or more new objects. If typeclass is given, the object
    is created as a child of this typeclass. The typeclass script is
    assumed to be located under types/ and any further
    directory structure is given in Python notation. So if you have a
    correct typeclass 'RedButton' defined in
    types/examples/red_button.py, you could create a new
    object of this type like this:
       create/drop button;red : examples.red_button.RedButton
    """

    key = "create"
    switch_options = ("drop",)
    locks = "cmd:perm(create) or perm(Builder)"
    help_category = "Building"

    # lockstring of newly created objects, for easy overloading.
    # Will be formatted with the {id} of the creating object.
    new_obj_lockstring = "control:id({id}) or perm(Admin);delete:id({id}) or perm(Admin)"

    def func(self):
        """
        Creates the object.
        """

        caller = self.caller

        if not self.args:
            string = "Usage: create[/drop] <newname>[;alias;alias...] [:typeclass.path]"
            caller.msg(string)
            return

        # create the objects
        for objdef in self.lhs_objs:
            string = ""
            name = objdef['name']
            art = article(name)
            name = f"{art} {name}"
            aliases = objdef['aliases']
            typeclass = objdef['option']

            # create object (if not a valid typeclass, the default
            # object typeclass will automatically be used)
            lockstring = self.new_obj_lockstring.format(id=caller.id)
            obj = create.create_object(typeclass, name, caller,
                                       home=caller, aliases=aliases,
                                       locks=lockstring, report_to=caller)
            if not obj:
                continue
            if aliases:
                string = "You create a new %s: %s (aliases: %s)."
                string = string % (obj.typename, obj.name, ", ".join(aliases))
            else:
                string = "You create a new %s: %s."
                string = string % (obj.typename, obj.name)
            # set a default desc
            if not obj.db.desc:
                obj.db.desc = "You see nothing special."
            if 'drop' in self.switches:
                if caller.location:
                    obj.home = caller.location
                    obj.move_to(caller.location, quiet=True)
        if string:
            caller.msg(string)

class CmdInventory(Command):
    """
    Shows your inventory.

    Usage:
      inventory
      inv
      i
    """
    key = "inventory"
    aliases = ["inv", "i"]
    locks = "cmd:all()"

    def func(self):
        """check inventory"""

        caller = self.caller
        items = caller.contents
        left_hand, right_hand = caller.db.hands.values()

        # Remove hands and append all other items to a new list.
        filtered_items = []
        for i in items:
            if i not in [left_hand, right_hand]:
                filtered_items.append(i)

        if not filtered_items:
            string = "Your inventory is empty."
        else:
            table = self.styled_table(border="header")
            for item in filtered_items:
                table.add_row(f"|C{item.name}|n {item.db.desc or ''}")
            string = f"|wYou are carrying:\n{table}"
        caller.msg(string)

class CmdInhand(Command):
    key = 'inhand'
    aliases = 'inh'
    
    def func(self):
        caller = self.caller

        left_wield, right_wield, both_wield  = caller.db.wielding.values()

        left_hand, right_hand = caller.db.hands.values()

        if left_hand:
            left_item = left_hand.name
        else:
            left_item = 'nothing'

        if right_hand:
            right_item = right_hand.name
        else:
            right_item = 'nothing'

        if not left_hand and not right_hand:
            caller.msg(f"Your hands are empty.")
            return
        
        
        if left_wield and not right_wield:
            caller.msg(f"You are wielding {left_item} in your left hand and holding {right_item} in your right hand.")
        elif right_wield and not left_wield:
            caller.msg(f"You are holding {left_item} in your left hand and wielding {right_item} in your right hand.")
        elif left_wield and right_wield:
            caller.msg(f"You are wielding {left_item} in your left hand and {right_item} in your right hand.")
        elif both_wield:
            caller.msg(f"You are wielding {right_item} in both hands.")
        else:
            caller.msg(f"You are holding {left_item} in your left hand and {right_item} in your right hand.")

class CmdStand(Command):
    key = 'stand'
    def func(self):
        caller = self.caller
        db = caller.db
        if db.standing:
            caller.msg("You are already standing.")
            return
        else:
            db.standing = True
            db.kneeling = False
            db.sitting = False
            db.lying = False
            caller.msg("You stand up.")

class CmdSit(Command):
    key = 'sit'
    def func(self):
        caller = self.caller
        db = caller.db
        if db.sitting:
            caller.msg("You are already sitting.")
        else:
            db.standing = False
            db.kneeling = False
            db.sitting = True
            db.lying = False
            caller.msg("You sit down.")

class CmdKneel(Command):
    key = 'kneel'
    def func(self):
        caller = self.caller
        db = caller.db
        if db.kneeling:
            caller.msg("You are already kneeling.")
        else:
            db.standing = False
            db.kneeling = True
            db.sitting = False
            db.lying = False
            caller.msg("You kneel.")

class CmdLie(Command):
    key = 'lie'
    aliases = ['lay',]
    def func(self):
        caller = self.caller
        db = caller.db
        if db.lying:
            caller.msg("You are already lying down.")
        else:
            db.standing = False
            db.kneeling = False
            db.sitting = False
            db.lying = True
            caller.msg("You lie down.")


class CmdGet(Command):
    """
    Pick up something.

    Usage:
      get <obj>
      take <obj>

    Gets an object from your inventory or location and places it in your hands.
    """
    key = "get"
    aliases = ["take",]
    locks = "cmd:all()"
    

    def func(self):
        """implements the command."""

        caller = self.caller
        if not self.args:
            caller.msg("Get what?")
            return
        args = self.args.strip()

        left_wield, right_wield, both_wield  = caller.db.wielding.values()
        left_hand, right_hand = caller.db.hands.values()
        

        obj = caller.search(args, location=[caller.location, caller])
        if not obj:
            return
        if caller == obj:
            caller.msg("You can't get yourself.")
            return
        if not obj.access(caller, 'get'):
            if obj.db.get_err_msg:
                caller.msg(obj.db.get_err_msg)
            else:
                caller.msg("You can't get that.")
            return
        if obj in [left_hand, right_hand]:
            caller.msg(f"You are already carrying {obj.name}.")
            return

        # calling at_before_get hook method
        if not obj.at_before_get(caller):
            return
        
        # Check if wielding a single weapon/shield in left hand and stow it.
        if left_wield:
            caller.msg(f"You stop wielding {left_hand.name} and stow it away.")
            caller.db.hands['left'] = None
            caller.db.wielding['left'] = None

        # If both hands have objects, stow the dominate hand.
        if right_hand and left_hand:
            caller.msg(f"You stow away {right_hand.name}.")
            caller.location.msg_contents(f"{caller.name} stows away {right_hand.name}.", exclude=caller)
            caller.db.hands['right'] = None

        # Wielding with both hands technically only holds the item in the right hand (for now).
        # So we already know the left hand is free to get items.
        if both_wield:
            caller.msg(f"You stop wielding {both_wield.name}.")
            caller.location.msg_contents(f"{caller.name} stops wielding {both_wield.name}.", exclude=caller)
            caller.db.wielding['both'] = None

        # Decide the location of the item and echo it.
        elif obj.location == caller:
            caller.msg(f"You get {obj.name} from your inventory.")
            caller.location.msg_contents(f"{caller.name} gets {obj.name} from their inventory.", exclude=caller)
        elif obj.location == caller.location:
            caller.msg(f"You pick up {obj.name}.")
            caller.location.msg_contents(f"{caller.name} picks up {obj.name}.", exclude=caller)

        if right_hand and not left_hand:
            caller.db.hands['left'] = obj
        else:
            caller.db.hands['right'] = obj
        
        obj.move_to(caller, quiet=True)

        # calling at_get hook method
        obj.at_get(caller)

class CmdDrop(Command):
    """
    drop something
    Usage:
      drop <obj>
    Lets you drop an object from your inventory into the
    location you are currently in.
    """

    key = "drop"
    locks = "cmd:all()"
    

    def func(self):
        """Implement command"""

        caller = self.caller
        if not self.args:
            caller.msg("Drop what?")
            return
        args = self.args.strip()

        left_hand, right_hand = caller.db.hands.values()

        wielding = caller.db.wielding
        left_wield, right_wield, both_wield  = wielding.values()
        
        obj = caller.search(args, location=[caller, caller.location],
                            nofound_string=f"You can't find {args}.",
                            multimatch_string=f"There are more than one {args}.")
        if not obj:
            return

        # Call the object script's at_before_drop() method.
        if not obj.at_before_drop(caller):
            return

        
        if obj in [left_hand, right_hand]:
            # If the object is currently wielded, stop wielding it and drop it.
            if obj in [left_wield, right_wield, both_wield]:
                caller.msg(f"You stop wielding {obj.name} and drop it.")
                caller.location.msg_contents(f"{caller.name} stops wielding {obj.name} and drops it.", exclude=caller)
                if left_wield:
                    wielding['left'] = None
                else:
                    wielding['right'], wielding['both'] = None, None
            else:
                caller.msg(f"You drop {obj.name}.")
                caller.location.msg_contents(f"{caller.name} drops {obj.name}.", exclude=caller)
            if obj == left_hand:
                caller.db.hands['left'] = None
            else:
                caller.db.hands['right'] = None
        elif obj.location == caller:
            caller.msg(f"You pull {obj.name} from your inventory and drop it on the ground.")
            caller.location.msg_contents(f"{caller.name} pulls {obj.name} from their inventory and drops it on the ground.", exclude=caller)
        elif obj.location == caller.location:
            caller.msg(f"The {obj.name} is already on the ground.")
            return

        obj.move_to(caller.location, quiet=True)

        # Call the object script's at_drop() method.
        obj.at_drop(caller)

class CmdStow(Command):
    """
    pick up something
    Usage:
      get <obj>
    Picks up an object from your location and puts it in
    your inventory.
    """

    key = 'stow'
    locks = 'cmd:all()'
    

    def func(self):
        """implements the command."""
        caller = self.caller
        if not self.args:
            caller.msg("Stow what?")
            return
        args = self.args.strip()

        left_hand, right_hand = caller.db.hands.values()
        wielding = caller.db.wielding
        left_wield, right_wield, both_wield  = wielding.values()
        
        obj = caller.search(args, location=[caller.location, caller],
                            nofound_string=f"You can't find {args}.",
                            multimatch_string=f"There are more than one {args}.")
        if not obj:
            return
        if caller == obj:
            caller.msg("You can't get yourself.")
            return
        if not obj.access(caller, 'get'):
            if obj.db.get_err_msg:
                caller.msg(obj.db.get_err_msg)
            else:
                caller.msg("You can't get that.")
            return

        # calling at_before_get hook method
        if not obj.at_before_get(caller):
            return
        
        if obj in [left_hand, right_hand]:
            # If the stowed object is currently wielded, stop wielding it and stow it.
            if obj in [left_wield, right_wield, both_wield]:
                caller.msg(f"You stop wielding {obj.name} and stow it away.")
                caller.location.msg_contents(f"{caller.name} stops wielding {obj.name} and stows it away.", exclude=caller)
                if obj == left_wield:
                    wielding['left'] = None
                elif obj == right_wield:
                    wielding['right'] = None
                else:
                    wielding['both'] = None
            else:
                caller.msg(f"You stow away {obj.name}.")
                caller.location.msg_contents(f"{caller.name} stows away {obj.name}.", exclude=caller)
            if obj == left_hand:
                caller.db.hands['left'] = None
            else:
                caller.db.hands['right'] = None
        elif obj.location == caller.location:
            caller.msg(f"You pick up {obj.name} and stow it away.")
            caller.location.msg_contents(f"{caller.name} picks up {obj.name} and stows it away.", exclude=caller)
            obj.move_to(caller, quiet=True)
        elif obj.location == caller:
            caller.msg(f"You already have {obj.name} in your inventory.")
            return

        # calling at_get hook method
        obj.at_get(caller)

class CmdWield(Command):
    """
    Wield a weapon.
    
    Usage: wield <weapon>
    """
    key = 'wield'

    def func(self):
        caller = self.caller
        if not self.args:
            caller.msg("Usage: wield <weapon>")
            return
        args = self.args.strip()
        left_hand, right_hand = caller.db.hands.values()
        left_wield, right_wield, both_wield = caller.db.wielding.values()

        obj = caller.search(args, location=[caller],
                            nofound_string="You must be holding a weapon to wield it.",
                            multimatch_string=f"There are more than one {args}.")
        if not obj:
            return
        if obj == caller:
            caller.msg("You can't wield yourself.")
            return
        if not obj.attributes.get('wieldable'):
            caller.msg("That's not a wieldable item.")
        if obj in [left_wield, right_wield, both_wield]: # Check for an item already wielded.
            caller.msg(f"You are already wielding {obj.name}.")
            return

        hands_req = obj.attributes.get('wieldable')

        # Right hand is dominate.


        if obj not in [left_hand, right_hand]: # Automagically get the object from the inventory.
            if right_hand and not right_wield:
                caller.msg(f"You stow away {right_hand.name}.")
                caller.location.msg_contents(f"{caller.name} stows away {right_hand.name}.", exclude=caller)
                caller.db.hands['right'] = None
            caller.msg(f"You get {obj.name} from your inventory.")
            caller.location.msg_contents(f"{caller.name} gets {obj.name} from their inventory.", exclude=caller)
            caller.db.hands['right'] = obj
            # Refresh hand variables before the next check.
            left_hand, right_hand = caller.db.hands.values()
            
        
        if obj in [left_hand, right_hand]:
            if hands_req == 1:
                if inherits_from(obj, 'typeclasses.objects.OffHand'): #For wielding shields.
                    if obj == right_hand and not right_wield:
                        if left_hand: # If theres any item in the left hand, stow it first.
                            caller.db.hands['left'] = None
                            caller.msg(f"You stow away {left_hand.name}.")
                            caller.location.msg_contents(f"{caller.name} stows away {left_hand.name}.", exclude=caller)
                        # Send the offhand weapon to the left hand.
                        caller.db.hands['right'] = None
                        caller.db.hands['left'] = obj
                        caller.msg(f"You swap {obj.name} to your left hand.")
                        caller.location.msg_contents(f"{caller.name} swaps {obj.name} to their left hand.", exclude=caller)
                    # Offhand item is certainly already in the left hand.
                    caller.msg(f"You wield {obj.name} in your left hand.")
                    caller.location.msg_contents(f"{caller.name} wields {obj.name} in their left hand.", exclude=caller)
                    caller.db.wielding['left'] = obj
                elif obj == left_hand and not inherits_from(obj, 'typeclasses.objects.OffHand'): # Make sure the item is a main hand wield.
                    caller.msg(f"You swap the contents of your hands and wield {obj.name} in your right hand.")
                    caller.location.msg_contents(f"{caller.name} swaps the content of their hands "
                                                    f"and wields {obj.name} in their right hand.", exclude=caller)
                    caller.db.hands['right'] = obj
                    if right_hand:
                        caller.db.hands['right'] = None
                        caller.db.hands['left'] = obj
                    caller.db.wielding['right'] = obj
                elif obj == right_hand and not inherits_from(obj, 'typeclasses.objects.OffHand'): # Make sure the item is a main hand wield.
                    caller.msg(f"You wield {obj.name} in your right hand.")
                    caller.location.msg_contents(f"{caller.name} wields {obj.name} in their right hand.", exclude=caller)
                    caller.db.wielding['right'] = obj
            elif hands_req == 2:
                if obj == left_hand:
                    if right_hand:
                        caller.msg(f"You stow away {right_hand.name}.")
                        caller.location.msg_contents(f"{caller.name} stows away {right_hand}.", exclude=caller)
                        caller.db.hands['right'] = None
                elif obj == right_hand:
                    if left_hand:
                        caller.msg(f"You stow away {left_hand.name}.")
                        caller.location.msg_contents(f"{caller.name} stows away {left_hand}.", exclude=caller)
                        caller.db.hands['left'] = None
                caller.msg(f"You wield {obj.name} in both hands.")
                caller.location.msg_contents(f"{caller.name} wields {obj.name} in both hands.", exclude=caller)
                caller.db.wielding['both'] = obj
        elif obj.location == caller.location:
            caller.msg(f"You must be carrying a weapon to wield it.")
            return

class CmdUnwield(Command):
    """
    Unwield a weapon.
    Usage: unwield
    """

    key = 'unwield'

    def func(self):
        caller = self.caller
        wielding = caller.db.wielding
        left_wield, right_wield, both_wield  = wielding.values()
        
        if left_wield:
            caller.msg(f"You stop wielding {left_wield.name} in your offhand.")
            caller.location.msg_contents(f"{caller.name} stops wielding {left_wield.name} in their offhand.", exclude=caller)
            wielding['left'] = None
        elif right_wield and not left_wield:
            caller.msg(f"You stop wielding {right_wield.name}.")
            caller.location.msg_contents(f"{caller.name} stops wielding {right_wield.name}.", exclude=caller)
            wielding['right'] = None
        else:
            caller.msg(f"You stop wielding {both_wield.name}.")
            caller.location.msg_contents(f"{caller.name} stops wielding {both_wield.name}.", exclude=caller)
            wielding['both'] = None

class CmdLook(Command):
    """
    look at location or object
    Usage:
      look
      look <obj>
      look *<account>
    Observes your location or objects in your vicinity.
    """
    key = "look"
    aliases = ["l", "ls"]
    locks = "cmd:all()"
    
    def func(self):
        """
        Handle the looking.
        """
        caller = self.caller
        if not self.args:
            target = caller.location
            if not target:
                caller.msg("You have no location to look at!")
                return
        else:
            args = self.args.strip()
            target = caller.search(args, location=[caller, caller.location])
            if not target:
                return
        self.msg((caller.at_look(target), {'type': 'look'}), options=None)


class CmdMatch(Command): #TODO: NOT FINISHED
    """
    Matches object in location or inventory.

    Usage: match <object>
    """
    key = 'match'

    def func(self):
        if not self.args:
            self.caller.msg("Usage: match <object>")
            return
        
        args = self.args.lstrip()

        obj = self.caller.search(args, location=[self.caller.location, self.caller])

        if not obj:
            self.caller.msg(f"Could not find {self.args}.")
            return
        else:
            self.caller.msg(f"Object found {self.args}.")
    pass