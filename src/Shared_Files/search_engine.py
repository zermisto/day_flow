"""
search_engine.py

Search engine for seeking for the specific event
including these function
-event_search           - search by similarity
-event_range_search     - search by the range to display event

Created by Mhon, 10th October 2023
"""

import  sqlite3

connection = sqlite3.connect("Database/eventDB.db")
cursor = connection.cursor()
search_types = ["name", "start_date", "end_date", "start_time", "end_time"]

""" Search for the event by the pattern
    arguments:
    The pattern can be the name, start date, end date, start time, end time
    The type is the type of the pattern
    The maximum_items is the maximum number of the items that will be returned
    The default value of maximum_items is 5
"""
def event_search(pattern, type="name", maximum_items = 5):
    with connection:
        cursor.execute("SELECT * FROM events WHERE {} LIKE ?;".format(type), 
                       ('%{}%'.format(pattern),))
        selected_events = cursor.fetchall()
        items_count = len(selected_events)
        if items_count < maximum_items:
            maximum_items = items_count
        selected_events = selected_events[0:maximum_items]
        return selected_events
    
""" Search for the event by the range of the date
    arguments:
    The start_date is the start date of the range
    The end_date is the end date of the range
"""
def event_range_search(start_date, end_date):
    with connection:
        cursor.execute("""SELECT * FROM events
                          WHERE end_date >= ? AND start_date <= ?;""",
                       (start_date, end_date))
        selected_events = cursor.fetchall()
        return selected_events

""" Search for the recurring event by the id
    arguments:
    The id is the id of the event
    The order_by is the order of the event
    The default value of order_by is start_date
"""
def event_search_recurring(id, order_by="start_date"):
    with connection:
        cursor.execute("""SELECT * FROM events
                          WHERE id = ? ORDER BY ? ASC;""",
                          (id, order_by))
        selected_events = cursor.fetchall()
        return selected_events