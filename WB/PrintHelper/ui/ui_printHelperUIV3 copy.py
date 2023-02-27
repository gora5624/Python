# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'printHelperUIV3hPREHZ.ui'
##
## Created by: Qt User Interface Compiler version 6.1.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *


class Ui_PrintHelper(object):
    def setupUi(self, PrintHelper):
        if not PrintHelper.objectName():
            PrintHelper.setObjectName(u"PrintHelper")
        PrintHelper.resize(422, 395)
        sizePolicy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(PrintHelper.sizePolicy().hasHeightForWidth())
        PrintHelper.setSizePolicy(sizePolicy)
        font = QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setKerning(False)
        font.setStyleStrategy(QFont.PreferDefault)
        PrintHelper.setFont(font)
        PrintHelper.setStyleSheet(u"")
        self.selectFileButt = QPushButton(PrintHelper)
        self.selectFileButt.setObjectName(u"selectFileButt")
        self.selectFileButt.setGeometry(QRect(20, 30, 381, 41))
        font1 = QFont()
        font1.setPointSize(15)
        font1.setBold(True)
        font1.setKerning(False)
        font1.setStyleStrategy(QFont.PreferDefault)
        self.selectFileButt.setFont(font1)
        self.selectFileButt.setStyleSheet(u"")
        self.label = QLabel(PrintHelper)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(20, -1, 381, 31))
        font2 = QFont()
        font2.setPointSize(14)
        font2.setBold(False)
        font2.setKerning(False)
        font2.setStyleStrategy(QFont.PreferDefault)
        self.label.setFont(font2)
        self.label.setLayoutDirection(Qt.LeftToRight)
        self.label.setAlignment(Qt.AlignCenter)
        self.label_2 = QLabel(PrintHelper)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(20, 70, 381, 21))
        self.label_2.setFont(font)
        self.label_2.setLayoutDirection(Qt.LeftToRight)
        self.label_2.setFrameShape(QFrame.NoFrame)
        self.label_2.setAlignment(Qt.AlignCenter)
        self.frameSmall = QFrame(PrintHelper)
        self.frameSmall.setObjectName(u"frameSmall")
        self.frameSmall.setGeometry(QRect(20, 100, 381, 251))
        self.frameSmall.setFont(font1)
        self.frameSmall.setFrameShape(QFrame.NoFrame)
        self.frameSmall.setFrameShadow(QFrame.Sunken)
        self.frameSmall.setMidLineWidth(0)
        self.verticalLayoutWidget_3 = QWidget(self.frameSmall)
        self.verticalLayoutWidget_3.setObjectName(u"verticalLayoutWidget_3")
        self.verticalLayoutWidget_3.setGeometry(QRect(0, 0, 381, 241))
        self.verticalLayout_3 = QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.smallButt = QPushButton(self.verticalLayoutWidget_3)
        self.smallButt.setObjectName(u"smallButt")
        self.smallButt.setEnabled(True)
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.smallButt.sizePolicy().hasHeightForWidth())
        self.smallButt.setSizePolicy(sizePolicy1)

        self.verticalLayout_3.addWidget(self.smallButt)

        self.smallButtBooks = QPushButton(self.verticalLayoutWidget_3)
        self.smallButtBooks.setObjectName(u"smallButtBooks")
        self.smallButtBooks.setEnabled(True)
        sizePolicy1.setHeightForWidth(self.smallButtBooks.sizePolicy().hasHeightForWidth())
        self.smallButtBooks.setSizePolicy(sizePolicy1)

        self.verticalLayout_3.addWidget(self.smallButtBooks)

        self.smallButtPlastins = QPushButton(self.verticalLayoutWidget_3)
        self.smallButtPlastins.setObjectName(u"smallButtPlastins")
        self.smallButtPlastins.setEnabled(True)
        sizePolicy1.setHeightForWidth(self.smallButtPlastins.sizePolicy().hasHeightForWidth())
        self.smallButtPlastins.setSizePolicy(sizePolicy1)

        self.verticalLayout_3.addWidget(self.smallButtPlastins)

        self.smallButtCartholders = QPushButton(self.verticalLayoutWidget_3)
        self.smallButtCartholders.setObjectName(u"smallButtCartholders")
        self.smallButtCartholders.setEnabled(True)
        sizePolicy1.setHeightForWidth(self.smallButtCartholders.sizePolicy().hasHeightForWidth())
        self.smallButtCartholders.setSizePolicy(sizePolicy1)

        self.verticalLayout_3.addWidget(self.smallButtCartholders)

        self.frameBig = QFrame(PrintHelper)
        self.frameBig.setObjectName(u"frameBig")
        self.frameBig.setGeometry(QRect(20, 100, 381, 71))
        self.frameBig.setFrameShape(QFrame.NoFrame)
        self.frameBig.setFrameShadow(QFrame.Sunken)
        self.frameBig.setLineWidth(1)
        self.verticalLayoutWidget = QWidget(self.frameBig)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(0, 0, 381, 77))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setSpacing(8)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.verticalLayout.setContentsMargins(0, 4, 0, 4)
        self.bigButt = QPushButton(self.verticalLayoutWidget)
        self.bigButt.setObjectName(u"bigButt")
        self.bigButt.setEnabled(True)
        sizePolicy1.setHeightForWidth(self.bigButt.sizePolicy().hasHeightForWidth())
        self.bigButt.setSizePolicy(sizePolicy1)
        font3 = QFont()
        font3.setPointSize(14)
        font3.setBold(True)
        font3.setKerning(False)
        font3.setStyleStrategy(QFont.PreferDefault)
        self.bigButt.setFont(font3)
        self.bigButt.setIconSize(QSize(32, 32))
        self.bigButt.setFlat(False)

        self.verticalLayout.addWidget(self.bigButt)

        self.frameMed = QFrame(PrintHelper)
        self.frameMed.setObjectName(u"frameMed")
        self.frameMed.setGeometry(QRect(20, 100, 381, 141))
        self.frameMed.setFrameShape(QFrame.NoFrame)
        self.frameMed.setFrameShadow(QFrame.Raised)
        self.verticalLayoutWidget_2 = QWidget(self.frameMed)
        self.verticalLayoutWidget_2.setObjectName(u"verticalLayoutWidget_2")
        self.verticalLayoutWidget_2.setGeometry(QRect(0, 0, 381, 146))
        self.verticalLayout_2 = QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setSizeConstraint(QLayout.SetMinimumSize)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.medButt = QPushButton(self.verticalLayoutWidget_2)
        self.medButt.setObjectName(u"medButt")
        self.medButt.setEnabled(True)
        sizePolicy1.setHeightForWidth(self.medButt.sizePolicy().hasHeightForWidth())
        self.medButt.setSizePolicy(sizePolicy1)
        self.medButt.setFont(font1)

        self.verticalLayout_2.addWidget(self.medButt)

        self.medButtBooks = QPushButton(self.verticalLayoutWidget_2)
        self.medButtBooks.setObjectName(u"medButtBooks")
        self.medButtBooks.setEnabled(True)
        sizePolicy1.setHeightForWidth(self.medButtBooks.sizePolicy().hasHeightForWidth())
        self.medButtBooks.setSizePolicy(sizePolicy1)
        self.medButtBooks.setFont(font1)

        self.verticalLayout_2.addWidget(self.medButtBooks)

        self.frameMain = QFrame(PrintHelper)
        self.frameMain.setObjectName(u"frameMain")
        self.frameMain.setGeometry(QRect(20, 90, 381, 261))
        sizePolicy2 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.frameMain.sizePolicy().hasHeightForWidth())
        self.frameMain.setSizePolicy(sizePolicy2)
        self.frameMain.setFrameShape(QFrame.NoFrame)
        self.frameMain.setFrameShadow(QFrame.Raised)
        self.verticalLayoutWidget_5 = QWidget(self.frameMain)
        self.verticalLayoutWidget_5.setObjectName(u"verticalLayoutWidget_5")
        self.verticalLayoutWidget_5.setGeometry(QRect(0, 5, 381, 251))
        self.verticalLayout_5 = QVBoxLayout(self.verticalLayoutWidget_5)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.bigButtInt = QPushButton(self.verticalLayoutWidget_5)
        self.bigButtInt.setObjectName(u"bigButtInt")
        self.bigButtInt.setStyleSheet(u"")
        self.bigButtInt.setIconSize(QSize(236, 130))

        self.verticalLayout_5.addWidget(self.bigButtInt)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.smallButtInt = QPushButton(self.verticalLayoutWidget_5)
        self.smallButtInt.setObjectName(u"smallButtInt")
        self.smallButtInt.setEnabled(True)
        palette = QPalette()
        brush = QBrush(QColor(0, 120, 215, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Highlight, brush)
        brush1 = QBrush(QColor(240, 240, 240, 255))
        brush1.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Inactive, QPalette.Highlight, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.Highlight, brush)
        self.smallButtInt.setPalette(palette)
        self.smallButtInt.setStyleSheet(u"")
        self.smallButtInt.setIconSize(QSize(112, 200))

        self.horizontalLayout.addWidget(self.smallButtInt)

        self.medButtInt = QPushButton(self.verticalLayoutWidget_5)
        self.medButtInt.setObjectName(u"medButtInt")
        palette1 = QPalette()
        palette1.setBrush(QPalette.Active, QPalette.Highlight, brush)
        palette1.setBrush(QPalette.Inactive, QPalette.Highlight, brush1)
        palette1.setBrush(QPalette.Disabled, QPalette.Highlight, brush)
        self.medButtInt.setPalette(palette1)
        self.medButtInt.setStyleSheet(u"")
        self.medButtInt.setIconSize(QSize(119, 200))

        self.horizontalLayout.addWidget(self.medButtInt)


        self.verticalLayout_5.addLayout(self.horizontalLayout)

        self.mainPageButt = QPushButton(PrintHelper)
        self.mainPageButt.setObjectName(u"mainPageButt")
        self.mainPageButt.setGeometry(QRect(220, 350, 181, 23))
        self.frameSettings = QFrame(PrintHelper)
        self.frameSettings.setObjectName(u"frameSettings")
        self.frameSettings.setGeometry(QRect(20, 90, 381, 281))
        sizePolicy2.setHeightForWidth(self.frameSettings.sizePolicy().hasHeightForWidth())
        self.frameSettings.setSizePolicy(sizePolicy2)
        self.frameSettings.setFrameShape(QFrame.StyledPanel)
        self.frameSettings.setFrameShadow(QFrame.Raised)
        self.verticalLayoutWidget_4 = QWidget(self.frameSettings)
        self.verticalLayoutWidget_4.setObjectName(u"verticalLayoutWidget_4")
        self.verticalLayoutWidget_4.setGeometry(QRect(9, 0, 361, 281))
        self.verticalLayout_4 = QVBoxLayout(self.verticalLayoutWidget_4)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(12)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setSizeConstraint(QLayout.SetFixedSize)
        self.horizontalLayout_2.setContentsMargins(-1, -1, -1, 0)
        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(-1, -1, 0, 0)
        self.label_3 = QLabel(self.verticalLayoutWidget_4)
        self.label_3.setObjectName(u"label_3")
        sizePolicy2.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy2)
        font4 = QFont()
        font4.setPointSize(9)
        font4.setBold(False)
        font4.setKerning(False)
        font4.setStyleStrategy(QFont.PreferDefault)
        self.label_3.setFont(font4)

        self.verticalLayout_6.addWidget(self.label_3)

        self.bigAcsButt = QCheckBox(self.verticalLayoutWidget_4)
        self.bigAcsButt.setObjectName(u"bigAcsButt")

        self.verticalLayout_6.addWidget(self.bigAcsButt)

        self.medAcsButt = QCheckBox(self.verticalLayoutWidget_4)
        self.medAcsButt.setObjectName(u"medAcsButt")

        self.verticalLayout_6.addWidget(self.medAcsButt)

        self.smallAcsButt = QCheckBox(self.verticalLayoutWidget_4)
        self.smallAcsButt.setObjectName(u"smallAcsButt")

        self.verticalLayout_6.addWidget(self.smallAcsButt)


        self.horizontalLayout_2.addLayout(self.verticalLayout_6)

        self.verticalLayout_8 = QVBoxLayout()
        self.verticalLayout_8.setSpacing(0)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setSizeConstraint(QLayout.SetFixedSize)
        self.verticalLayout_8.setContentsMargins(39, -1, 0, 0)
        self.label_5 = QLabel(self.verticalLayoutWidget_4)
        self.label_5.setObjectName(u"label_5")
        sizePolicy2.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy2)

        self.verticalLayout_8.addWidget(self.label_5)

        self.label_6 = QLabel(self.verticalLayoutWidget_4)
        self.label_6.setObjectName(u"label_6")
        sizePolicy2.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy2)
        font5 = QFont()
        font5.setPointSize(8)
        font5.setBold(False)
        font5.setKerning(False)
        font5.setStyleStrategy(QFont.PreferDefault)
        self.label_6.setFont(font5)

        self.verticalLayout_8.addWidget(self.label_6)

        self.lineEditNameSize1C = QLineEdit(self.verticalLayoutWidget_4)
        self.lineEditNameSize1C.setObjectName(u"lineEditNameSize1C")

        self.verticalLayout_8.addWidget(self.lineEditNameSize1C)

        self.label_7 = QLabel(self.verticalLayoutWidget_4)
        self.label_7.setObjectName(u"label_7")
        sizePolicy2.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy2)
        self.label_7.setFont(font5)

        self.verticalLayout_8.addWidget(self.label_7)

        self.lineEditNameFileSize = QLineEdit(self.verticalLayoutWidget_4)
        self.lineEditNameFileSize.setObjectName(u"lineEditNameFileSize")

        self.verticalLayout_8.addWidget(self.lineEditNameFileSize)

        self.addSizeButt = QPushButton(self.verticalLayoutWidget_4)
        self.addSizeButt.setObjectName(u"addSizeButt")

        self.verticalLayout_8.addWidget(self.addSizeButt)

        self.pushButtonShowSizes = QPushButton(self.verticalLayoutWidget_4)
        self.pushButtonShowSizes.setObjectName(u"pushButtonShowSizes")

        self.verticalLayout_8.addWidget(self.pushButtonShowSizes)


        self.horizontalLayout_2.addLayout(self.verticalLayout_8)


        self.verticalLayout_4.addLayout(self.horizontalLayout_2)

        self.label_4 = QLabel(self.verticalLayoutWidget_4)
        self.label_4.setObjectName(u"label_4")
        sizePolicy3 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy3)

        self.verticalLayout_4.addWidget(self.label_4)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.bigSilAcsButt = QCheckBox(self.verticalLayoutWidget_4)
        self.bigSilAcsButt.setObjectName(u"bigSilAcsButt")

        self.verticalLayout_7.addWidget(self.bigSilAcsButt)

        self.medSilAcsButt = QCheckBox(self.verticalLayoutWidget_4)
        self.medSilAcsButt.setObjectName(u"medSilAcsButt")

        self.verticalLayout_7.addWidget(self.medSilAcsButt)

        self.smallSilAcsButt = QCheckBox(self.verticalLayoutWidget_4)
        self.smallSilAcsButt.setObjectName(u"smallSilAcsButt")

        self.verticalLayout_7.addWidget(self.smallSilAcsButt)


        self.horizontalLayout_3.addLayout(self.verticalLayout_7)

        self.verticalLayout_9 = QVBoxLayout()
        self.verticalLayout_9.setSpacing(0)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.medBkAcsButt = QCheckBox(self.verticalLayoutWidget_4)
        self.medBkAcsButt.setObjectName(u"medBkAcsButt")

        self.verticalLayout_9.addWidget(self.medBkAcsButt)

        self.smallBkAcsButt = QCheckBox(self.verticalLayoutWidget_4)
        self.smallBkAcsButt.setObjectName(u"smallBkAcsButt")

        self.verticalLayout_9.addWidget(self.smallBkAcsButt)

        self.smallPlAcsButt = QCheckBox(self.verticalLayoutWidget_4)
        self.smallPlAcsButt.setObjectName(u"smallPlAcsButt")

        self.verticalLayout_9.addWidget(self.smallPlAcsButt)

        self.sallHldAcsButt = QCheckBox(self.verticalLayoutWidget_4)
        self.sallHldAcsButt.setObjectName(u"sallHldAcsButt")

        self.verticalLayout_9.addWidget(self.sallHldAcsButt)


        self.horizontalLayout_3.addLayout(self.verticalLayout_9)


        self.verticalLayout_4.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.applySettButt = QPushButton(self.verticalLayoutWidget_4)
        self.applySettButt.setObjectName(u"applySettButt")

        self.horizontalLayout_4.addWidget(self.applySettButt)

        self.pushButton = QPushButton(self.verticalLayoutWidget_4)
        self.pushButton.setObjectName(u"pushButton")

        self.horizontalLayout_4.addWidget(self.pushButton)


        self.verticalLayout_4.addLayout(self.horizontalLayout_4)

        self.settButt = QPushButton(PrintHelper)
        self.settButt.setObjectName(u"settButt")
        self.settButt.setGeometry(QRect(20, 350, 75, 23))
        self.lineEditPass = QLineEdit(PrintHelper)
        self.lineEditPass.setObjectName(u"lineEditPass")
        self.lineEditPass.setGeometry(QRect(100, 351, 113, 20))
        self.lineEditPass.setInputMethodHints(Qt.ImhHiddenText)
        self.frameSettings2 = QFrame(PrintHelper)
        self.frameSettings2.setObjectName(u"frameSettings2")
        self.frameSettings2.setGeometry(QRect(20, 90, 371, 281))
        self.frameSettings2.setFrameShape(QFrame.StyledPanel)
        self.frameSettings2.setFrameShadow(QFrame.Raised)
        self.lineEditMinRAM = QLineEdit(self.frameSettings2)
        self.lineEditMinRAM.setObjectName(u"lineEditMinRAM")
        self.lineEditMinRAM.setGeometry(QRect(10, 30, 113, 22))
        self.label_8 = QLabel(self.frameSettings2)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setGeometry(QRect(10, 10, 261, 16))
        self.frameSettings2.raise_()
        self.selectFileButt.raise_()
        self.label.raise_()
        self.label_2.raise_()
        self.mainPageButt.raise_()
        self.frameBig.raise_()
        self.frameMed.raise_()
        self.frameSmall.raise_()
        self.frameMain.raise_()
        self.settButt.raise_()
        self.lineEditPass.raise_()
        self.frameSettings.raise_()

        self.retranslateUi(PrintHelper)

        QMetaObject.connectSlotsByName(PrintHelper)
    # setupUi

    def retranslateUi(self, PrintHelper):
        PrintHelper.setWindowTitle(QCoreApplication.translate("PrintHelper", u"Print Helper", None))
        self.selectFileButt.setText(QCoreApplication.translate("PrintHelper", u"\u0412\u044b\u0431\u0435\u0440\u0438\u0442\u0435 \u0444\u0430\u0439\u043b", None))
        self.label.setText(QCoreApplication.translate("PrintHelper", u"\u0412\u044b\u0431\u0435\u0440\u0438\u0442\u0435 \u0444\u0430\u0439\u043b \u0441 \u0437\u0430\u043a\u0430\u0437\u043e\u043c:", None))
        self.label_2.setText(QCoreApplication.translate("PrintHelper", u"\u0412\u044b\u0431\u0435\u0440\u0438\u0442\u0435 \u0440\u0435\u0436\u0438\u043c \u0440\u0430\u0431\u043e\u0442\u044b", None))
        self.smallButt.setText(QCoreApplication.translate("PrintHelper", u"\u0421\u0438\u043b\u0438\u043a\u043e\u043d \u043c\u0430\u043b\u0435\u043d\u044c\u043a\u0438\u0439 \u0441\u0442\u0430\u043d\u043e\u043a (90*60)", None))
        self.smallButtBooks.setText(QCoreApplication.translate("PrintHelper", u"\u041a\u043d\u0438\u0436\u043a\u0438 \u043c\u0430\u043b\u0435\u043d\u044c\u043a\u0438\u0439 (90*60)", None))
        self.smallButtPlastins.setText(QCoreApplication.translate("PrintHelper", u"\u041f\u043b\u0430\u043d\u043a\u0438 \u043c\u0430\u043b\u0435\u043d\u043a\u0438\u0439 (90*60)", None))
        self.smallButtCartholders.setText(QCoreApplication.translate("PrintHelper", u"\u041a\u0430\u0440\u0442\u0445\u043e\u043b\u0434\u0435\u0440\u044b \u043c\u0430\u043b\u0435\u043d\u044c\u043a\u0438\u0439 (90*60)", None))
        self.bigButt.setText(QCoreApplication.translate("PrintHelper", u"\u0421\u0438\u043b\u0438\u043a\u043e\u043d \u0431\u043e\u043b\u044c\u0448\u043e\u0439 \u0441\u0442\u0430\u043d\u043e\u043a (3*2)", None))
        self.medButt.setText(QCoreApplication.translate("PrintHelper", u"\u0421\u0441\u0438\u043b\u0438\u043a\u043e\u043d \u0441\u0440\u0435\u0434\u043d\u0438\u0439 \u0441\u0442\u0430\u043d\u043e\u043a (105*160)", None))
        self.medButtBooks.setText(QCoreApplication.translate("PrintHelper", u"\u041a\u043d\u0438\u0436\u043a\u0438 \u0441\u0440\u0435\u0434\u043d\u0438\u0439 \u0441\u0442\u0430\u043d\u043e\u043a (105*160)", None))
        self.bigButtInt.setText(QCoreApplication.translate("PrintHelper", u"\u0411\u043e\u043b\u044c\u0448\u043e\u0439", None))
