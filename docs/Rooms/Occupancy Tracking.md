Rooms are grouped together by zone tag.

Each time a human moves a character into a room, the room checks to see if its zone tag is already on the occupied list. 

If not, then a tag is to the room added as 
``('zonename', category='occupied')``

```python
def at_object_receive(self, new_arrival, source_location)
    self.room.set_room_occupied() #Ask the room handler

def at_object_leave(self. moved_obj, target_location)
    self.room.set_room_vacant()
```

Inside of the room handler, there are two methods that go through the motions of managing the occupancy.

In setting the room to occupied, the first thing we want to do is check to see if the room and zone are already marked as occupied.
```python
def set_room_occupied(self):
    owner = self.owner
    zone_controller = get_zone_controller()
    occupied_zones_list = zone_controller.attributes.get('occupied_zones')
    
    if owner has tag with the category of occupied:
        return
    
    if owner.db.zone in occupied_zones_list:
        return
    else:
        occupied_zones_list.append('owner.db.zone')
    
```

```python
def get_zone_controller():
    zone_controller_obj = list(search_tag(category='zone_controller'))[0]
    return zone_controller_obj
```


```python
def get_occupants():
    occupants = []
    temp_contents = []
    occupied_rooms = list(search_tag(category='occupied'))
    
	for room in occupied_rooms:
	    temp_contents = room.contents
		for obj in temp_contents:
		    if obj.has_account:
                occupants.append(obj)
    return occupants
```