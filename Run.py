import platform
import sys
import os
import PyQt5
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QLineEdit
from PyQt5 import uic
class Password(QMainWindow):
    def show_alert(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Alert")
        msg.setText("Caution!")
        msg.setInformativeText("password incorrect, please check again.".title())
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
    def __init__(self):
        super(Password, self).__init__()
        uic.loadUi("Password.ui", self)
        self.findChild(PyQt5.QtWidgets.QPushButton, "Enter").clicked.connect(self.check)
    def RunMainWindow(self):
        from MainWindow import MyWindow
        self.mainwidow = MyWindow()
        self.mainwidow.show()
    def check(self, check):
        if self.findChild(QLineEdit,"Password").text() == "Pass":
            print(check)
            self.close()
            self.RunMainWindow()
        else:
            self.show_alert()
class Main():
    def __init__(self):
        system_version = platform.mac_ver()[0][0:4]
        system_machine = platform.machine()
        system_processor = platform.processor()
        if float(system_version) >= 10.5:
            app = QApplication(sys.argv)
            window = Password()
            window.setWindowTitle("Password")
            window.show()
            sys.exit(app.exec_())

if __name__=="__main__":
    print("Running....")
    Main()