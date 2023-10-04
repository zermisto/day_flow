import  sqlite3

connection = sqlite3.connect("eventDB.db")
cursor = connection.cursor()

def name_search(cursor, pattern, maximum_items = 10):
    cursor.execute("SELECT * FROM events WHERE name LIKE ?;", (pattern,))
    selected_events = cursor.fetchall()
    items_count = len(selected_events)
    if items_count < maximum_items:
        maximum_items = items_count
    selected_events = selected_events[0:maximum_items]
    return selected_events

def date_search(cursor, pattern, maximum_items = 10):
    cursor.execute("SELECT * FROM events WHERE start_date LIKE ? OR end_date LIKE ?;", (pattern, pattern))
    selected_events = cursor.fetchall()
    items_count = len(selected_events)
    if items_count < maximum_items:
        maximum_items = items_count
    selected_events = selected_events[0:maximum_items]
    return selected_events

#print(anme_search(cursor, '%%', 3))
#print(date_search(cursor, '%%', 3))