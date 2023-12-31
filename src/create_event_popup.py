""" 
create_event.py
Create Event Function GUI for the Personal Calendar Application

Created by King, 19th October 2023
"""

from PyQt5 import QtCore, QtWidgets
import sqlite3
import uuid
import time
from datetime import datetime as Datetime
from Shared_Files.Classes.all_classes import eventClass
from Database.sqlite_demo import insert_event, remove_event
from Shared_Files.search_engine import event_search_recurring
from Shared_Files.user_input_validation import check_char_limit, check_valid_input, check_start_end_date
import os
import sys
import Database.sqlite_demo as sqlite_func

destination_path = sqlite_func.find_db_path()
connection = sqlite3.connect(destination_path)
cursor = connection.cursor()

""" Create a class for the create event popup window
    The popup window will ask the user to input 
    the event title, start date, end date, start time, end time, 
    description, location, repeat pattern, repeat every, repeat count
    The popup window will also have an 
    OK button, a Delete button and a Cancel button
    The OK button will call the insert_event function to 
    insert the event to the database
    The Delete button will call the remove_event function 
    to delete the event from the database
    The Cancel button will close the popup window
"""
class CreateEventPopup(QtWidgets.QWidget):
    """ 
    Set up the UI for the create event popup window
    Set up the UI elements for the popup window
    Set up the title for the popup window
    arguments:
        Form        - the popup window
        event_id    - the id of the event
    """
    def set_up_ui(self, Form, event_id=None):
        Form.setObjectName("Form")
        Form.resize(440, 481)

        # Main widget box
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setGeometry(QtCore.QRect(50, 40, 351, 391))

        # Event Title
        self.event_title_text = QtWidgets.QTextEdit(self.widget)
        self.event_title_text.setGeometry(QtCore.QRect(0, 0, 351, 31))
        self.event_title_text.setPlaceholderText("Event Title")
        self.event_title_text.textChanged.connect(
            lambda: check_char_limit(self.event_title_text, 100))

        # Label Start Date
        self.label_start_date = QtWidgets.QLabel(self.widget)
        self.label_start_date.setGeometry(QtCore.QRect(0, 40, 121, 31))

        # Start Date
        self.start_date_widget = QtWidgets.QDateEdit(self.widget)
        self.start_date_widget.setGeometry(QtCore.QRect(65, 40, 91, 31))
        self.start_date_widget.setDisplayFormat("yyyy-MM-dd")
        self.start_date_widget.setDateTime(QtCore.QDateTime.currentDateTime())
        self.start_date_widget.dateChanged.connect(self.update_repeat_every)

        # Label Start Time
        self.label_start_time = QtWidgets.QLabel(self.widget)
        self.label_start_time.setGeometry(QtCore.QRect(0, 80, 121, 31))

        # Start Time
        self.start_time_widget = QtWidgets.QTimeEdit(self.widget)
        self.start_time_widget.setGeometry(QtCore.QRect(65, 80, 81, 31))
        self.start_time_widget.setDisplayFormat("hh:mm")
        self.start_time_widget.setDateTime(QtCore.QDateTime.currentDateTime())
        
        # Label End Date
        self.label_end_state = QtWidgets.QLabel(self.widget)
        self.label_end_state.setGeometry(QtCore.QRect(170, 40, 121, 31))

        # End Date
        self.end_date_widget = QtWidgets.QDateEdit(self.widget)
        self.end_date_widget.setGeometry(QtCore.QRect(230, 40, 91, 31))
        self.end_date_widget.setDisplayFormat("yyyy-MM-dd")
        self.end_date_widget.setDateTime(QtCore.QDateTime.currentDateTime())
        self.end_date_widget.dateChanged.connect(self.on_end_date_changed)

        # Label End Time
        self.label_end_time = QtWidgets.QLabel(self.widget)
        self.label_end_time.setGeometry(QtCore.QRect(170, 80, 121, 31))

        # End Time
        self.end_time_widget = QtWidgets.QTimeEdit(self.widget)
        self.end_time_widget.setGeometry(QtCore.QRect(230, 80, 81, 31))
        self.end_time_widget.setDisplayFormat("hh:mm")
        self.end_time_widget.setDateTime(QtCore.QDateTime.currentDateTime())

        # Description
        self.description_text = QtWidgets.QTextEdit(self.widget)
        self.description_text.setGeometry(QtCore.QRect(0, 120, 351, 91))
        self.description_text.setPlaceholderText("Description")
        self.description_text.textChanged.connect(
            lambda: check_char_limit(self.description_text, 100))

        # Location
        self.location_text = QtWidgets.QTextEdit(self.widget)
        self.location_text.setGeometry(QtCore.QRect(0, 220, 351, 51))
        self.location_text.setPlaceholderText("Location")
        self.location_text.textChanged.connect(
            lambda: check_char_limit(self.location_text, 100))

        # Label Repeat Pattern
        self.label_repeat_pattern = QtWidgets.QLabel(self.widget)
        self.label_repeat_pattern.setGeometry(QtCore.QRect(0, 290, 101, 20))

        # Repeat Pattern
        self.repeat_pattern_widget = QtWidgets.QComboBox(self.widget)
        self.repeat_pattern_widget.setGeometry(QtCore.QRect(10, 310, 73, 22))
        self.repeat_pattern_widget.addItems(
            ["Daily", "Weekly", "Monthly", "Yearly"])
        self.repeat_pattern_widget.currentIndexChanged.connect(self.on_end_date_changed)
       
        # Label Repeat Every
        self.label_repeat_every = QtWidgets.QLabel(self.widget)
        self.label_repeat_every.setGeometry(QtCore.QRect(120, 290, 101, 20))

        # Repeat Every
        self.repeat_every_widget = QtWidgets.QComboBox(self.widget)
        self.repeat_every_widget.setGeometry(QtCore.QRect(120, 310, 73, 22))
        self.repeat_every_widget.addItems(
            ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])
        self.repeat_every_widget.setDisabled(True)

        # Label Repeat Count
        self.label_repeat_count = QtWidgets.QLabel(self.widget)
        self.label_repeat_count.setGeometry(QtCore.QRect(230, 290, 101, 20))

        # Ends After Label
        self.label_ends_after = QtWidgets.QLabel(self.widget)
        self.label_ends_after.setGeometry(QtCore.QRect(230, 315, 61, 16))

        # Number of Event Occurrences SpinBox
        self.repeat_count_widget = QtWidgets.QSpinBox(self.widget)
        self.repeat_count_widget.setGeometry(QtCore.QRect(290, 315, 42, 22))
        self.repeat_count_widget.setMinimum(1)  # Set the minimum value to 1
        self.repeat_count_widget.setMaximum(9999)
        
        # Comfirm Button
        self.comfirm_button_widget = QtWidgets.QPushButton(self.widget)
        self.comfirm_button_widget.setGeometry(QtCore.QRect(20, 360, 93, 28))

        # Delete Button
        self.delete_button_widget = QtWidgets.QPushButton(self.widget)
        self.delete_button_widget.setGeometry(QtCore.QRect(120, 360, 93, 28))

        # Cancel Button
        self.cancel_button_widget = QtWidgets.QPushButton(self.widget)
        self.cancel_button_widget.setGeometry(QtCore.QRect(230, 360, 93, 28))

        self.retranslate_ui(Form)

        # Load data into the frame if any event_id is given.
        if event_id is not None:
            # Get a target item
            event_items = event_search_recurring(str(event_id), "id")
            if len(event_items) < 1:
                QtWidgets.QMessageBox.warning(
                    Form, "No Item Found for the given ID.")
                Form.close()
                return False
            first_event = event_items[0]
            last_event = event_items[-1]
            self.event_title_text.setText(first_event[1])
            self.start_date_widget.setDate(QtCore.QDate.fromString
                                           (first_event[2], "yyyy-MM-dd"))
            self.end_date_widget.setDate(QtCore.QDate.fromString
                                         (last_event[3], "yyyy-MM-dd"))
            self.start_time_widget.setTime(QtCore.QTime.fromString
                                           (first_event[4], "hh:mm"))
            self.end_time_widget.setTime(QtCore.QTime.fromString
                                         (last_event[5], "hh:mm"))
            self.description_text.setText(first_event[6])
            self.location_text.setText(first_event[7])
            index = self.repeat_every_widget.findText(first_event[8])
            if index >= 0:
                self.repeat_every_widget.setCurrentIndex(index)
            index = self.repeat_pattern_widget.findText(first_event[9])
            if index >= 0:
                self.repeat_pattern_widget.setCurrentIndex(index)
            self.repeat_count_widget.setValue(first_event[10])

        """ 
        if there is any change in the repeat_count, 
        repeat_pattern, or repeat_every, update the label
        """
        self.update_labels()
        self.repeat_pattern_widget.currentTextChanged.connect(self.update_labels)
        self.repeat_every_widget.currentTextChanged.connect(self.update_labels)
        self.repeat_count_widget.valueChanged.connect(self.update_labels)

        """ 
        OK Button Clicked
        Check if the input from the user is valid
        Check if the start date is before the end date
        Insert the event to the database
        Close the popup window
        """
        def on_comfirm_button_clicked():
            if event_id is not None:
                remove_event(event_id)
            if check_valid_input(self.event_title_text):
                if check_start_end_date(self.start_date_widget.date(), 
                                        self.end_date_widget.date()) == True:
                    self.insert_event_types(self.get_input_from_user(), 
                                            self.repeat_pattern_widget.currentText())
                    Form.close()

        # Connect the OK button click event to the slot
        self.comfirm_button_widget.clicked.connect(on_comfirm_button_clicked)

        """ 
        Delete Button Clicked
        Remove the event from the database
        Close the popup window
        """
        def on_delete_button_clicked():
            # Create a popup window to confirm the deletion
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("Delete Event")
            msg.setText("Are you sure you want to delete this event?")
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setStandardButtons(QtWidgets.QMessageBox.Yes 
                                   | QtWidgets.QMessageBox.No)
            msg.setDefaultButton(QtWidgets.QMessageBox.No)
            msg.buttonClicked.connect(lambda x: remove_event(event_id) 
                                      if x.text() == "&Yes" else None)
            msg.exec_()
            Form.close()

        # Connect the Delete button click event to the slot
        self.delete_button_widget.clicked.connect(on_delete_button_clicked)

        # Connect the Cancel button click event to the slot
        self.cancel_button_widget.clicked.connect(Form.close)
        QtCore.QMetaObject.connectSlotsByName(Form)

    """ 
    Retranslate UI
    Sets initialize the properties of the UI including
    text title and so on
    arguments:
        Form    - the popup window
    """
    def retranslate_ui(self, Form):
        Form.setWindowTitle("Form")
        self.label_start_date.setText("Start Date")
        self.label_start_time.setText("Start Time")
        self.label_end_state.setText("End Date")
        self.label_end_time.setText("End Time")
        self.label_repeat_count.setText("Repeat Count?")
        self.label_repeat_pattern.setText("Repeat Pattern?")
        self.label_repeat_every.setText("Repeat Every?")
        self.label_ends_after.setText("Ends After")
        self.comfirm_button_widget.setText("Confirm")
        self.delete_button_widget.setText("Delete")
        self.cancel_button_widget.setText("CANCEL")      

    """ 
    Update Repeat Every Widget (days of the week)
    Update the repeat_every_widget to the day of the week 
    of the start date
    """
    def update_repeat_every(self):
        new_date = self.start_date_widget.date()
        start_date = new_date.toString("yyyy-MM-dd")
        start_date = self.start_date_widget.date().toString("yyyy-MM-dd")
        temp = Datetime.strptime(start_date, '%Y-%m-%d')
        repeat_every = temp.strftime("%a") #Mon
        # for loop the days in the week where mon = 0 and sun = 6
        for i in range(7):
            if repeat_every == self.repeat_every_widget.itemText(i):
                break
        self.repeat_every_widget.setCurrentIndex(i)

    """ 
    Update Repeat Every Widget coresponding with the
    repeat count and repeat pattern
    """
    def on_end_date_changed(self):
        repetition_type = self.repeat_pattern_widget.currentText()
        if repetition_type == "Daily":
            self.end_date_widget.setDisabled(False)
            start_date = self.start_date_widget.date()
            end_date = self.end_date_widget.date()
            start_year, start_month, start_day = start_date.year(), start_date.month(), start_date.day()
            end_year, end_month, end_day = end_date.year(), end_date.month(), end_date.day()
            start_datetime = Datetime(start_year, start_month, start_day)
            end_datetime = Datetime(end_year, end_month, end_day)
            delta_days = (end_datetime - start_datetime).days + 1
            self.repeat_count_widget.setValue(delta_days)
        else:
            self.end_date_widget.setDisabled(True)

    """ 
    Update Labels (Repeat Pattern, Repeat Every, Repeat Count)
    Update the labels for the repeat pattern, repeat every and repeat count
    return the repeat pattern, repeat count and create_event_repeat_count
    """
    def update_labels(self):
        repeat_pattern = self.repeat_pattern_widget.currentText()
        repeat_count = self.repeat_count_widget.value()
        create_event_repeat_count = repeat_count - 1
        
        if repeat_pattern == "Daily":
            if repeat_count == 1: # enddate = startdate 
                self.end_date_widget.setDate(self.start_date_widget.date())
            else: # enddate = startdate + repeat_count - 1
                create_event_repeat_count = repeat_count - 1
                self.end_date_widget.setDate(self.start_date_widget.date().
                                             addDays(create_event_repeat_count))
        if repeat_pattern == "Weekly":
            self.update_repeat_every()
            self.end_date_widget.setDate(self.start_date_widget.date().
                                         addDays(7*create_event_repeat_count))

        if repeat_pattern == "Monthly":
            self.update_repeat_every()
            self.end_date_widget.setDate(self.start_date_widget.date().
                                         addMonths(create_event_repeat_count))

        if repeat_pattern == "Yearly":
            self.update_repeat_every()
            self.end_date_widget.setDate(self.start_date_widget.date().
                                         addYears(create_event_repeat_count))

        return repeat_pattern, repeat_count, create_event_repeat_count
            
    """ 
    Get Input From User
    Gets the input from the user and returns an event object
    return the event object
    """
    def get_input_from_user(self):
        id = uuid.uuid4().int & (1 << 16)-1  # 16-bit random id
        event_name = self.event_title_text.toPlainText()  
        start_date = self.start_date_widget.text()
        end_date = self.end_date_widget.text()
        start_time = self.start_time_widget.text()
        end_time = self.end_time_widget.text()
        description = self.description_text.toPlainText()
        location = self.location_text.toPlainText()
        repeat_pattern = self.repeat_pattern_widget.currentText()
        repeat_every = self.repeat_every_widget.currentText()

        repeat_count = self.repeat_count_widget.value()    
        event_data = eventClass(id, event_name, start_date, end_date, start_time,
                                end_time, description, location, repeat_every, 
                                repeat_pattern, repeat_count)
        return event_data
    
    """ 
    Insert event to the database 
    also correct the date format
    arguments
        event           - target event class to be inserted
        repeat_interval - string type of repetition
    """
    def insert_event_types(self, event, repeat_interval):
        repeat_count = event.repeat_count
        id = event.id

        for j in range(repeat_count):
            event.id = id
        
            if repeat_interval == "Daily":
                start_date = self.start_date_widget.date().addDays(j) 
            elif repeat_interval == "Weekly":
                start_date = self.start_date_widget.date().addDays(j*7)
            elif repeat_interval == "Monthly":
                start_date = self.start_date_widget.date().addMonths(j)
            elif repeat_interval == "Yearly":
                start_date = self.start_date_widget.date().addYears(j)

            event.start_date = start_date.toString("yyyy-MM-dd")
            event.end_date = start_date.toString("yyyy-MM-dd")

            insert_event(event)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = CreateEventPopup()
    ui.set_up_ui(Form)
    Form.show()
    sys.exit(app.exec_())

