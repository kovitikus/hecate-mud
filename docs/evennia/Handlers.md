#### Introduction
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
Within your handler module, create a new Python class. This class will not inherit another.

```python
class CombatHandler:
	def __init__(self, owner):
		self.owner = owner
```

The `owner` value was passed into this method during the call to the CombatHandler in the character typeclass. It refers to the object that spawned this instance of the handler.

The initialization method is used to gather relevant data about the character. It significantly reduces your calls to read the database by referencing data cached in memory while this instance of the handler remains alive.

#### Managing Data
```python
class CombatHandler:
	def __init__(self, owner):
		self.owner = owner
		
		self.set_hp()
		self.set_level
		self.set_strength
		
	def set_hp(self):
		self.hp = owner.db.hp
	def set_level(self):
		self.level = owner.db.level
	def set_strength(self):
		self.strength = owner.db.strength
		
	def take_damage(self, damage):
		current_hp = self.hp
		remaining_hp = current_hp - damage
		
		self.hp = remaining_hp
		owner.db.hp = remaining_hp
```

A handler should pre-load data that it uses frequently. The best way to manage your data is to only gather it once from the database when the handler comes to life. Data is saved to class properties. Within the handler class, self is a reference to the instantiated object it is executed on. This means that `self.hp = owner.db.hp` is saved to the instance of the handler that lives on rat#28938872. From anywhere else within the combat handler, you can call upon the owner's (rat's) health points by using `self.hp` rather than `owner.db.hp`.

There's a catch though. You now have to "save" your information twice instead of once. You'll still do your normal database save; such as `owner.db.hp = 10`, but you'll also need to add `self.hp = 10` as well.

Essentially we've traded adding an extra line of code that gets info from the database to an extra line of code that saves to the handler. So long as you always adjust the handler's version of the variable alongside the database change, your handler data should always be equal to the database. 

> **TIP:** [Unit testing](https://www.evennia.com/docs/latest/Unit-Testing.html) would be a good candidate for checking that your data matches your expectations.

#### Conclusion
That's all you really need to know about handlers. They are very simple mechanisms that allow you to dynamically add functionality to objects. It's useful to keep all of your logic compartmentalized within handlers, so that you have a central location for changing the behaviors. 

Handlers can be used for just about anything. They offer a bit more basic functionality over simply dumping loose functions into a module.