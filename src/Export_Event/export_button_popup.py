# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Export_Button.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

"""
export_button_popup.py

Popup window for export button
Created by Toiek, 10th October 2023
"""

from PyQt5 import QtCore, QtWidgets
from Shared_Files.Classes.all_classes import exportEventClass
from Export_Event.export_events import export_events_to_csv
from Shared_Files.user_input_validation import check_char_limit, check_valid_input, check_start_end_date


class ExportEventPopup(object):
    def set_up_ui(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(407, 207)

        self.widget = QtWidgets.QWidget(Dialog)
        self.widget.setGeometry(QtCore.QRect(30, 20, 351, 161))
        self.widget.setObjectName("widget")

        self.export_filename = QtWidgets.QTextEdit(self.widget)
        self.export_filename.setGeometry(QtCore.QRect(0, 0, 351, 31))
        self.export_filename.setObjectName("ExportFileName")
        self.export_filename.textChanged.connect(
            lambda: check_char_limit(self.export_filename, 25))

        self.start_date = QtWidgets.QDateEdit(self.widget)
        self.start_date.setGeometry(QtCore.QRect(70, 40, 91, 31))
        self.start_date.setAutoFillBackground(False)
        self.start_date.setDateTime(QtCore.QDateTime.currentDateTime())
        self.start_date.setDisplayFormat("yyyy-MM-dd")
        self.start_date.setObjectName("startDate")

        self.label_5 = QtWidgets.QLabel(self.widget)
        self.label_5.setGeometry(QtCore.QRect(10, 40, 61, 30))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.widget)
        self.label_6.setGeometry(QtCore.QRect(180, 40, 61, 30))
        self.label_6.setObjectName("label_6")

        self.end_date = QtWidgets.QDateEdit(self.widget)
        self.end_date.setGeometry(QtCore.QRect(250, 40, 91, 31))
        self.end_date.setAutoFillBackground(False)
        self.end_date.setDateTime(QtCore.QDateTime.currentDateTime())
        self.end_date.setDisplayFormat("yyyy-MM-dd")
        self.end_date.setObjectName("EndDate")

        self.ok_button = QtWidgets.QPushButton(self.widget)
        self.ok_button.setGeometry(QtCore.QRect(60, 100, 93, 28))
        self.ok_button.setObjectName("OkButton")

        def on_ok_button_clicked():
            if check_valid_input(self.export_filename):
                if check_start_end_date(self.start_date.date(), self.end_date.date()) == True:
                    export_events_to_csv(self.get_input_from_user())
                    Dialog.close()

        # Connect the OK button click event to the slot
        self.ok_button.clicked.connect(on_ok_button_clicked)

        #  Cancel button
        self.cancel_button = QtWidgets.QPushButton(self.widget)
        self.cancel_button.setGeometry(QtCore.QRect(210, 100, 93, 28))
        self.cancel_button.setObjectName("CancelButton")
        self.cancel_button.clicked.connect(Dialog.close)

        self.retranslate_ui(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def get_input_from_user(self):
        filename = self.export_filename.toPlainText()
        start_date = self.start_date.text()
        end_date = self.end_date.text()
        export_event_data = exportEventClass(filename, start_date, end_date)
        return export_event_data

    def retranslate_ui(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.start_date.setDisplayFormat(_translate("Dialog", "yyyy-MM-dd"))
        self.ok_button.setText(_translate("Dialog", "OK"))
        self.cancel_button.setText(_translate("Dialog", "CANCEL"))
        self.label_5.setText(_translate("Dialog", "start_date"))
        self.label_6.setText(_translate("Dialog", "end_date"))
        self.end_date.setDisplayFormat(_translate("Dialog", "yyyy-MM-dd"))
        self.export_filename.setPlaceholderText(
            _translate("Dialog", "file-name or file_name"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = ExportEventPopup()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
