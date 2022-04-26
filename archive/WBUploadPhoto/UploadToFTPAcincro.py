import aioftp
from os.path import join as joinPath, isdir, basename
from os import listdir
import time
import asyncio
start_time = time.time()

tgtDir = '/wordpress_1/public_html/upload'
imageFilesPath = r'F:\Для загрузки'
hostUrl = 'vh344.timeweb.ru'
login = ('cj15871','758wj3ZS5bp0')
sem = asyncio.Semaphore(7)

async def download(filePath, ftpPath):
    async with sem:
        client = aioftp.Client()
        while True:
            try:
                await client.connect(hostUrl)
                await client.login('cj15871','758wj3ZS5bp0')
                await client.upload(filePath, ftpPath, write_into=True)
                await client.quit()
                break
            except OSError:
                print('ошибка {}'.format(filePath))
                await asyncio.sleep(5)
                continue


def scanDir(path):
    listToUpload = []
    if isdir(path):
        for stuff in listdir(path):
            pathNew = joinPath(path, stuff)
            if not isdir(pathNew):
                listToUpload.append(pathNew)
            else:
                listToUpload.extend(scanDir(pathNew))
        return listToUpload
    else:
        listToUpload.append(pathNew)
    return listToUpload


async def createDirs(listToUpload):
    listToCreate = []
    for file in listToUpload:
        folder = file.replace('\\'+basename(file),'')
        if folder not in listToCreate:
            listToCreate.append(folder)
    for folder in listToCreate:
        folderFTP = folder.replace(imageFilesPath,tgtDir).replace('\\','/')
        client = aioftp.Client(socket_timeout=10)
        await client.connect(hostUrl)
        await client.login('cj15871','758wj3ZS5bp0')
        await client.make_directory(folderFTP)
        await client.quit()

async def main():
    listToUpload = scanDir(imageFilesPath)
    await createDirs(listToUpload)
    # await asyncio.wait([asyncio.create_task(createDirs(listToUpload))])
    tasks = []
    for filePath in listToUpload:
        ftpPath = filePath.replace(imageFilesPath, tgtDir).replace('\\','/')
        tasks.append(asyncio.create_task(download(filePath, ftpPath)))
    await asyncio.wait(tasks)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
    print("--- %s seconds ---" % (time.time() - start_time))