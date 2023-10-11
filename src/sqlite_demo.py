# sqlite_demo.py
# Create a database file called eventDB.db 
# Creates a table called events
# Created by DayFlow

import sqlite3
from event_manager import event

# creating database file called eventDB.db 
# (change to eventDB.db to :memory: to create a database in RAM for testing)
connection = sqlite3.connect("eventDB.db")    #creating connection object
cursor = connection.cursor()    #creating cursor object

with connection:    #creating table called events
    cursor.execute(
        """CREATE TABLE events (
            id integer, 
            name text, 
            start_date text,
            end_date text,
            start_time text,
            end_time text,
            description text,
            location text,
            repeat_every text,
            repeat_pattern text,
            repeat_count integer
            )""")
    
# insert event into table
def insert_event(event):
    with connection:
        cursor.execute("""INSERT INTO events VALUES (:id, :name, :start_date, :end_date, :start_time, :end_time, :description,
                        :location, :repeat_every, :repeat_pattern, :repeat_count)""", {'id': event.id, 'name': event.name,
                        'start_date': event.start_date, 'end_date': event.end_date, 'start_time': event.start_time,
                        'end_time': event.end_time, 'description': event.description, 'location': event.location,
                        'repeat_every': event.repeat_every, 'repeat_pattern': event.repeat_pattern,
                        'repeat_count': event.repeat_count})
    
# edit event in table
def edit_event(event):
    with connection:
        cursor.execute("""UPDATE events SET name=:name, start_date=:start_date, end_date=:end_date, start_time=:start_time,
                        end_time=:end_time, description=:description, location=:location, repeat_every=:repeat_every,
                        repeat_pattern=:repeat_pattern, repeat_count=:repeat_count WHERE id=:id""", {'id': event.id,
                        'name': event.name, 'start_date': event.start_date, 'end_date': event.end_date,
                        'start_time': event.start_time, 'end_time': event.end_time, 'description': event.description,
                        'location': event.location, 'repeat_every': event.repeat_every, 'repeat_pattern': event.repeat_pattern,
                        'repeat_count': event.repeat_count})
        
# remove event from table using id
def remove_event(id):
    with connection:
        cursor.execute("DELETE from events WHERE id=:id", {'id': id})

# search for event by name 
def get_event_by_name(name):
    cursor.execute("SELECT * FROM events WHERE name=:name", {'name': name})
    return cursor.fetchall()

# search for event by start date
def get_event_by_start_date(start_date):
    cursor.execute("SELECT * FROM events WHERE start_date=:start_date", {'start_date': start_date})
    return cursor.fetchall()


## TEST CODE ##

# update event in table
event1 = event(1, 'Sports Day', '2023-09-27', '2023-09-27', '09:00', '17:00', 'Sports Day', 'Sports Hall', 'Once', 'Once', 0)
event2 = event(2, 'Meeting', '2023-10-05', '2023-10-05', '09:00', '17:00', 'Meeting', 'Meeting Room', 'Wed', 'W', 10)
event3 = event(3, 'Open House', '2023-09-09', '2023-10-09', '09:00', '17:00', 'Open House', 'Hall', 'Once', 'Once', 0)

insert_event(event1)
insert_event(event2)
insert_event(event3)

# search for events with name containing "Sports Day"
events = get_event_by_name("Sports Day")
print(events)

# search for events with date containing "2023-10-05"
events = get_event_by_start_date("2023-10-05")
print(events)

# update event with id 1
event1.name = "Sports Day 2023"
edit_event(event1)

print("\n*********************************\n")
# search for all events
cursor.execute("SELECT * FROM events")
for row in cursor.fetchall():
    print(row)







