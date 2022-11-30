import sys, os

from PyQt5.QtWidgets import (
    QErrorMessage, QWidget, QDialogButtonBox, QMessageBox, QDialog
)
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.uic import loadUi

from src.gui.resources.select_action import Ui_Dialog as SelectionDialog
from src.gui.resources.provide_sequence import Ui_Dialog as SequenceDialog

class ActionDialog(QDialog, SelectionDialog):
    ''' dialog for entering action list'''

    def __init__(self, parent = None):
        QDialog.__init__(self, parent = parent)
        # save reference to parent for later use
        self.parent = parent

        # set-up UI of this form first
        self.setupUi(self)

        # create a list object for the actions to be added
        self.action_list = []

        # rename buttons to next and back
        self.buttonBox.button(QDialogButtonBox.StandardButton.Ok).setText("Next")
        self.buttonBox.button(QDialogButtonBox.StandardButton.Cancel).setText("Back")

        # update the list of currently chosen actions
        self.textBrowser.setText(str(self.action_list))

        # connect signals to slots
        self.connectSignalsToSlots()

    def connectSignalsToSlots(self):
        # connect action list manipulation buttons to slots
        self.pushButton_addAction.clicked.connect(self.add_action_to_list)
        self.pushButton_applyList.clicked.connect(self.apply_action_list)

        # connect dialog buttons to slots
        self.buttonBox.accepted.connect(self.proceed)
        self.buttonBox.rejected.connect(self.back_to_home)


    @pyqtSlot()
    def add_action_to_list(self):
        ''' adds action to list of actions '''
        # get name of action to add
        action = self.lineEdit_action.text()

        # add action to list of actions and update text browser
        self.action_list.append(action)
        self.textBrowser.setText(str(self.action_list))
        self.textBrowser.update()
    
    @pyqtSlot()
    def apply_action_list(self):
        ''' applies an entire list of actions '''
        # get string representation of list to add
        list_str: str = self.lineEdit_list.text()

        # show error dialog box if syntax was not correct
        if list_str[0] != '[' or list_str[-1] != ']':
            error_box = QErrorMessage(self)
            error_box.setWindowModality(Qt.WindowModality.ApplicationModal)
            error_box.setWindowTitle("Syntax Error")
            error_box.showMessage("Syntax Error! Can't read list.")
            error_box.exec()
            return

        # insert empty list [] or [ ] to reset the list
        if list_str in ["[]", "[ ]"]:
            self.action_list = []
            return

        # parse string into action list
        tmp_list = list_str[1:-1].split(',')
        self.action_list = [(elem[1:] if elem[0] == ' ' else elem) for elem in tmp_list] 

        # update action list
        self.textBrowser.setText(str(self.action_list))
        self.textBrowser.update()

    @pyqtSlot()
    def proceed(self):
        ''' proceeds by writing actions to parent and closing window'''
        self.parent.action_list = self.action_list
        self.close()

    @pyqtSlot()
    def back_to_home(self):
        ''' closes window without any information propagated '''
        self.close()

        
class SequenceDialog(QDialog, SequenceDialog):
    ''' Dialog for entering template sequence'''

    def __init__(self, parent = None):
        QDialog.__init__(self, parent = parent)
        # save reference to parent for later use
        self.parent = parent

        # set-up UI of this form first
        self.setupUi(self)

        # create template sequence as an empty list
        self.template_sequence = []

        # rename buttons to next and back
        self.buttonBox.button(QDialogButtonBox.StandardButton.Ok).setText("Next")
        self.buttonBox.button(QDialogButtonBox.StandardButton.Cancel).setText("Back")

        # update the current template sequence and available action list
        self.textBrowser_availableActions.setText(str(self.parent.action_list))
        self.textBrowser_availableActions.update()
        self.textBrowser.setText(str(self.template_sequence))

        # connect signals no slots
        self.connectSignalsToSlots()

    def connectSignalsToSlots(self):
        # connect template sequence manipulation buttons to slots
        self.pushButton_appendAction.clicked.connect(self.append_action)
        self.pushButton_provideSequence.clicked.connect(self.provide_sequence)

        # connect dialog buttons to slots
        self.buttonBox.accepted.connect(self.proceed)
        self.buttonBox.rejected.connect(self.back_to_home)

    
    @pyqtSlot()
    def append_action(self):
        ''' append action to template sequence '''
        # get name of action to add
        action = self.lineEdit_action.text()

        # add action to template sequence and update text browser
        self.template_sequence.append(action)
        self.textBrowser.setText(str(self.template_sequence))
        self.textBrowser.update()

    @pyqtSlot()
    def provide_sequence(self):
        ''' stores an entire template sequence provided by user '''
        # get string representation of template sequence
        seq_str: str = self.lineEdit_sequence.text()

        # show error dialog box if syntax was not correct
        if seq_str[0] != '[' or seq_str[-1] != ']':
            error_box = QErrorMessage(self)
            error_box.setWindowModality(Qt.WindowModality.ApplicationModal)
            error_box.setWindowTitle("Syntax Error")
            error_box.showMessage("Syntax Error! Can't read list.")
            error_box.exec()
            return
        
        # insert empty sequence [] or [ ] to reset sequence
        if seq_str in ["[]", "[ ]"]:
            self.template_sequence = []
            return
        
        # parse string into template sequence
        tmp_seq = seq_str[1:-1].split(',')
        self.template_sequence = [(elem[1:] if elem[0] == ' ' else elem) for elem in tmp_seq] 

        # update template sequence
        self.textBrowser.setText(str(self.template_sequence))
        self.textBrowser.update()

    @pyqtSlot()
    def proceed(self):
        ''' proceeds by writing template sequence to parent and closing window'''
        # reject sequence if it contains elements that are not in the action set
        # by showing an error message and not proceeding
        non_matches = []
        for elem in self.template_sequence:
            if elem not in self.parent.action_list:
                non_matches.append(elem)
                
        if len(non_matches) > 0:
            error_box = QErrorMessage()
            error_box.setWindowModality(Qt.WindowModality.ApplicationModal)
            error_box.setWindowTitle("Invalid Action Error")
            error_box.showMessage("Matching Error! The following actions are invalid: {}".format(non_matches))
            error_box.exec()
            return
        
        # otherwise, write template sequence back and close
        self.parent.template_sequence = self.template_sequence
        self.close()

    @pyqtSlot()
    def back_to_home(self):
        ''' closes window without any information propagated '''
        self.close()

        