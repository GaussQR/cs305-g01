from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtPrintSupport import *
import sys
import sqlite3
import time
import input_window

import os


class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 file dialogs - pythonspot.com'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()
        self.close()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.openFileNameDialog()
        self.openFileNamesDialog()
        self.saveFileDialog()

        self.show()

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(
            self, "QFileDialog.getOpenFileName()", "", "All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            print(fileName)

    def openFileNamesDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(
            self, "QFileDialog.getOpenFileNames()", "", "All Files (*);;Python Files (*.py)", options=options)
        if files:
            print(files)

    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(
            self, "QFileDialog.getSaveFileName()", "", "All Files (*);;Text Files (*.txt)", options=options)
        if fileName:
            print(fileName)


class MainDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(MainDialog, self).__init__(*args, **kwargs)

        self.setFixedWidth(300)
        self.setFixedHeight(120)

        layout = QVBoxLayout()

        self.QBtn = QPushButton()
        self.QBtn.setText("Login")
        self.setWindowTitle('Login')
        self.QBtn.clicked.connect(self.login)

        self.QBtnn = QPushButton()
        self.QBtnn.setText("Register")
        self.setWindowTitle('Register')
        self.QBtnn.clicked.connect(self.register)

        title = QLabel(":: Video Mining Software ::")
        font = title.font()
        font.setPointSize(16)
        title.setFont(font)

        layout.addWidget(title)

        layout.addWidget(self.QBtn)
        layout.addWidget(self.QBtnn)
        self.setLayout(layout)

    def login(self):
        dlg = LoginDialog()
        dlg.exec_()

    def register(self):
        dlg = InsertDialog()
        dlg.exec_()


class LoginDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(LoginDialog, self).__init__(*args, **kwargs)

        self.QBtn = QPushButton()
        self.QBtn.setText("Login")

        self.setWindowTitle("Login-using Email")
        self.setFixedWidth(300)
        self.setFixedHeight(200)

        self.QBtn.clicked.connect(self.login)

        layout = QVBoxLayout()

        self.emailinput = QLineEdit()
        self.emailinput.setPlaceholderText("Email")
        layout.addWidget(self.emailinput)

        self.passinput = QLineEdit()
        self.passinput.setPlaceholderText("Password")
        layout.addWidget(self.passinput)

        layout.addWidget(self.QBtn)
        self.setLayout(layout)

    def login(self):
        email = ""
        email = self.emailinput.text()
        password = self.passinput.text()

        self.conn = sqlite3.connect("user.db")

        self.c = self.conn.cursor()
        print("EMAIL", str(email))
        result = self.c.execute(
            "SELECT * from users where email = ? AND password= ? ", (email, password,))
        print("result brought")
        row = result.fetchall()
        print("ROW", row)
        self.conn.commit()
        self.c.close()
        self.conn.close()
        print("here")
        print(len(row))
        if(len(row) > 0):

            print("login succesful")
            dlg = input_window.InuputScreen()
            dlg.exec_()
        self.close()


class InsertDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(InsertDialog, self).__init__(*args, **kwargs)

        self.QBtn = QPushButton()
        self.QBtn.setText("Register")

        self.setWindowTitle("Add User")
        self.setFixedWidth(400)
        self.setFixedHeight(400)

        self.QBtn.clicked.connect(self.addstudent)

        layout = QVBoxLayout()

        self.nameinput = QLineEdit()
        self.nameinput.setPlaceholderText("Name")
        layout.addWidget(self.nameinput)

        self.emailinput = QLineEdit()
        self.emailinput.setPlaceholderText("Email")
        layout.addWidget(self.emailinput)

        self.passinput = QLineEdit()
        self.passinput.setPlaceholderText("Password( Max. Len- 6)")
        layout.addWidget(self.passinput)

        self.mobileinput = QLineEdit()
        self.mobileinput.setPlaceholderText("Mobile")

        layout.addWidget(self.mobileinput)

        self.addressinput = QLineEdit()
        self.addressinput.setPlaceholderText("Address")
        layout.addWidget(self.addressinput)

        layout.addWidget(self.QBtn)
        self.setLayout(layout)

    def addstudent(self):

        name = ""
        email = ""
        password = -1
        mobile = -1
        address = ""

        name = self.nameinput.text()
        email = self.emailinput.text()
        password = self.passinput.text()
        mobile = self.mobileinput.text()
        address = self.addressinput.text()
        try:
            self.conn = sqlite3.connect("user.db")
            self.c = self.conn.cursor()
            self.c.execute("INSERT INTO users (name,email,password,Mobile,address) VALUES (?,?,?,?,?)",
                           (name, email, password, mobile, address))
            self.conn.commit()
            self.c.close()
            self.conn.close()
            QMessageBox.information(
                QMessageBox(), 'Successful', 'USER  is added successfully to the database.')
            self.close()
        except Exception:
            QMessageBox.warning(QMessageBox(), 'Error',
                                'Could not add user to the database.')


app = QApplication(sys.argv)
w = MainDialog()
sys.exit(w.exec_())
sys.exit(app.exec_())
