from evennia import create_object

def main(self, raw_string, **kwargs):
    text = 'Please create your character.'
    options = (
        {"key": ("1", "name"),
        "desc": "Name your character.",
        "goto": "enter_name"},
        {"key": ("f", "finish", "create"),
        "desc": "Finish and create.",
        "goto": _create_char}
    )
    return text, options

def enter_name(self, raw_string, **kwargs):
    # Check for a previous name.
    prev_entry = kwargs.get("prev_entry")

    if prev_entry:
        text = f"Current Name: {prev_entry}.\nEnter another name or press RETURN to accept."
    else:
        text = "Enter your character's name or press RETURN to abort."
    
    options = {"key": "_default",
                "goto": (_set_name, {"prev_entry": prev_entry})}
    return text, options

def _set_name(self, raw_string, **kwargs):
    inp = raw_string.strip()

    prev_entry = kwargs.get("prev_entry")

    if not inp:
        # A blank input either means OK or Abort
        if prev_entry:
            self.ndb._menutree.name = prev_entry
            self.msg(f"Your character's name has been set to |c{prev_entry}|n.")
            return "main"
        else:
            self.msg("Aborted.")
            return "main"
    else:
        #Re-run old node, but pass in the name given.
        return None, {"prev_entry": inp}

def _create_char(self, raw_string, **kwargs):
    name = self.ndb._menutree.name

    # Check for chars attribute and initilize if none.
    if not self.attributes.get("chars"):
        self.db.chars = {}
    chars_len = len(self.db.chars) + 1
    self.msg("You currently have a total of {chars_len} characters.")

    #Add the new character object to the chars attribute as next number in the character list.
    self.db.chars[f'{chars_len}'] = create_object(typeclass="typeclasses.characters.Player_Character", key=name, home=None)
    self.msg("|gChargen completed!|n")
    return "exit"

def exit(self, raw_string, **kwargs):
    options = None
