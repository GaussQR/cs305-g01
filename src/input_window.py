import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import file_access


class InuputScreen(QDialog):
    def __init__(self, *args, **kwargs):
        super(InuputScreen, self).__init__(*args, **kwargs)
        self.setFixedWidth(300)
        self.setFixedHeight(300)
        self.setWindowTitle('VidiMiWare')
        layout1 = QVBoxLayout()
        self.label1 = QLabel()
        self.label1.setText("VidiMiWare")
        self.label1.setFont(QFont("Times", 25, QFont.Bold))
        self.label1.show()
        self.btn = QPushButton()
        self.btn.setText("FACES FOR IDENTIFICATION")
        self.btn.show()
        self.btn.clicked.connect(file_access.file_wrapper1)
        self.btn2 = QPushButton()
        self.btn2.setText("IMAGES FOR RECOGNITION")
        self.btn2.show()
        self.btn2.clicked.connect(file_access.file_wrapper2)
        layout1.setSpacing(20)
        layout1.addWidget(self.label1)
        layout1.addWidget(self.btn)
        layout1.addWidget(self.btn2)
        self.setLayout(layout1)

        self.close()

    def dialog(self):
        mbox = QMessageBox()

        mbox.setText("Your allegiance has been noted")
        mbox.setDetailedText(
            "You are now a disciple and subject of the all-knowing Guru")
        mbox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        mbox.exec_()
