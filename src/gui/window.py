import sys, os
import yaml
from functools import partial
import logging as log

from PyQt5.QtWidgets import (
    QApplication, QDialog, QMainWindow, QMessageBox, QFileDialog, QDialogButtonBox,
    QErrorMessage, QWidget
)
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.uic import loadUi 

# local imports
from src.gui.resources.main_window import Ui_MainWindow
from src.gui.dialogs import ActionDialog, SequenceDialog

class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, parent = None):
        super().__init__(parent)
        # set-up UI first and add a few standard values
        self.setupUi(self)

        # create a field for action list and template sequence that dialogs can access
        self.action_list = None
        self.template_sequence = None

        # uncomment to set default input and output paths to current directory
        #cur_dir = os.getcwd()
        #self.input_path_edit.setText(cur_dir)
        #self.output_path_edit.setText(cur_dir)

        # check and disable the basic analysis execution option
        self.general_checkBox.setChecked(True)
        self.general_checkBox.setDisabled(True)

        # change text of Ok/Cancel boxes to apply/reset
        self.options_buttonBox.button(QDialogButtonBox.StandardButton.Ok).setText("Apply")
        self.options_buttonBox.button(QDialogButtonBox.StandardButton.Cancel).setText("Reset")

        # reset progress bar and disable start button
        self.progressBar.reset()
        self.start_button.setDisabled(True)

        # disable save configuration when program starts, activate after options are applied
        self.actionSave_Configuration.setDisabled(True)

        # connect signals (buttons) to slots
        self.connectSignalsToSlots()

    def connectSignalsToSlots(self):
        # connect path browsing buttons to a function that opens a dialog
        self.input_browse_button.clicked.connect(self.getInputPath)
        self.output_browse_button.clicked.connect(self.getOutputPath)

        # connect execution options buttons to slots: 
        self.options_buttonBox.accepted.connect(self.applyExecutionOptions)
        self.options_buttonBox.rejected.connect(self.resetExecutionOptions)

        # connect start button to slot that starts main function
        self.start_button.clicked.connect(self.start_main)

        # connect actions to corresponding slots
        self.actionLoad_Configuration.triggered.connect(self.load_configuration)
        self.actionSave_Configuration.triggered.connect(self.save_configuration)
        self.actionMinimize.triggered.connect(self.showMinimized)
        self.actionExit.triggered.connect(self.close)
        self.actionAbout.triggered.connect(self.about)

        #test
        #self.hitradius_spinBox.valueChanged.connect(self.test)

    #def test(self):
        #print('value has changed, oh no')

    def about(self):
        QMessageBox.about(
            self,
            "Automated ET Analysis Framework",
            "Version 0.1.0"
        )

    def getConfigDict(self) -> dict:
        ''' returns the current configuration as a dictionary '''

        config_dict = {
            'paths' : {
                'input' : self.input_path_edit.text(),
                'output' : self.output_path_edit.text(),
            },
            'executionOptions' : {
                'general_analysis' : True,
                'kcoeff_analysis' : self.kCoefficient_checkBox.isChecked(),
                'action_analysis' : self.action_checkBox.isChecked(),
                'ooi_analysis' : self.ooi_checkBox.isChecked(),
                'sequence_comparison' : self.sequence_checkBox.isChecked(),
                'entropy_stats' : self.entropy_checkBox.isChecked(),
                'novice_results' : True,
                'hitradius': self.hitradius_spinBox.value()   
                 },
            'action_list' : self.action_list,
            'template_sequence' : self.template_sequence
        }
        return config_dict

    def configureFromDict(self, config: dict):
        ''' configures the application from a dictionary '''
        # set input and output paths and hits radius 
        self.input_path_edit.setText(config['paths']['input'])
        self.output_path_edit.setText(config['paths']['output'])
        

        # set checkboxes according to config file, and disable all of them
        self.kCoefficient_checkBox.setChecked(config['executionOptions']['kcoeff_analysis'])
        self.action_checkBox.setChecked(config['executionOptions']['action_analysis'])
        self.ooi_checkBox.setChecked(config['executionOptions']['ooi_analysis'])
        self.sequence_checkBox.setChecked(config['executionOptions']['sequence_comparison'])
        self.entropy_checkBox.setChecked(config['executionOptions']['entropy_stats'])
        self.kCoefficient_checkBox.setDisabled(True)
        self.action_checkBox.setDisabled(True)
        self.ooi_checkBox.setDisabled(True)
        self.sequence_checkBox.setDisabled(True)
        self.entropy_checkBox.setDisabled(True)

        self.hitradius_spinBox.setValue(config['executionOptions']['hitradius'])
        self.hitradius_spinBox.setDisabled(True)

        # disable the "apply" button
        self.options_buttonBox.button(QDialogButtonBox.StandardButton.Ok).setDisabled(True)

        # read the action list and template sequence
        self.action_list = config['action_list']
        self.template_sequence = config['template_sequence']

        # enable the configuration saving action
        self.actionSave_Configuration.setEnabled(True)

        # enable the start execution button
        self.start_button.setEnabled(True)

    # ----------------------------- SLOTS -------------------------------------------
    @pyqtSlot()
    def getInputPath(self):
        ''' slot that opens a file dialog to select input path '''
        selected_dir = QFileDialog.getExistingDirectory(
            parent = self, 
            caption = "Select input directory",
            directory = ".",
            options = QFileDialog.ShowDirsOnly
        )
        self.input_path_edit.setText(selected_dir)

    @pyqtSlot()
    def getOutputPath(self):
        ''' slot that opens a file dialog to select output path '''
        selected_dir = QFileDialog.getExistingDirectory(
            parent = self, 
            caption = "Select output directory",
            directory = ".",
            options = QFileDialog.ShowDirsOnly
        )
        self.output_path_edit.setText(selected_dir)

    @pyqtSlot()
    def applyExecutionOptions(self):
        '''
        slot that applies execution options. special cases for sequence or action-based analysis:
        
        - Case 1: action-based analysis: opens window to select from possible actions
        - Case 2: sequence comparison: opens window to select optimal sequence
        '''
        
        # first, make all boxes uncheckable --> can be undone by clicking on reset
        self.kCoefficient_checkBox.setDisabled(True)
        self.ooi_checkBox.setDisabled(True)
        self.action_checkBox.setDisabled(True)
        self.sequence_checkBox.setDisabled(True)
        self.entropy_checkBox.setDisabled(True)
        # make hitradius unchangeable --> can be undone by clicking on reset
        self.hitradius_spinBox.setDisabled(True)

        # if action-based analysis is checked, then show new window to select actions
        if self.action_checkBox.isChecked():
            ad = ActionDialog(self)
            ad.setWindowModality(Qt.WindowModality.ApplicationModal)
            ad.exec()
            
        # sequence comparison can only be performed in action-based analysis is selected
        if self.sequence_checkBox.isChecked():
            sd = SequenceDialog(self)
            sd.setWindowModality(Qt.WindowModality.ApplicationModal)
            sd.exec()

        # enable start button and disable "apply" button
        self.start_button.setEnabled(True)
        self.options_buttonBox.button(QDialogButtonBox.StandardButton.Ok).setDisabled(True)

        # enable configuration saving
        self.actionSave_Configuration.setEnabled(True)

    @pyqtSlot()
    def resetExecutionOptions(self):
        ''' resets all execution options and makes them checkable again '''

        # set checkboxes to unchecked (except for general analysi)
        self.kCoefficient_checkBox.setChecked(False)
        self.ooi_checkBox.setChecked(False)
        self.action_checkBox.setChecked(False)
        self.sequence_checkBox.setChecked(False)
        self.entropy_checkBox.setChecked(False)

        # make checkboxes checkable again
        self.kCoefficient_checkBox.setDisabled(False)
        self.ooi_checkBox.setDisabled(False)
        self.action_checkBox.setDisabled(False)
        self.sequence_checkBox.setDisabled(False)
        self.entropy_checkBox.setDisabled(False)

        # make hitradius changeable again
        self.hitradius_spinBox.setDisabled(False)

        # (re)activate apply button and disable start button
        self.options_buttonBox.button(QDialogButtonBox.StandardButton.Ok).setEnabled(True)
        self.start_button.setDisabled(True)

    @pyqtSlot()
    def start_main(self):
        ''' collect all the data contained in the UI and start the main function '''
        # import start_analysis here to avoid a circular dependency
        from app import start_analysis

        # store all information in a dictionary
        args_dict = self.getConfigDict()

        # start analysis
        log.info("starting main with args = {}".format(args_dict))
        start_analysis(args_dict)   

    @pyqtSlot()
    def save_configuration(self):
        ''' save current configuration to disk '''
        # get file name from user input via file dialog
        file_dialog = QFileDialog()
        file_dialog.setDefaultSuffix(".yaml")
        filename, _ = file_dialog.getSaveFileName(self, "Save Configuration")

        # if file-name does not end with .yaml already, add it
        if not filename.endswith(".yaml"):
            filename += ".yaml"

        # dump configuration to yaml file
        with open(filename, 'w', encoding = "utf-8") as outfile:
            yaml.dump(self.getConfigDict(), outfile, default_flow_style=False)

    @pyqtSlot()
    def load_configuration(self):
        ''' load configuration from disk '''
        # get file name from user input via file dialog
        file_dialog = QFileDialog()
        filename, _ = file_dialog.getOpenFileName(self, "Load Configuration")

        # open yaml file and turn it into a dictionary
        with open(filename, 'r', encoding = "utf-8") as infile:
            config_dict = yaml.load(infile, Loader=yaml.FullLoader)
        
        # configure the rest of the UI with respect to the config file
        self.configureFromDict(config_dict)



if __name__ == "__main__":

    # allow the application to scale to high DPI screens
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)

    # create an application with the command-line arguments, show window
    application = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    # start the application event-loop - terminate, when the window is closed
    sys.exit(application.exec())