#if QT_CONFIG(shortcut)
        self.bigButtInt.setShortcut("")
#endif // QT_CONFIG(shortcut)
        self.smallButtInt.setText(QCoreApplication.translate("PrintHelper", u"\u041c\u0430\u043b\u0435\u043d\u044c\u043a\u0438\u0439", None))
        self.medButtInt.setText(QCoreApplication.translate("PrintHelper", u"\u0421\u0440\u0435\u0434\u043d\u0438\u0439", None))
        self.mainPageButt.setText(QCoreApplication.translate("PrintHelper", u"\u041d\u0430 \u0433\u043b\u0430\u0432\u043d\u0443\u044e \u043a \u0432\u044b\u0431\u043e\u0440\u0443 \u0441\u0442\u0430\u043d\u043a\u0430", None))
        self.label_3.setText(QCoreApplication.translate("PrintHelper", u"\u041a\u043d\u043e\u043f\u043a\u0438 \u043e\u0431\u043e\u0440\u0443\u0434\u043e\u0432\u0430\u043d\u0438\u044f", None))
        self.bigAcsButt.setText(QCoreApplication.translate("PrintHelper", u"\u0411\u043e\u043b\u044c\u0448\u043e\u0439", None))
        self.medAcsButt.setText(QCoreApplication.translate("PrintHelper", u"\u0421\u0440\u0435\u0434\u043d\u0438\u0439", None))
        self.smallAcsButt.setText(QCoreApplication.translate("PrintHelper", u"\u041c\u0430\u043b\u0435\u043d\u044c\u043a\u0438\u0439", None))
        self.label_5.setText(QCoreApplication.translate("PrintHelper", u"\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u0440\u0430\u0437\u043c\u0435\u0440 \u0432 \u043a\u043e\u043d\u0444\u0438\u0433\u0438", None))
        self.label_6.setText(QCoreApplication.translate("PrintHelper", u"\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u0440\u0430\u0437\u043c\u0435\u0440\u0430 1\u0421", None))
        self.label_7.setText(QCoreApplication.translate("PrintHelper", u"\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u0444\u0430\u0439\u043b\u0430", None))
        self.addSizeButt.setText(QCoreApplication.translate("PrintHelper", u"\u041f\u0440\u0438\u043c\u0435\u043d\u0438\u0442\u044c", None))
        self.pushButtonShowSizes.setText(QCoreApplication.translate("PrintHelper", u"\u041f\u043e\u043a\u0430\u0437\u0430\u0442\u044c \u0432\u0441\u0435 \u0440\u0430\u0437\u043c\u0435\u0440\u044b", None))
        self.label_4.setText(QCoreApplication.translate("PrintHelper", u"\u0414\u043e\u0441\u0442\u0443\u043f \u043a \u0440\u0430\u0441\u043a\u043b\u0430\u0434\u043a\u0430\u043c", None))
        self.bigSilAcsButt.setText(QCoreApplication.translate("PrintHelper", u"\u0421\u0438\u043b\u0438\u043a\u043e\u043d \u0431\u043e\u043b\u044c\u0448\u043e\u0439", None))
        self.medSilAcsButt.setText(QCoreApplication.translate("PrintHelper", u"\u0421\u0438\u043b\u0438\u043a\u043e\u043d \u0441\u0440\u0435\u0434\u043d\u0438\u0439", None))
        self.smallSilAcsButt.setText(QCoreApplication.translate("PrintHelper", u"\u0421\u0438\u043b\u0438\u043a\u043e\u043d \u043c\u0430\u043b\u0435\u043d\u044c\u043a\u0438\u0439", None))
        self.medBkAcsButt.setText(QCoreApplication.translate("PrintHelper", u"\u041a\u043d\u0438\u0436\u043a\u0438 \u0441\u0440\u0435\u0434\u043d\u0438\u0439", None))
        self.smallBkAcsButt.setText(QCoreApplication.translate("PrintHelper", u"\u041a\u043d\u0438\u0436\u043a\u0438 \u043c\u0430\u043b\u0435\u043d\u044c\u043a\u0438\u0439", None))
        self.smallPlAcsButt.setText(QCoreApplication.translate("PrintHelper", u"\u041f\u043b\u0430\u043d\u043a\u0438 \u043c\u0430\u043b\u0435\u043d\u044c\u043a\u0438\u0439", None))
        self.sallHldAcsButt.setText(QCoreApplication.translate("PrintHelper", u"\u041a\u0430\u0440\u0442\u0445\u043e\u043b\u0434\u0435\u0440\u044b \u043c\u0430\u043b\u0435\u043d\u044c\u043a\u0438\u0439", None))
        self.applySettButt.setText(QCoreApplication.translate("PrintHelper", u"\u041f\u0440\u0438\u043c\u0435\u043d\u0438\u0442\u044c", None))
        self.pushButton.setText(QCoreApplication.translate("PrintHelper", u"\u0421\u043b\u0435\u0434\u0443\u044e\u0449\u0435\u0435 \u043c\u0435\u043d\u044e", None))
        self.settButt.setText(QCoreApplication.translate("PrintHelper", u"\u041d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0438", None))
        self.label_8.setText(QCoreApplication.translate("PrintHelper", u"\u041c\u0438\u043d\u0438\u043c\u0443\u043c \u043f\u0430\u043c\u044f\u0442\u0438 \u0434\u043b\u044f \u043f\u0440\u0435\u0434\u0443\u043f\u0440\u0435\u0436\u0434\u0435\u043d\u0438\u044f, \u0413\u0431", None))
    # retranslateUi

