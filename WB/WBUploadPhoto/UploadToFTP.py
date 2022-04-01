from ftplib import FTP, error_perm
from os.path import join as joinPath, isdir, basename
from os import listdir
import time
import asyncio
start_time = time.time()

tgtDir = '/wordpress_1/public_html/upload'
imageFilesPath = r'F:\Готовые принты\test'
hostUrl = 'vh344.timeweb.ru'
login = ('cj15871','758wj3ZS5bp0')
pathStart = ''
uploadFileList=[]


def changeDir(path,exit=True,hostUrl=None,login=None,ftp=None):
    if ftp == None:
        ftp = FTP(hostUrl)
        ftp.login(*login)
    ftp.cwd('/')
    pathNew = path[len(ftp.pwd()):]
    for catalog in pathNew.split('/'):
        if ftp.pwd() == '/':
            newDir = ftp.pwd() + catalog
        else:
            newDir = ftp.pwd() + '/' + catalog
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

    

def scanDir(path, ftp):
    if isdir(path):
        if listdir(path) != []:
            for att in listdir(path):
                newPath = joinPath(path, att)
                scanDir(newPath, ftp)
        else:
            ftp = changeDir(tgtDir + path.replace(pathStart,'').replace('\\','/'), ftp=ftp, exit=False)
    else:
        uploadFileList.append(path)
        #uploadFile(path, ftp)




async def uploadFile(path, ftp):
    ftp = changeDir(tgtDir + path.replace(pathStart,'').replace('\\'+basename(path),'').replace('\\','/'), ftp=ftp, exit=False)
    listAttFTP = ftp.nlst()
    if basename(path) not in listAttFTP:
        ftp.storbinary('STOR ' + basename(path), open(path, 'rb'))


# def uploadFile(path, ftp):
#     ftp = changeDir(tgtDir + path.replace(pathStart,'').replace('\\'+basename(path),'').replace('\\','/'), ftp=ftp, exit=False)
#     listAttFTP = ftp.nlst()
#     if basename(path) not in listAttFTP:
#         ftp.storbinary('STOR ' + basename(path), open(path, 'rb'))

def uploadMain(path):
    global pathStart
    pathStart = path
    ftp = FTP(hostUrl)
    ftp.login(*login)
    scanDir(path, ftp)
    ioloop = asyncio.get_event_loop()
    tasks = []
    for file in uploadFileList:
        tasks.append(ioloop.create_task(uploadFile(file, ftp)))
        # uploadFile(file, ftp)
    wait_tasks = asyncio.wait(tasks)
    ioloop.run_until_complete(wait_tasks)
    ioloop.close()
    ftp.quit()


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