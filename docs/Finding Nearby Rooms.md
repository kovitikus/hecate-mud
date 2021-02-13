#### Source Code
```python
from evennia.utils.utils import inherits_from

def get_nearby_rooms(location):
    room_list = []
    location_contents = location.contents
    
    for obj in location_contents:
        if inherits_from(obj, Exit):
            if obj.destination:
                room_list.append(exit.destination)
    return room_list
```

#### Explaination
Check all items in the target location, looking for exits using [`inherits_from`](https://github.com/evennia/evennia/blob/master/evennia/utils/utils.py#L941)

```python
# Lists are declared before the for loop to maintain scope between loops.
exit_list = [] 
location_contents = location.contents`

for obj in location_contents:
    if inherits_from(object, Exit):
        exit_list.append(location)
```

The list of exits are references of the object. This allows access to the information stored on that object, including the `destination` property.

`exit_object.destination`
> **[Source](https://www.evennia.com/docs/latest/Objects.html#properties-and-functions-on-objects):** Destination is a custom property that is available to all objects, but is generally only used by exit objects.

It's time to iterate again, this time over the exit objects.

```python
room_list = []

for exit in exit_list:
    if exit.destination:
        room_list.append(exit.destination)
```

It's important to understand that the destination property holds a reference to the object. This means that you are also able to directly access the object's properties with that refereance.