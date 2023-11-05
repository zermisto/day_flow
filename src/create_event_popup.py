# create_event.py
# Create Event Function GUI for the Personal Calendar Application
# Created by King, 19th October 2023

from PyQt5 import QtCore, QtWidgets
import sqlite3
import uuid
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
        self.comboBox_widget = QtWidgets.QComboBox(self.widget)
        self.comboBox_widget.setGeometry(QtCore.QRect(10, 310, 73, 22))
        self.comboBox_widget.addItems(["Daily", "Weekly", "Monthly", "Yearly"])

        # Label Repeat Every
        self.label_repeat_every = QtWidgets.QLabel(self.widget)
        self.label_repeat_every.setGeometry(QtCore.QRect(120, 290, 101, 20))

        # Repeat Every
        self.comboBox_2_widget = QtWidgets.QComboBox(self.widget)
        self.comboBox_2_widget.setGeometry(QtCore.QRect(120, 310, 73, 22))
        self.comboBox_2_widget.addItems(["Mon", "Tue", "Wed", "Thu", "Fri"])

        # Label Repeat Count
        self.label_repeat_count = QtWidgets.QLabel(self.widget)
        self.label_repeat_count.setGeometry(QtCore.QRect(230, 290, 101, 20))

        # Forever CheckBox
        self.checkBox_widget = QtWidgets.QCheckBox(self.widget)
        self.checkBox_widget.setGeometry(QtCore.QRect(230, 310, 91, 20))
        self.checkBox_widget.setText("Forever")
        # if user click forever, disable the spinBox
        self.checkBox_widget.stateChanged.connect(
            lambda: self.spinBox_widget.setDisabled(self.checkBox_widget.isChecked()))

        # Ends After Label
        self.label_ends_after = QtWidgets.QLabel(self.widget)
        self.label_ends_after.setGeometry(QtCore.QRect(230, 330, 61, 16))

        # Number of Event Occurrences SpinBox
        self.spinBox_widget = QtWidgets.QSpinBox(self.widget)
        self.spinBox_widget.setGeometry(QtCore.QRect(290, 330, 42, 22))
        self.spinBox_widget.setMinimum(1)

        # OK Button
        self.ok_button_widget = QtWidgets.QPushButton(self.widget)
        self.ok_button_widget.setGeometry(QtCore.QRect(20, 360, 93, 28))
        #print type of ok_button_widget
        #print(type(self.ok_button_widget))

        # Cancel Button
        self.cancel_button_widget = QtWidgets.QPushButton(self.widget)
        self.cancel_button_widget.setGeometry(QtCore.QRect(230, 360, 93, 28))

        self.retranslate_ui(Form)

        def on_ok_button_clicked():
            if check_valid_input(self.event_title_text):
                if check_start_end_date(self.start_date_widget.date(), self.end_date_widget.date()) == True:
                    insert_event(self.get_input_from_user())
                    Form.close()

        # Connect the OK button click event to the slot
        self.ok_button_widget.clicked.connect(on_ok_button_clicked)

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
        self.ok_button_widget.setText("OK")
        self.cancel_button_widget.setText("CANCEL")

    # Get Input From User
    # Gets the input from the user and returns an event object
    def get_input_from_user(self):
        id = uuid.uuid4().int & (1 << 16)-1  # 16-bit random id
        event_name = self.event_title_text.toPlainText()  # get event name
        start_date = self.start_date_widget.text()
        end_date = self.end_date_widget.text()
        start_time = self.start_time_widget.text()
        end_time = self.end_time_widget.text()
        description = self.description_text.toPlainText()
        location = self.location_text.toPlainText()
        repeat_pattern = self.comboBox_widget.currentText()
        repeat_every = self.comboBox_2_widget.currentText()
        forever = self.checkBox_widget.isChecked()
        # if user click forever, repeat_count = -1 and disable the spinBoxq
        if forever:
            repeat_count = -1
        else:
            repeat_count = self.spinBox_widget.value()

        event_data = eventClass(id, event_name, start_date, end_date, start_time,
                                end_time, description, location, repeat_every, repeat_pattern, repeat_count)
        return event_data


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = CreateEventPopup()
    ui.set_up_ui(Form)
    Form.show()
    sys.exit(app.exec_())
