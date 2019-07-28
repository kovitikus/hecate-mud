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
        self.db.height_desc = 'short'
        self.db.build_desc = 'burly'
        self.db.gender = 'male'

        # Facial Attributes
        self.db.eye_color = 'blue'
        self.db.nose_shape = 'thin'
        self.db.lip_shape = 'thin'
        self.db.chin_shape = 'pointed'
        self.db.face_shape = 'narrow'
        self.db.face_color = 'ivory'

    def create_figure(self):
        # The figure should result in "You see a short burly man."
        figure = []
        figure.append(self.attributes.get("height_desc"))
        figure.append(self.attributes.get("build_desc"))
        figure.append(self.attributes.get("gender"))
        full_figure = f"You see a {figure[0]} {figure[1]} {figure[2]}."
        return full_figure

    def create_facial(self):
        # The facial should result in "He has <color> eyes set above an <shape> nose, <shape> lips and a <shape> chin in a <shape> <color> face."
        facial = []
        facial.append("He" if self.attributes.get("gender") == 'male' else "She")
        facial.append(self.attributes.get("eye_color"))
        facial.append(self.attributes.get("nose_shape"))
        facial.append(self.attributes.get("lip_shape"))
        facial.append(self.attributes.get("chin_shape"))
        facial.append(self.attributes.get("face_shape"))
        facial.append(self.attributes.get("face_color"))
        full_facial = f"{facial[0]} has {facial[1]} eyes set above a {facial[2]} nose, {facial[3]} lips and a {facial[4]} chin in a {facial[5]} {facial[6]} face."
        return full_facial