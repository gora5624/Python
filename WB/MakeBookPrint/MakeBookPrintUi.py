# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\MyProduct\Python\WB\MakeBookPrint\MakeBookPrintUi.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(272, 505)
        self.tabWidget = QtWidgets.QTabWidget(Form)
        self.tabWidget.setGeometry(QtCore.QRect(0, 10, 271, 491))
        self.tabWidget.setObjectName("tabWidget")
        self.tabBook = QtWidgets.QWidget()
        self.tabBook.setObjectName("tabBook")
        self.CreatePrint = QtWidgets.QPushButton(self.tabBook)
        self.CreatePrint.setGeometry(QtCore.QRect(0, 400, 101, 23))
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
        self.DeleteImage = QtWidgets.QPushButton(self.tabBook)
        self.DeleteImage.setGeometry(QtCore.QRect(150, 440, 111, 23))
        self.DeleteImage.setObjectName("DeleteImage")
        self.textEditModel = QtWidgets.QTextEdit(self.tabBook)
        self.textEditModel.setGeometry(QtCore.QRect(0, 340, 261, 31))
        self.textEditModel.setObjectName("textEditModel")
        self.CreateImageFolderForWB = QtWidgets.QPushButton(self.tabBook)
        self.CreateImageFolderForWB.setGeometry(QtCore.QRect(0, 440, 131, 23))
        self.CreateImageFolderForWB.setObjectName("CreateImageFolderForWB")
        self.label_5 = QtWidgets.QLabel(self.tabBook)
        self.label_5.setGeometry(QtCore.QRect(210, 380, 16, 16))
        self.label_5.setObjectName("label_5")
        self.CreateExcel = QtWidgets.QPushButton(self.tabBook)
        self.CreateExcel.setGeometry(QtCore.QRect(160, 400, 101, 23))
        self.CreateExcel.setObjectName("CreateExcel")
        self.label = QtWidgets.QLabel(self.tabBook)
        self.label.setGeometry(QtCore.QRect(0, 10, 201, 16))
        self.label.setAutoFillBackground(True)
        self.label.setObjectName("label")
        self.label_4 = QtWidgets.QLabel(self.tabBook)
        self.label_4.setGeometry(QtCore.QRect(40, 380, 16, 16))
        self.label_4.setObjectName("label_4")
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
        self.CreateSiliconImage.setGeometry(QtCore.QRect(190, 100, 75, 23))
        self.CreateSiliconImage.setObjectName("CreateSiliconImage")
        self.ChekMask = QtWidgets.QPushButton(self.tabSilicon)
        self.ChekMask.setGeometry(QtCore.QRect(0, 100, 101, 23))
        self.ChekMask.setObjectName("ChekMask")
        self.CreateExcelForSilicon = QtWidgets.QPushButton(self.tabSilicon)
        self.CreateExcelForSilicon.setGeometry(QtCore.QRect(0, 440, 101, 23))
        self.CreateExcelForSilicon.setObjectName("CreateExcelForSilicon")
        self.textSiliconBrand = QtWidgets.QTextEdit(self.tabSilicon)
        self.textSiliconBrand.setGeometry(QtCore.QRect(0, 160, 51, 21))
        self.textSiliconBrand.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textSiliconBrand.setObjectName("textSiliconBrand")
        self.textSiliconName = QtWidgets.QTextEdit(self.tabSilicon)
        self.textSiliconName.setGeometry(QtCore.QRect(0, 190, 261, 41))
        self.textSiliconName.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textSiliconName.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.textSiliconName.setObjectName("textSiliconName")
        self.textSiliconCompability = QtWidgets.QTextEdit(self.tabSilicon)
        self.textSiliconCompability.setGeometry(QtCore.QRect(0, 240, 261, 41))
        self.textSiliconCompability.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.textSiliconCompability.setObjectName("textSiliconCompability")
        self.textSiliconModel = QtWidgets.QTextEdit(self.tabSilicon)
        self.textSiliconModel.setGeometry(QtCore.QRect(0, 290, 261, 41))
        self.textSiliconModel.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textSiliconModel.setObjectName("textSiliconModel")
        self.ModelSelector = QtWidgets.QComboBox(self.tabSilicon)
        self.ModelSelector.setGeometry(QtCore.QRect(0, 130, 261, 22))
        self.ModelSelector.setObjectName("ModelSelector")
        self.ApplyAddin = QtWidgets.QPushButton(self.tabSilicon)
        self.ApplyAddin.setGeometry(QtCore.QRect(190, 340, 75, 23))
        self.ApplyAddin.setObjectName("ApplyAddin")
        self.CameraType = QtWidgets.QComboBox(self.tabSilicon)
        self.CameraType.setGeometry(QtCore.QRect(0, 340, 121, 22))
        self.CameraType.setObjectName("CameraType")
        self.CameraType.addItem("")
        self.CameraType.addItem("")
        self.textPrice = QtWidgets.QTextEdit(self.tabSilicon)
        self.textPrice.setGeometry(QtCore.QRect(60, 160, 71, 21))
        self.textPrice.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textPrice.setObjectName("textPrice")
        self.CreateCase = QtWidgets.QPushButton(self.tabSilicon)
        self.CreateCase.setGeometry(QtCore.QRect(174, 440, 91, 23))
        self.CreateCase.setObjectName("CreateCase")
        self.FileSelector = QtWidgets.QComboBox(self.tabSilicon)
        self.FileSelector.setGeometry(QtCore.QRect(0, 370, 261, 22))
        self.FileSelector.setObjectName("FileSelector")
        self.IPSelector = QtWidgets.QComboBox(self.tabSilicon)
        self.IPSelector.setGeometry(QtCore.QRect(0, 400, 91, 22))
        self.IPSelector.setObjectName("IPSelector")
        self.IPSelector.addItem("")
        self.IPSelector.addItem("")
        self.tabWidget.addTab(self.tabSilicon, "")

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(1)
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
        self.DeleteImage.setText(_translate("Form", "Удалить данные"))
        self.CreateImageFolderForWB.setText(_translate("Form", "Размесить фото в папки"))
        self.label_5.setText(_translate("Form", "2"))
        self.CreateExcel.setText(_translate("Form", "Создать Excel"))
        self.label.setText(_translate("Form", "Выберете цвета для создания принтов"))
        self.label_4.setText(_translate("Form", "1"))
        self.label_3.setText(_translate("Form", "Модель"))
        self.label_2.setText(_translate("Form", "Бренд"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabBook), _translate("Form", "Книжки"))
        self.CreateSiliconImage.setText(_translate("Form", "Создать всё"))
        self.ChekMask.setText(_translate("Form", "Проверить маски"))
        self.CreateExcelForSilicon.setText(_translate("Form", "Создать эксель"))
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
        self.textSiliconCompability.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Совместимость</p></body></html>"))
        self.textSiliconModel.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Модель</p></body></html>"))
        self.ApplyAddin.setText(_translate("Form", "Применить"))
        self.CameraType.setItemText(0, _translate("Form", "с закрытой камерой"))
        self.CameraType.setItemText(1, _translate("Form", "с открытой камерой"))
        self.textPrice.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Цена</p></body></html>"))
        self.CreateCase.setText(_translate("Form", "Создать чехлы"))
        self.IPSelector.setItemText(0, _translate("Form", "Караханян"))
        self.IPSelector.setItemText(1, _translate("Form", "Абраамян"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabSilicon), _translate("Form", "Силикон"))
