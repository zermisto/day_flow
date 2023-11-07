"""
main_ui.py

The main user interface program for the day_flow project
including these features
-Search for events by their title – show all matches with date, time
-Display month, week, and day display
-Edit and delete event
-Export events for a specified date range in CSV format
most functionalities involve a lot on user interfaces

Created by Roong 19 October 2023
Last update Mhon 5th November 2023
"""

# Built-in
import sys
import datetime
import calendar
import math
# external libraries
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog
# Our libraries
import Shared_Files.search_engine as search_engine
from Export_Event.export_button_popup import ExportEventPopup
from create_event_popup import CreateEventPopup

# Constant
ITEM_THRESHOLD = 1440
AM_PM = ["AM", "PM"]
DAYS_A_WEEK = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]
HOURS_A_DAY = 24
MONTHS = [
    'January', 'February', 'March', 'April', 
    'May', 'June', 'July', 'August', 
    'September', 'October', 'November', 'December'
]
VIEWS = ["Day", "Week", "Month"]
FRAME_STEPSIZE = [1, 7, 30]
MONTH_ROW = 6
MONTH_COL = 7
DISPLAY_COL = 7

# Initialize variables
today = datetime.date.today()
today_index = today.weekday()
current_time = datetime.datetime.now()
month_index = today.month
first_day_index = today.replace(day=1).weekday()
month_buttons_container : list = []
week_buttons_container : list = []
day_buttons_container : list = []
to_edit_event_id = -1

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

        # Month frame
        self.monthDisplay = QtWidgets.QTableWidget(self.widget)
        self.monthDisplay.setEnabled(True)
        self.monthDisplay.setGeometry(QtCore.QRect(10, 40, 701, 521))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.monthDisplay.setFont(font)
        self.monthDisplay.setAutoScrollMargin(16)
        self.monthDisplay.setRowCount(MONTH_ROW)
        self.monthDisplay.setObjectName("Month Widget")
        self.monthDisplay.setColumnCount(MONTH_COL)
        for i in range(MONTH_ROW):
            item = QtWidgets.QTableWidgetItem()
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.monthDisplay.setVerticalHeaderItem(i, item)
        for i in range(MONTH_COL):
            item = QtWidgets.QTableWidgetItem()
            self.monthDisplay.setHorizontalHeaderItem(i, item)
        self.monthDisplay.horizontalHeader().setVisible(True)
        self.monthDisplay.horizontalHeader().setCascadingSectionResizes(True)
        self.monthDisplay.horizontalHeader().setDefaultSectionSize(100)
        self.monthDisplay.horizontalHeader().setMinimumSectionSize(0)
        self.monthDisplay.verticalHeader().setDefaultSectionSize(80)
        self.monthDisplay.verticalHeader().setMinimumSectionSize(0)

        # Day frame
        self.dayDisplay = QtWidgets.QTableWidget(self.widget)
        self.dayDisplay.setGeometry(QtCore.QRect(10, 40, 701, 531))
        self.dayDisplay.setObjectName("Day Widget")
        self.dayDisplay.setColumnCount(1)
        self.dayDisplay.setRowCount(HOURS_A_DAY)
        self.dayDisplay.horizontalHeader().setDefaultSectionSize(701 - 45)

        # Week frame
        self.weekDisplay = QtWidgets.QTableWidget(self.widget)
        self.weekDisplay.setGeometry(QtCore.QRect(10, 40, 701, 531))
        self.weekDisplay.setObjectName("Week Widget")
        self.weekDisplay.setColumnCount(MONTH_COL)
        self.weekDisplay.setRowCount(HOURS_A_DAY)
        self.weekDisplay.setVisible(False)

        for i in range(DISPLAY_COL):
            item = QtWidgets.QTableWidgetItem()
            self.weekDisplay.setHorizontalHeaderItem(i, item)

        # Initialize all week and day vertical header
        count = 0
        for _ in AM_PM:
            for _ in range(1, 13, 1):
                item = QtWidgets.QTableWidgetItem()
                self.dayDisplay.setVerticalHeaderItem(count, item)
                self.weekDisplay.setVerticalHeaderItem(count, item)
                count += 1

        # Set selection mode to NoSelection for both headers in day and week tables
        for item in ([self.dayDisplay, self.weekDisplay]):
            item.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
            item.horizontalHeader().setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
            item.verticalHeader().setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)

        # Date search button
        self.dateSearchButton = QtWidgets.QPushButton(self.widget)
        self.dateSearchButton.setGeometry(QtCore.QRect(418, 0, 40, 33))
        self.dateSearchButton.setObjectName("dateSearchButton")
        self.dateSearchButton.clicked.connect(self.enter_date)

        # Next time frame button
        self.nextButton = QtWidgets.QPushButton(self.widget)
        self.nextButton.setGeometry(QtCore.QRect(450, 0, 51, 33))
        self.nextButton.setObjectName("nextButton")
        self.nextButton.clicked.connect(self.move_next_frame)

        # Previous time frame button
        self.previousButton = QtWidgets.QPushButton(self.widget)
        self.previousButton.setGeometry(QtCore.QRect(240, 0, 51, 33))
        self.previousButton.setObjectName("previousButton")
        self.previousButton.clicked.connect(self.move_prev_frame)

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

    def move_to_targetdate(self, input_date : datetime.date):
        # Refresh all frames
        self.refresh_day_display(today)
        self.refresh_week_display(today)
        self.refresh_month_display(today)
        self.dateEdit.setDate(QtCore.QDate(today.year, today.month, today.day))

        # Update day display
        start_date = input_date.strftime('%Y-%m-%d')
        events_in_day = search_engine.event_range_search(start_date, start_date)
        for event in events_in_day:
            start_time = int(event[4].split(":")[0])
            end_time = int(event[5].split(":")[0])
            for i in range(start_time, end_time + 1):
                item_label = str(event[1]) + " \t[" + str(event[4]) + "-" + str((event[5])) +  " ]\t" + str(event[6])
                item = QtWidgets.QListWidgetItem(item_label)
                item.setData(1, event[0])
                day_buttons_container[i].addItem(item)

        # Update week display
        start_date = input_date.strftime('%Y-%m-%d')
        temp_date = input_date + datetime.timedelta(days=7)
        end_date = temp_date.strftime('%Y-%m-%d')
        events_in_week = search_engine.event_range_search(start_date, end_date)

        # Add item in the list in each week cells
        for event in events_in_week:
            # Roong TODO 
            pass
        
        # Update month display
        last_day = calendar.monthrange(input_date.year, today.month)[1]
        start_date = input_date.strftime('%Y-%m-01')
        end_date = input_date.strftime('%Y-%m-'+str(last_day))
        events_in_month = search_engine.event_range_search(start_date, end_date)
        first_day_index = input_date.replace(day=1, month=input_date.month).weekday()

        # Add item in the list in each month cells
        for event in events_in_month:
            temp_y_m_d = event[2].split("-")
            temp_key = int(temp_y_m_d[2]) - 1 + first_day_index
            item = QtWidgets.QListWidgetItem(event[1])
            item.setData(1, event[0])
            month_buttons_container[temp_key].addItem(item)

    def enter_date(self):
        global today
        date = self.dateEdit.date()
        today = today.replace(year=date.year(), month=date.month(), day=date.day())
        self.move_to_targetdate(today)
                
    def move_next_frame(self):
        global today
        day_step_size = FRAME_STEPSIZE[self.selectViewBy.currentIndex()]
        new_date = today + datetime.timedelta(days=day_step_size)
        today = new_date
        self.move_to_targetdate(today)

    def move_prev_frame(self):
        global today
        day_step_size = FRAME_STEPSIZE[self.selectViewBy.currentIndex()]
        new_date = today - datetime.timedelta(days=day_step_size)
        today = new_date
        self.move_to_targetdate(today)

    def refresh_day_display(self, target_date):
        day_text = "{} {}".format(DAYS_A_WEEK[target_date.weekday()], target_date.day)
        header_item = QtWidgets.QTableWidgetItem(day_text)
        self.dayDisplay.setHorizontalHeaderItem(0, header_item)
        # Clear all items in list
        for i in range(HOURS_A_DAY):
            day_buttons_container[i].clear()

    def refresh_week_display(self, target_date):
        for i, day in enumerate(DAYS_A_WEEK):
            day_text = "{} {}".format(day, target_date.day + i)
            header_item = QtWidgets.QTableWidgetItem(day_text)
            self.weekDisplay.setHorizontalHeaderItem(i, header_item)
        # Clear all items in list
        count = 0
        for i in range(DISPLAY_COL):
            for j in range(HOURS_A_DAY):
                # ROONG TODO Here
                # week_buttons_container[count].clear()
                count += 1

    def refresh_month_display(self, target_day : datetime.date):
        _translate = QtCore.QCoreApplication.translate
        self.monthDisplay.setSortingEnabled(False)
        # set header columns
        for i, day in enumerate(DAYS_A_WEEK):
            item = self.monthDisplay.horizontalHeaderItem(i)
            item.setText(_translate("Form", day))
        __sortingEnabled = self.monthDisplay.isSortingEnabled()

        first_day_index = target_day.replace(year=target_day.year ,day=1).weekday()
        temp_day = 0
        temp_current_month_day = 1
        temp_next_month_day = 1
        target_day_index = target_day.day
        target_month_index = (target_day.month - 2) % 12
        last_day_prev_month = calendar.monthrange(target_day.year, target_month_index + 1)[1]
        last_day = calendar.monthrange(target_day.year, target_day.month)[1]
        temp_last_day_prev_month = last_day_prev_month - first_day_index + 1
        count = 0
        for i in range(MONTH_ROW):
            for j in range(MONTH_COL):
                item = self.monthDisplay.item(i, j)
                if count < first_day_index:
                    item.setForeground(QtGui.QColor('grey'))
                    temp_day = temp_last_day_prev_month
                    temp_last_day_prev_month += 1
                elif count >= first_day_index + last_day:
                    item.setForeground(QtGui.QColor('grey'))
                    temp_day = temp_next_month_day
                    temp_next_month_day += 1
                else:
                    if target_day_index == temp_current_month_day:
                        item.setForeground(QtGui.QColor('cyan'))
                    elif count % 7 == 6 or count % 7 == 5:
                        item.setForeground(QtGui.QColor('indianred'))
                    else:
                        item.setForeground(QtGui.QColor(''))
                    temp_day = temp_current_month_day
                    temp_current_month_day += 1
                item.setText(_translate("Form", "{}".format(temp_day)))
                month_buttons_container[count].clear()
                count += 1
        self.monthDisplay.setSortingEnabled(__sortingEnabled)        
    
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
            for arg in result_items:
                label_str = arg[1] + "\n{}[{}] - {}[{}]".format(arg[2], arg[4], arg[3], arg[5])
                item = QtWidgets.QListWidgetItem(label_str)
                item.setData(1, arg[2])
                self.searchResult.addItem(item)
        self.searchResult.setGeometry(QtCore.QRect(30, 40, 245, (num_item * 100)))
    
    def on_search_result_clicked(self, item):
        if item is not None: # handle deleted items
            global today
            temp_str :str = item.data(1)
            data = temp_str.split("-")
            today = today.replace(year=int(data[0]), month=int(data[1]), day=int(data[2]))
            self.move_to_targetdate(today)  
            self.searchBox.clear()        
    
    def item_clicked(self, item):
        if item is not None: # handle deleted items
            # Create an instance of the event creation dialog
            event_dialog = QDialog()
            ui = CreateEventPopup()     
            id = item.data(1)   
            ui.set_up_ui(event_dialog, id)
            event_dialog.exec_() # Show the dialog

    def show_event_dialog(self):
        # Create an instance of the event creation dialog
        event_dialog = QDialog()
        ui = CreateEventPopup()                  
        ui.set_up_ui(event_dialog)
        event_dialog.exec_() # Show the dialog
    
    def show_export_event(self):
        # Create an instance of the event creation dialog
        event_export = QDialog()
        ui = ExportEventPopup()                  
        ui.set_up_ui(event_export)
        event_export.exec_() # Show the dialog

    def on_display_changed(self, index):
        # Set the visibility of the TableWidgets based on the selected text
        objects = [self.dayDisplay, self.weekDisplay, self.monthDisplay]
        for object in objects:
            object.setVisible(False)
        objects[index].setVisible(True)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        for i, view in enumerate(VIEWS):
            self.selectViewBy.setItemText(i, _translate("Form", view))

        for i, searchCat in enumerate([
                "By Title [event name]", 
                "By Start Date [yyyy-mm-dd]", "By End Date [yyyy-mm-dd]", 
                "By Start Time [hh:mm]", "By End Time [hh:mm]"
            ]):
            self.searchBy.setItemText(i, _translate("Form", searchCat))
            
        # Day and Week Display
        target_tables = [self.weekDisplay, self.dayDisplay]
        count = 0
        for i in AM_PM:
            for j in range(1, 13, 1):
                for target_table in target_tables:
                    item = target_table.verticalHeaderItem(count)
                    item.setText(_translate("Form", "{} {}".format(j, i)))
                count += 1
        
        # Day display buttons
        j = 0
        for i in range(HOURS_A_DAY):
            item = QtWidgets.QTableWidgetItem()
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
            self.dayDisplay.setItem(i, j, item)
            # Add list object
            eventList = QtWidgets.QListWidget()
            eventList.setStyleSheet("margin-top: 5px; background-color: transparent;")
            eventList.font().setPointSize(20)
            self.dayDisplay.setCellWidget(i, j, eventList)
            eventList.itemClicked.connect(self.item_clicked)
            day_buttons_container.append(eventList)
        self.dayDisplay.verticalHeader().setDefaultSectionSize(50)

        # Week display buttons
        for i in range(DISPLAY_COL):
            for j in range(HOURS_A_DAY):
                # ROONG TODO here
                pass

        # Month display Buttons
        global month_buttons_container
        for i in range(MONTH_ROW):
            for j in range(MONTH_COL):
                item = QtWidgets.QTableWidgetItem()
                item.setFlags(QtCore.Qt.ItemIsEnabled)
                item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
                self.monthDisplay.setItem(i, j, item)
                # Add list
                eventList = QtWidgets.QListWidget()
                eventList.setStyleSheet("margin-top: 15px; background-color: transparent;")
                self.monthDisplay.setCellWidget(i, j, eventList)
                eventList.itemClicked.connect(self.item_clicked)
                month_buttons_container.append(eventList)

        # Others
        self.nextButton.setText(_translate("Form", ">"))
        self.previousButton.setText(_translate("Form", "<"))
        self.dateSearchButton.setText(_translate("Form", "🔎"))
        self.create_event_button.setText(_translate("Form", "Create"))
        self.searchBox.setPlaceholderText(_translate("Form", "Search Event"))
        self.exportButton.setText(_translate("Form", "Export"))
        self.currentDayLabel.setText(_translate("Form", "{} {} {}"
        .format(today.day, MONTHS[today.month - 1], today.year)))

        # Load all today display
        self.move_to_targetdate(today)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
