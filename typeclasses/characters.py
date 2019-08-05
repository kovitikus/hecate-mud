"""
Characters

Characters are (by default) Objects setup to be puppeted by Accounts.
They are what you "see" in game. The Character class in this module
is setup to be the "default" character type created by the default
creation commands.

"""
from evennia import DefaultCharacter
from collections import defaultdict
from evennia.utils.utils import (list_to_string, inherits_from, lazy_property)


class Character(DefaultCharacter):
    """
    The Character defaults to reimplementing some of base Object's hook methods with the
    following functionality:

    at_basetype_setup - always assigns the DefaultCmdSet to this object type
                    (important!)sets locks so character cannot be picked up
                    and its commands only be called by itself, not anyone else.
                    (to change things, use at_object_creation() instead).
    at_after_move(source_location) - Launches the "look" command after every move.
    at_post_unpuppet(account) -  when Account disconnects from the Character, we
                    store the current location in the pre_logout_location Attribute and
                    move it to a None-location so the "unpuppeted" character
                    object does not need to stay on grid. Echoes "Account has disconnected"
                    to the room.
    at_pre_puppet - Just before Account re-connects, retrieves the character's
                    pre_logout_location Attribute and move it back on the grid.
    at_post_puppet - Echoes "AccountName has entered the game" to the room.

    """
    pass

class Player_Character(DefaultCharacter):
    # @lazy_property
    # def combat(self):
    #     return CombatHandler(self)

    # def at_object_creation(self):
    #     self.scripts.add(ScrptCombat, autostart=True)
    #     self.db.combat_script = ScrptCombat
    #     pass

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