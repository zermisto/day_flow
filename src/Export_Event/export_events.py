"""
export_events.py

Export events within a date range to a CSV file
Ask the user for a start date, end date, and CSV file name

Created by Toiek, 4th October 2023
"""

import sqlite3
import csv
from Shared_Files.user_input_validation import check_event_timeframe
import os
import sys

destination_path = os.path.join(os.path.dirname(sys.executable), "eventDB.db")
connection = sqlite3.connect(destination_path)
cursor = connection.cursor()

""" Export events within a date range to a CSV file"""
def export_events_to_csv(export_event_data):

    # create a Exported_Files directory if it doesn't exist
    if not os.path.exists("Exported_Files"):
        os.mkdir("Exported_Files")
        
    #export the file to dir Exported_Files
    filename = "Exported_Files/" + export_event_data.filename + ".csv"
    start_date = export_event_data.start_date
    end_date = export_event_data.end_date

    with connection:
        cursor.execute("SELECT * FROM events WHERE start_date BETWEEN ? AND ?", 
                       (start_date, end_date))
        selected_events = cursor.fetchall()

    if (check_event_timeframe(selected_events) == False):
        return
    try:
        with open(filename, mode='w', newline='') as csv_file: 
            fieldnames = ['ID', 'Name', 'Start Date', 'End Date', 'Start Time', 'End Time', 
                        'Description', 'Location', 'Repeat Every', 'Repeat Pattern', 'Repeat Count']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)   
            writer.writeheader()
            for event in selected_events:
                writer.writerow({
                    'ID': event[0],
                    'Name': event[1],
                    'Start Date': event[2],
                    'End Date': event[3],
                    'Start Time': event[4],
                    'End Time': event[5],
                    'Description': event[6],
                    'Location': event[7],
                    'Repeat Every': event[8],
                    'Repeat Pattern': event[9],
                    'Repeat Count': event[10]
                })
    except Exception as e:
        print("Error: " + e)
    print(f"Selected events have been exported to '{filename}'.")


