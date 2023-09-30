import sqlite3

connection = sqlite3.connect("eventDB.db")  #creating database file called eventDB.db
#connection = sqlite3.connect(":memory:")   #creating database in memory (so no need to delete eventDB.db file every time)

cursor = connection.cursor()    #creating cursor object

with connection:    #creating table called events
    cursor.execute(
        """CREATE TABLE events (
            event_id integer, 
            event_name text, 
            event_date text, 
            event_description text, 
            event_location text
            )""")

# insert some data into the table
event_list = [
    (1, "Sports Day", "2023-09-27", "Annual sports event", "Sports Stadium"),
    (2, "Meeting", "2023-10-05", "Team meeting", "Office Room A"),
    (3, "Conference", "2023-11-15jj", "Tech conference", "Convention Center"),
    (4, "Party", "2023-12-31", "New Year's Eve Party", "Downtown Hotel")
]

# insert the event_list into the table
with connection:
    cursor.executemany("INSERT INTO events values (?, ?, ?, ?, ?)", event_list)

#  print the event table
for row in cursor.execute("select * from events"):
    print(row)

# search for events with name containing "Sports Day"
cursor.execute("select * from events where event_name like '%Sports Day%'")
print(cursor.fetchall())



