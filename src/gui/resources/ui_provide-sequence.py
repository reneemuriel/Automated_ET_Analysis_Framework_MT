# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/jenseirik/Documents/renee-ma/et-framework/src/gui/resources/provide-sequence.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(501, 391)
        Dialog.setMinimumSize(QtCore.QSize(500, 320))
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(20, 270, 191, 16))
        self.label.setObjectName("label")
        self.gridLayoutWidget = QtWidgets.QWidget(Dialog)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(20, 160, 451, 102))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.pushButton_appendAction = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_appendAction.setObjectName("pushButton_appendAction")
        self.gridLayout.addWidget(self.pushButton_appendAction, 1, 2, 1, 1)
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
        self.lineEdit_sequence = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.lineEdit_sequence.setObjectName("lineEdit_sequence")
        self.gridLayout.addWidget(self.lineEdit_sequence, 4, 0, 1, 1)
        self.pushButton_provideSequence = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_provideSequence.setObjectName("pushButton_provideSequence")
        self.gridLayout.addWidget(self.pushButton_provideSequence, 4, 2, 1, 1)
        self.textBrowser = QtWidgets.QTextBrowser(Dialog)
        self.textBrowser.setGeometry(QtCore.QRect(20, 290, 451, 51))
        self.textBrowser.setObjectName("textBrowser")
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(300, 350, 166, 24))
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(20, 20, 451, 91))
        self.label_2.setObjectName("label_2")
        self.textBrowser_availableActions = QtWidgets.QTextBrowser(Dialog)
        self.textBrowser_availableActions.setGeometry(QtCore.QRect(20, 120, 451, 31))
        self.textBrowser_availableActions.setObjectName("textBrowser_availableActions")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Template Sequence"))
        self.label.setText(_translate("Dialog", "Current Template Sequence:"))
        self.pushButton_appendAction.setText(_translate("Dialog", "Add Action"))
        self.options_label_3.setText(_translate("Dialog", "<html><head/><body><p><span style=\" font-weight:600;\">Provide Entire Template Sequence</span></p></body></html>"))
        self.options_label_2.setText(_translate("Dialog", "<html><head/><body><p><span style=\" font-weight:600;\">Append Individual Action</span></p></body></html>"))
        self.lineEdit_action.setText(_translate("Dialog", "Syntax: Action"))
        self.lineEdit_sequence.setText(_translate("Dialog", "Syntax: [Action1, Action2, Action3]"))
        self.pushButton_provideSequence.setText(_translate("Dialog", "Provide Seq."))
        self.textBrowser.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">None</p></body></html>"))
        self.label_2.setText(_translate("Dialog", "You have selected \"sequence comparison\". Please provide a tem-\n"
"plate sequence by either appending each action individually\n"
"to a list, or by providing the entire list directly.\n"
"\n"
"The following actions are available:"))
