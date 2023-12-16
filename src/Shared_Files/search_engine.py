"""
search_engine.py

Search engine for seeking for the specific event
including these function
-event_search           - search by similarity
-event_range_search     - search by the range to display event

Created by Mhon, 10th October 2023
"""

import sqlite3
import sys
import os
import Database.sqlite_demo as sqlite_func

destination_path = sqlite_func.find_db_path()
connection = sqlite3.connect(destination_path)
cursor = connection.cursor()
search_types = ["name", "start_date", "end_date", "start_time", "end_time"]

""" Search for the event by the pattern
    arguments:
        type        - The pattern can be the name, start_date, end_date, start_time, end_time
        pattern     - Pattern to search
        maximumitem - The maximum_items is the maximum number of
                    the items that will be returned 
    return:
        selected_events     - list of all desired events
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
        start_date  - The start_date is the start date of the range
        end_date    - The end_date is the end date of the range
    return:
        selected_events     - list of all desired events
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
        id          - The id is the id of the event
        order_by    - The order_by is the order of the event
                    The default value of order_by is start_date
    return:
        selected_events     - list of all desired events
"""
def event_search_recurring(id, order_by="start_date"):
    with connection:
        cursor.execute("""SELECT * FROM events
                          WHERE id = ? ORDER BY ? ASC;""",
                          (id, order_by))
        selected_events = cursor.fetchall()
        return selected_events