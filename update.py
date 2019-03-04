import os
import urllib.request, json
import sys
from PySide2.QtWidgets import QApplication, QLabel
def getFile(path):
    return  [os.path.join(r,file) for r,d,f in os.walk(path) for file in f]

def updateSizePython(files):
    for i in range(len(files)):
        statinfo = os.stat(files[i])
        files[i] =  files[i].replace('./', '')
        files[i] =  files[i].replace('\\', '/')
        files[i] = [files[i], statinfo.st_size]
    return files


def getDataDiff():
    with urllib.request.urlopen("http://update.sevenonline.fr") as url:
        data = json.loads(url.read().decode())
    return (data)
def downloadfile(file):
    print('http://update.sevenonline.fr/' +  file[0])
    url = 'http://update.sevenonline.fr/' + file[0]

    path = "./"
    dir = file[0].split("/")
    del dir[len(dir) - 1]
    for pathcut in dir:
        path = path + pathcut + "/"
    #print("Creation du dossier : " + path)
    if os.path.isdir(path):
        print ("[+] Path " + path + " OK")
    else:
        os.makedirs(path)
    try:
        urllib.request.urlretrieve(url, './' + file[0])
    except FileNotFoundError:
        print ("[-] Erreur lors de la copie du fichier")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    label = QLabel("Hello World")
    label.show()

    print("Update Sevenonline")
    files = getFile("./")
    files = updateSizePython(files)
    dataremote = getDataDiff()
    #print (dataremote)
    #print (files)
    diff = lambda l1,l2: [x for x in l1 if x not in l2]

    #à DL = diff(dataremote,files)
    #a remove = diff(files, dataremote)
    download = diff(dataremote,files)
    for i in range(len(download)):
        print (download[i])
        downloadfile(download[i])
    sys.exit(app.exec_())
    #print (diff(files, dataremote))
    #input("")
    #diffFiles = diff(dataremote, files)
