"""
search_engine.py

Search engine for seeking for the specific event
including these function
-event_search           - search by similarity
-event_range_search     - search by the range to display event

Created by Mhon, 10th October 2023
Last update Mhon 5th November 2023
"""

import sqlite3
import sys
import os
import Database.sqlite_demo as sqlite

destination_path = sqlite.find_db_path()
connection = sqlite3.connect(destination_path)
cursor = connection.cursor()

search_types = ["name", "start_date", "end_date", "start_time", "end_time"]

def event_search(pattern, type="name", maximum_items = 5):
    with connection:
        cursor.execute("SELECT * FROM events WHERE {} LIKE ?;".format(type), ('%{}%'.format(pattern),))
        selected_events = cursor.fetchall()
        items_count = len(selected_events)
        if items_count < maximum_items:
            maximum_items = items_count
        selected_events = selected_events[0:maximum_items]
        return selected_events

def event_range_search(start_date, end_date):
    with connection:
        cursor.execute("""SELECT * FROM events
                          WHERE end_date >= ? AND start_date <= ?;""",
                       (start_date, end_date))
        selected_events = cursor.fetchall()
        return selected_events

def event_search_recurring(id, order_by="start_date"):
    with connection:
        cursor.execute("""SELECT * FROM events
                          WHERE id = ? ORDER BY ? ASC;""",
                          (id, order_by))
        selected_events = cursor.fetchall()
        return selected_events