# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'e:\MyProduct\Python\.git-rewrite\t\archive\PrintHelper\ui\printHelperUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 251)
        self.selectFileButt = QtWidgets.QPushButton(Form)
        self.selectFileButt.setGeometry(QtCore.QRect(20, 20, 361, 23))
        self.selectFileButt.setObjectName("selectFileButt")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(20, 0, 361, 20))
        self.label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(20, 50, 361, 20))
        self.label_2.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.bigButt = QtWidgets.QPushButton(Form)
        self.bigButt.setEnabled(False)
        self.bigButt.setGeometry(QtCore.QRect(20, 80, 171, 41))
        self.bigButt.setFlat(False)
        self.bigButt.setObjectName("bigButt")
        self.medButt = QtWidgets.QPushButton(Form)
        self.medButt.setGeometry(QtCore.QRect(210, 80, 171, 41))
        self.medButt.setObjectName("medButt")
        self.smallButt = QtWidgets.QPushButton(Form)
        self.smallButt.setGeometry(QtCore.QRect(20, 140, 171, 41))
        self.smallButt.setObjectName("smallButt")
        self.smallButtPlastins = QtWidgets.QPushButton(Form)
        self.smallButtPlastins.setGeometry(QtCore.QRect(210, 140, 171, 41))
        self.smallButtPlastins.setObjectName("smallButtPlastins")
        self.smallButtBooks = QtWidgets.QPushButton(Form)
        self.smallButtBooks.setEnabled(True)
        self.smallButtBooks.setGeometry(QtCore.QRect(20, 200, 171, 41))
        self.smallButtBooks.setObjectName("smallButtBooks")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.selectFileButt.setText(_translate("Form", "Выберите файл"))
        self.label.setText(_translate("Form", "Выберите файл с заказом:"))
        self.label_2.setText(_translate("Form", "Выберите режим работы"))
        self.bigButt.setText(_translate("Form", "Большой принтер силикон"))
        self.medButt.setText(_translate("Form", "Средний принтер силикон"))
        self.smallButt.setText(_translate("Form", "Маленький принтер силикон"))
        self.smallButtPlastins.setText(_translate("Form", "Маленький принтер планки"))
        self.smallButtBooks.setText(_translate("Form", "Маленький принтер книжки"))
