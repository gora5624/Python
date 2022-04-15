from ftplib import FTP, all_errors
import ftplib
from os.path import join as joinPath, isdir, basename
from os import listdir
import time
import multiprocessing
import copy
start_time = time.time()

tgtDir = '/wordpress_1/public_html/upload'
imageFilesPath = r'F:\Для загрузки'
hostUrl = 'vh344.timeweb.ru'
login = ('cj15871','758wj3ZS5bp0')
uploadFileList=[]


def changeDir(path,exit=True,hostUrl=None,login=None,ftp=None):
    if ftp == None:
        while True:
            try:
                ftp = FTP(hostUrl)
                ftp.login(*login)
                break
            except:
                print('Ошибка')
                time.sleep(1)
                continue
    ftp.cwd('/')
    pathNew = path[len(ftp.pwd()):]
    if pathNew[-1] =='/':
        pathNew = pathNew[0:-1]
    b = ftp.pwd()
    for catalog in pathNew.split('/'):
        if ftp.pwd() == '/':
            newDir = ftp.pwd() + catalog
        else:
            newDir = ftp.pwd() + '/' + catalog
        a = ftp.nlst()
        if newDir.split('/')[-1] not in ftp.nlst():
            ftp.mkd(newDir)
            ftp.cwd(newDir)
        else:
            ftp.cwd(newDir)
    if exit:
        ftp.quit()
        return None
    else:
        return ftp

    
def scanDir(path,pathStart):
    if isdir(path):
        if listdir(path) != []:
            a =listdir(path)
            for att in listdir(path):
                newPath = joinPath(path, att)
                scanDir(newPath,pathStart)
    else:
        if path.replace(basename(path),'') not in uploadFileList:
            uploadFileList.append(path.replace(basename(path),''))


def uploadFile(pathToFile,pathFTP,ftp):
    ftp.cwd(pathFTP)
    file = basename(pathToFile)
    listAttFTP = ftp.nlst()
    if file not in listAttFTP:
        ftp.storbinary('STOR ' + file, open(pathToFile, 'rb'))
        print(file)
    listAttFTP = ftp.nlst()
    if file not in listAttFTP:
        print('Не удалось загрузить {}, пробую повторно'.format(file))
        uploadFile(pathToFile,pathFTP)
    ftp.quit()


def uploadFileFromDir(path,pathFTP):
    pool = multiprocessing.Pool(10)
    ftp = FTP(hostUrl, timeout=5000)
    ftp.login(*login)
    ftpN = copy.copy(ftp)
    for file in listdir(path):
        if file != 'Thumbs.db':
            pathToFile = joinPath(path, file)
            pool.apply_async(uploadFile, args=(pathToFile,pathFTP, ftpN, ))
    pool.close()
    pool.join()


def uploadMain(path):
    pathStart = copy.deepcopy(path)
    scanDir(path,pathStart)
    for path in uploadFileList:
        pathFTP = tgtDir + path.replace(pathStart,'').replace('\\','/')
        #changeDir(pathFTP,hostUrl=hostUrl,login=login)
    i = 0
    for path in uploadFileList:    
        pathFTP = tgtDir + path.replace(pathStart,'').replace('\\','/')
        p = multiprocessing.Process(target=uploadFileFromDir, args=(path,pathFTP, ))
        i += 1
        if i >= 1:
            p.start()
            p.join()
            i = 0
    p.join()

if __name__ =='__main__':
    uploadMain(imageFilesPath)
    print("--- %s seconds ---" % (time.time() - start_time))