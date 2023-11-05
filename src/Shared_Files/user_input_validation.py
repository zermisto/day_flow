"""
user_input_validation.py

Contains all functions for validating user input

Created by King, 31th October 2023
"""

from PyQt5 import QtCore, QtWidgets

# Check Character Limit
# Checks the character limit of the text in the QTextEdit


def check_char_limit(text_name, char_limit):
    if len(text_name.toPlainText()) > char_limit:
        text_name.setStyleSheet("color: red")  # Set the text color to red

        # Get the current text from the QTextEdit
        text = text_name.toPlainText()
        text = text[:char_limit]  # Cut off at 300 characters
        text_name.setPlainText(text)  # Reset text

        # Reset the cursor to the end position
        cursor = text_name.textCursor()
        cursor.setPosition(text_name.document().characterCount() - 1)
        text_name.setTextCursor(cursor)

    elif len(text_name.toPlainText()) < char_limit:
        text_name.setStyleSheet("color: black")  # Set the text color to black

# Check Valid Input
# Checks if the user input is valid


def check_valid_input(text_name):
    name = text_name.toPlainText()
    if name == "":
        # create a messabge box pop up
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle("Error")
        msg.setText("Please fill in all the fields")
        msg.setIcon(QtWidgets.QMessageBox.Warning)
        msg.exec_()
        return False
    elif any(not c.isalnum() and c not in ('-', '_') for c in name):
        # Check for non-alphanumeric characters in the event title
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle("Error")
        msg.setText("Event title contains non-alphanumeric characters")
        msg.setIcon(QtWidgets.QMessageBox.Warning)
        msg.exec_()
        return False
    else:
        return True

### For export_button_popup.py ###

# Check start date and end date
# Checks if the start date is before the end date (valid)


def check_start_end_date(start_date, end_date):
    if start_date > end_date:
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle("Error")
        msg.setText("Start date cannot be later than end date.")
        msg.setIcon(QtWidgets.QMessageBox.Warning)
        msg.exec_()
        return False

    else:
        return True

# Check event timeframe
# Checks if there are events within the specified date range


def check_event_timeframe(selected_events):
    if not selected_events:  # if selected_events is empty
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle("Error")
        msg.setText("No events found within the specified date range.")
        msg.setIcon(QtWidgets.QMessageBox.Warning)
        msg.exec_()
        return False
    else:
        return True
