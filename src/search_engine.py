# search_engine.py
# Search engine for seeking for the specific event
# Created by Roong, 10th October 2023

import  sqlite3

connection = sqlite3.connect("eventDB.db")
cursor = connection.cursor()

def name_search(cursor, pattern, maximum_items = 10):
    with connection:
        cursor.execute("SELECT * FROM events WHERE name LIKE ?;", (pattern,))
        selected_events = cursor.fetchall()
        items_count = len(selected_events)
        if items_count < maximum_items:
            maximum_items = items_count
        selected_events = selected_events[0:maximum_items]
        return selected_events

def date_search(cursor, pattern, maximum_items = 10):
    with connection:
        cursor.execute("SELECT * FROM events WHERE start_date LIKE ? OR end_date LIKE ?;", (pattern, pattern))
        selected_events = cursor.fetchall()
        items_count = len(selected_events)
        if items_count < maximum_items:
            maximum_items = items_count
        selected_events = selected_events[0:maximum_items]
        return selected_events

# Put the name or letter in between the % signs to search for the event
# and the number is the max number of items to return
print(name_search(cursor, '%s%', 3))

# You can put the start_date or end_date in the format YYYY-MM-DD to search for the event
print(date_search(cursor, '%%', 3))