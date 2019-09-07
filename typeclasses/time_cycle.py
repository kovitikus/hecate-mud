import datetime

from typeclasses.scripts import Script
from typeclasses.rooms import Room

class TimeCycle(Script):
    def at_script_creation(self):
        self.key = 'time_cycle'
        self.desc = "Tracks global timed events."
        self.interval = 1
        self.persistent = True

    def at_repeat(self):
        now = datetime.datetime.now()
        cur_hour = now.hour
        cur_min = now.minute
        cur_sec = now.second
        if cur_sec != 0:
            return
        if cur_min not in [0, 20, 40]:
            return

        # Daytime begins.
        if cur_hour in [2, 6, 10, 14, 18, 22]:
            if cur_min == 0:
                # Phase 1
                string = "The sun rises above the eastern horizon."
            elif cur_min == 20:
                # Phase 2
                string = "It's now mid-morning."
            elif cur_min == 40:
                # Phase 3
                string = "It's now early-noon."
        elif cur_hour in [3, 7, 11, 15, 19, 23]:
            if cur_min == 0:
                # Phase 4
                string = "It's now high-noon."
            elif cur_min == 20:
                # Phase 5
                string = "It's now mid-afternoon."
            elif cur_min == 40:
                # Phase 6
                string = "It's now dusk."
        # Nighttime begins.
        elif cur_hour in [0, 4, 8, 12, 16, 20]:
            if cur_min == 0:
                # Phase 1
                string = "The sun has set and the moon begins to glow."
            elif cur_min == 20:
                # Phase 2
                string = "It's now early-evening."
            elif cur_min == 40:
                # Phase 3
                string = "It's now late-evening."
        elif cur_hour in [1, 5, 9, 13, 17, 21]:
            if cur_min == 0:
                # Phase 4
                string = "It's now midnight."
            elif cur_min == 20:
                # Phase 5
                string = "It's now early-morning."
            elif cur_min == 40:
                # Phase 6
                string = "The break of dawn approaches."
        # Send out the string to all rooms.
        for room in Room.objects.all():
            room.msg_contents(string)