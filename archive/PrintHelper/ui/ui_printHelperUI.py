# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\Python\archive\PrintHelper\ui\printHelperUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_PrintHelper(object):
    def setupUi(self, PrintHelper):
        PrintHelper.setObjectName("PrintHelper")
        PrintHelper.resize(400, 420)
        self.selectFileButt = QtWidgets.QPushButton(PrintHelper)
        self.selectFileButt.setGeometry(QtCore.QRect(20, 20, 361, 21))
        self.selectFileButt.setObjectName("selectFileButt")
        self.label = QtWidgets.QLabel(PrintHelper)
        self.label.setGeometry(QtCore.QRect(20, 0, 361, 20))
        self.label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(PrintHelper)
        self.label_2.setGeometry(QtCore.QRect(10, 50, 381, 21))
        self.label_2.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.bigButt = QtWidgets.QPushButton(PrintHelper)
        self.bigButt.setEnabled(True)
        self.bigButt.setGeometry(QtCore.QRect(20, 90, 361, 41))
        self.bigButt.setIconSize(QtCore.QSize(32, 32))
        self.bigButt.setFlat(False)
        self.bigButt.setObjectName("bigButt")
        self.medButt = QtWidgets.QPushButton(PrintHelper)
        self.medButt.setGeometry(QtCore.QRect(20, 140, 361, 41))
        self.medButt.setObjectName("medButt")
        self.smallButt = QtWidgets.QPushButton(PrintHelper)
        self.smallButt.setGeometry(QtCore.QRect(20, 190, 361, 41))
        self.smallButt.setObjectName("smallButt")
        self.smallButtPlastins = QtWidgets.QPushButton(PrintHelper)
        self.smallButtPlastins.setGeometry(QtCore.QRect(20, 310, 361, 41))
        self.smallButtPlastins.setObjectName("smallButtPlastins")
        self.smallButtBooks = QtWidgets.QPushButton(PrintHelper)
        self.smallButtBooks.setEnabled(True)
        self.smallButtBooks.setGeometry(QtCore.QRect(20, 250, 171, 41))
        self.smallButtBooks.setObjectName("smallButtBooks")
        self.smallButtCartholders = QtWidgets.QPushButton(PrintHelper)
        self.smallButtCartholders.setEnabled(True)
        self.smallButtCartholders.setGeometry(QtCore.QRect(20, 360, 361, 41))
        self.smallButtCartholders.setObjectName("smallButtCartholders")
        self.medButtBooks = QtWidgets.QPushButton(PrintHelper)
        self.medButtBooks.setEnabled(True)
        self.medButtBooks.setGeometry(QtCore.QRect(210, 250, 171, 41))
        self.medButtBooks.setObjectName("medButtBooks")
        self.frame = QtWidgets.QFrame(PrintHelper)
        self.frame.setGeometry(QtCore.QRect(10, 80, 381, 161))
        self.frame.setFrameShape(QtWidgets.QFrame.Panel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.frame.setLineWidth(1)
        self.frame.setObjectName("frame")
        self.frame_2 = QtWidgets.QFrame(PrintHelper)
        self.frame_2.setGeometry(QtCore.QRect(10, 240, 381, 61))
        self.frame_2.setFrameShape(QtWidgets.QFrame.Panel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.frame_2.setMidLineWidth(0)
        self.frame_2.setObjectName("frame_2")
        self.frame_2.raise_()
        self.frame.raise_()
        self.selectFileButt.raise_()
        self.label.raise_()
        self.label_2.raise_()
        self.bigButt.raise_()
        self.medButt.raise_()
        self.smallButt.raise_()
        self.smallButtPlastins.raise_()
        self.smallButtBooks.raise_()
        self.smallButtCartholders.raise_()
        self.medButtBooks.raise_()

        self.retranslateUi(PrintHelper)
        QtCore.QMetaObject.connectSlotsByName(PrintHelper)

    def retranslateUi(self, PrintHelper):
        _translate = QtCore.QCoreApplication.translate
        PrintHelper.setWindowTitle(_translate("PrintHelper", "Print Helper"))
        self.selectFileButt.setText(_translate("PrintHelper", "Выберите файл"))
        self.label.setText(_translate("PrintHelper", "Выберите файл с заказом:"))
        self.label_2.setText(_translate("PrintHelper", "Выберите режим работы"))
        self.bigButt.setText(_translate("PrintHelper", "Большой принтер силикон (3*2)"))
        self.medButt.setText(_translate("PrintHelper", "Средний принтер силикон (105*160)"))
        self.smallButt.setText(_translate("PrintHelper", "Силикон маленький (90*60)"))
        self.smallButtPlastins.setText(_translate("PrintHelper", "Планки маленкий (90*60)"))
        self.smallButtBooks.setText(_translate("PrintHelper", "Книжки маленький (90*60)"))
        self.smallButtCartholders.setText(_translate("PrintHelper", "Картхолдеры маленький (90*60)"))
        self.medButtBooks.setText(_translate("PrintHelper", "Книжки средний (105*160)"))
