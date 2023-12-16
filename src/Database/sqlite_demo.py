"""
sqlite_demo.py
Create a database file called eventDB.db 
Creates a table called events

Created by King, 1st October 2023
"""

import sqlite3  
from Shared_Files.Classes.all_classes import eventClass
import sys
import os
import shutil

"""
creating database file called eventDB.db 
(change to eventDB.db to :memory: to create a database in RAM for testing)
Creating a connection object to the specified database file
"""
def find_db_path():
    db_name = "eventDB.db"
    destination_path = ""
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        db_path = os.path.join(sys._MEIPASS, db_name)
        destination_path = os.path.join(os.path.dirname(sys.executable), db_name)
        if not os.path.exists(destination_path):
            shutil.copy2(db_path, destination_path)
            print("Copied," + db_name, "to", destination_path)
        else:
            print(f"Database file not found at {db_path}")
        
        return destination_path
    else:
        print("Not frozen")
        destination_path = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), db_name)
        print("destinationpath is: ", destination_path)

        return destination_path

# Creating a connection object to the specified database file
destination_path = find_db_path()
connection = sqlite3.connect(destination_path)
cursor = connection.cursor()

"""
creating table called events
"""
def build_table():
    with connection:    #creating table called events
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS events (
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
 
    
""" 
repeat_every can be "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"
repeat_pattern can be "D", "W", "M", "Y" (daily, weekly, monthly, yearly)
repeat_count is the number of times the event repeats (0 for infinite)"""

""" 
insert event into table
arguments:
    event - an eventClass object
"""
def insert_event(event):
    with connection:
        cursor.execute("""INSERT INTO events VALUES (:id, :name, :start_date, :end_date, :start_time, 
                        :end_time, :description,
                        :location, :repeat_every, 
                        :repeat_pattern, :repeat_count)""", 
                        {'id': event.id, 'name': event.name,
                        'start_date': event.start_date, 'end_date': event.end_date, 
                        'start_time': event.start_time, 'end_time': event.end_time, 
                        'description': event.description, 'location': event.location,
                        'repeat_every': event.repeat_every, 'repeat_pattern': event.repeat_pattern,
                        'repeat_count': event.repeat_count})
    
""" 
edit event in table
arguments:
    event - an eventClass object
"""
def edit_event(event):
    with connection:
        cursor.execute("""UPDATE events SET name=:name, start_date=:start_date, 
                        end_date=:end_date, start_time=:start_time,
                        end_time=:end_time, description=:description, 
                        location=:location, repeat_every=:repeat_every,
                        repeat_pattern=:repeat_pattern, repeat_count=:repeat_count 
                        WHERE id=:id""", 
                        {'id': event.id,
                        'name': event.name, 'start_date': event.start_date, 
                        'end_date': event.end_date, 'start_time': event.start_time, 
                        'end_time': event.end_time, 'description': event.description,
                        'location': event.location, 'repeat_every': event.repeat_every, 
                        'repeat_pattern': event.repeat_pattern, 'repeat_count': event.repeat_count})
        
""" 
remove event from table using id
arguments:
    id  - an integer
"""
def remove_event(id):
    with connection:
        cursor.execute("DELETE from events WHERE id = ?", (id,))
    
""" 
TEST CODE 
creating 3 events and inserting them into the table
then updating the first event
"""
def test_code():
    # update event in table
    event1 = eventClass(1, 'Sports Day', '2023-09-27', '2023-09-27', 
                        '09:00', '17:00', 'Sports Day', 'Sports Hall', 'Once', 'Once', 0)
    event2 = eventClass(2, 'Meeting', '2023-10-05', '2023-10-05', 
                        '09:00', '17:00', 'Meeting', 'Meeting Room', 'Wed', 'W', 10)
    event3 = eventClass(3, 'Open House', '2023-09-09', '2023-10-09', 
                        '09:00', '17:00', 'Open House', 'Hall', 'Once', 'Once', 0)

    insert_event(event1)
    insert_event(event2)
    insert_event(event3)

    # update event with id 1
    event1.name = "Sports Day 2023"
    edit_event(event1)

def close_all():
    cursor.close()
    connection.commit()
    connection.close()

# select all events from and print in rows
def select_all():
    cursor.execute("SELECT * FROM events")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

# select all events from and print in rows
select_all()
 








