from PyQt6 import QtWidgets, QtCore
from PyQt6 import QtGui
from ui.ui_spyBot import Ui_SpyBot
import pandas as pd
import json
from os.path import exists

class SpyBot(QtWidgets.QMainWindow):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("SpyBot")
        self.ui = Ui_SpyBot()
        self.ui.setupUi(self)
        #self.ui.columnView
        # testOne = ['One_one', 'One_two', 'One_three']
        # testTwo = [['1_1','1_2','1_3'], ['2_1', '2_2', '2_3'], ['3_1', '3_2', '3_3']]
        # testThree = [[['1_1_1', '1_1_2', '1_1_3'], ['1_2_1', '1_2_2', '1_2_3'], ['1_3_1', '1_3_2', '1_3_3']], [['2_1_1', '2_1_2', '2_1_3'], ['2_2_1', '2_2_2', '2_2_3'], ['2_3_1', '2_3_2', '2_3_3']], [['3_1_1', '3_1_2', '3_1_3'], ['3_2_1', '3_2_2', '3_2_3'], ['3_3_1', '3_3_2', '3_3_3']]]
        # self.model = QtGui.QStandardItemModel()
        # for i_one, one in enumerate(testOne):
        #     oneModel = QtGui.QStandardItem(one)
        #     for i_two, two in enumerate(testTwo[i_one]):
        #         twoModel = QtGui.QStandardItem(two)
        #         oneModel.appendRow(twoModel)
        #         for i_three, three in enumerate(testThree[i_one][i_two]):
        #             threeModel = QtGui.QStandardItem(three)
        #             twoModel.appendRow(threeModel)
        #     self.model.appendRow(oneModel)
        # self.ui.columnView.setModel(self.model)
        self.pathToListNom = r'\\192.168.0.33\shared\_Общие документы_\Егор\ШК\Список стандартный поиск номенклатура.txt'
        self.listNom = pd.read_table(self.pathToListNom, sep='\t', dtype=str)
        # print(self.listNom)['Наименование']
        self.ui.comboBoxChooseNom.addItems(self.listNom['Наименование'].to_list())
        self.ui.comboBoxChooseNom.setEditable(True)
        self.ui.comboBoxChooseNom.setInsertPolicy(QtWidgets.QComboBox.InsertPolicy.NoInsert)
        self.ui.comboBoxChooseNom.completer().setCompletionMode(QtWidgets.QCompleter.CompletionMode.PopupCompletion)
        self.ui.comboBoxChooseNom.addItems(self.listNom['Наименование'].to_list())
        self.ui.pushButtonAddItem.clicked.connect(self.addItem)
        self.DBpath = r'D:\Python\WB\shyBot\DB.json'
        self.data = []
        self.readDBJson()
        self.initView()
        # self.data = []
        

    def initView(self):
        for item in self.data:
            self.ui.columnViewAlreadySpy.fi



    def addItem(self):
        nom = self.ui.comboBoxChooseNom.currentText()
        art = self.ui.lineEditAddWBId.text()
        self.data.append({
            'Name':nom,
            'Art':art,
        })
        self.makeDBjson()

    def readDBJson(self):
        if exists(self.DBpath):
            with open(self.DBpath, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
                # print(self.data)
                f.close()

    
    def makeDBjson(self):
        with open(self.DBpath, 'w', encoding='utf-8') as f:
            json.dump(self.data, f)
            f.close()





if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = SpyBot()
    window.show()
    app.exec()
