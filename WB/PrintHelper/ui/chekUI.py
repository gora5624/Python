pathTouiVesionFile = r'C:\Users\Public\Documents\WBHelpTools\PrintHelper\uiVesion.txt'
def chekUIVesion():
    pathTouiVesionFile = r'C:\Users\Public\Documents\WBHelpTools\PrintHelper\uiVesion.txt'
    with open(pathTouiVesionFile, 'r') as fileUI:
        uiVersion = fileUI.readline()
        fileUI.close()
        return uiVersion