import sys

from PyQt5.QtWidgets import (
    QApplication, QDialog, QMainWindow, QMessageBox
)

from PyQt5.uic import loadUi

from main_window import Ui_MainWindow

class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setupUi(self)
        self.connectSignalsToSlots()

    def connectSignalsToSlots(self):
        pass



if __name__ == "__main__":
    application = QApplication(sys.argv)
    window = Window()
    window.show() # display gui
    sys.exit(application.exec()) # starts application, leaves it open until actively being closed
