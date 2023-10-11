# event_class.py
# Class for event objects
# Created by DayFlow

class event:

    def __init__(self, id, name, start_date, end_date, start_time, end_time, description, location, repeat_every, repeat_pattern, repeat_count):
        self.id = id    
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.start_time = start_time
        self.end_time = end_time
        self.description = description
        self.location = location
        self.repeat_every = repeat_every        # ('Once', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun')
        self.repeat_pattern = repeat_pattern    # ('Once', 'D', 'W', 'M', 'Y')
        self.repeat_count = repeat_count        # (negative for infinite, 
                                                # positive for finite, 
                                                # 0 for no repeat)

    