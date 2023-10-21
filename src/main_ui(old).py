# main_ui.py
# GUI for the Personal Calendar Application
# Created by Roong, 4th October 2023

from create_event import CreateEventPopup

from calendar import Calendar
from PyQt5.QtWidgets import (
    QApplication,   
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QCalendarWidget,
    QLineEdit,
    QMenu,
    QAction,
    QMessageBox,
    QDialog
)
from PyQt5.QtCore import Qt, QDate
import sys

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Calendar')
        self.setFixedWidth(500)
        self.setFixedHeight(500)
        self.setup_ui()
        self.show()

    def setup_ui(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Create a horizontal layout for the top bar
        top_bar_layout = QHBoxLayout()

        # Create a "Create Event" button
        create_event_button = QPushButton('+ Create', self)


        # Create a search bar
        search_bar = QLineEdit(self)
        search_bar.setPlaceholderText('Search for Events')
        search_bar.setAlignment(Qt.AlignCenter)
        search_bar.setMaximumWidth(200)

        # Add "Create Event" button and search bar to the top bar layout
        top_bar_layout.addWidget(create_event_button)
        top_bar_layout.addWidget(search_bar)  

        # Create a vertical layout for the central widget
        layout = QVBoxLayout(central_widget)

        # Add the top bar layout to the main layout
        layout.addLayout(top_bar_layout)

        # Create a calendar widget
        calendar = QCalendarWidget(self)

        # Set the first day of the week to Monday
        calendar.setFirstDayOfWeek(Qt.Monday)
        
        # Connect the clicked signal to the show_popup slot
        calendar.clicked.connect(self.show_popup)

        # Hide the week numbers
        calendar.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)

        # Add calendar to the main layout
        layout.addWidget(calendar)

        # Set the layout for the central widget
        central_widget.setLayout(layout)

        # Connect the create_event_button clicked signal to the show_event_dialog slot
        create_event_button.clicked.connect(self.show_event_dialog)

    def show_popup(self, date):
        # Create a popup menu
        popup_menu = QMenu(self)

        # Create an action for the popup menu
        popup_action = QAction(f'Popup for {date.toString()}', self)
        popup_action.triggered.connect(lambda: self.popup_message(date))
        popup_menu.addAction(popup_action)

        # Show the popup menu at the cursor position
        pos = self.sender().mapToGlobal(self.sender().pos())
        popup_menu.exec_(pos)

    def popup_message(self, date):
        QMessageBox.information(self, 'Selected Date', f'You clicked on {date.toString()}')        

    def show_event_dialog(self):
        # Create an instance of the event creation dialog
        event_dialog = QDialog()
        ui = CreateEventPopup()                  
        ui.setupUi(event_dialog)

        # Show the dialog
        event_dialog.exec_()

if __name__ == '__main__':
    App = QApplication([])                                               
    cal = MainWindow() 
    sys.exit(App.exec_()) 

    
