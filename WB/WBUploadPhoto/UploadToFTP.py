from ftplib import FTP, all_errors
import ftplib
from os.path import join as joinPath, isdir, basename
from os import listdir
import time
import multiprocessing
import copy
start_time = time.time()

tgtDir = '/wordpress_1/public_html/upload'
imageFilesPath = r'F:\Готовые принты'
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
        #uploadFile(path, ftp)




# def uploadFile(path,pathStart, hostUrl, login):
#     ftp = FTP(hostUrl)
#     ftp.login(*login)
#     ftp = changeDir(tgtDir + path.replace(pathStart,'').replace('\\'+basename(path),'').replace('\\','/'), ftp=ftp, exit=False)
#     listAttFTP = ftp.nlst()
#     if basename(path) not in listAttFTP:
#         ftp.storbinary('STOR ' + basename(path), open(path, 'rb'))
#         listAttFTP = ftp.nlst()
#         if basename(path) not in listAttFTP:
#             print('Не удалось загрузить {}, пробую повторно'.format(path))
#             uploadFile(path,pathStart, hostUrl, login)
#         print(basename(path))
#     ftp.quit()



# def uploadFile(path, ftp):
#     ftp = changeDir(tgtDir + path.replace(pathStart,'').replace('\\'+basename(path),'').replace('\\','/'), ftp=ftp, exit=False)
#     listAttFTP = ftp.nlst()
#     if basename(path) not in listAttFTP:
#         ftp.storbinary('STOR ' + basename(path), open(path, 'rb'))


# def uploadFile(path,pathFTP):
#     print(path)
#     ftp = FTP(hostUrl)
#     ftp.login(*login)
#     ftp.cwd(pathFTP)
#     a = listdir(path)
#     for file in listdir(path):
#         listAttFTP = ftp.nlst()
#         if file not in listAttFTP:
#             ftp.storbinary('STOR ' + file, open(joinPath(path, file), 'rb'))
#             listAttFTP = ftp.nlst()
#             if file not in listAttFTP:
#                 print('Не удалось загрузить {}, пробую повторно'.format(path))
#                 uploadFile(path, file, ftp)
#             print(file)
#     ftp.quit()



def uploadFile(pathToFile,pathFTP):
    while True:
        try:
            ftp = FTP(hostUrl, timeout=5000)
            ftp.login(*login)
            break
        except all_errors:
            print('Ошибка')
            time.sleep(1)
            continue
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
    for file in listdir(path):
        pathToFile = joinPath(path, file)
        pool.apply_async(uploadFile, args=(pathToFile,pathFTP, ))
    pool.close()
    pool.join()






def uploadMain(path):
    pathStart = copy.deepcopy(path)
    scanDir(path,pathStart)
    for path in uploadFileList:
        pathFTP = tgtDir + path.replace(pathStart,'').replace('\\','/')
        changeDir(pathFTP,hostUrl=hostUrl,login=login)
    for path in uploadFileList:    
        pathFTP = tgtDir + path.replace(pathStart,'').replace('\\','/')
        p = multiprocessing.Process(target=uploadFileFromDir, args=(path,pathFTP,))
        # uploadFile(file, hostUrl=hostUrl, login=login)
        p.start()
    p.join()
    # ftp.quit()


# def uploadMain(path):
#     pathStart = copy.deepcopy(path)
#     ftp = FTP(hostUrl)
#     ftp.login(*login)
#     scanDir(path,pathStart, ftp)
#     pool = multiprocessing.Pool(1)
#     for file in uploadFileList.keys():
#         pool.apply_async(uploadFile, args=(file,pathStart, hostUrl, login,))
#         # uploadFile(file, hostUrl=hostUrl, login=login)
#     pool.close()
#     pool.join()
#     # ftp.quit()


if __name__ =='__main__':
    uploadMain(imageFilesPath)
    print("--- %s seconds ---" % (time.time() - start_time))

# Устарело
# def uploadFileFromDir(pathScrLoc, pathTrgFTP,exit=True,hostUrl=None,login=None, ftp=None):
#     try:
#         ftp.voidcmd("NOOP")
#     except:
#         ftp = FTP(hostUrl)
#         ftp.login(*login)
#     ftp.cwd(pathTrgFTP)    
#     for file in listdir(pathScrLoc):
#         ftp.storbinary('STOR ' + file, open(joinPath(pathScrLoc, file), 'rb'))
#     if exit:
#         ftp.quit()






# if __name__ == '__main__':
#     for model in listdir(imageFilesPath):
#         for color in listdir(joinPath(imageFilesPath, model)):
#             ftp = changeDir(tgtDir + model + '/' + color.lower(),hostUrl=hostUrl, login=login, exit=False)
#             uploadFileFromDir(joinPath(imageFilesPath, model, color), tgtDir + model + '/' + color.lower(), ftp=ftp)