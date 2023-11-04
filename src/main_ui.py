import sys
from Export_Event.export_button_popup import ExportEventPopup
import Shared_Files.search_engine as search_engine
from create_event_popup import CreateEventPopup
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog
import datetime
import calendar
import math

am_pm = ["AM", "PM"]
days_in_week = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]
months = [
    'January', 'February', 'March', 'April', 
    'May', 'June', 'July', 'August', 
    'September', 'October', 'November', 'December'
]
select_view_list = [1, 7, 30]
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

        # Set item flags to make items non-editable
        def set_non_editable_items(table_widget):
            for i in range(table_widget.rowCount()):
                item = QtWidgets.QTableWidgetItem()
                item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)
                table_widget.setItem(i, 0, item)

        # Set item flags to make items non-editable
        set_non_editable_items(self.weekDisplay)

        # Set selection mode to NoSelection for both headers
        self.weekDisplay.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.weekDisplay.horizontalHeader().setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.weekDisplay.verticalHeader().setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        
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

        # Set item flags to make items non-editable
        set_non_editable_items(self.dayDisplay)

        # Set selection mode to NoSelection for both headers
        self.dayDisplay.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.dayDisplay.horizontalHeader().setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.dayDisplay.verticalHeader().setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)

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

    def refresh_month_display(self, target_day : datetime.date):
        _translate = QtCore.QCoreApplication.translate
        self.monthDisplay.setSortingEnabled(False)
        # set header columns
        for i, day in enumerate(days_in_week):
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
        for i in range(num_month_row):
            for j in range(num_month_column):
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
                        item.setForeground(QtGui.QColor('black'))
                    temp_day = temp_current_month_day
                    temp_current_month_day += 1
                item.setText(_translate("Form", "{}".format(temp_day)))
                month_buttons_container[count].setText("")
                count += 1
        self.monthDisplay.setSortingEnabled(__sortingEnabled)

    def refresh_date_textbox(self, target_day, target_month, target_year):
        self.dateEdit.setDate(QtCore.QDate(target_year, target_month, target_day))

    def move_to_targetdate(self, input_date : datetime.date):
        # Update dateEdit box
        self.refresh_date_textbox(today.day, today.month, today.year)
        # Update day display
        self.update_day_header(today)
        # Update week display
        self.update_week_header(today)
        # Update month display
        self.refresh_month_display(today)
        month = input_date.month
        year = input_date.year
        start_date = str(year) + "-" + str(month) +  "-" + "1"
        end_date = str(year) + "-" + str(month) + "-" + str(month - 1)
        events_in_month = {}
        events_in_month = search_engine.event_range_search(start_date, end_date)
        first_day_index = input_date.replace(day=1, month=month_index).weekday()

        # Update day display
        start_date = str(2000) + "-" + str(month) +  "-" + "1"
        end_date = str(3000) + "-" + str(month) + "-" + str(month - 1)
        events_in_day = {}
        events_in_day = search_engine.event_range_search(start_date, end_date)
        print(events_in_day, "events in day")

        # Set column header text
        today_column_text = "{} {}".format(days_in_week[today_index], today.day)
        header_item = QtWidgets.QTableWidgetItem(today_column_text)
        self.dayDisplay.setHorizontalHeaderItem(0, header_item)

        # Clear all cells in the day display
        for row in range(self.dayDisplay.rowCount()):
            item = self.dayDisplay.item(row, 0)
            item.setText("")
            item.setForeground(QtGui.QColor('black'))

        for event in events_in_day:
            event_name = event[1]
            start_date_str = event[2]
            end_date_str = event[3]
            start_time_str = event[4]
            end_time_str = event[5]

            # print(event_name, start_date_str, end_date_str, start_time_str, end_time_str)
            startD = start_date_str.split(" ")[0]
            year, month, day = startD.split("-")
            print(year, month, day)
            
            # Check if the event is on the target day
            if start_date_str == end_date_str:
                if start_date_str == str(today.year) + "-" + str(today.month).zfill(2) + "-" + str(today.day).zfill(2):
                    # Extract hours from the datetime strings
                    start_hour = math.ceil(float(start_time_str.split(':')[0]))
                    end_hour = math.ceil(float(end_time_str.split(':')[0]))

                    # Ensure the indices are within the valid range (0 to 23)
                    start_index = start_hour % 24
                    end_index = end_hour % 24

                    # Update cells in the day display based on day_dict keys
                    for index in range(start_index, end_index):
                        indicies = index
                        print(indicies)
                        item = self.dayDisplay.item(indicies, 0)
                        item.setText(event_name)
                        item.setForeground(QtGui.QColor('green'))  # Set the text color to green
            else:
                if start_date_str == str(today.year) + "-" + str(today.month).zfill(2) + "-" + str(today.day).zfill(2):
                    # Extract hours from the datetime strings
                    start_hour = math.ceil(float(start_time_str.split(':')[0]))
                    end_hour = math.ceil(float(end_time_str.split(':')[0]))

                    # Ensure the indices are within the valid range (0 to 23)
                    start_index = start_hour % 24
                    end_index = end_hour % 24

                    # Update cells in the day display based on day_dict keys
                    for index in range(start_index, end_index):
                        indicies = index
                        print(indicies)
                        item = self.dayDisplay.item(indicies, 0)
                        item.setText(event_name)
                        item.setForeground(QtGui.QColor('green'))  # Set the text color to green

                if end_date_str == str(today.year) + "-" + str(today.month).zfill(2) + "-" + str(today.day).zfill(2):
                    # Extract hours from the datetime strings
                    start_hour = math.ceil(float(start_time_str.split(':')[0]))
                    end_hour = math.ceil(float(end_time_str.split(':')[0]))

                    # Ensure the indices are within the valid range (0 to 23)
                    start_index = start_hour % 24
                    end_index = end_hour % 24

                    # Update cells in the day display based on day_dict keys
                    for index in range(start_index, end_index):
                        indicies = index
                        print(indicies)
                        item = self.dayDisplay.item(indicies, 0)
                        item.setText(event_name)
                        item.setForeground(QtGui.QColor('green'))  # Set the text color to green

            for event in events_in_day:
                event_name = event[1]
                start_date_str = event[2]
                end_date_str = event[3]
                start_time_str = event[4]
                end_time_str = event[5]

                # print(event_name, start_date_str, end_date_str, start_time_str, end_time_str)
                startD = start_date_str.split(" ")[0]
                year, month, day = startD.split("-")
                print(year, month, day)

                # Iterate over the days of the week
                for i, weekday in enumerate(days_in_week):
                    # Calculate the date for the current day in the week
                    current_date = today + datetime.timedelta(days=i)

                    # Check if the event falls on the current day
                    if (
                        current_date.year == int(year)
                        and current_date.month == int(month)
                        and current_date.day == int(day)
                    ):
                        # Extract hours from the datetime strings
                        start_hour = math.ceil(float(start_time_str.split(':')[0]))
                        end_hour = math.ceil(float(end_time_str.split(':')[0]))

                        # Ensure the indices are within the valid range (0 to 23)
                        start_index = start_hour % 24
                        end_index = end_hour % 24

                        # Initialize items in the week display if not already initialized
                        for row in range(self.weekDisplay.rowCount()):
                            if self.weekDisplay.item(row, i) is None:
                                item = QtWidgets.QTableWidgetItem()
                                self.weekDisplay.setItem(row, i, item)

                        # Update cells in the week display based on the day_dict keys
                        for index in range(start_index, end_index):
                            indicies = index
                            print(indicies)
                            item = self.weekDisplay.item(indicies, i)
                            item.setText(event_name)
                            item.setForeground(QtGui.QColor('green'))  # Set the text color to green


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
            step_size = 1
            if recurring_pattern == 'W':
                step_size = 7
            for i in range(1, recurring_count, step_size):
                cursor = (step_size * i) + temp_key 
                if cursor <= num_month_column * num_month_row:
                    add_event_to_dict(cursor, temp_value)
                else:
                    break
            
        # Display in the all events and place in the frame
        for key in day_dict:
            month_buttons_container[key].setText(day_dict[key])
    
    def enter_date(self):
        global today
        date = self.dateEdit.date()
        today = today.replace(year=date.year(), month=date.month(), day=date.day())
        self.move_to_targetdate(today)
                
    def move_next_frame(self):
        global today
        day_step_size = select_view_list[self.selectViewBy.currentIndex()]
        new_date = today + datetime.timedelta(days=day_step_size)
        today = new_date
        self.move_to_targetdate(today)

    def move_prev_frame(self):
        global today
        day_step_size = select_view_list[self.selectViewBy.currentIndex()]
        new_date = today - datetime.timedelta(days=day_step_size)
        today = new_date
        self.move_to_targetdate(today)

    def update_day_header(self, target_date):
        day_text = "{} {}".format(days_in_week[target_date.weekday()], target_date.day)
        header_item = QtWidgets.QTableWidgetItem(day_text)
        self.dayDisplay.setHorizontalHeaderItem(0, header_item)

    def update_week_header(self, target_date):
        for i, day in enumerate(days_in_week):
            day_text = "{} {}".format(day, target_date.day + i)
            header_item = QtWidgets.QTableWidgetItem(day_text)
            self.weekDisplay.setHorizontalHeaderItem(i, header_item)
        
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
        if item is not None:
            global today
            temp_str :str = item.data(1)
            data = temp_str.split("-")
            today = today.replace(year=int(data[0]), month=int(data[1]), day=int(data[2]))
            self.move_to_targetdate(today)  
            self.searchBox.clear()        
                
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
        self.dateSearchButton.setText(_translate("Form", "🔎"))
        # Reset date edit configure
        self.refresh_date_textbox(today.day, today.month, today.year)

        # Reset month configure
        self.refresh_month_display(today)

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
        self.move_to_targetdate(today)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
