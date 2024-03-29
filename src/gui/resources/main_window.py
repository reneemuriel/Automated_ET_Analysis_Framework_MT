# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/gui/resources/main-window.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(400, 590)
        MainWindow.setMinimumSize(QtCore.QSize(400, 590))
        MainWindow.setMaximumSize(QtCore.QSize(400, 590))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setMinimumSize(QtCore.QSize(0, 520))
        self.centralwidget.setObjectName("centralwidget")
        self.version_label = QtWidgets.QLabel(self.centralwidget)
        self.version_label.setGeometry(QtCore.QRect(10, 530, 371, 20))
        self.version_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.version_label.setObjectName("version_label")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 9, 381, 121))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.paths_layout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.paths_layout.setContentsMargins(0, 0, 0, 0)
        self.paths_layout.setObjectName("paths_layout")
        self.output_path_label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.output_path_label.setObjectName("output_path_label")
        self.paths_layout.addWidget(self.output_path_label, 4, 0, 1, 1)
        self.input_browse_button = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.input_browse_button.setObjectName("input_browse_button")
        self.paths_layout.addWidget(self.input_browse_button, 1, 1, 1, 1)
        self.input_path_label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.input_path_label.setObjectName("input_path_label")
        self.paths_layout.addWidget(self.input_path_label, 0, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 100, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        self.paths_layout.addItem(spacerItem, 3, 0, 1, 1)
        self.output_browse_button = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.output_browse_button.setObjectName("output_browse_button")
        self.paths_layout.addWidget(self.output_browse_button, 5, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.paths_layout.addItem(spacerItem1, 2, 0, 1, 1)
        self.output_path_edit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.output_path_edit.setObjectName("output_path_edit")
        self.paths_layout.addWidget(self.output_path_edit, 5, 0, 1, 1)
        self.input_path_edit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.input_path_edit.setObjectName("input_path_edit")
        self.paths_layout.addWidget(self.input_path_edit, 1, 0, 1, 1)
        self.path_separator_line = QtWidgets.QFrame(self.centralwidget)
        self.path_separator_line.setGeometry(QtCore.QRect(10, 138, 381, 16))
        self.path_separator_line.setFrameShape(QtWidgets.QFrame.HLine)
        self.path_separator_line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.path_separator_line.setObjectName("path_separator_line")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 160, 382, 241))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.options_layout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.options_layout.setContentsMargins(0, 0, 0, 0)
        self.options_layout.setObjectName("options_layout")
        self.options_label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.options_label.setMaximumSize(QtCore.QSize(16777215, 20))
        self.options_label.setObjectName("options_label")
        self.options_layout.addWidget(self.options_label)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.ooi_checkBox = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.ooi_checkBox.setObjectName("ooi_checkBox")
        self.gridLayout_2.addWidget(self.ooi_checkBox, 2, 1, 1, 1)
        self.general_checkBox = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.general_checkBox.setObjectName("general_checkBox")
        self.gridLayout_2.addWidget(self.general_checkBox, 0, 1, 1, 1)
        self.sequence_checkBox = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.sequence_checkBox.setObjectName("sequence_checkBox")
        self.gridLayout_2.addWidget(self.sequence_checkBox, 4, 1, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem2, 0, 0, 1, 1)
        self.action_checkBox = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.action_checkBox.setObjectName("action_checkBox")
        self.gridLayout_2.addWidget(self.action_checkBox, 3, 1, 1, 1)
        self.entropy_checkBox = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.entropy_checkBox.setObjectName("entropy_checkBox")
        self.gridLayout_2.addWidget(self.entropy_checkBox, 5, 1, 1, 1)
        self.kCoefficient_checkBox = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.kCoefficient_checkBox.setObjectName("kCoefficient_checkBox")
        self.gridLayout_2.addWidget(self.kCoefficient_checkBox, 1, 1, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        spacerItem3 = QtWidgets.QSpacerItem(100, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        self.hitradius_spinBox = QtWidgets.QSpinBox(self.verticalLayoutWidget)
        self.hitradius_spinBox.setObjectName("hitradius_spinBox")
        self.horizontalLayout.addWidget(self.hitradius_spinBox)
        self.gridLayout_2.addLayout(self.horizontalLayout, 6, 1, 1, 1)
        self.options_layout.addLayout(self.gridLayout_2)
        self.options_buttonBox = QtWidgets.QDialogButtonBox(self.centralwidget)
        self.options_buttonBox.setGeometry(QtCore.QRect(220, 410, 166, 24))
        self.options_buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.options_buttonBox.setObjectName("options_buttonBox")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(10, 460, 381, 51))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.label.setObjectName("label")
        self.verticalLayout_3.addWidget(self.label)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.progressBar = QtWidgets.QProgressBar(self.verticalLayoutWidget_2)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.horizontalLayout_3.addWidget(self.progressBar)
        spacerItem4 = QtWidgets.QSpacerItem(100, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem4)
        self.start_button = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.start_button.setObjectName("start_button")
        self.horizontalLayout_3.addWidget(self.start_button)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.options_separator_line = QtWidgets.QFrame(self.centralwidget)
        self.options_separator_line.setGeometry(QtCore.QRect(10, 430, 381, 16))
        self.options_separator_line.setFrameShape(QtWidgets.QFrame.HLine)
        self.options_separator_line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.options_separator_line.setObjectName("options_separator_line")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 400, 21))
        self.menubar.setObjectName("menubar")
        self.menuWindow = QtWidgets.QMenu(self.menubar)
        self.menuWindow.setObjectName("menuWindow")
        self.menuSettings = QtWidgets.QMenu(self.menubar)
        self.menuSettings.setObjectName("menuSettings")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setSizeGripEnabled(True)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionSave_Configuration = QtWidgets.QAction(MainWindow)
        self.actionSave_Configuration.setObjectName("actionSave_Configuration")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionMinimize = QtWidgets.QAction(MainWindow)
        self.actionMinimize.setObjectName("actionMinimize")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionLoad_Configuration = QtWidgets.QAction(MainWindow)
        self.actionLoad_Configuration.setObjectName("actionLoad_Configuration")
        self.menuWindow.addAction(self.actionAbout)
        self.menuWindow.addSeparator()
        self.menuWindow.addAction(self.actionMinimize)
        self.menuWindow.addAction(self.actionExit)
        self.menuSettings.addAction(self.actionLoad_Configuration)
        self.menuSettings.addAction(self.actionSave_Configuration)
        self.menuSettings.addSeparator()
        self.menubar.addAction(self.menuWindow.menuAction())
        self.menubar.addAction(self.menuSettings.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Automated ET Analysis Framework"))
        self.version_label.setText(_translate("MainWindow", "Automated ET Analysis Framework, v0.1.0."))
        self.output_path_label.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-weight:600;\">Output Path</span></p></body></html>"))
        self.input_browse_button.setText(_translate("MainWindow", "Browse"))
        self.input_path_label.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-weight:600;\">Input Path</span></p></body></html>"))
        self.output_browse_button.setText(_translate("MainWindow", "Browse"))
        self.output_path_edit.setText(_translate("MainWindow", "Enter the path to your output folder."))
        self.input_path_edit.setText(_translate("MainWindow", "Enter the path to your input folder."))
        self.options_label.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-weight:600;\">Execution Options</span></p></body></html>"))
        self.ooi_checkBox.setText(_translate("MainWindow", "Perform OOI-Based Analysis"))
        self.general_checkBox.setText(_translate("MainWindow", "Perform General Analysis"))
        self.sequence_checkBox.setText(_translate("MainWindow", "Perform Sequence Comparison (req. Action-Based A.)"))
        self.action_checkBox.setText(_translate("MainWindow", "Perform Action-Based Analysis (req. OOI-Based A.)"))
        self.entropy_checkBox.setText(_translate("MainWindow", "Compute Entropy Statistics (req. OOi-Based A.)"))
        self.kCoefficient_checkBox.setText(_translate("MainWindow", "Caculate K-Coefficient"))
        self.label_2.setText(_translate("MainWindow", "Hit Radius (in Pixels)"))
        self.options_buttonBox.setToolTip(_translate("MainWindow", "<html><head/><body><p><br/></p></body></html>"))
        self.label.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-weight:600;\">Execution Progress</span></p></body></html>"))
        self.start_button.setText(_translate("MainWindow", "Start"))
        self.menuWindow.setTitle(_translate("MainWindow", "Window"))
        self.menuSettings.setTitle(_translate("MainWindow", "Settings"))
        self.actionSave_Configuration.setText(_translate("MainWindow", "Save Configuration"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionMinimize.setText(_translate("MainWindow", "Minimize"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionLoad_Configuration.setText(_translate("MainWindow", "Load Configuration"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
