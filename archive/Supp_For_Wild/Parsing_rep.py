import xlrd


def GetDataNanoglass(NanoPath):

    Book = xlrd.open_workbook(os.path.join(NanoPath))
    Sheet = Book.sheet_by_index(0)
    ListRowTit = Sheet.
