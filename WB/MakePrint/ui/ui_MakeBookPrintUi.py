# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'e:\MyProduct\Python\WB\MakePrint\ui\MakeBookPrintUi.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(318, 491)
        self.tabWidget = QtWidgets.QTabWidget(Form)
        self.tabWidget.setGeometry(QtCore.QRect(0, 30, 321, 461))
        self.tabWidget.setObjectName("tabWidget")
        self.tabBook = QtWidgets.QWidget()
        self.tabBook.setObjectName("tabBook")
        self.CreatePrint = QtWidgets.QPushButton(self.tabBook)
        self.CreatePrint.setGeometry(QtCore.QRect(160, 380, 101, 23))
        self.CreatePrint.setObjectName("CreatePrint")
        self.splitterColor = QtWidgets.QSplitter(self.tabBook)
        self.splitterColor.setGeometry(QtCore.QRect(0, 40, 101, 221))
        self.splitterColor.setAutoFillBackground(False)
        self.splitterColor.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.splitterColor.setFrameShadow(QtWidgets.QFrame.Plain)
        self.splitterColor.setLineWidth(0)
        self.splitterColor.setMidLineWidth(0)
        self.splitterColor.setOrientation(QtCore.Qt.Vertical)
        self.splitterColor.setOpaqueResize(True)
        self.splitterColor.setObjectName("splitterColor")
        self.checkBox_2_SkyBlue = QtWidgets.QCheckBox(self.splitterColor)
        self.checkBox_2_SkyBlue.setObjectName("checkBox_2_SkyBlue")
        self.checkBox_4_Gold = QtWidgets.QCheckBox(self.splitterColor)
        self.checkBox_4_Gold.setObjectName("checkBox_4_Gold")
        self.checkBox_6_Pink = QtWidgets.QCheckBox(self.splitterColor)
        self.checkBox_6_Pink.setObjectName("checkBox_6_Pink")
        self.checkBox_5_Red = QtWidgets.QCheckBox(self.splitterColor)
        self.checkBox_5_Red.setObjectName("checkBox_5_Red")
        self.checkBox_7_Grey = QtWidgets.QCheckBox(self.splitterColor)
        self.checkBox_7_Grey.setObjectName("checkBox_7_Grey")
        self.checkBox_9_Black = QtWidgets.QCheckBox(self.splitterColor)
        self.checkBox_9_Black.setObjectName("checkBox_9_Black")
        self.checkBox_3_Green = QtWidgets.QCheckBox(self.splitterColor)
        self.checkBox_3_Green.setObjectName("checkBox_3_Green")
        self.checkBox_8_Blue = QtWidgets.QCheckBox(self.splitterColor)
        self.checkBox_8_Blue.setObjectName("checkBox_8_Blue")
        self.checkBox_1_Vinous = QtWidgets.QCheckBox(self.splitterColor)
        self.checkBox_1_Vinous.setObjectName("checkBox_1_Vinous")
        self.textEditModel = QtWidgets.QTextEdit(self.tabBook)
        self.textEditModel.setGeometry(QtCore.QRect(0, 340, 261, 31))
        self.textEditModel.setObjectName("textEditModel")
        self.label = QtWidgets.QLabel(self.tabBook)
        self.label.setGeometry(QtCore.QRect(0, 10, 201, 16))
        self.label.setAutoFillBackground(True)
        self.label.setObjectName("label")
        self.textLog = QtWidgets.QTextBrowser(self.tabBook)
        self.textLog.setGeometry(QtCore.QRect(120, 40, 141, 221))
        self.textLog.setObjectName("textLog")
        self.label_3 = QtWidgets.QLabel(self.tabBook)
        self.label_3.setGeometry(QtCore.QRect(0, 320, 41, 16))
        self.label_3.setAutoFillBackground(True)
        self.label_3.setObjectName("label_3")
        self.label_2 = QtWidgets.QLabel(self.tabBook)
        self.label_2.setGeometry(QtCore.QRect(0, 260, 31, 16))
        self.label_2.setAutoFillBackground(True)
        self.label_2.setObjectName("label_2")
        self.textEditBrand = QtWidgets.QTextEdit(self.tabBook)
        self.textEditBrand.setGeometry(QtCore.QRect(0, 280, 261, 31))
        self.textEditBrand.setObjectName("textEditBrand")
        self.tabWidget.addTab(self.tabBook, "")
        self.tabSilicon = QtWidgets.QWidget()
        self.tabSilicon.setObjectName("tabSilicon")
        self.textSiliconMask = QtWidgets.QTextBrowser(self.tabSilicon)
        self.textSiliconMask.setGeometry(QtCore.QRect(0, 10, 261, 81))
        self.textSiliconMask.setObjectName("textSiliconMask")
        self.CreateSiliconImage = QtWidgets.QPushButton(self.tabSilicon)
        self.CreateSiliconImage.setGeometry(QtCore.QRect(180, 160, 75, 23))
        self.CreateSiliconImage.setObjectName("CreateSiliconImage")
        self.ChekMask = QtWidgets.QPushButton(self.tabSilicon)
        self.ChekMask.setGeometry(QtCore.QRect(0, 160, 101, 23))
        self.ChekMask.setObjectName("ChekMask")
        self.AddPhotoSelector = QtWidgets.QComboBox(self.tabSilicon)
        self.AddPhotoSelector.setGeometry(QtCore.QRect(180, 130, 69, 22))
        self.AddPhotoSelector.setObjectName("AddPhotoSelector")
        self.AddPhotoSelector.addItem("")
        self.AddPhotoSelector.addItem("")
        self.label_4 = QtWidgets.QLabel(self.tabSilicon)
        self.label_4.setGeometry(QtCore.QRect(190, 100, 61, 20))
        self.label_4.setObjectName("label_4")
        self.SiliconeMode = QtWidgets.QCheckBox(self.tabSilicon)
        self.SiliconeMode.setGeometry(QtCore.QRect(0, 130, 131, 17))
        self.SiliconeMode.setObjectName("SiliconeMode")
        self.tabWidget.addTab(self.tabSilicon, "")
        self.plastins = QtWidgets.QWidget()
        self.plastins.setObjectName("plastins")
        self.makePlastinsBut = QtWidgets.QPushButton(self.plastins)
        self.makePlastinsBut.setGeometry(QtCore.QRect(0, 10, 111, 23))
        self.makePlastinsBut.setObjectName("makePlastinsBut")
        self.tabWidget.addTab(self.plastins, "")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.CreateCase = QtWidgets.QPushButton(self.tab)
        self.CreateCase.setGeometry(QtCore.QRect(0, 410, 91, 23))
        self.CreateCase.setObjectName("CreateCase")
        self.ChekImage = QtWidgets.QPushButton(self.tab)
        self.ChekImage.setGeometry(QtCore.QRect(160, 410, 101, 23))
        self.ChekImage.setObjectName("ChekImage")
        self.textSiliconBrand = QtWidgets.QTextEdit(self.tab)
        self.textSiliconBrand.setGeometry(QtCore.QRect(0, 40, 51, 21))
        self.textSiliconBrand.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textSiliconBrand.setObjectName("textSiliconBrand")
        self.textSiliconName = QtWidgets.QTextEdit(self.tab)
        self.textSiliconName.setGeometry(QtCore.QRect(0, 70, 261, 41))
        self.textSiliconName.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textSiliconName.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.textSiliconName.setObjectName("textSiliconName")
        self.CameraType = QtWidgets.QComboBox(self.tab)
        self.CameraType.setGeometry(QtCore.QRect(0, 220, 121, 22))
        self.CameraType.setObjectName("CameraType")
        self.CameraType.addItem("")
        self.CameraType.addItem("")
        self.textSiliconCompability = QtWidgets.QTextEdit(self.tab)
        self.textSiliconCompability.setGeometry(QtCore.QRect(0, 120, 261, 41))
        self.textSiliconCompability.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.textSiliconCompability.setObjectName("textSiliconCompability")
        self.ApplyAddin = QtWidgets.QPushButton(self.tab)
        self.ApplyAddin.setGeometry(QtCore.QRect(194, 220, 71, 21))
        self.ApplyAddin.setObjectName("ApplyAddin")
        self.CreateExcelForSilicon = QtWidgets.QPushButton(self.tab)
        self.CreateExcelForSilicon.setGeometry(QtCore.QRect(160, 280, 101, 23))
        self.CreateExcelForSilicon.setObjectName("CreateExcelForSilicon")
        self.textSiliconModel = QtWidgets.QTextEdit(self.tab)
        self.textSiliconModel.setGeometry(QtCore.QRect(0, 170, 261, 41))
        self.textSiliconModel.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textSiliconModel.setObjectName("textSiliconModel")
        self.textPrice = QtWidgets.QTextEdit(self.tab)
        self.textPrice.setGeometry(QtCore.QRect(60, 40, 71, 21))
        self.textPrice.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textPrice.setObjectName("textPrice")
        self.IPSelector = QtWidgets.QComboBox(self.tab)
        self.IPSelector.setGeometry(QtCore.QRect(0, 280, 91, 22))
        self.IPSelector.setObjectName("IPSelector")
        self.IPSelector.addItem("")
        self.IPSelector.addItem("")
        self.IPSelector.addItem("")
        self.FileSelector = QtWidgets.QComboBox(self.tab)
        self.FileSelector.setGeometry(QtCore.QRect(0, 250, 261, 22))
        self.FileSelector.setObjectName("FileSelector")
        self.ModelSelector = QtWidgets.QComboBox(self.tab)
        self.ModelSelector.setGeometry(QtCore.QRect(0, 10, 261, 22))
        self.ModelSelector.setObjectName("ModelSelector")
        self.updateListModel = QtWidgets.QPushButton(self.tab)
        self.updateListModel.setGeometry(QtCore.QRect(164, 40, 101, 23))
        self.updateListModel.setObjectName("updateListModel")
        self.ForceUpdate = QtWidgets.QCheckBox(self.tab)
        self.ForceUpdate.setGeometry(QtCore.QRect(100, 380, 161, 17))
        self.ForceUpdate.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.ForceUpdate.setObjectName("ForceUpdate")
        self.tabWidget.addTab(self.tab, "")
        self.label_6 = QtWidgets.QLabel(Form)
        self.label_6.setGeometry(QtCore.QRect(10, 10, 111, 16))
        self.label_6.setObjectName("label_6")

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(2)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.CreatePrint.setText(_translate("Form", "Создать принты"))
        self.checkBox_2_SkyBlue.setText(_translate("Form", "Голубой"))
        self.checkBox_4_Gold.setText(_translate("Form", "Золотой"))
        self.checkBox_6_Pink.setText(_translate("Form", "Розовое золото"))
        self.checkBox_5_Red.setText(_translate("Form", "Красный"))
        self.checkBox_7_Grey.setText(_translate("Form", "Серый"))
        self.checkBox_9_Black.setText(_translate("Form", "Черный"))
        self.checkBox_3_Green.setText(_translate("Form", "Зеленый"))
        self.checkBox_8_Blue.setText(_translate("Form", "Синий"))
        self.checkBox_1_Vinous.setText(_translate("Form", "Бордовый"))
        self.label.setText(_translate("Form", "Выберете цвета для создания принтов"))
        self.label_3.setText(_translate("Form", "Модель"))
        self.label_2.setText(_translate("Form", "Бренд"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabBook), _translate("Form", "Книжки"))
        self.CreateSiliconImage.setText(_translate("Form", "Создать всё"))
        self.ChekMask.setText(_translate("Form", "Проверить маски"))
        self.AddPhotoSelector.setItemText(0, _translate("Form", "2.jpg"))
        self.AddPhotoSelector.setItemText(1, _translate("Form", "3.jpg"))
        self.label_4.setText(_translate("Form", "Доп. фото"))
        self.SiliconeMode.setText(_translate("Form", "Натянуть все принты"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabSilicon), _translate("Form", "Силикон"))
        self.makePlastinsBut.setText(_translate("Form", "Создать пластины"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.plastins), _translate("Form", "Пластины"))
        self.CreateCase.setText(_translate("Form", "Создать чехлы"))
        self.ChekImage.setText(_translate("Form", "Перезалить фото"))
        self.textSiliconBrand.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Mobi711</p></body></html>"))
        self.textSiliconName.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Наименование ВБ</p></body></html>"))
        self.CameraType.setItemText(0, _translate("Form", "с закрытой камерой"))
        self.CameraType.setItemText(1, _translate("Form", "с открытой камерой"))
        self.textSiliconCompability.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Совместимость</p></body></html>"))
        self.ApplyAddin.setText(_translate("Form", "Применить"))
        self.CreateExcelForSilicon.setText(_translate("Form", "Создать эксель"))
        self.textSiliconModel.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Модель</p></body></html>"))
        self.textPrice.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Цена</p></body></html>"))
        self.IPSelector.setItemText(0, _translate("Form", "Караханян"))
        self.IPSelector.setItemText(1, _translate("Form", "Абраамян"))
        self.IPSelector.setItemText(2, _translate("Form", "Самвел"))
        self.updateListModel.setText(_translate("Form", "Обновить список"))
        self.ForceUpdate.setText(_translate("Form", "Обновить принудительно"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Form", "Создание товара"))
        self.label_6.setText(_translate("Form", "Создание принтов"))
