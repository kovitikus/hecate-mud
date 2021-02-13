A handler is a Python object that you attach to other objects, granting access to methods located on the handler. A handler lives only in memory and therefore does not survive a server reload, neither does the information stored within. 

When your game is reloaded, all existing handler objects are destroyed. When the server starts up, all existing objects will no handlers on them. Handlers spawn for the first time when called upon within code via calling a handler's method. This handler will stay spawned on this object and will fulfill the object's quests, until any arbitrary event destroys it; in which case a new one will spawn the next it's needed.

References between the handler and object must be created to enable a handler and object to communicate with each other freely. 

#### Reference to the Handler
The object must recognize a handler and and store an instance in a variable. This variable is more like a shortcut, or bridge, that allows you to access methods from the handler.

You can achieve this with Evennia's built-in [`@lazy_property`](https://github.com/evennia/evennia/blob/master/evennia/utils/utils.py#L1732). 

> **TIP**: `@lazy_property` is a Python decorator. [Click here](https://realpython.com/primer-on-python-decorators/) to learn more about them.

It must be added just above the method you define. The method's name will then become the property you use when calling a method from the handler.

```python
from evennia import DefaultCharacter
from evennia.utils.utils import @lazy_property

from skills.combat_handler import CombatHandler

class Character(DefaultCharacter):
	@lazy_property
	def combat(self):
		# self is a reference to the character.
		# It is passed on to the handler.
		return CombatHandler(self) 
		
	def attack(self, target):
		# Use the combat property to access the attack method on the handler.
		self.combat.attack(target)
```

#### Reference to the Owner
