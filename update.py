import os
import urllib.request, json
import sys
from PySide2.QtWidgets import QApplication, QLabel, QProgressBar, QWidget, QTextEdit, QPushButton
from PySide2 import *
from time import sleep

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

def downloadfile(file, progressBar, pourcent, textarea):
    oldText = textarea.toPlainText()
    #print('http://update.sevenonline.fr/' +  file[0])
    url = 'http://update.sevenonline.fr/' + file[0]
    path = "./"
    dir = file[0].split("/")
    del dir[len(dir) - 1]
    for pathcut in dir:
        path = path + pathcut + "/"
    if os.path.isdir(path) == False:
        textarea.setPlainText(oldText + "[+] Création du dossier " + path + "\n" )
        os.makedirs(path)
    oldText = textarea.toPlainText()
    try:
        urllib.request.urlretrieve(url, './' + file[0])
        add = progressBar.va + pourcent
        if progressBar.value() + pourcent >= 100:
            add = 100
        progressBar.setProperty("value", add)
        textarea.setPlainText(oldText + "[+] Décompression du fichier " + file[0] + "\n")

    except FileNotFoundError:
        textarea.setPlainText(oldText + "[+] Erreur lors de la décompression du fichier " + file[0] + "\n")

def start():
    os.startfile("SevenOnline.exe")
    sys.exit(0)

def runUpdate():
    #sleep(1)
    #print("Update Sevenonline")
    files = getFile("./")
    files = updateSizePython(files)
    textarea.setPlainText("[+] Téléchargement de l'index \n")
    dataremote = getDataDiff()
    diff = lambda l1,l2: [x for x in l1 if x not in l2]

    #à DL = diff(dataremote,files)
    #a remove = diff(files, dataremote)
    download = diff(dataremote,files)


    nbDownload = len(download)
    if nbDownload == 0:
        oldText = textarea.toPlainText()
        textarea.setPlainText( oldText + "[+] Sevenonline est à jour \n")
        progressBar.setProperty("value", 100)
    else:
        for i in range(len(download)):
            #print (download[i])
            downloadfile(download[i], progressBar, round(100 / nbDownload), textarea)
    btnStart.setVisible(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    windows = QWidget()
    windows.setFixedSize(450, 400)
    progressBar = QProgressBar(windows)
    progressBar.setGeometry(20, 10, 400, 23)
    progressBar.setProperty("value", 0)
    progressBar.setTextVisible(False)
    progressBar.setObjectName("progressBar")
    windows.setWindowTitle("Update SevenOnline")
    textarea = QTextEdit(windows)
    textarea.move(20,50)
    textarea.setMinimumSize(400,100)
    textarea.setReadOnly(1)
    btnStart = QPushButton('Lancer le jeu',windows)
    btnStart.setVisible(False)
    btnStart.move(20,260)
    btnStart.connect(btnStart, QtCore.SIGNAL('clicked()'), start)
    windows.show()


    QtCore.QTimer.singleShot(1000, runUpdate)
    sys.exit(app.exec_())
