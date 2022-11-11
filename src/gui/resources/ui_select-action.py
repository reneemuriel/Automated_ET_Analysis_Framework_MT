# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/jenseirik/Documents/renee-ma/et-framework/src/gui/resources/select-action.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(500, 320)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QtCore.QSize(500, 320))
        self.textBrowser = QtWidgets.QTextBrowser(Dialog)
        self.textBrowser.setGeometry(QtCore.QRect(20, 220, 451, 51))
        self.textBrowser.setObjectName("textBrowser")
        self.gridLayoutWidget = QtWidgets.QWidget(Dialog)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(20, 90, 451, 102))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.pushButton_addAction = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_addAction.setObjectName("pushButton_addAction")
        self.gridLayout.addWidget(self.pushButton_addAction, 1, 2, 1, 1)
        self.options_label_3 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.options_label_3.setMaximumSize(QtCore.QSize(16777215, 20))
        self.options_label_3.setObjectName("options_label_3")
        self.gridLayout.addWidget(self.options_label_3, 3, 0, 1, 1)
        self.options_label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.options_label_2.setMaximumSize(QtCore.QSize(16777215, 20))
        self.options_label_2.setObjectName("options_label_2")
        self.gridLayout.addWidget(self.options_label_2, 0, 0, 1, 1)
        self.lineEdit_action = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.lineEdit_action.setObjectName("lineEdit_action")
        self.gridLayout.addWidget(self.lineEdit_action, 1, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 2, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 1, 1, 1)
        self.lineEdit_list = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.lineEdit_list.setObjectName("lineEdit_list")
        self.gridLayout.addWidget(self.lineEdit_list, 4, 0, 1, 1)
        self.pushButton_applyList = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_applyList.setObjectName("pushButton_applyList")
        self.gridLayout.addWidget(self.pushButton_applyList, 4, 2, 1, 1)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(20, 200, 191, 16))
        self.label.setObjectName("label")
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(300, 280, 166, 24))
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(20, 10, 451, 71))
        self.label_2.setObjectName("label_2")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Action List"))
        self.textBrowser.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">None</p></body></html>"))
        self.pushButton_addAction.setText(_translate("Dialog", "Add Action"))
        self.options_label_3.setText(_translate("Dialog", "<html><head/><body><p><span style=\" font-weight:600;\">Add Action List</span></p></body></html>"))
        self.options_label_2.setText(_translate("Dialog", "<html><head/><body><p><span style=\" font-weight:600;\">Add Individual Actions</span></p></body></html>"))
        self.lineEdit_action.setText(_translate("Dialog", "Syntax: Action"))
        self.lineEdit_list.setText(_translate("Dialog", "Syntax: [Action1, Action2, Action3]"))
        self.pushButton_applyList.setText(_translate("Dialog", "Apply List"))
        self.label.setText(_translate("Dialog", "Current List of Actions:"))
        self.label_2.setText(_translate("Dialog", "You have selected \"action-based analysis\". Please add the actions \n"
"you want to analyze to proceed. You can either add actions indi-\n"
"vidually or as a list."))
