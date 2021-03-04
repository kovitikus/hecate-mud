from evennia import DefaultCharacter
from evennia.utils.create import create_object
from evennia.utils.utils import (list_to_string, inherits_from, lazy_property)

from skills.combat_handler import CombatHandler
from skills.skill_handler import SkillHandler
from npcs.merchant_handler import MerchantHandler
from items.item_handler import ItemHandler
from characters.equipment_handler import EquipmentHandler
from characters.inventory_handler import InventoryHandler


class Character(DefaultCharacter):

    @lazy_property
    def skill(self):
        return SkillHandler(self)

    @lazy_property
    def combat(self):
        return CombatHandler(self)

    @lazy_property
    def inv(self):
        return InventoryHandler(self)
        
    @lazy_property
    def equip(self):
        return EquipmentHandler(self)

    @lazy_property
    def item(self):
        return ItemHandler(self)

    def at_object_creation(self):
        # Stats
        self.attributes.add('hp', {'max_hp': 100, 'current_hp': 100})
        self.attributes.add('inventory_slots', {'max_slots': 0, 'occupied_slots': 0})
        self.attributes.add('coin', {'plat': 0, 'gold': 0, 'silver': 0, 'copper': 0})
        
        self.equip.generate_equipment()

        # Statuses
        self.attributes.add('approached', [])
        self.attributes.add('ko', False)
        self.attributes.add('feinted', None)
        self.attributes.add('busy', False)
        self.attributes.add('hands', {'main': None, 'off': None})
        self.attributes.add('hands_desc', {'main': 'right', 'off': 'left'})
        self.attributes.add('wielding', {'main': None, 'off': None, 'both': None})
        self.attributes.add('stance', None)
        self.attributes.add('standing', True)
        self.attributes.add('kneeling', False)
        self.attributes.add('sitting', False)
        self.attributes.add('lying', False)

    def announce_move_from(self, destination, msg=None, mapping=None, **kwargs):
        """
        Called if the move is to be announced. This is
        called while we are still standing in the old
        location.
        Args:
            destination (Object): The place we are going to.
            msg (str, optional): a replacement message.
            mapping (dict, optional): additional mapping objects.
            **kwargs (dict): Arbitrary, optional arguments for users
                overriding the call (unused by default).
        You can override this method and call its parent with a
        message to simply change the default message.  In the string,
        you can use the following as mappings (between braces):
            object: the object which is moving.
            exit: the exit from which the object is moving (if found).
            origin: the location of the object before the move.
            destination: the location of the object after moving.
        """
        if not self.location:
            return
        location = self.location
        origin = location or "nowhere"
        exits = [o for o in location.contents if o.location is location and o.destination is destination]
        var_exit = exits[0] if exits else "somewhere"

        # If the player is teleported or travels through a 1 way exit, give a generic announcement.
        if not hasattr(var_exit, 'destination'):
            location.msg_contents(f"{self.name} departs to {var_exit}.", exclude=(self, ))
            return
        
        # Determine which traversal string will be generated.
        if inherits_from(var_exit, "rooms.exits.Door"):
            self_str = f"You walk away through {var_exit.db.desc}, to the {var_exit.name}."
            others_str = f"{self.name} walks away through {var_exit.db.desc}, to the {var_exit.name}."
        elif inherits_from(var_exit, "rooms.exits.Stair"):
            if var_exit.name in ['up', 'down']:
                self_str = f"You depart, climbing {var_exit.name} {var_exit.db.desc}."
                others_str = f"{self.name} departs, climbing {var_exit.name} {var_exit.db.desc}."
            else:
                self_str = f"You depart, climbing {var_exit.name} to the {var_exit.db.desc}."
                others_str = f"{self.name} departs, climbing {var_exit.name} to the {var_exit.db.desc}."
        else:
            self_str = f"You walk away to {var_exit.destination.name}, to the {var_exit.name}."
            others_str = f"{self.name} walks away to {var_exit.destination.name}, to the {var_exit.name}."

        self.msg(self_str)
        location.msg_contents(others_str, exclude=(self, ))

    def announce_move_to(self, source_location, msg=None, mapping=None, **kwargs):
        """
        Called after the move if the move was not quiet. At this point
        we are standing in the new location.
        Args:
            source_location (Object): The place we came from
            msg (str, optional): the replacement message if location.
            mapping (dict, optional): additional mapping objects.
            **kwargs (dict): Arbitrary, optional arguments for users
                overriding the call (unused by default).
        Notes:
            You can override this method and call its parent with a
            message to simply change the default message.  In the string,
            you can use the following as mappings (between braces):
                object: the object which is moving.
                exit: the exit from which the object is moving (if found).
                origin: the location of the object before the move.
                destination: the location of the object after moving.
        """
        #TODO: Add contents of hands and wielding description for arriving characters.

        if not source_location and self.location.has_account:
            # This was created from nowhere and added to an account's
            # inventory; it's probably the result of a create command.
            string = f"You now have {self.get_display_name(self.location)} in your possession." 
            self.location.msg(string)
            return

        origin = source_location
        destination = self.location
        exits = []
        if origin:
            exits = [o for o in destination.contents if o.location is destination and o.destination is origin]
            origin_exit = exits[0] if exits else "somewhere"

        # If the player is teleported or travels through a 1 way exit, give a generic announcement.
        if not hasattr(origin_exit, 'destination'):
            if origin:
                destination.msg_contents(f"{self.name} arrives from {origin_exit}.", exclude=(self, ))
            return
        
        # Determine which traversal string will be generated.
        if origin:
            if inherits_from(origin_exit, "rooms.exits.Door"):
                others_str = f"{self.name} walks in through {origin_exit.db.desc}, from the {origin_exit.name}."
            elif inherits_from(origin_exit, "rooms.exits.Stair"):
                if origin_exit.name in ['up', 'down']:
                    others_str = f"{self.name} arrives, climbing {'down' if origin_exit.name == 'up' else 'up'} {origin_exit.db.desc}."
                else:
                    others_str = f"{self.name} arrives, climbing {origin_exit.db.desc} from the {origin_exit.name}."
            else:
                others_str = f"{self.name} walks in from {origin.name}, from the {origin_exit.name}."
        else:
            others_str = f"{self.name} arrives."

        destination.msg_contents(others_str, exclude=(self, ))
        
    def at_after_move(self, source_location):
        """
        This hook's default behavior is to look at the room after it moves to it.
        """
        # Force the character to be greeted with the room's short description.
        if not source_location:
            return
        self.msg(f"{self.location.short_desc(self)}")

    def return_appearance(self, looker, **kwargs):
        if not looker:
            return ""
        
        # get description, build string
        string  = self.create_desc()
        return string

    def create_desc(self):
        desc = ""
        
        figure = self.db.figure
        facial = self.db.facial
        hair = self.db.hair

        height = figure.get('height')
        build = figure.get('build')
        sex = figure.get('gender')

        eye_color = facial.get('eye_color')
        nose = facial.get('nose')
        lips = facial.get('lips')
        chin = facial.get('chin')
        face = facial.get('face')
        skin_color = facial.get('skin_color')

        length = hair.get('length')
        texture = hair.get('texture')
        hair_color = hair.get('hair_color')
        style = hair.get('style')

        # The figure should result in "You see a <height> <build> <gender>."
        gender = ('man' if sex == 'male' else 'woman')
        desc += f"You see a {height} {build} {gender}. "
        
        # The facial should result in "He has <color> eyes set above an <shape> nose, <shape> lips and a <shape> chin in a <shape> <color> face."
        gender = ('He' if sex == 'male' else 'She')
        desc += (f"{gender} has {eye_color} eyes set above a {nose} nose, "
                f"{lips} lips and a {chin} chin in a {face} {skin_color} face. ")

        # The hair should result in "<gender> has <length> <texture> <color> hair <style>."
        if length == 'bald':
            desc += f"{gender} is {length}. "
        else:
            desc += f"{gender} has {length} {texture} {hair_color} hair {style}. "
        return desc

class OOC_Character(Character):
    pass

class Player_Character(Character):
    def at_object_creation(self):
        super().at_object_creation()
        self.skill.generate_fresh_skillset(self, 'martial arts')

class NPC(Character):
    pass

class Merchant(NPC):
    @lazy_property
    def merch(self):
        return MerchantHandler(self)
    
    def at_object_creation(self):
        self.attributes.add('stock', [])
