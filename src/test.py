import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout

# Built-in
import sys
import datetime
import calendar
# external libraries
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog
import pdb
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
to_edit_event_id = -1


class SimpleUIApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Simple PyQt UI')
        self.setGeometry(100, 100, 400, 200)  # Set the window size (x, y, width, height)

        # Create widgets
        self.label = QLabel('Hello, PyQt!', self)
        self.button = QPushButton('Click me!', self)
        self.button.clicked.connect(self.onButtonClick)  # Connect button click event to a function

        # Set up the layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button)

        # Set the main layout for the window
        self.setLayout(layout)

    def onButtonClick(self):
        self.label.setText('Button Clicked!')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SimpleUIApp()
    window.show()
    sys.exit(app.exec_())
