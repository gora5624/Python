# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'e:\MyProduct\Python\WB\NEW_API\getOrdersNew\ui\GetOrders.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_GetOrders(object):
    def setupUi(self, GetOrders):
        GetOrders.setObjectName("GetOrders")
        GetOrders.resize(410, 313)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        GetOrders.setFont(font)
        GetOrders.setAutoFillBackground(False)
        GetOrders.setAnimated(False)
        GetOrders.setTabShape(QtWidgets.QTabWidget.Rounded)
        GetOrders.setUnifiedTitleAndToolBarOnMac(False)
        self.centralwidget = QtWidgets.QWidget(GetOrders)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.pushButtonSaveToExcel = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonSaveToExcel.setObjectName("pushButtonSaveToExcel")
        self.gridLayout_2.addWidget(self.pushButtonSaveToExcel, 1, 0, 1, 1)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 2)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 2)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setSizeConstraint(QtWidgets.QLayout.SetMinAndMaxSize)
        self.verticalLayout_3.setContentsMargins(3, -1, -1, -1)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.checkBoxAllSellers = QtWidgets.QCheckBox(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.checkBoxAllSellers.setFont(font)
        self.checkBoxAllSellers.setChecked(True)
        self.checkBoxAllSellers.setObjectName("checkBoxAllSellers")
        self.verticalLayout_3.addWidget(self.checkBoxAllSellers)
        self.checkBoxKar = QtWidgets.QCheckBox(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.checkBoxKar.setFont(font)
        self.checkBoxKar.setCheckable(True)
        self.checkBoxKar.setObjectName("checkBoxKar")
        self.verticalLayout_3.addWidget(self.checkBoxKar)
        self.checkBoxMan = QtWidgets.QCheckBox(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.checkBoxMan.setFont(font)
        self.checkBoxMan.setCheckable(True)
        self.checkBoxMan.setObjectName("checkBoxMan")
        self.verticalLayout_3.addWidget(self.checkBoxMan)
        self.checkBoxSam = QtWidgets.QCheckBox(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.checkBoxSam.setFont(font)
        self.checkBoxSam.setCheckable(True)
        self.checkBoxSam.setObjectName("checkBoxSam")
        self.verticalLayout_3.addWidget(self.checkBoxSam)
        self.checkBoxFed = QtWidgets.QCheckBox(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.checkBoxFed.setFont(font)
        self.checkBoxFed.setCheckable(True)
        self.checkBoxFed.setObjectName("checkBoxFed")
        self.verticalLayout_3.addWidget(self.checkBoxFed)
        self.gridLayout.addLayout(self.verticalLayout_3, 6, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 5, 0, 1, 1)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.checkBoxInsertNom = QtWidgets.QCheckBox(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.checkBoxInsertNom.setFont(font)
        self.checkBoxInsertNom.setChecked(True)
        self.checkBoxInsertNom.setObjectName("checkBoxInsertNom")
        self.verticalLayout_4.addWidget(self.checkBoxInsertNom)
        self.checkBoxAllSellerInOne = QtWidgets.QCheckBox(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.checkBoxAllSellerInOne.setFont(font)
        self.checkBoxAllSellerInOne.setObjectName("checkBoxAllSellerInOne")
        self.verticalLayout_4.addWidget(self.checkBoxAllSellerInOne)
        self.checkBoxConsolid = QtWidgets.QCheckBox(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.checkBoxConsolid.setFont(font)
        self.checkBoxConsolid.setObjectName("checkBoxConsolid")
        self.verticalLayout_4.addWidget(self.checkBoxConsolid)
        self.checkBoxSaveSKU = QtWidgets.QCheckBox(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.checkBoxSaveSKU.setFont(font)
        self.checkBoxSaveSKU.setChecked(True)
        self.checkBoxSaveSKU.setObjectName("checkBoxSaveSKU")
        self.verticalLayout_4.addWidget(self.checkBoxSaveSKU)
        self.checkBoxRAW = QtWidgets.QCheckBox(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.checkBoxRAW.setFont(font)
        self.checkBoxRAW.setObjectName("checkBoxRAW")
        self.verticalLayout_4.addWidget(self.checkBoxRAW)
        self.gridLayout.addLayout(self.verticalLayout_4, 6, 1, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.dateEditFrom = QtWidgets.QDateEdit(self.centralwidget)
        self.dateEditFrom.setMaximumDateTime(QtCore.QDateTime(QtCore.QDate(9999, 12, 30), QtCore.QTime(23, 59, 59)))
        self.dateEditFrom.setCalendarPopup(True)
        self.dateEditFrom.setObjectName("dateEditFrom")
        self.verticalLayout.addWidget(self.dateEditFrom)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.dateEditTo = QtWidgets.QDateEdit(self.centralwidget)
        self.dateEditTo.setCalendarPopup(True)
        self.dateEditTo.setObjectName("dateEditTo")
        self.verticalLayout_2.addWidget(self.dateEditTo)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 2)
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 5, 1, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        GetOrders.setCentralWidget(self.centralwidget)
        self.statusBar = QtWidgets.QStatusBar(GetOrders)
        self.statusBar.setObjectName("statusBar")
        GetOrders.setStatusBar(self.statusBar)

        self.retranslateUi(GetOrders)
        QtCore.QMetaObject.connectSlotsByName(GetOrders)

    def retranslateUi(self, GetOrders):
        _translate = QtCore.QCoreApplication.translate
        GetOrders.setWindowTitle(_translate("GetOrders", "Заказы для аналитики"))
        self.pushButtonSaveToExcel.setText(_translate("GetOrders", "Выгрузить в эксель"))
        self.label_3.setText(_translate("GetOrders", "Настройки"))
        self.checkBoxAllSellers.setText(_translate("GetOrders", "Все ИП"))
        self.checkBoxKar.setText(_translate("GetOrders", "Караханян"))
        self.checkBoxMan.setText(_translate("GetOrders", "Абраамян М.С."))
        self.checkBoxSam.setText(_translate("GetOrders", "Абррамян С.М."))
        self.checkBoxFed.setText(_translate("GetOrders", "Федоров И.И."))
        self.label_4.setText(_translate("GetOrders", "Выберите ИП (по умолчанию все)"))
        self.checkBoxInsertNom.setText(_translate("GetOrders", "Подставить номенклатуру"))
        self.checkBoxAllSellerInOne.setText(_translate("GetOrders", "Все ИП в один файл"))
        self.checkBoxConsolid.setText(_translate("GetOrders", "Консолидация данных"))
        self.checkBoxSaveSKU.setText(_translate("GetOrders", "Сохранить поле ШК"))
        self.checkBoxRAW.setText(_translate("GetOrders", "Сохранить все поля"))
        self.label.setText(_translate("GetOrders", "Дата от"))
        self.label_2.setText(_translate("GetOrders", "Дата до"))
        self.label_5.setText(_translate("GetOrders", "Поля"))
