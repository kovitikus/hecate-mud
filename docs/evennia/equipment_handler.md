### Table of Contents
* **[Initialization](https://github.com/kovitikus/hecate/wiki/EquipmentHandler#initialization)**
* **[Equipment Slot Generation](https://github.com/kovitikus/hecate/wiki/EquipmentHandler#equipment-slot-generation)**
* **[Unit Testing - Equipment Slots](https://github.com/kovitikus/hecate/wiki/EquipmentHandler#unit-testing---equipment-slots)**
* **[Inventory Container Prototype](https://github.com/kovitikus/hecate/wiki/EquipmentHandler#inventory-container-prototype)**

***

### Initialization
Create the new handler module. Navigate to the world directory and make a new file named `equipment_handler.py`.

Create the new `EquipmentHandler` class. This will be a Python only object, meaning that it doesn't exist on the Evennia database or within the Evennia object class. It will only exist on the server within the memory (RAM).

```py
class EquipmentHandler:

    def __init__(self, owner):
        self.owner = owner
```

This handler's first method will tell it to respond to the object that called upon it. 

The `owner` is assigned when this object is created and loaded into memory. `owner` is passed to this method via the calling object, as you will see in the `Character` class `@lazy_property` method. The `owner` is then assigned to `self.owner`, so that it can be stored and accessed across all methods of the handler object.

Make sure to save this new module.

***

The `EquipmentHandler` needs be added to the class that will call upon it. In this case, it will be added to the `Character` class. It is the parent class for all other character and mob types. This is accomplished by using `@lazy_property`, which must be imported.

```py
from evennia.utils.utils import lazy_property
```

Within the top of the character class, add the `EquipmentHandler`.

```py
class Character(DefaultCharacter):

    @lazy_property
    def equip(self):
        return EquipmentHandler(self)
```

This property will allow the `Character` object to easily access the methods of the `EquipmentHandler` object via `equip`.

```py
# Just an example.
self.equip.add(helmet) 
self.equip.remove(boots)
```

***

### Equipment Slot Generation
* **[Table of Contents](https://github.com/kovitikus/hecate/wiki/EquipmentHandler#table-of-contents)**

A listing of equipment slot types must be generated.

```
Head - Crown/Helmet/Hat
Neck - Necklace/Amulet
Shoulders - Shoulder Pads
Chest - Chest Armor
Arms - Sleeves
Hands - Pair of Gloves
Fingers - Rings (Maximum of 4 for balancing purposes.)
Waist - Belt/Sash
Thighs - Greaves
Calves - Greaves
Feet - Boots/Shoes/Sandals

Bag - Satchel/Backpack/Sack/Bag (Determines maximum inventory slots.)

Weapons
    - Any weapon can be manually wielded from the inventory or the ground via the `wield` command.
    - Equipped weapons are automatically wielded if no other weapon is manually wielded.
    - Shields and other offhands can also be equipped.
    - 2H weapons have a limit of 1 slot per type.
    - 1H weapons have a limit of 2 slots per type (Sword, Dagger, etc.) to compensate for dual-wielding.
    - Offhand weapons have a limit of 1 slot per type (Shield, Tome, etc.).
```

> **TIP:** It is highly recommended to write out raw data in an easy to reference location, such as in a text document on a second monitor. This will help with keeping track of the desired result while coding. It can also be pasted as comment blocks in areas of the code as a quick reference.

These slots must be added to a character's attributes. It will be most effective to utilize a dictionary for this task.

Create a new method within the `EquipmentHandler` and call it `generate_equipment_slots`. This method needs no additional arguments, but it must have `self` as a reference to the `EquipmentHandler` object itself.

For this method, the `create_object` method must be imported.

```py
from evennia.utils.create import create_object
```

```py
def generate_equipment_slots(self):
    owner = self.owner
    if not owner.attributes.has('equipment'):
        basic_bag = create_object(typeclass='typeclasses.objects.InventoryContainer', key='Basic Bag')
        equip_dic = {'head': None, 'neck': None, 'shoulder': None, 'chest': None, 'arms': None, 'hands': None,
                    'fingers': None, 'waist': None, 'thighs': None, 'calves': None, 'feet': None, 'bag': basic_bag}
        owner.attributes.add('equipment', equip_dic)
```

Non-critical dictionary values are initialized as `None`. The bag slot is a requirement; without it the character would not be able to hold items.

The bag object is created using a specific typeclass. This is for organizational purposes. Within the `typeclasses/objects.py` module lives the `Object` class. From this, a new `Container` class is made as a child of `Object` and subsequently `InventoryContainer` is made as a child of `Container`.

```py
# Within typeclasses/objects.py
class Object(DefaultObject):
    pass
class Container(Object):
    pass
class InventoryContainer(Container):
    pass
```

> **TIP:** `pass` is used when a class, method, or function is empty or incomplete. It prevents Python from generating errors. Using `pass` does not prevent the class, method, or function from existing within the project. Classes can still be inherited. Methods and functions can be called, but nothing will be executed.

It is helpful to have an identifying tag on objects. Add one within the `InventoryContainer` class via the `at_object_creation` method.

```py
class InventoryContainer(Container):
    def at_object_creation(self):
        self.tags.add('equipment_bag', category='container')
```

Add the `generate_equipment_slots` method to the `on_object_creation` method within the `Character` class.

```py
    def at_object_creation(self):
        self.equip.generate_equipment()
```

***

### Unit Testing - Equipment Slots
* **[Table of Contents](https://github.com/kovitikus/hecate/wiki/EquipmentHandler#table-of-contents)**

Unit testing ensures the logic of the project's code functions properly, without having to reload the server. It also prevents code rot, a situation in which the engine may change in the future and break the functionality of the game. Unit testing locates and identify potential issues efficiently. 

_[Click here for more information on Evennia's unit testing](https://github.com/evennia/evennia/wiki/Unit-Testing)._

Within the same directory as the `EquipmentHandler` create a new Python module named `tests.py`.

> **TIP:** Test modules can be named anything, so long as it begins with `test`. Additional words should be added after an underscore in order to retain readability, but Evennia will know it's a test either way. Hence why `tests` is located by Evennia, despite the added `s`.

Import EvenniaTest at the top of the module. This will function as the inherited class.

```py
from evennia.utils.test_resources import EvenniaTest
```

Unit testing may require additional materials in order to properly function; such as character objects and other such entities. For this, we will  utilize the `setUp` and `tearDown` methods.

Create a new class specific to the module that requires testing. Add to it the two methods and request that the parent methods also be executed by using `super()`.

```py
class TestEquipmentHandler(EvenniaTest):
    def setUp(self):
        super().setUp()
    
    def tearDown(self):
        super().tearDown()
```

> **TIP:** Evennia's built-in `setUp` and `tearDown` methods have generic objects. These are not always helpful, but it does not hurt to run them anyway. Check the `EvenniaTest` class for more information on what is provided by default. It is located in the same path as the import: `evennia > utils > test_resources`.


### Inventory Container Prototype
* **[Table of Contents](https://github.com/kovitikus/hecate/wiki/EquipmentHandler#table-of-contents)**

Setup the `inventory_container` spawner prototype and exchange the create_object call of the `generate_equipment_slots` method to spawn a bag instead.