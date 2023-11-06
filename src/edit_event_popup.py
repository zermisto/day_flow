from PyQt5 import QtCore, QtWidgets
import sqlite3
import uuid
import datetime
from Shared_Files.Classes.all_classes import eventClass
from Database.sqlite_demo import insert_event
from Shared_Files.user_input_validation import check_char_limit, check_valid_input, check_start_end_date

connection = sqlite3.connect("Database/eventDB.db")
cursor = connection.cursor()

class CreateEventPopup(QtWidgets.QWidget):
    def set_up_ui(self, Form):
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
        self.repeat_pattern_widget.addItems(["Daily", "Weekly", "Monthly", "Yearly"])
       
        # Label Repeat Every
        self.label_repeat_every = QtWidgets.QLabel(self.widget)
        self.label_repeat_every.setGeometry(QtCore.QRect(120, 290, 101, 20))

        # Repeat Every
        self.repeat_every_widget = QtWidgets.QComboBox(self.widget)
        self.repeat_every_widget.setGeometry(QtCore.QRect(120, 310, 73, 22))
        self.repeat_every_widget.addItems(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])

        # Label Repeat Count
        self.label_repeat_count = QtWidgets.QLabel(self.widget)
        self.label_repeat_count.setGeometry(QtCore.QRect(230, 290, 101, 20))

        # Forever CheckBox
        self.forever_widget = QtWidgets.QCheckBox(self.widget)
        self.forever_widget.setGeometry(QtCore.QRect(230, 310, 91, 20))
        self.forever_widget.setText("Forever")
        # if user click forever, disable the spinBox
        self.forever_widget.stateChanged.connect(
            lambda: self.repeat_count_widget.setDisabled(self.forever_widget.isChecked()))

        # Ends After Label
        self.label_ends_after = QtWidgets.QLabel(self.widget)
        self.label_ends_after.setGeometry(QtCore.QRect(230, 330, 61, 16))

        # Number of Event Occurrences SpinBox
        self.repeat_count_widget = QtWidgets.QSpinBox(self.widget)
        self.repeat_count_widget.setGeometry(QtCore.QRect(290, 330, 42, 22))
        self.repeat_count_widget.setMinimum(1)  # Set the minimum value to 1
        
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

        # if there is any change in the repeat_count, repeat_pattern, or repeat_every, update the label
        self.update_labels()
        self.repeat_pattern_widget.currentTextChanged.connect(self.update_labels)
        self.repeat_every_widget.currentTextChanged.connect(self.update_labels)
        self.repeat_count_widget.valueChanged.connect(self.update_labels)

        # Comfirm Button Clicked
        def on_comfirm_button_clicked():
            # TODO Delete the event with the same id
            
            if check_valid_input(self.event_title_text):
                if check_start_end_date(self.start_date_widget.date(), self.end_date_widget.date()) == True:
                    if self.repeat_pattern_widget.currentText() == "Daily":
                        self.insert_event_daily(self.get_input_from_user()) # insert event into table
                    elif self.repeat_pattern_widget.currentText() == "Weekly": 
                        self.insert_event_weekly(self.get_input_from_user()) # insert event into table
                    elif self.repeat_pattern_widget.currentText() == "Monthly":
                        self.insert_event_monthly(self.get_input_from_user())
                    else: # Yearly
                        self.d(self.get_input_from_user())
                        self.insert_event_yearly(self.get_input_from_user()) # insert event into table
                    Form.close()

        # Connect the OK button click event to the slot
        self.comfirm_button_widget.clicked.connect(on_comfirm_button_clicked)

        def on_delete_button_clicked():
            # Create a message box pop up to confirm delete
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle("Delete Event")
                msg.setText("Are you sure you want to delete this event?")
                msg.setIcon(QtWidgets.QMessageBox.Warning)
                msg.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
                msg.setDefaultButton(QtWidgets.QMessageBox.No)
                if msg.exec_() == QtWidgets.QMessageBox.Yes:
                    #id = TODO get id of event
                    # print(id)
                    # remove_event(id)
                    # Create a message box pop up
                    msg = QtWidgets.QMessageBox()
                    msg.setWindowTitle("Delete Event")
                    msg.setText("Event deleted successfully")
                    msg.setIcon(QtWidgets.QMessageBox.Information)
                Form.close()
        
        # Connect the delete button click event to the slot
        self.delete_button_widget.clicked.connect(on_delete_button_clicked)

        # Connect the Cancel button click event to the slot
        self.cancel_button_widget.clicked.connect(Form.close)
        QtCore.QMetaObject.connectSlotsByName(Form)

    # Retranslate UI
    # Sets the text and title of the widgets
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
        self.comfirm_button_widget.setText("Comfirm")
        self.cancel_button_widget.setText("Cancel")
        self.delete_button_widget.setText("Delete")

    # Update Repeat Every Widget (days of the week)
    def update_repeat_every(self):
        new_date = self.start_date_widget.date()
        start_date = new_date.toString("yyyy-MM-dd")
        start_date = self.start_date_widget.date().toString("yyyy-MM-dd")
        temp = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        repeat_every = temp.strftime("%a") #Mon
        # for loop the days in the week where mon = 0 and sun = 6
        for i in range(7):
            if repeat_every == self.repeat_every_widget.itemText(i):
                break
        self.repeat_every_widget.setCurrentIndex(i)

    # Update Labels (Repeat Pattern, Repeat Every, Repeat Count)
    def update_labels(self):
        repeat_pattern = self.repeat_pattern_widget.currentText()
        repeat_count = self.repeat_count_widget.value()
        create_event_repeat_count = repeat_count - 1
        
        if repeat_pattern == "Daily":   
            self.repeat_every_widget.setDisabled(True)   # disable the repeat_every_widget
            
            if repeat_count == 1: # enddate = startdate 
                self.end_date_widget.setDate(self.start_date_widget.date())
            else: # enddate = startdate + repeat_count - 1
                create_event_repeat_count = repeat_count - 1
                self.end_date_widget.setDate(self.start_date_widget.date().addDays(create_event_repeat_count))
        else:
            self.repeat_every_widget.setDisabled(False) 
        
        if repeat_pattern == "Weekly":
            self.update_repeat_every()
            self.end_date_widget.setDate(self.start_date_widget.date().addDays(7*create_event_repeat_count))

        if repeat_pattern == "Monthly":
            self.update_repeat_every()
            self.end_date_widget.setDate(self.start_date_widget.date().addMonths(create_event_repeat_count))

        if repeat_pattern == "Yearly":
            self.update_repeat_every()
            self.end_date_widget.setDate(self.start_date_widget.date().addYears(create_event_repeat_count))

        return repeat_pattern, repeat_count, create_event_repeat_count
            
    # Get Input From User
    # Gets the input from the user and returns an event object
    def get_input_from_user(self):
        id = uuid.uuid4().int & (1 << 16)-1  # 16-bit random id
        event_name = self.event_title_text.toPlainText()  
        start_date = self.start_date_widget.text()
        end_date = self.end_date_widget.text()
        start_time = self.start_time_widget.text()
        end_time = self.end_time_widget.text()
        description = self.description_text.toPlainText()
        location = self.location_text.toPlainText()
        forever = self.forever_widget.isChecked()
        repeat_pattern = self.repeat_pattern_widget.currentText()
        repeat_every = self.repeat_every_widget.currentText()

        if forever:
            repeat_count = -1
        else:
            repeat_count = self.repeat_count_widget.value()    

        event_data = eventClass(id, event_name, start_date, end_date, start_time,
                                end_time, description, location, repeat_every, repeat_pattern, repeat_count)
        return event_data
    
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


