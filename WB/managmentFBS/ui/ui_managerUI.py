# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'e:\MyProduct\Python\WB\managmentFBS\ui\managerUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(550, 500)
        self.updateDbBtn = QtWidgets.QPushButton(Form)
        self.updateDbBtn.setGeometry(QtCore.QRect(10, 10, 170, 25))
        self.updateDbBtn.setObjectName("updateDbBtn")
        self.addFilterStringBtn = QtWidgets.QPushButton(Form)
        self.addFilterStringBtn.setGeometry(QtCore.QRect(190, 10, 170, 25))
        self.addFilterStringBtn.setObjectName("addFilterStringBtn")
        self.comboBox = QtWidgets.QComboBox(Form)
        self.comboBox.setGeometry(QtCore.QRect(440, 10, 100, 25))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(365, 10, 81, 25))
        self.label.setObjectName("label")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.updateDbBtn.setText(_translate("Form", "Обновить базу номенклатур"))
        self.addFilterStringBtn.setText(_translate("Form", "Добавить строку для фильтра"))
        self.comboBox.setItemText(0, _translate("Form", "Все"))
        self.comboBox.setItemText(1, _translate("Form", "Караханян"))
        self.comboBox.setItemText(2, _translate("Form", "Абраамян"))
        self.comboBox.setItemText(3, _translate("Form", "Самвел"))
        self.label.setText(_translate("Form", "Выберите ИП"))
