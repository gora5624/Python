# Form implementation generated from reading ui file 'e:\MyProduct\Python\WB\PrintHelper\ui\printHelperUIV2.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_PrintHelper(object):
    def setupUi(self, PrintHelper):
        PrintHelper.setObjectName("PrintHelper")
        PrintHelper.resize(422, 385)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(PrintHelper.sizePolicy().hasHeightForWidth())
        PrintHelper.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setKerning(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferDefault)
        PrintHelper.setFont(font)
        PrintHelper.setStyleSheet("")
        self.selectFileButt = QtWidgets.QPushButton(parent=PrintHelper)
        self.selectFileButt.setGeometry(QtCore.QRect(20, 30, 381, 41))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setKerning(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferDefault)
        self.selectFileButt.setFont(font)
        self.selectFileButt.setStyleSheet("")
        self.selectFileButt.setObjectName("selectFileButt")
        self.label = QtWidgets.QLabel(parent=PrintHelper)
        self.label.setGeometry(QtCore.QRect(20, -1, 381, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(False)
        font.setKerning(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferDefault)
        self.label.setFont(font)
        self.label.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(parent=PrintHelper)
        self.label_2.setGeometry(QtCore.QRect(20, 70, 381, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setKerning(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferDefault)
        self.label_2.setFont(font)
        self.label_2.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.label_2.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.label_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.frameSmall = QtWidgets.QFrame(parent=PrintHelper)
        self.frameSmall.setGeometry(QtCore.QRect(20, 100, 381, 251))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setKerning(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferDefault)
        self.frameSmall.setFont(font)
        self.frameSmall.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.frameSmall.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.frameSmall.setMidLineWidth(0)
        self.frameSmall.setObjectName("frameSmall")
        self.verticalLayoutWidget_3 = QtWidgets.QWidget(parent=self.frameSmall)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(0, 0, 381, 241))
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.smallButt = QtWidgets.QPushButton(parent=self.verticalLayoutWidget_3)
        self.smallButt.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.smallButt.sizePolicy().hasHeightForWidth())
        self.smallButt.setSizePolicy(sizePolicy)
        self.smallButt.setObjectName("smallButt")
        self.verticalLayout_3.addWidget(self.smallButt)
        self.smallButtBooks = QtWidgets.QPushButton(parent=self.verticalLayoutWidget_3)
        self.smallButtBooks.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.smallButtBooks.sizePolicy().hasHeightForWidth())
        self.smallButtBooks.setSizePolicy(sizePolicy)
        self.smallButtBooks.setObjectName("smallButtBooks")
        self.verticalLayout_3.addWidget(self.smallButtBooks)
        self.smallButtPlastins = QtWidgets.QPushButton(parent=self.verticalLayoutWidget_3)
        self.smallButtPlastins.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.smallButtPlastins.sizePolicy().hasHeightForWidth())
        self.smallButtPlastins.setSizePolicy(sizePolicy)
        self.smallButtPlastins.setObjectName("smallButtPlastins")
        self.verticalLayout_3.addWidget(self.smallButtPlastins)
        self.smallButtCartholders = QtWidgets.QPushButton(parent=self.verticalLayoutWidget_3)
        self.smallButtCartholders.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.smallButtCartholders.sizePolicy().hasHeightForWidth())
        self.smallButtCartholders.setSizePolicy(sizePolicy)
        self.smallButtCartholders.setObjectName("smallButtCartholders")
        self.verticalLayout_3.addWidget(self.smallButtCartholders)
        self.frameBig = QtWidgets.QFrame(parent=PrintHelper)
        self.frameBig.setGeometry(QtCore.QRect(20, 100, 381, 151))
        self.frameBig.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.frameBig.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.frameBig.setLineWidth(1)
        self.frameBig.setObjectName("frameBig")
        self.verticalLayoutWidget = QtWidgets.QWidget(parent=self.frameBig)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 381, 141))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetDefaultConstraint)
        self.verticalLayout.setContentsMargins(0, 4, 0, 4)
        self.verticalLayout.setSpacing(8)
        self.verticalLayout.setObjectName("verticalLayout")
        self.bigButt = QtWidgets.QPushButton(parent=self.verticalLayoutWidget)
        self.bigButt.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bigButt.sizePolicy().hasHeightForWidth())
        self.bigButt.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setKerning(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferDefault)
        self.bigButt.setFont(font)
        self.bigButt.setIconSize(QtCore.QSize(32, 32))
        self.bigButt.setFlat(False)
        self.bigButt.setObjectName("bigButt")
        self.verticalLayout.addWidget(self.bigButt)
        self.bigButtBooks = QtWidgets.QPushButton(parent=self.verticalLayoutWidget)
        self.bigButtBooks.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bigButtBooks.sizePolicy().hasHeightForWidth())
        self.bigButtBooks.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setKerning(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferDefault)
        self.bigButtBooks.setFont(font)
        self.bigButtBooks.setIconSize(QtCore.QSize(32, 32))
        self.bigButtBooks.setFlat(False)
        self.bigButtBooks.setObjectName("bigButtBooks")
        self.verticalLayout.addWidget(self.bigButtBooks)
        self.frameMed = QtWidgets.QFrame(parent=PrintHelper)
        self.frameMed.setGeometry(QtCore.QRect(20, 100, 381, 141))
        self.frameMed.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.frameMed.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frameMed.setObjectName("frameMed")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(parent=self.frameMed)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(0, 0, 381, 146))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetMinimumSize)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.medButt = QtWidgets.QPushButton(parent=self.verticalLayoutWidget_2)
        self.medButt.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.medButt.sizePolicy().hasHeightForWidth())
        self.medButt.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setKerning(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferDefault)
        self.medButt.setFont(font)
        self.medButt.setObjectName("medButt")
        self.verticalLayout_2.addWidget(self.medButt)
        self.medButtBooks = QtWidgets.QPushButton(parent=self.verticalLayoutWidget_2)
        self.medButtBooks.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.medButtBooks.sizePolicy().hasHeightForWidth())
        self.medButtBooks.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setKerning(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferDefault)
        self.medButtBooks.setFont(font)
        self.medButtBooks.setObjectName("medButtBooks")
        self.verticalLayout_2.addWidget(self.medButtBooks)
        self.frameMain = QtWidgets.QFrame(parent=PrintHelper)
        self.frameMain.setGeometry(QtCore.QRect(20, 90, 381, 261))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frameMain.sizePolicy().hasHeightForWidth())
        self.frameMain.setSizePolicy(sizePolicy)
        self.frameMain.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.frameMain.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frameMain.setObjectName("frameMain")
        self.verticalLayoutWidget_5 = QtWidgets.QWidget(parent=self.frameMain)
        self.verticalLayoutWidget_5.setGeometry(QtCore.QRect(0, 5, 381, 251))
        self.verticalLayoutWidget_5.setObjectName("verticalLayoutWidget_5")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_5)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.bigButtInt = QtWidgets.QPushButton(parent=self.verticalLayoutWidget_5)
        self.bigButtInt.setStyleSheet("")
        self.bigButtInt.setIconSize(QtCore.QSize(236, 130))
        self.bigButtInt.setShortcut("")
        self.bigButtInt.setObjectName("bigButtInt")
        self.verticalLayout_5.addWidget(self.bigButtInt)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.smallButtInt = QtWidgets.QPushButton(parent=self.verticalLayoutWidget_5)
        self.smallButtInt.setEnabled(True)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 120, 215))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Highlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(240, 240, 240))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Highlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 120, 215))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Highlight, brush)
        self.smallButtInt.setPalette(palette)
        self.smallButtInt.setStyleSheet("")
        self.smallButtInt.setIconSize(QtCore.QSize(112, 200))
        self.smallButtInt.setObjectName("smallButtInt")
        self.horizontalLayout.addWidget(self.smallButtInt)
        self.medButtInt = QtWidgets.QPushButton(parent=self.verticalLayoutWidget_5)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 120, 215))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Highlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(240, 240, 240))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Highlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 120, 215))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Highlight, brush)
        self.medButtInt.setPalette(palette)
        self.medButtInt.setStyleSheet("")
        self.medButtInt.setIconSize(QtCore.QSize(119, 200))
        self.medButtInt.setObjectName("medButtInt")
        self.horizontalLayout.addWidget(self.medButtInt)
        self.verticalLayout_5.addLayout(self.horizontalLayout)
        self.mainPageButt = QtWidgets.QPushButton(parent=PrintHelper)
        self.mainPageButt.setGeometry(QtCore.QRect(220, 350, 181, 31))
        self.mainPageButt.setObjectName("mainPageButt")
        self.frameSettings = QtWidgets.QFrame(parent=PrintHelper)
        self.frameSettings.setGeometry(QtCore.QRect(20, 90, 381, 281))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frameSettings.sizePolicy().hasHeightForWidth())
        self.frameSettings.setSizePolicy(sizePolicy)
        self.frameSettings.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frameSettings.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frameSettings.setObjectName("frameSettings")
        self.verticalLayoutWidget_4 = QtWidgets.QWidget(parent=self.frameSettings)
        self.verticalLayoutWidget_4.setGeometry(QtCore.QRect(9, 0, 361, 329))
        self.verticalLayoutWidget_4.setObjectName("verticalLayoutWidget_4")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_4)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetFixedSize)
        self.horizontalLayout_2.setContentsMargins(-1, -1, -1, 0)
        self.horizontalLayout_2.setSpacing(12)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setContentsMargins(-1, -1, 0, 0)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.label_3 = QtWidgets.QLabel(parent=self.verticalLayoutWidget_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        font.setKerning(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferDefault)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_6.addWidget(self.label_3)
        self.bigAcsButt = QtWidgets.QCheckBox(parent=self.verticalLayoutWidget_4)
        self.bigAcsButt.setObjectName("bigAcsButt")
        self.verticalLayout_6.addWidget(self.bigAcsButt)
        self.medAcsButt = QtWidgets.QCheckBox(parent=self.verticalLayoutWidget_4)
        self.medAcsButt.setObjectName("medAcsButt")
        self.verticalLayout_6.addWidget(self.medAcsButt)
        self.smallAcsButt = QtWidgets.QCheckBox(parent=self.verticalLayoutWidget_4)
        self.smallAcsButt.setObjectName("smallAcsButt")
        self.verticalLayout_6.addWidget(self.smallAcsButt)
        self.horizontalLayout_2.addLayout(self.verticalLayout_6)
        self.verticalLayout_8 = QtWidgets.QVBoxLayout()
        self.verticalLayout_8.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetFixedSize)
        self.verticalLayout_8.setContentsMargins(39, -1, 0, 0)
        self.verticalLayout_8.setSpacing(0)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.label_5 = QtWidgets.QLabel(parent=self.verticalLayoutWidget_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_8.addWidget(self.label_5)
        self.label_6 = QtWidgets.QLabel(parent=self.verticalLayoutWidget_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(False)
        font.setKerning(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferDefault)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_8.addWidget(self.label_6)
        self.lineEdit = QtWidgets.QLineEdit(parent=self.verticalLayoutWidget_4)
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout_8.addWidget(self.lineEdit)
        self.label_7 = QtWidgets.QLabel(parent=self.verticalLayoutWidget_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(False)
        font.setKerning(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferDefault)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.verticalLayout_8.addWidget(self.label_7)
        self.lineEdit_2 = QtWidgets.QLineEdit(parent=self.verticalLayoutWidget_4)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.verticalLayout_8.addWidget(self.lineEdit_2)
        self.pushButton = QtWidgets.QPushButton(parent=self.verticalLayoutWidget_4)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout_8.addWidget(self.pushButton)
        self.horizontalLayout_2.addLayout(self.verticalLayout_8)
        self.verticalLayout_4.addLayout(self.horizontalLayout_2)
        self.label_4 = QtWidgets.QLabel(parent=self.verticalLayoutWidget_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_4.addWidget(self.label_4)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.bigSilAcsButt = QtWidgets.QCheckBox(parent=self.verticalLayoutWidget_4)
        self.bigSilAcsButt.setObjectName("bigSilAcsButt")
        self.verticalLayout_7.addWidget(self.bigSilAcsButt)
        self.bigBkAcsButt = QtWidgets.QCheckBox(parent=self.verticalLayoutWidget_4)
        self.bigBkAcsButt.setObjectName("bigBkAcsButt")
        self.verticalLayout_7.addWidget(self.bigBkAcsButt)
        self.medSilAcsButt = QtWidgets.QCheckBox(parent=self.verticalLayoutWidget_4)
        self.medSilAcsButt.setObjectName("medSilAcsButt")
        self.verticalLayout_7.addWidget(self.medSilAcsButt)
        self.smallSilAcsButt = QtWidgets.QCheckBox(parent=self.verticalLayoutWidget_4)
        self.smallSilAcsButt.setObjectName("smallSilAcsButt")
        self.verticalLayout_7.addWidget(self.smallSilAcsButt)
        self.horizontalLayout_3.addLayout(self.verticalLayout_7)
        self.verticalLayout_9 = QtWidgets.QVBoxLayout()
        self.verticalLayout_9.setSpacing(0)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.medBkAcsButt = QtWidgets.QCheckBox(parent=self.verticalLayoutWidget_4)
        self.medBkAcsButt.setObjectName("medBkAcsButt")
        self.verticalLayout_9.addWidget(self.medBkAcsButt)
        self.smallBkAcsButt = QtWidgets.QCheckBox(parent=self.verticalLayoutWidget_4)
        self.smallBkAcsButt.setObjectName("smallBkAcsButt")
        self.verticalLayout_9.addWidget(self.smallBkAcsButt)
        self.smallPlAcsButt = QtWidgets.QCheckBox(parent=self.verticalLayoutWidget_4)
        self.smallPlAcsButt.setObjectName("smallPlAcsButt")
        self.verticalLayout_9.addWidget(self.smallPlAcsButt)
        self.sallHldAcsButt = QtWidgets.QCheckBox(parent=self.verticalLayoutWidget_4)
        self.sallHldAcsButt.setObjectName("sallHldAcsButt")
        self.verticalLayout_9.addWidget(self.sallHldAcsButt)
        self.horizontalLayout_3.addLayout(self.verticalLayout_9)
        self.verticalLayout_4.addLayout(self.horizontalLayout_3)
        self.applySettButt = QtWidgets.QPushButton(parent=self.verticalLayoutWidget_4)
        self.applySettButt.setObjectName("applySettButt")
        self.verticalLayout_4.addWidget(self.applySettButt)
        self.oldNewButt = QtWidgets.QPushButton(parent=self.verticalLayoutWidget_4)
        self.oldNewButt.setObjectName("oldNewButt")
        self.verticalLayout_4.addWidget(self.oldNewButt)
        self.settButt = QtWidgets.QPushButton(parent=PrintHelper)
        self.settButt.setGeometry(QtCore.QRect(20, 350, 75, 23))
        self.settButt.setObjectName("settButt")
        self.lineEditPass = QtWidgets.QLineEdit(parent=PrintHelper)
        self.lineEditPass.setGeometry(QtCore.QRect(100, 351, 113, 20))
        self.lineEditPass.setInputMethodHints(QtCore.Qt.InputMethodHint.ImhHiddenText)
        self.lineEditPass.setObjectName("lineEditPass")
        self.selectFileButt.raise_()
        self.label.raise_()
        self.label_2.raise_()
        self.mainPageButt.raise_()
        self.frameMed.raise_()
        self.frameSmall.raise_()
        self.frameMain.raise_()
        self.settButt.raise_()
        self.lineEditPass.raise_()
        self.frameSettings.raise_()
        self.frameBig.raise_()

        self.retranslateUi(PrintHelper)
        QtCore.QMetaObject.connectSlotsByName(PrintHelper)

    def retranslateUi(self, PrintHelper):
        _translate = QtCore.QCoreApplication.translate
        PrintHelper.setWindowTitle(_translate("PrintHelper", "Print Helper"))
        self.selectFileButt.setText(_translate("PrintHelper", "Выберите файл"))
        self.label.setText(_translate("PrintHelper", "Выберите файл с заказом:"))
        self.label_2.setText(_translate("PrintHelper", "Выберите режим работы"))
        self.smallButt.setText(_translate("PrintHelper", "Силикон маленький станок (90*60)"))
        self.smallButtBooks.setText(_translate("PrintHelper", "Книжки маленький (90*60)"))
        self.smallButtPlastins.setText(_translate("PrintHelper", "Планки маленкий (90*60)"))
        self.smallButtCartholders.setText(_translate("PrintHelper", "Картхолдеры маленький (90*60)"))
        self.bigButt.setText(_translate("PrintHelper", "Силикон большой станок (3*2)"))
        self.bigButtBooks.setText(_translate("PrintHelper", "Книжки большой станок (3*2)"))
        self.medButt.setText(_translate("PrintHelper", "Ссиликон средний станок (105*160)"))
        self.medButtBooks.setText(_translate("PrintHelper", "Книжки средний станок (105*160)"))
        self.bigButtInt.setText(_translate("PrintHelper", "Большой"))
        self.smallButtInt.setText(_translate("PrintHelper", "Маленький"))
        self.medButtInt.setText(_translate("PrintHelper", "Средний"))
        self.mainPageButt.setText(_translate("PrintHelper", "На главную к выбору станка"))
        self.label_3.setText(_translate("PrintHelper", "Кнопки оборудования"))
        self.bigAcsButt.setText(_translate("PrintHelper", "Большой"))
        self.medAcsButt.setText(_translate("PrintHelper", "Средний"))
        self.smallAcsButt.setText(_translate("PrintHelper", "Маленький"))
        self.label_5.setText(_translate("PrintHelper", "Добавить размер в конфиги"))
        self.label_6.setText(_translate("PrintHelper", "Название размера 1С"))
        self.label_7.setText(_translate("PrintHelper", "Название файла"))
        self.pushButton.setText(_translate("PrintHelper", "Применить"))
        self.label_4.setText(_translate("PrintHelper", "Доступ к раскладкам"))
        self.bigSilAcsButt.setText(_translate("PrintHelper", "Силикон большой"))
        self.bigBkAcsButt.setText(_translate("PrintHelper", "Книжки большой"))
        self.medSilAcsButt.setText(_translate("PrintHelper", "Силикон средний"))
        self.smallSilAcsButt.setText(_translate("PrintHelper", "Силикон маленький"))
        self.medBkAcsButt.setText(_translate("PrintHelper", "Книжки средний"))
        self.smallBkAcsButt.setText(_translate("PrintHelper", "Книжки маленький"))
        self.smallPlAcsButt.setText(_translate("PrintHelper", "Планки маленький"))
        self.sallHldAcsButt.setText(_translate("PrintHelper", "Картхолдеры маленький"))
        self.applySettButt.setText(_translate("PrintHelper", "Применить"))
        self.oldNewButt.setText(_translate("PrintHelper", "Вернуть старый интерфейс"))
        self.settButt.setText(_translate("PrintHelper", "Настройки"))
