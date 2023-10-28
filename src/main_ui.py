# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

# TestGUI.py
# GUI for the Personal Calendar Application
# Created by Roong, 20th October 2023

import sys
from export_button_popup import ExportEventPopup
import search_engine
from create_event import CreateEventPopup
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog
import datetime

am_pm = ["AM", "PM"]
days_in_week = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]
months = [
    'January', 'February', 'March', 'April', 
    'May', 'June', 'July', 'August', 
    'September', 'October', 'November', 'December'
]
days_in_month = [
    31, 28, 31, 30,
    31, 30, 31, 31,
    30, 31, 30, 31
]
today = datetime.date.today()
today_index = today.weekday()
current_time = datetime.datetime.now()
month_index = today.month
first_day_index = today.replace(day=1).weekday()

num_month_row = 6
num_month_column = 7
month_buttons_container : list = []
items_in_month = []
items_in_week = []

# Leap year
if today.year % 4 != 0:
    days_in_month[1] = 29

class Ui_Form(object): 
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(757, 654)
        self.widget = QtWidgets.QWidget(Form) # Create a widget for the ComboBox and TableWidgets
        self.widget.setEnabled(True)
        self.widget.setGeometry(QtCore.QRect(20, 60, 711, 591))
        self.widget.setObjectName("widget")

        # Select view by day week or month buttons
        self.selectViewBy = QtWidgets.QComboBox(self.widget)
        self.selectViewBy.setEnabled(True)
        self.selectViewBy.setGeometry(QtCore.QRect(10, 10, 111, 26))
        self.selectViewBy.setToolTipDuration(0)
        self.selectViewBy.setObjectName("selectView")
        for i in range(3):
            self.selectViewBy.addItem("")
        
        # Current date button
        self.dateEdit = QtWidgets.QDateEdit(self.widget) # Create a DateEdit widget
        self.dateEdit.setEnabled(True)
        self.dateEdit.setGeometry(QtCore.QRect(290, 0, 131, 31))
        self.dateEdit.setMouseTracking(False)
        self.dateEdit.setTabletTracking(False)
        self.dateEdit.setAcceptDrops(False)
        self.dateEdit.setProperty("showGroupSeparator", False)
        self.dateEdit.setObjectName("dateEdit")

        # Next time frame button
        self.nextButton = QtWidgets.QPushButton(self.widget)
        self.nextButton.setGeometry(QtCore.QRect(420, 0, 51, 33))
        self.nextButton.setObjectName("nextButton")

        # Previous time frame button
        self.previousButton = QtWidgets.QPushButton(self.widget)
        self.previousButton.setGeometry(QtCore.QRect(240, 0, 51, 33))
        self.previousButton.setObjectName("previousButton")

        # Month frame
        self.monthDisplay = QtWidgets.QTableWidget(self.widget)
        self.monthDisplay.setEnabled(True)
        self.monthDisplay.setGeometry(QtCore.QRect(10, 40, 701, 521))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.monthDisplay.setFont(font)
        self.monthDisplay.setAutoScrollMargin(16)
        self.monthDisplay.setRowCount(num_month_row)
        self.monthDisplay.setObjectName("Month Widget")
        self.monthDisplay.setColumnCount(num_month_column)
        for i in range(num_month_row):
            item = QtWidgets.QTableWidgetItem()
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.monthDisplay.setVerticalHeaderItem(i, item)
        for i in range(num_month_column):
            item = QtWidgets.QTableWidgetItem()
            self.monthDisplay.setHorizontalHeaderItem(i, item)
        global month_buttons_container
        for i in range(num_month_row):
            for j in range(num_month_column):
                item = QtWidgets.QTableWidgetItem()
                item.setFlags(QtCore.Qt.ItemIsEnabled)
                item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
                self.monthDisplay.setItem(i, j, item)
                # Add button objects
                eventButton = QtWidgets.QToolButton()
                eventButton.setStyleSheet("margin-top: 15px; background-color: transparent;")
                self.monthDisplay.setCellWidget(i, j, eventButton)
                month_buttons_container.append(eventButton)
        self.monthDisplay.horizontalHeader().setVisible(True)
        self.monthDisplay.horizontalHeader().setCascadingSectionResizes(True)
        self.monthDisplay.horizontalHeader().setDefaultSectionSize(100)
        self.monthDisplay.horizontalHeader().setMinimumSectionSize(0)
        self.monthDisplay.verticalHeader().setDefaultSectionSize(80)
        self.monthDisplay.verticalHeader().setMinimumSectionSize(0)

        # Week frame
        self.weekDisplay = QtWidgets.QTableWidget(self.widget)
        self.weekDisplay.setGeometry(QtCore.QRect(10, 40, 701, 531))
        self.weekDisplay.setObjectName("Week Widget")
        self.weekDisplay.setColumnCount(num_month_column)
        self.weekDisplay.setRowCount(24)
        count = 0
        for i in am_pm:
            for j in range(1, 13, 1):
                item = QtWidgets.QTableWidgetItem()
                self.weekDisplay.setVerticalHeaderItem(count, item)
                count += 1
        for i, _ in enumerate(days_in_week):
            item = QtWidgets.QTableWidgetItem()
            self.weekDisplay.setHorizontalHeaderItem(i, item)
        
        # Day frame
        self.dayDisplay = QtWidgets.QTableWidget(self.widget)
        self.dayDisplay.setGeometry(QtCore.QRect(10, 40, 701, 531))
        self.dayDisplay.setObjectName("Day Widget")
        self.dayDisplay.setColumnCount(1)
        self.dayDisplay.setRowCount(24)
        count = 0
        for i in am_pm:
            for j in range(1, 13, 1):
                item = QtWidgets.QTableWidgetItem()
                self.dayDisplay.setVerticalHeaderItem(count, item)
                count += 1
        item = QtWidgets.QTableWidgetItem()
        self.dayDisplay.setHorizontalHeaderItem(0, item)

        # Create button
        self.create_event_button = QtWidgets.QPushButton(Form)
        self.create_event_button.setGeometry(QtCore.QRect(255, 10, 81, 33))
        self.create_event_button.setObjectName("createEvent")
        self.create_event_button.clicked.connect(self.show_event_dialog)

        # Search text box
        self.searchBox = QtWidgets.QLineEdit(Form)
        self.searchBox.setGeometry(QtCore.QRect(20, 10, 240, 31))
        self.searchBox.setText("")
        self.searchBox.setObjectName("searchBox")
        self.searchBox.textChanged.connect(self.on_text_changed)

        # Search type dropdown menu
        self.searchBy = QtWidgets.QComboBox(Form)
        self.searchBy.setEnabled(True)
        self.searchBy.setGeometry(QtCore.QRect(15, 40, 245, 20))
        self.searchBy.setToolTipDuration(0)
        self.searchBy.setObjectName("searchBy")
        for i in range(5):
            self.searchBy.addItem("")

        # Export button
        self.exportButton = QtWidgets.QPushButton(Form)
        self.exportButton.setGeometry(QtCore.QRect(640, 10, 100, 33))
        self.exportButton.setObjectName("exportButton")
        self.exportButton.clicked.connect(self.show_export_event)

        # Current day label
        self.currentDayLabel = QtWidgets.QLabel(Form)
        self.currentDayLabel.setGeometry(QtCore.QRect(450, 10, 241, 31))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.currentDayLabel.setFont(font)
        self.currentDayLabel.setObjectName("currentDayLabel")

        # Search result list
        self.searchResult = QtWidgets.QListWidget(Form)
        self.searchResult.setGeometry(QtCore.QRect(20, 40, 245, 0))
        self.searchResult.setObjectName("searchResult")
        self.searchResult.itemClicked.connect(self.on_search_result_clicked)
        self.selectViewBy.currentIndexChanged.connect(self.on_display_changed)

        self.on_display_changed(0) # Call the slot initially to set the initial state
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
    
    def refresh_month_display(self, target_day_index, month_index):
        _translate = QtCore.QCoreApplication.translate
        for i, day in enumerate(days_in_week):
            item = self.monthDisplay.horizontalHeaderItem(i)
            item.setText(_translate("Form", day))
        __sortingEnabled = self.monthDisplay.isSortingEnabled()
        self.monthDisplay.setSortingEnabled(False)
        count = 0
        temp_current_month_day = 1
        temp_next_month_day = 1
        temp_prev_month_day = days_in_month[(month_index - 2) % 12]
        temp_prev_month_day -= target_day_index - 1
        for i in range(num_month_row):
            for j in range(num_month_column):
                item = self.monthDisplay.item(i, j)
                if count < first_day_index:
                    item.setForeground(QtGui.QColor('grey'))
                    temp_day = temp_prev_month_day
                    temp_prev_month_day += 1
                elif count > first_day_index + days_in_month[month_index]:
                    item.setForeground(QtGui.QColor('grey'))
                    temp_day = temp_next_month_day
                    temp_next_month_day += 1
                else:
                    temp_day = temp_current_month_day
                    temp_current_month_day += 1
                    if count % 7 == 6 or count % 7 == 5:
                        item.setForeground(QtGui.QColor('indianred'))
                if today.day == temp_current_month_day - 1:
                    item.setForeground(QtGui.QColor('cyan'))
                item.setText(_translate("Form", "{}".format(temp_day)))
                month_buttons_container[count].setText("")
                count += 1
        self.monthDisplay.setSortingEnabled(__sortingEnabled)

    def refresh_date_textbox(self, target_day, target_month, target_year):
        self.dateEdit.setDate(QtCore.QDate(target_year, target_month, target_day))

    def move_to_targetdate(self, input_date : str):
        # Update day display
        print("TODO Update day display")
        # Update week display
        print("TODO Update week display")
        # Update month display
        count = 0
        target_y_m_d = input_date.split("-")
        month_index = int(target_y_m_d[1])
        start_date = target_y_m_d[0] + "-" + target_y_m_d[1] +  "-" + "1"
        end_date = target_y_m_d[0] + "-" + target_y_m_d[1] + "-" + str(days_in_month[month_index])
        events_in_month = search_engine.event_range_search(start_date, end_date)
        first_day_index = today.replace(day=1, month=month_index).weekday()
        
        # Put all events in the dictionary
        day_dict = {}
        def add_event_to_dict(temp_key, temp_value):
            if day_dict.get(temp_key) == None:
                day_dict[temp_key] = str(temp_value) + "\n"
            else:
                splited_events = day_dict[temp_key].split("\n")
                if len(splited_events) < 3:
                    day_dict[temp_key] = str(day_dict[temp_key]) + str(temp_value)
                else:
                    day_dict[temp_key] = str(day_dict[temp_key]) + "..."

        for event in events_in_month:
            temp_y_m_d = event[2].split("-")
            temp_key = int(temp_y_m_d[2]) - 1 + first_day_index
            temp_value = event[1]
            add_event_to_dict(temp_key, temp_value)
            recurring_count = event[10]
            recurring_pattern = event[9]
            step_size = 7
            if recurring_pattern == 'D':
                step_size = 1
            for i in range(1, recurring_count, step_size):
                cursor = (step_size * i) + temp_key 
                if cursor <= num_month_column * num_month_row:
                    add_event_to_dict(cursor, temp_value)
                else:
                    break
            
        # Get all events and place in the frame
        for key in day_dict:
            month_buttons_container[key].setText(day_dict[key])
    
    def on_text_changed(self):
        self.searchResult.clear()
        num_item = 0
        result_items = []
        search_text = self.searchBox.text().strip()
        search_types = search_engine.search_types
        if not search_text:
            num_item = 0
        else:
            selected_index = self.searchBy.currentIndex()
            result_items = search_engine.event_search(search_text, search_types[selected_index])
            num_item = len(result_items)
            for item in result_items:
                label_string = item[1] + "\n{}[{}] - {}[{}]".format(item[2], item[4], item[3], item[5])
                self.searchResult.addItem(label_string)
        self.searchResult.setGeometry(QtCore.QRect(30, 40, 245, (num_item * 100)))
    
    def on_search_result_clicked(self, item):
        if item is not None:
            self.move_to_targetdate()            
                
    def show_event_dialog(self):
        # Create an instance of the event creation dialog
        event_dialog = QDialog()
        ui = CreateEventPopup()                  
        ui.set_up_ui(event_dialog)
        # Show the dialog
        event_dialog.exec_()
    
    def show_export_event(self):
        # Create an instance of the event creation dialog
        event_export = QDialog()
        ui = ExportEventPopup()                  
        ui.set_up_ui(event_export)
        # Show the dialog
        event_export.exec_()

    def on_display_changed(self, index):
        # Get the selected text from the ComboBox
        selected_text = self.selectViewBy.currentText()

        # Set the visibility of the TableWidgets based on the selected text
        if selected_text == "Month":
            self.monthDisplay.setVisible(True)
            self.weekDisplay.setVisible(False)
            self.dayDisplay.setVisible(False)
        elif selected_text == "Week":
            self.monthDisplay.setVisible(False)
            self.weekDisplay.setVisible(True)
            self.dayDisplay.setVisible(False)
        elif selected_text == "Day":
            self.monthDisplay.setVisible(False)
            self.weekDisplay.setVisible(False)
            self.dayDisplay.setVisible(True)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.selectViewBy.setItemText(0, _translate("Form", "Day"))
        self.selectViewBy.setItemText(1, _translate("Form", "Week"))
        self.selectViewBy.setItemText(2, _translate("Form", "Month"))

        self.searchBy.setItemText(0, _translate("Form", "By Title [event name]"))
        self.searchBy.setItemText(1, _translate("Form", "By Start Date [yyyy-mm-dd]"))
        self.searchBy.setItemText(2, _translate("Form", "By End Date [yyyy-mm-dd]"))
        self.searchBy.setItemText(3, _translate("Form", "By Start Time [hh:mm]"))
        self.searchBy.setItemText(4, _translate("Form", "By End Time [hh:mm]"))

        self.nextButton.setText(_translate("Form", ">"))
        self.previousButton.setText(_translate("Form", "<"))
        # Reset date edit configurq
        self.refresh_date_textbox(today.day, today.month, today.year)

        # Reset month configure
        self.refresh_month_display(first_day_index, today.month)

        # Week display
        count = 0
        for i in am_pm:
            for j in range(1, 13, 1):
                item = self.weekDisplay.verticalHeaderItem(count)
                item.setText(_translate("Form", "{} {}".format(j, i)))
                count += 1
        for i, day in enumerate(days_in_week):
            item = self.weekDisplay.horizontalHeaderItem(i)
            item.setText(_translate("Form", "{} {}".format(day, today.day + i)))

        count = 0
        for i in am_pm: 
            for j in range(1, 13, 1):
                item = self.dayDisplay.verticalHeaderItem(count)
                item.setText(_translate("Form", "{} {}".format(j, i)))
                count += 1

        self.create_event_button.setText(_translate("Form", "Create"))
        self.searchBox.setPlaceholderText(_translate("Form", "Search Event"))
        self.exportButton.setText(_translate("Form", "Export"))
        self.currentDayLabel.setText(_translate("Form", "{} {} {}"
        .format(today.day, months[today.month - 1], today.year)))
        # Load all today display
        target_date_str = str(today.year) + "-" + str(today.month) +  "-" + str(today.day)
        self.move_to_targetdate(target_date_str)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
