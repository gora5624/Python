import pandas
import os

def updateFileForUpload(self):
        self.vendorCodesAndBarcodes = self.vendorCodesAndBarcodes.set_index('Артикул товара')
        self.vendorCodesAndBarcodes = self.vendorCodesAndBarcodes.reindex(index=self.data['Артикул товара'])
        self.vendorCodesAndBarcodes = self.vendorCodesAndBarcodes.reset_index()
        self.data['Баркод товара'] = self.vendorCodesAndBarcodes['Баркоды']
        self.dataDict = self.data.to_dict('records')
        self.dataDictNew = []
        for i, line in enumerate(self.dataDict):
            if len(line['Баркод товара']) > 1:
                for barcode in line['Баркод товара']:
                    lineNew = copy.deepcopy(line)
                    tmp = {'Баркод товара':barcode}
                    lineNew.update(tmp)
                    self.dataDictNew.append(lineNew)
            else:
                tmp = {'Баркод товара':''.join(line['Баркод товара'])}
                line.update(tmp)
                self.dataDictNew.append(line)
        df = pandas.DataFrame(self.dataDictNew)
        df.to_excel(self.pathToFileForUpload, index=False)


def main():
    mainPath = r'F:\Для загрузки\Готовые принты'
    data = pandas.read_excel(r"F:\Маски силикон\карточки.xlsx")
    for file in os.listdir(mainPath):
        if '.xlsx' in file:
            df = pandas.read_excel(os.path.join(mainPath, file))
            dfNew = df['Баркод товара'] = data.loc[data['Артикул товара'] == df['Артикул продавца']]['Баркод']
            dfNew.to_excel(os.path.join(r'F:\для 1с',file),index=False)


main()

