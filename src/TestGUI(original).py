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


from PyQt5 import QtCore, QtGui, QtWidgets 

class Ui_Form(object): 
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(757, 654)
        self.widget = QtWidgets.QWidget(Form) # Create a widget for the ComboBox and TableWidgets
        self.widget.setEnabled(True)
        self.widget.setGeometry(QtCore.QRect(20, 60, 711, 551))
        self.widget.setObjectName("widget")
        self.comboBox = QtWidgets.QComboBox(self.widget)
        self.comboBox.setEnabled(True)
        self.comboBox.setGeometry(QtCore.QRect(10, 10, 111, 26))
        self.comboBox.setToolTipDuration(0)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.dateEdit = QtWidgets.QDateEdit(self.widget) # Create a DateEdit widget
        self.dateEdit.setEnabled(False)
        self.dateEdit.setGeometry(QtCore.QRect(290, 0, 131, 31))
        self.dateEdit.setMouseTracking(False)
        self.dateEdit.setTabletTracking(False)
        self.dateEdit.setAcceptDrops(False)
        self.dateEdit.setProperty("showGroupSeparator", False)
        self.dateEdit.setObjectName("dateEdit")
        self.pushButton_3 = QtWidgets.QPushButton(self.widget)
        self.pushButton_3.setGeometry(QtCore.QRect(420, 0, 51, 33))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(self.widget)
        self.pushButton_4.setGeometry(QtCore.QRect(240, 0, 51, 33))
        self.pushButton_4.setObjectName("pushButton_4")
        self.tableWidget = QtWidgets.QTableWidget(self.widget)
        self.tableWidget.setEnabled(True)
        self.tableWidget.setGeometry(QtCore.QRect(10, 40, 701, 501))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.tableWidget.setFont(font)
        self.tableWidget.setAutoScrollMargin(16)
        self.tableWidget.setRowCount(5)
        self.tableWidget.setObjectName("Month Widget")
        self.tableWidget.setColumnCount(7)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.tableWidget.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.tableWidget.setItem(0, 1, item)
        self.tableWidget.horizontalHeader().setVisible(True)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(True)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(100)
        self.tableWidget.horizontalHeader().setMinimumSectionSize(0)
        self.tableWidget.verticalHeader().setDefaultSectionSize(95)
        self.tableWidget.verticalHeader().setMinimumSectionSize(0)
        self.tableWidget_2 = QtWidgets.QTableWidget(self.widget)
        self.tableWidget_2.setGeometry(QtCore.QRect(10, 40, 701, 501))
        self.tableWidget_2.setObjectName("Week Widget")
        self.tableWidget_2.setColumnCount(5)
        self.tableWidget_2.setRowCount(24)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(8, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(9, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(10, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(11, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(12, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(13, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(14, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(15, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(16, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(17, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(18, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(19, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(20, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(21, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(22, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(23, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(4, item)
        self.tableWidget_3 = QtWidgets.QTableWidget(self.widget)
        self.tableWidget_3.setGeometry(QtCore.QRect(10, 40, 701, 501))
        self.tableWidget_3.setObjectName("Day Widget")
        self.tableWidget_3.setColumnCount(1)
        self.tableWidget_3.setRowCount(23)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setVerticalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setVerticalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setVerticalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setVerticalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setVerticalHeaderItem(8, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setVerticalHeaderItem(9, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setVerticalHeaderItem(10, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setVerticalHeaderItem(11, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setVerticalHeaderItem(12, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setVerticalHeaderItem(13, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setVerticalHeaderItem(14, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setVerticalHeaderItem(15, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setVerticalHeaderItem(16, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setVerticalHeaderItem(17, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setVerticalHeaderItem(18, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setVerticalHeaderItem(19, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setVerticalHeaderItem(20, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setVerticalHeaderItem(21, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setVerticalHeaderItem(22, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setHorizontalHeaderItem(0, item)
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(180, 10, 81, 33))
        self.pushButton.setObjectName("pushButton")
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(20, 10, 161, 31))
        self.lineEdit.setText("")
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(640, 10, 100, 33))
        self.pushButton_2.setObjectName("pushButton_2")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(390, 10, 241, 31))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.listWidget = QtWidgets.QListWidget(Form)
        self.listWidget.setGeometry(QtCore.QRect(20, 40, 161, 21))
        self.listWidget.setObjectName("listWidget")
        # Connect the currentIndexChanged signal of the ComboBox to the slot
        self.comboBox.currentIndexChanged.connect(self.onComboBoxIndexChanged)
        # Call the slot initially to set the initial state
        self.onComboBoxIndexChanged(0)  # assuming the initial index is 0

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def onComboBoxIndexChanged(self, index):
        # Get the selected text from the ComboBox
        selected_text = self.comboBox.currentText()

    # Set the visibility of the TableWidgets based on the selected text
        if selected_text == "Month":
            self.tableWidget.setVisible(True)
            self.tableWidget_2.setVisible(False)
            self.tableWidget_3.setVisible(False)
        elif selected_text == "Week":
            self.tableWidget.setVisible(False)
            self.tableWidget_2.setVisible(True)
            self.tableWidget_3.setVisible(False)
        elif selected_text == "Day":
            self.tableWidget.setVisible(False)
            self.tableWidget_2.setVisible(False)
            self.tableWidget_3.setVisible(True)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.comboBox.setItemText(0, _translate("Form", "Day"))
        self.comboBox.setItemText(1, _translate("Form", "Week"))
        self.comboBox.setItemText(2, _translate("Form", "Month"))
        self.pushButton_3.setText(_translate("Form", ">"))
        self.pushButton_4.setText(_translate("Form", "<"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Form", "Sun"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Form", "Mon"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Form", "Tue"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("Form", "Wed"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("Form", "Thu"))
        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText(_translate("Form", "Fri"))
        item = self.tableWidget.horizontalHeaderItem(6)
        item.setText(_translate("Form", "Sat"))
        __sortingEnabled = self.tableWidget.isSortingEnabled()
        self.tableWidget.setSortingEnabled(False)
        item = self.tableWidget.item(0, 0)
        item.setText(_translate("Form", "1\n" "Sport Day"))
        self.tableWidget.setSortingEnabled(__sortingEnabled)
        item = self.tableWidget_2.verticalHeaderItem(0)
        item.setText(_translate("Form", "1 AM"))
        item = self.tableWidget_2.verticalHeaderItem(1)
        item.setText(_translate("Form", "2 AM"))
        item = self.tableWidget_2.verticalHeaderItem(2)
        item.setText(_translate("Form", "3 AM"))
        item = self.tableWidget_2.verticalHeaderItem(3)
        item.setText(_translate("Form", "4 AM"))
        item = self.tableWidget_2.verticalHeaderItem(4)
        item.setText(_translate("Form", "5 AM"))
        item = self.tableWidget_2.verticalHeaderItem(5)
        item.setText(_translate("Form", "6 AM"))
        item = self.tableWidget_2.verticalHeaderItem(6)
        item.setText(_translate("Form", "7 AM"))
        item = self.tableWidget_2.verticalHeaderItem(7)
        item.setText(_translate("Form", "8 AM"))
        item = self.tableWidget_2.verticalHeaderItem(8)
        item.setText(_translate("Form", "9 AM"))
        item = self.tableWidget_2.verticalHeaderItem(9)
        item.setText(_translate("Form", "10 AM"))
        item = self.tableWidget_2.verticalHeaderItem(10)
        item.setText(_translate("Form", "11 AM"))
        item = self.tableWidget_2.verticalHeaderItem(11)
        item.setText(_translate("Form", "12 AM"))
        item = self.tableWidget_2.verticalHeaderItem(12)
        item.setText(_translate("Form", "1 PM"))
        item = self.tableWidget_2.verticalHeaderItem(13)
        item.setText(_translate("Form", "2 PM"))
        item = self.tableWidget_2.verticalHeaderItem(14)
        item.setText(_translate("Form", "3 PM"))
        item = self.tableWidget_2.verticalHeaderItem(15)
        item.setText(_translate("Form", "4 PM"))
        item = self.tableWidget_2.verticalHeaderItem(16)
        item.setText(_translate("Form", "5 PM"))
        item = self.tableWidget_2.verticalHeaderItem(17)
        item.setText(_translate("Form", "6 PM"))
        item = self.tableWidget_2.verticalHeaderItem(18)
        item.setText(_translate("Form", "7 PM"))
        item = self.tableWidget_2.verticalHeaderItem(19)
        item.setText(_translate("Form", "8 PM"))
        item = self.tableWidget_2.verticalHeaderItem(20)
        item.setText(_translate("Form", "9 PM"))
        item = self.tableWidget_2.verticalHeaderItem(21)
        item.setText(_translate("Form", "10 PM"))
        item = self.tableWidget_2.verticalHeaderItem(22)
        item.setText(_translate("Form", "11 PM"))
        item = self.tableWidget_2.verticalHeaderItem(23)
        item.setText(_translate("Form", "12 PM"))
        item = self.tableWidget_2.horizontalHeaderItem(0)
        item.setText(_translate("Form", "WED 1"))
        item = self.tableWidget_2.horizontalHeaderItem(1)
        item.setText(_translate("Form", "THU 2"))
        item = self.tableWidget_2.horizontalHeaderItem(2)
        item.setText(_translate("Form", "FRI 3"))
        item = self.tableWidget_2.horizontalHeaderItem(3)
        item.setText(_translate("Form", "SAT 4"))
        item = self.tableWidget_2.horizontalHeaderItem(4)
        item.setText(_translate("Form", "SUN 5"))
        item = self.tableWidget_3.verticalHeaderItem(0)
        item.setText(_translate("Form", "1 AM"))
        item = self.tableWidget_3.verticalHeaderItem(1)
        item.setText(_translate("Form", "2 AM"))
        item = self.tableWidget_3.verticalHeaderItem(2)
        item.setText(_translate("Form", "3 AM"))
        item = self.tableWidget_3.verticalHeaderItem(3)
        item.setText(_translate("Form", "4 AM"))
        item = self.tableWidget_3.verticalHeaderItem(4)
        item.setText(_translate("Form", "5 AM"))
        item = self.tableWidget_3.verticalHeaderItem(5)
        item.setText(_translate("Form", "6 AM"))
        item = self.tableWidget_3.verticalHeaderItem(6)
        item.setText(_translate("Form", "7 AM"))
        item = self.tableWidget_3.verticalHeaderItem(7)
        item.setText(_translate("Form", "8 AM"))
        item = self.tableWidget_3.verticalHeaderItem(8)
        item.setText(_translate("Form", "9 AM"))
        item = self.tableWidget_3.verticalHeaderItem(9)
        item.setText(_translate("Form", "10 AM"))
        item = self.tableWidget_3.verticalHeaderItem(10)
        item.setText(_translate("Form", "11 AM"))
        item = self.tableWidget_3.verticalHeaderItem(11)
        item.setText(_translate("Form", "12 AM"))
        item = self.tableWidget_3.verticalHeaderItem(12)
        item.setText(_translate("Form", "1 PM"))
        item = self.tableWidget_3.verticalHeaderItem(13)
        item.setText(_translate("Form", "2 PM"))
        item = self.tableWidget_3.verticalHeaderItem(14)
        item.setText(_translate("Form", "3 PM"))
        item = self.tableWidget_3.verticalHeaderItem(15)
        item.setText(_translate("Form", "4 PM"))
        item = self.tableWidget_3.verticalHeaderItem(16)
        item.setText(_translate("Form", "6 PM"))
        item = self.tableWidget_3.verticalHeaderItem(17)
        item.setText(_translate("Form", "4 PM"))
        item = self.tableWidget_3.verticalHeaderItem(18)
        item.setText(_translate("Form", "7 PM"))
        item = self.tableWidget_3.verticalHeaderItem(19)
        item.setText(_translate("Form", "8 PM"))
        item = self.tableWidget_3.verticalHeaderItem(20)
        item.setText(_translate("Form", "9 PM"))
        item = self.tableWidget_3.verticalHeaderItem(21)
        item.setText(_translate("Form", "10 PM"))
        item = self.tableWidget_3.verticalHeaderItem(22)
        item.setText(_translate("Form", "12 PM"))
        item = self.tableWidget_3.horizontalHeaderItem(0)
        item.setText(_translate("Form", "FRI 20"))
        self.pushButton.setText(_translate("Form", "Create"))
        self.lineEdit.setPlaceholderText(_translate("Form", "Search Event"))
        self.pushButton_2.setText(_translate("Form", "Export"))
        self.label.setText(_translate("Form", "19 October 2023"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())