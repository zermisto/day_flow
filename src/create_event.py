# create_event.py
# Create Event Function GUI for the Personal Calendar Application
# Created by King, 19th October 2023

from PyQt5 import QtCore, QtGui, QtWidgets

class CreateEventPopup(QtWidgets.QWidget):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(440, 481)

        # Main widget
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setGeometry(QtCore.QRect(50, 40, 351, 381))
        self.widget.setObjectName("widget")

        # Event Title TextEdit
        self.textEdit_7 = QtWidgets.QTextEdit(self.widget)
        self.textEdit_7.setGeometry(QtCore.QRect(0, 0, 351, 31))
        self.textEdit_7.setObjectName("textEdit_7")
        self.textEdit_7.setPlaceholderText("Event Title")

        # DateEdit
        self.dateEdit = QtWidgets.QDateEdit(self.widget)
        self.dateEdit.setGeometry(QtCore.QRect(0, 40, 121, 31))
        self.dateEdit.setDisplayFormat("yyyy/mm/dd")
        self.dateEdit.setObjectName("dateEdit")

        # Description TextEdit
        self.textEdit_5 = QtWidgets.QTextEdit(self.widget)
        self.textEdit_5.setGeometry(QtCore.QRect(0, 80, 351, 91))
        self.textEdit_5.setObjectName("textEdit_5")
        self.textEdit_5.setPlaceholderText("Description")

        # Location TextEdit
        self.textEdit_6 = QtWidgets.QTextEdit(self.widget)
        self.textEdit_6.setGeometry(QtCore.QRect(0, 180, 351, 51))
        self.textEdit_6.setObjectName("textEdit_6")
        self.textEdit_6.setPlaceholderText("Location")

        # Repeat Count Label
        self.label_4 = QtWidgets.QLabel(self.widget)
        self.label_4.setGeometry(QtCore.QRect(230, 250, 101, 20))
        self.label_4.setObjectName("label_4")

        # Repeat Pattern ComboBox
        self.comboBox = QtWidgets.QComboBox(self.widget)
        self.comboBox.setGeometry(QtCore.QRect(10, 270, 73, 22))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItems(["Daily", "Weekly", "Monthly", "Yearly"])

        # Days of the Week ComboBox
        self.comboBox_2 = QtWidgets.QComboBox(self.widget)
        self.comboBox_2.setGeometry(QtCore.QRect(120, 270, 73, 22))
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.addItems(["Mon", "Tue", "Wed", "Thu", "Fri"])

        # Repeat Every Label
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setGeometry(QtCore.QRect(120, 250, 101, 20))
        self.label_3.setObjectName("label_3")

        # Repeat Pattern Label
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setGeometry(QtCore.QRect(0, 250, 101, 20))
        self.label_2.setObjectName("label_2")

        # Ends After Label
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setGeometry(QtCore.QRect(230, 290, 61, 16))
        self.label.setObjectName("label")

        # Number of Occurrences SpinBox
        self.spinBox = QtWidgets.QSpinBox(self.widget)
        self.spinBox.setGeometry(QtCore.QRect(290, 290, 42, 22))
        self.spinBox.setObjectName("spinBox")

        # Forever CheckBox
        self.checkBox = QtWidgets.QCheckBox(self.widget)
        self.checkBox.setGeometry(QtCore.QRect(230, 270, 91, 20))
        self.checkBox.setObjectName("checkBox")
        self.checkBox.setText("Forever")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle("Form")
        self.label_4.setText("Repeat Count?")
        self.label_2.setText("Repeat Pattern?")
        self.label_3.setText("Repeat Every?")
        self.label.setText("Ends After")

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = CreateEventPopup()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
