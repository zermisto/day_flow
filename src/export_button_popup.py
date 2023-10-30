# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Export_Button.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

# export_button_popup.py
# Popup window for export button
# Created by Toiek, 10th October 2023

from PyQt5 import QtCore, QtWidgets
from export_event_class import exportEventClass
from export_events import export_events_to_csv


class ExportEventPopup(object):
    def set_up_ui(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(407, 207)

        self.widget = QtWidgets.QWidget(Dialog)
        self.widget.setGeometry(QtCore.QRect(30, 20, 351, 161))
        self.widget.setObjectName("widget")

        self.export_filename = QtWidgets.QTextEdit(self.widget)
        self.export_filename.setGeometry(QtCore.QRect(0, 0, 351, 31))
        self.export_filename.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.export_filename.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.export_filename.setLineWrapMode(QtWidgets.QTextEdit.FixedPixelWidth)
        self.export_filename.setTabStopWidth(54)
        self.export_filename.setObjectName("ExportFileName")
        

        self.start_date = QtWidgets.QDateEdit(self.widget)
        self.start_date.setGeometry(QtCore.QRect(70, 40, 91, 31))
        self.start_date.setAutoFillBackground(False)
        self.start_date.setDateTime(QtCore.QDateTime.currentDateTime())
        #change format to yyyy-MM-dd
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
        self.ok_button.clicked.connect(lambda: export_events_to_csv(self.get_input_from_user()))


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
        print(export_event_data.filename)
        print(export_event_data.start_date)
        print(export_event_data.end_date)
        return export_event_data

    def retranslate_ui(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.start_date.setDisplayFormat(_translate("Dialog", "yyyy/mm/dd"))
        self.ok_button.setText(_translate("Dialog", "OK"))
        self.cancel_button.setText(_translate("Dialog", "CANCEL"))
        self.label_5.setText(_translate("Dialog", "start_date"))
        self.label_6.setText(_translate("Dialog", "end_date"))
        self.end_date.setDisplayFormat(_translate("Dialog", "yyyy/mm/dd"))
        self.export_filename.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
        "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
        "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.export_filename.setPlaceholderText(_translate("Dialog", "Export File Name"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = ExportEventPopup()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
