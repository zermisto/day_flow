# export_events.py 
# Export events within a date range to a CSV file
# Ask the user for a start date, end date, and CSV file name
# Created by Toiek, 4th October 2023

import sqlite3
import csv
import export_event_class as exportEventClass

connection = sqlite3.connect("eventDB.db")    #creating connection object

cursor = connection.cursor()    #creating cursor object

# Export events within a date range to a CSV file
def export_events_to_csv(export_event_data):
    
    # start_date = input("Enter the start date (YYYY-MM-DD): ")
    # end_date = input("Enter the end date (YYYY-MM-DD): ")
    # filename = input("Enter the CSV file name (make sure to add .csv at the end): ")
    # use the event_class.py to get the start_date, end_date and filename from export_event_data

    #attach csv to file name nas well so if user put 'test' it will be test.csv
    filename = export_event_data.filename + ".csv"
    start_date = export_event_data.start_date
    end_date = export_event_data.end_date

    print("filename: ", filename)
    print("start_date: ", start_date)
    print("end_date: ", end_date)
    

    with connection:
        cursor.execute("SELECT * FROM events WHERE start_date BETWEEN ? AND ?", (start_date, end_date))
        selected_events = cursor.fetchall()

    if not selected_events: # if selected_events is empty
        print("No events found within the specified date range.")
        return

    with open(filename, mode='w', newline='') as csv_file: 
        fieldnames = ['ID', 'Name', 'Start Date', 'End Date', 'Start Time', 'End Time', 'Description', 'Location',
                      'Repeat Every', 'Repeat Pattern', 'Repeat Count']
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
    
    print(f"Selected events have been exported to '{filename}'.")

# Example usage of exporting events to CSV
#if __name__ == "__main__":

    #export_events_to_csv("2023-09-01", "2023-11-01", "selected_events.csv")
    # start_date = "2023-09-01"  # Replace with your desired start date
    # end_date = "2023-11-01"    # Replace with your desired end date
    # csv_filename = "selected_events.csv"  # Specify the CSV file name

    #export_events_to_csv(start_date, end_date, csv_filename)
