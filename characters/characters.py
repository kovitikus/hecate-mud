from django.utils.functional import lazy
from evennia import DefaultCharacter
from evennia.utils.utils import (lazy_property)

from skills.combat_handler import CombatHandler
from skills.skill_handler import SkillHandler
from items.item_handler import ItemHandler
from characters.character_handler import CharacterHandler
from characters.equipment_handler import EquipmentHandler
from characters.inventory_handler import InventoryHandler
from characters.currency_handler import CurrencyHandler
from characters.status_handler import StatusHandler
from travel.travel_handler import TravelHandler
from rooms.instance_handler import InstanceHandler
from sentients.sentient_handler import SentientHandler
from sentients.merchant_handler import MerchantHandler


class Character(DefaultCharacter):
    @lazy_property
    def instance(self):
        return InstanceHandler(self)
    @lazy_property
    def status(self):
        return StatusHandler(self)
    @lazy_property
    def travel(self):
        return TravelHandler(self)
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
    def char(self):
        return CharacterHandler(self)
    @lazy_property
    def item(self):
        return ItemHandler(self)
    @lazy_property
    def currency(self):
        return CurrencyHandler(self)
    @lazy_property
    def merch(self):
        return MerchantHandler(self)
    @lazy_property
    def sentient(self):
        return SentientHandler(self)

    def at_object_creation(self):
        # Command Sets
        self.cmdset.add("travel.travel_cmdset.TravelCmdSet", permanent=True)

        # Stats
        self.char.init_char_stats()
        self.attributes.add('inventory_slots', {'max_slots': 0, 'occupied_slots': 0})
        self.attributes.add('coin', {'plat': 0, 'gold': 0, 'silver': 0, 'copper': 0})
        self.equip.initialize_equipment_attribute()

        # Avoids execution of this code on initial setup of superuser.
        # Prototype spawner attempts to set objects' home specifically
        # to DEFAULT_HOME, which is Limbo.
        # In the initial_setup module, Limbo isn't created until after
        # the superuser. https://gist.github.com/kovitikus/9b358ea0ebc09ec1e3840f332e93c00d
        if not self.dbref == '#1':
            self.equip.generate_starting_equipment()

        # Follow and lead behaviors for traversing an exit as a group.
        self.cmdset.add('travel.travel_cmdset.TravelCmdSet')
        self.attributes.add('leader', None)
        self.attributes.add('followers', [])

        # Statuses
        self.attributes.add('approached', [])
        self.attributes.add('ko', False)
        self.attributes.add('feinted', None)
        self.attributes.add('busy', False)
        self.attributes.add('hands', {'main': None, 'off': None})
        self.attributes.add('hands_desc', {'main': 'right', 'off': 'left'})
        self.attributes.add('wielding', {'main': None, 'off': None, 
                            'both': None})
        self.attributes.add('stance', None)
        self.attributes.add('standing', True)
        self.attributes.add('kneeling', False)
        self.attributes.add('sitting', False)
        self.attributes.add('lying', False)
        self.attributes.add('afk_timer', 600) # 10 minute timeout

        # Skills
        self.skill.generate_fresh_skillset('martial arts')

    def announce_move_from(self, destination, msg=None, mapping=None, 
                            **kwargs):
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

        # Tells the handler to find an exit and store that exit on 
        # itself as self.exit_obj
        self.travel.find_exit_by_destination(destination)
        if self.travel.travel_one_way(destination): # If the player is teleported.
            return
        self.travel.pick_departure_string()
        self.travel.send_departure_string()

    def announce_move_to(self, source_location, msg=None, mapping=None, 
                        **kwargs):
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
        #TODO: Add contents of hands and wielding description for 
        #                                           arriving characters.

        if not source_location and self.location.has_account:
            # This was created from nowhere and added to an account's
            # inventory; it's probably the result of a create command.
            string = (f"You now have {self.get_display_name(self.location)} " 
                        f"in your possession.")
            self.location.msg(string)
            return

        origin = source_location
        location = self.location

        if origin:
            self.travel.find_origin_exit(origin, location)
            
        # If the player is teleported or travels through a 1 way exit, 
        # give a generic announcement.
        if self.travel.origin_exit_missing_destination(origin, location):
            return

        # Determine which traversal string will be generated.
        self.travel.pick_arrival_string(origin)
        self.travel.send_arrival_string()
        
    def at_after_move(self, source_location):
        """
        Once the self object has settled in at it's new location, 
        this hook is called.

        This hook's default behavior is to look at the room, returning 
        the desc attribute on the room to the self object.
        ---
        I've instead changed it to call an attribute on the room that
        holds a short description.
        This is a custom system that returns an abbrevieted glance at
        the room and the most critical information.

        Example:
            You arrive at <destination name>. <Person/Sentient> <is/are> here.
            You see <exit name> to the <exit direction>, an <exit name>
            to the <exit direction>, and <exit name> to the <exit direction>.
        """
        # Force the character to be greeted with the room's short description.
        if not source_location:
            return
        self.msg(f"{self.travel.location_summary()}")

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
