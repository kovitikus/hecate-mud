"""
Characters

Characters are (by default) Objects setup to be puppeted by Accounts.
They are what you "see" in game. The Character class in this module
is setup to be the "default" character type created by the default
creation commands.

"""
from evennia import DefaultCharacter


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
    def at_object_creation(self):
        # Figure Attributes
        self.db.figure = {}
        self.db.figure['height'] = 'short'
        self.db.figure['build'] = 'burly'
        self.db.figure['gender'] = 'male'

        # Facial Attributes
        self.db.facial = {}
        self.db.facial['eye_color'] = 'blue'
        self.db.facial['nose'] = 'thin'
        self.db.facial['lips'] = 'thin'
        self.db.facial['chin'] = 'pointed'
        self.db.facial['face_shape'] = 'narrow'
        self.db.facial['face_color'] = 'ivory'

        # Hair Attributes
        self.db.hair = {}
        self.db.hair['length'] = 'long'
        self.db.hair['texture'] = 'bouncy'
        self.db.hair['color'] = 'tawny'
        self.db.hair['style'] = 'in a pony-tail'

    def create_figure(self):
        # The figure should result in "You see a short burly man."
        figure = self.db.figure
        full_figure = f"You see a {figure['height']} {figure['build']} {figure['gender']}."
        return full_figure

    def create_facial(self):
        # The facial should result in "He has <color> eyes set above an <shape> nose, <shape> lips and a <shape> chin in a <shape> <color> face."
        facial = self.db.facial
        gender = self.db.figure.get('gender')
        gender = ("He" if gender == 'male' else "She")
        full_facial = f"{gender} has {facial.get('eye_color')} eyes set above a {facial.get('nose')} nose, {facial.get('lips')} lips and a {facial.get('chin')} chin in a {facial.get('face_shape')} {facial.get('face_color')} face."
        return full_facial

    def create_hair(self):
        # The hair should result in "<gender> has <length> <texture> <color> hair <style>."
        hair = self.db.hair
        gender = self.db.figure.get('gender')
        gender = ("He" if gender == 'male' else "She")
        full_hair = f"{gender} has {hair.get('length')} {hair.get('texture')} {hair.get('color')} hair {hair.get('style')}."
        return full_hair