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
"""

# Built-in
import sys
import datetime
import calendar
from datetime import datetime as Datetime
# external libraries
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import Qt, QRect
# Our libraries
import Database.sqlite_demo as sqlite
import Shared_Files.search_engine as search_engine
from Export_Event.export_button_popup import ExportEventPopup
from create_event_popup import CreateEventPopup

# Constant
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

current_time = Datetime.now()
month_index = today.month
first_day_index = today.replace(day=1).weekday()
to_edit_event_id = -1

#build the table if it doesn't exist
sqlite.build_table()

"""
Main class consists of all ui components in the main page
,for example, the search box, the date label, create event button
etc.
"""
class Ui_Form(object):
    """
    Create a blank UI components initialize objects
    arguments:
        Form is the main widget
    """
    def setup_Ui(self, Form):
        Form.setObjectName("Form")
        Form.setFixedSize(757, 654)

        # Initialize containers
        self.month_lists_container: list = []
        self.week_lists_container: list = []
        self.day_lists_container: list = []

        # Initialize widget
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setEnabled(True)
        self.widget.setGeometry(QRect(20, 60, 711, 591))
        self.widget.setObjectName("widget")

        # Select view by day week or month buttons
        self.view_by = QtWidgets.QComboBox(self.widget)
        self.view_by.setEnabled(True)
        self.view_by.setGeometry(QRect(10, 10, 111, 26))
        self.view_by.setToolTipDuration(0)
        self.view_by.setObjectName("select_view")
        for i in range(3):
            self.view_by.addItem("")

        # Current date button
        self.date_edit = QtWidgets.QDateEdit(self.widget)
        self.date_edit.setEnabled(True)
        self.date_edit.setDisplayFormat("yyyy-MM-dd")
        self.date_edit.setGeometry(QRect(290, 0, 131, 31))
        self.date_edit.setMouseTracking(False)
        self.date_edit.setTabletTracking(False)
        self.date_edit.setAcceptDrops(False)
        self.date_edit.setProperty("show_group_separator", False)
        self.date_edit.setObjectName("dateEdit")

        # Month frame
        self.month_display = QtWidgets.QTableWidget(self.widget)
        self.month_display.setEnabled(True)
        self.month_display.setGeometry(QRect(10, 40, 701, 521))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.month_display.setFont(font)
        self.month_display.setAutoScrollMargin(16)
        self.month_display.setRowCount(MONTH_ROW)
        self.month_display.setObjectName("month_widget")
        self.month_display.setColumnCount(MONTH_COL)
        for i in range(MONTH_ROW):
            item = QtWidgets.QTableWidgetItem()
            item.setTextAlignment(Qt.AlignCenter)
            self.month_display.setVerticalHeaderItem(i, item)
        for i in range(MONTH_COL):
            item = QtWidgets.QTableWidgetItem()
            self.month_display.setHorizontalHeaderItem(i, item)
        self.month_display.horizontalHeader().setVisible(True)
        self.month_display.horizontalHeader().setCascadingSectionResizes(True)
        self.month_display.horizontalHeader().setDefaultSectionSize(100)
        self.month_display.horizontalHeader().setMinimumSectionSize(0)
        self.month_display.verticalHeader().setDefaultSectionSize(80)
        self.month_display.verticalHeader().setMinimumSectionSize(0)

        # Day frame
        self.day_display = QtWidgets.QTableWidget(self.widget)
        self.day_display.setGeometry(QRect(10, 40, 701, 531))
        self.day_display.setObjectName("day_widget")
        self.day_display.setColumnCount(1)
        self.day_display.setRowCount(HOURS_A_DAY)
        self.day_display.horizontalHeader().setDefaultSectionSize(701 - 45)

        # Week frame
        self.week_display = QtWidgets.QTableWidget(self.widget)
        self.week_display.setGeometry(QRect(10, 40, 701, 531))
        self.week_display.setObjectName("week_widget")
        self.week_display.setColumnCount(MONTH_COL)
        self.week_display.setRowCount(HOURS_A_DAY)
        self.week_display.setVisible(False)

        for i in range(DISPLAY_COL):
            item = QtWidgets.QTableWidgetItem()
            self.week_display.setHorizontalHeaderItem(i, item)

        # Initialize all week and day vertical header
        count = 0
        for _ in AM_PM:
            for _ in range(1, 13, 1):
                item = QtWidgets.QTableWidgetItem()
                self.day_display.setVerticalHeaderItem(count, item)
                self.week_display.setVerticalHeaderItem(count, item)
                count += 1

        # Set selection mode to NoSelection for week and day headers
        for item in ([self.day_display, self.week_display]):
            no_selection_attr = QtWidgets.QAbstractItemView.NoSelection
            item.setSelectionMode(no_selection_attr)
            item.horizontalHeader().setSelectionMode(no_selection_attr)
            item.verticalHeader().setSelectionMode(no_selection_attr)

        # Date search button
        self.date_search_button = QtWidgets.QPushButton(self.widget)
        self.date_search_button.setGeometry(QRect(418, 0, 40, 33))
        self.date_search_button.setObjectName("date_search_button")
        self.date_search_button.clicked.connect(self.enter_date)

        # Next time frame button
        self.next_button = QtWidgets.QPushButton(self.widget)
        self.next_button.setGeometry(QRect(450, 0, 51, 33))
        self.next_button.setObjectName("next_button")
        self.next_button.clicked.connect(self.move_next_frame)

        # Previous time frame button
        self.previous_button = QtWidgets.QPushButton(self.widget)
        self.previous_button.setGeometry(QRect(240, 0, 51, 33))
        self.previous_button.setObjectName("previous_button")
        self.previous_button.clicked.connect(self.move_prev_frame)

        # Create button
        self.create_event_button = QtWidgets.QPushButton(Form)
        self.create_event_button.setGeometry(QRect(255, 10, 81, 33))
        self.create_event_button.setObjectName("create_event")
        self.create_event_button.clicked.connect(self.show_event_dialog)

        # Search text box
        self.search_box = QtWidgets.QLineEdit(Form)
        self.search_box.setGeometry(QRect(15, 10, 245, 31))
        self.search_box.setText("")
        self.search_box.setObjectName("search_box")
        self.search_box.setMaxLength(100)
        self.search_box.textChanged.connect(self.on_text_changed)

        # Search type dropdown menu
        self.search_by = QtWidgets.QComboBox(Form)
        self.search_by.setEnabled(True)
        self.search_by.setGeometry(QRect(15, 40, 245, 20))
        self.search_by.setToolTipDuration(0)
        self.search_by.setObjectName("search_by")
        for i in range(5):
            self.search_by.addItem("")

        # Export button
        self.export_button = QtWidgets.QPushButton(Form)
        self.export_button.setGeometry(QRect(640, 10, 100, 33))
        self.export_button.setObjectName("export_button")
        self.export_button.clicked.connect(self.show_export_event)

        # Current day label
        self.current_day_label = QtWidgets.QLabel(Form)
        self.current_day_label.setGeometry(QRect(380, 10, 241, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.current_day_label.setFont(font)
        self.current_day_label.setObjectName("current_day_label")

        # Search result list
        self.search_result = QtWidgets.QListWidget(Form)
        self.search_result.setGeometry(QRect(20, 40, 245, 0))
        self.search_result.setObjectName("searchResult")
        self.search_result.itemClicked.connect(self.on_search_result_clicked)
        self.view_by.currentIndexChanged.connect(self.change_display)

        self.change_display(0)
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    """
    Move the the current date which will
    refresh all displays and replace it with a updated one
    arguments:
        input_date is the target date
    """
    def move_to_targetdate(self, input_date: datetime.date):
        # Refresh all frames
        self.refresh_day_display(today)
        self.refresh_week_display(today)
        self.refresh_month_display(today)
        year = today.year
        month = today.month
        day = today.day
        self.date_edit.setDate(QtCore.QDate(year, month, day))

        # Update day display
        start_date = input_date.strftime('%Y-%m-%d')
        events_a_day = search_engine.event_range_search(start_date, start_date)
        for event in events_a_day:
            start_time = int(event[4].split(":")[0])
            end_time = int(event[5].split(":")[0])
            for i in range(start_time, end_time + 1):
                item_label = str(event[1]) + " \t[" + str(event[4])
                item_label += "-" + str((event[5])) + " ]\t" + str(event[6])
                item = QtWidgets.QListWidgetItem(item_label)
                item.setData(1, event[0])
                self.day_lists_container[i].addItem(item)

        # Update week display
        start_date = input_date.strftime('%Y-%m-%d')
        temp_date = input_date + datetime.timedelta(days=DISPLAY_COL - 1)
        end_date = temp_date.strftime('%Y-%m-%d')
        events_a_week = search_engine.event_range_search(start_date, end_date)

        # Add item in the list in each week cells
        for event in events_a_week:
            event_start_date = Datetime.strptime(event[2], "%Y-%m-%d").date()
            event_end_date = Datetime.strptime(event[3], "%Y-%m-%d").date()
            event_start_time = Datetime.strptime(event[4], "%H:%M").time()
            event_end_time = Datetime.strptime(event[5], "%H:%M").time()
            for i in range(DISPLAY_COL):
                current_cell_date = input_date + datetime.timedelta(days=i)
                if event_start_date <= current_cell_date <= event_end_date:
                    start_hour = event_start_time.hour
                    end_hour = event_end_time.hour + 1
                    for j in range(start_hour, end_hour):
                        item_label = f"{event[1]}"
                        item = QtWidgets.QListWidgetItem(item_label)
                        item.setData(1, event[0])
                        temp_index = j + i * HOURS_A_DAY
                        temp_list = self.week_lists_container[temp_index]
                        temp_list.addItem(item)

        # Update month display
        month_range = calendar.monthrange(input_date.year, today.month)
        last_day = month_range[1]
        start_date = input_date.strftime('%Y-%m-01')
        end_date = input_date.strftime('%Y-%m-'+str(last_day))
        events_a_month = search_engine.event_range_search(start_date, end_date)
        first_date = input_date.replace(day=1, month=input_date.month)
        first_day_index = first_date.weekday()

        # Add item in the list in each month cells
        for event in events_a_month:
            temp_y_m_d = event[2].split("-")
            temp_key = int(temp_y_m_d[2]) - 1 + first_day_index
            item = QtWidgets.QListWidgetItem(event[1])
            item.setData(1, event[0])
            self.month_lists_container[temp_key].addItem(item)

    """
    Change the date in date edit box
    on the top of the widget
    """
    def enter_date(self):
        global today
        date = self.date_edit.date()
        temp_year = date.year()
        temp_month = date.month()
        temp_day = date.day()
        today = today.replace(year=temp_year, month=temp_month, day=temp_day)
        self.move_to_targetdate(today)

    """
    Change the display to the next frame
    which detemine by the current display type
    """
    def move_next_frame(self):
        global today
        day_step_size = FRAME_STEPSIZE[self.view_by.currentIndex()]
        new_date = today + datetime.timedelta(days=day_step_size)
        today = new_date
        self.move_to_targetdate(today)

    """
    Change the display to the previous frame
    which detemine by the current display type
    """
    def move_prev_frame(self):
        global today
        day_step_size = FRAME_STEPSIZE[self.view_by.currentIndex()]
        new_date = today - datetime.timedelta(days=day_step_size)
        today = new_date
        self.move_to_targetdate(today)

    """
    Refresh the day display frame
    aguments:
        target_date is the target date
    """
    def refresh_day_display(self, target_date):
        day = target_date.day
        day_text = "{} {}".format(DAYS_A_WEEK[target_date.weekday()], day)
        header_item = QtWidgets.QTableWidgetItem(day_text)
        self.day_display.setHorizontalHeaderItem(0, header_item)
        for i in range(HOURS_A_DAY):    # Clear all items in list
            self.day_lists_container[i].clear()

    """
    Refresh the week display frame
    arguments:
        target_date is the target date
    """
    def refresh_week_display(self, target_date):
        for i, day in enumerate(DAYS_A_WEEK):
            last_week_day = (target_date + datetime.timedelta(days=i)).day
            day_text = "{} {}".format(day, last_week_day)
            header_item = QtWidgets.QTableWidgetItem(day_text)
            self.week_display.setHorizontalHeaderItem(i, header_item)

        count = 0
        for i in range(DISPLAY_COL):        # Clear all items in the list
            for _ in range(HOURS_A_DAY):
                self.week_lists_container[count].clear()
                count += 1

    """
    Refresh the month display frame
    arguments:
        target_date is the target date
    """
    def refresh_month_display(self, target_day: datetime.date):
        _translate = QtCore.QCoreApplication.translate
        self.month_display.setSortingEnabled(False)
        # set header columns
        for i, day in enumerate(DAYS_A_WEEK):
            item = self.month_display.horizontalHeaderItem(i)
            item.setText(_translate("Form", day))
        __sortingEnabled = self.month_display.isSortingEnabled()
        # Add decoration and date label
        temp_year = target_day.year
        first_day_index = target_day.replace(temp_year, day=1).weekday()
        temp_day = 0
        temp_current_month_day = 1
        temp_next_month_day = 1
        target_day_index = target_day.day
        target_month_index = (target_day.month - 2) % 12
        prev_range = calendar.monthrange(temp_year, target_month_index + 1)
        last_day_prev_month = prev_range[1]
        last_day = calendar.monthrange(temp_year, target_day.month)[1]
        temp_last_day_prev_month = last_day_prev_month - first_day_index + 1
        count = 0
        for i in range(MONTH_ROW):
            for j in range(MONTH_COL):
                item = self.month_display.item(i, j)
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
                self.month_lists_container[count].clear()
                count += 1
        self.month_display.setSortingEnabled(__sortingEnabled)

    """
    Get the search result to show in the search result frame
    """
    def on_text_changed(self):
        self.search_result.clear()
        num_item = 0
        result_items = []
        search_text = self.search_box.text().strip()
        search_types = search_engine.search_types
        if not search_text:
            num_item = 0
        else:
            selected_index = self.search_by.currentIndex()
            search_type = search_types[selected_index]
            result_items = search_engine.event_search(search_text, search_type)
            num_item = len(result_items)
            for arg in result_items:
                label_str = arg[1] + "\n{}[{}] - {}[{}]".format(
                    arg[2], arg[4], arg[3], arg[5]
                )
                item = QtWidgets.QListWidgetItem(label_str)
                item.setData(1, arg[2])
                self.search_result.addItem(item)
        self.search_result.setGeometry(QRect(30, 40, 245, (num_item * 100)))

    """
    Move to the target frame when the
    result item in the search frame has been clicked
    arguments:
        item is the list item object
    """
    def on_search_result_clicked(self, item):
        if item is not None: # handle deleted items
            global today
            temp_str: str = item.data(1)
            data = temp_str.split("-")
            temp_year = int(data[0])
            temp_month = int(data[1])
            temp_day = int(data[2])
            today = today.replace(
                year=temp_year, month=temp_month, day=temp_day
            )
            self.move_to_targetdate(today)
            self.search_box.clear()
    
    """
    Move to the target frame when the
    event item in the search frame has been clicked
    arguments:
        item is the list item object 
    """
    def item_clicked(self, item):
        if item is not None: # handle deleted items
            # Create an instance of the event creation dialog
            event_dialog = QDialog()
            ui = CreateEventPopup()     
            id = item.data(1)   
            ui.set_up_ui(event_dialog, id)
            update_func = lambda: self.move_to_targetdate(today)
            event_dialog.accepted.connect(update_func)
            event_dialog.rejected.connect(update_func)
            event_dialog.exec_() # Show the dialog
   
    """
    Display the create event popup UI
    """
    def show_event_dialog(self):
        # Create an instance of the event creation dialog
        event_dialog = QDialog()
        ui = CreateEventPopup()                  
        ui.set_up_ui(event_dialog)
        event_dialog.accepted.connect(lambda: self.move_to_targetdate(today))
        event_dialog.rejected.connect(lambda: self.move_to_targetdate(today))
        event_dialog.exec_() # Show the dialog
    
    """
    Display the export event popup UI
    """
    def show_export_event(self):
        # Create an instance of the event creation dialog
        event_export = QDialog()
        ui = ExportEventPopup()                  
        ui.set_up_ui(event_export)
        event_export.exec_() # Show the dialog

    """
    Change the calendar display by the selected display type
    """
    def change_display(self, index):
        # Set the visibility of the TableWidgets based on the selected text
        objects = [self.day_display, self.week_display, self.month_display]
        for object in objects:
            object.setVisible(False)
        objects[index].setVisible(True)

    """ 
    Retranslate UI
    Sets initialize the properties of the UI including
    text title and so on
    arguments:
        Form    - the popup window
    """
    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Day Flow"))
        for i, view in enumerate(VIEWS):
            self.view_by.setItemText(i, _translate("Form", view))
        for i, searchCat in enumerate([
                "By Title [event name]", 
                "By Start Date [yyyy-mm-dd]", "By End Date [yyyy-mm-dd]", 
                "By Start Time [hh:mm]", "By End Time [hh:mm]"
            ]):
            self.search_by.setItemText(i, _translate("Form", searchCat))
            
        # Day and Week Display
        target_tables = [self.week_display, self.day_display]
        count = 0
        for i in AM_PM:
            for j in range(0, 12, 1):
                for target_table in target_tables:
                    item = target_table.verticalHeaderItem(count)
                    item.setText(_translate("Form", "{} {}".format(j, i)))
                    if count == 0:
                        item.setText(_translate("Form", "{}".format("GMT +7")))
                count += 1

        # Day display buttons
        j = 0
        for i in range(HOURS_A_DAY):
            item = QtWidgets.QTableWidgetItem()
            item.setFlags(Qt.ItemIsEnabled)
            item.setTextAlignment(Qt.AlignHCenter|Qt.AlignTop)
            self.day_display.setItem(i, j, item)
            # Add list object
            eventList = QtWidgets.QListWidget()
            temp_style = "margin-top: 5px; background-color: transparent;"
            eventList.setStyleSheet(temp_style)
            eventList.font().setPointSize(20)
            self.day_display.setCellWidget(i, j, eventList)
            eventList.itemClicked.connect(self.item_clicked)
            self.day_lists_container.append(eventList)
        self.day_display.verticalHeader().setDefaultSectionSize(50)

        # Week display buttons
        for i in range(DISPLAY_COL):
            for j in range(HOURS_A_DAY):
                item = QtWidgets.QTableWidgetItem() 
                item.setFlags(Qt.ItemIsEnabled)
                item.setTextAlignment(Qt.AlignHCenter|Qt.AlignTop)
                self.week_display.setItem(j, i, item)
                # Add list object
                eventList = QtWidgets.QListWidget()
                temp_style = "margin-top: 5px; background-color: transparent;"
                eventList.setStyleSheet(temp_style)
                eventList.font().setPointSize(20)
                self.week_display.setCellWidget(j, i, eventList)
                eventList.itemClicked.connect(self.item_clicked)
                self.week_lists_container.append(eventList)
        self.week_display.verticalHeader().setDefaultSectionSize(50)

        # Month display Buttons
        for i in range(MONTH_ROW):
            for j in range(MONTH_COL):
                item = QtWidgets.QTableWidgetItem()
                item.setFlags(Qt.ItemIsEnabled)
                item.setTextAlignment(Qt.AlignHCenter|Qt.AlignTop)
                self.month_display.setItem(i, j, item)
                # Add list
                eventList = QtWidgets.QListWidget()
                temp_style = "margin-top: 23px; background-color: transparent;"
                eventList.setStyleSheet(temp_style)
                self.month_display.setCellWidget(i, j, eventList)
                eventList.itemClicked.connect(self.item_clicked)
                self.month_lists_container.append(eventList)

        # Others
        self.next_button.setText(_translate("Form", ">"))
        self.previous_button.setText(_translate("Form", "<"))
        self.date_search_button.setText(_translate("Form", "🔎"))
        self.create_event_button.setText(_translate("Form", "Create"))
        self.search_box.setPlaceholderText(_translate("Form", "Search Event"))
        self.export_button.setText(_translate("Form", "Export"))
        self.current_day_label.setText(_translate("Form", "Today is {} {} {}"
        .format(today.day, MONTHS[today.month - 1], today.year)))

        # Load all today display
        self.move_to_targetdate(today)

    """
    To clear all event listener item form the list
    and close the data base related variables
    """
    def clear_buttons_lists(self):
        self.month_lists_container.clear()
        self.week_lists_container.clear()
        self.day_lists_container.clear()   
        sqlite.close_all()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_widget = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setup_Ui(main_widget)
    main_widget.show()
    app.aboutToQuit.connect(ui.clear_buttons_lists)
    sys.exit(app.exec_())
