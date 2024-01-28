"""
python2 e python3.
"""

#Testato per aprire il file di rilevamento misure corpo e rilevamento colore


import time
import socket
from mediapipeV2_TOR_rilevaCorpo import calcolaTaglia
from prova_colore_medio import scatta_foto
from prova_colore_medio import ottieni_colore_medio


####################################
user = {
    'taglia' : '',
    'colore_capelli' : '',
    'sesso' : 'M',
    'vestito' : 'maglia',
    'taglia_succ': False
}
####################################


# Creare un socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Assegnare l'indirizzo IP e la porta
server_address = ('192.168.1.108', 22222)
server_socket.bind(server_address)

# Ascoltare le connessioni in arrivo
server_socket.listen(1)
print("Server pronto")
while True:
    try:
        # Accetta le connessioni
        client_socket, client_address = server_socket.accept()

        while True:
            try:
                
                data = client_socket.recv(2048)
                if not data:
                    print('Il client si è disconnesso')
                    break
                print('ricevuto "{}"'.format(data))

                # Risponde
                response = 'Per favore mettiti in posizione davanti alla fotocamera, così potrò capire le tue taglie'
                client_socket.sendall(response.encode())    #sendall al posto che send manda tutti i dati presenti nel buffer, invece send normale solo il numero di byte indicati ogni volta
                time.sleep(10)   #aspetta 5 secondi

                if(data == "INIZIO"):
                    print("AVVIO....")
                    script_misure = './mediapipeV2_TOR_rilevaCorpo.py'
                    # subprocess.run(['python3', script_misure, 'maglia', 'M'])
                    taglia = calcolaTaglia(user['vestito'], user['sesso'], user['taglia_succ'])
                    print(taglia)
                    time.sleep(1)
                    script_colore = './prova_colore_medio.py'
                    frame = scatta_foto()
                    colore = ottieni_colore_medio(frame)
                
                response = 'Ho trovato che per la maglia ti sta bene la taglia M, vuoi una taglia in più?'
                client_socket.sendall(response.encode())
                data = client_socket.recv(2048)
                rx=data.decode()
                print("Risposta alla domanda dal client: "+rx)
                                  
                
                if rx=="si":
                    response = 'Ho aumentato di una taglia'
                    client_socket.sendall(response.encode())
                else:
                    response = 'Hai confermato la taglia'
                    client_socket.sendall(response.encode())
                
                time.sleep(10)

            except socket.error as e:
                print("Errore durante la comunicazione con il client: {}".format(e))    #stampa il tipo di errore che ha riscontrato
                break

        # Pulire la connessione
        client_socket.close()

    except socket.error as e:
        print("Errore di connessione: {}".format(e))



'''
# Creo Socket
s = socket.socket()


s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((SERVER_ADDRESS, SERVER_PORT))
s.listen(5)

print("SERVER avviato... sono in attesa %s. Kill con Ctrl-C" %
      str((SERVER_ADDRESS, SERVER_PORT)))

while True:
        #c, addr = s.accept() #per nao
        #print("\nConnessione ricevuta da NAO %s" % str(addr)) #per nao

        while True:
            #data = c.recv(2048) #per nao
            data="INIZIO"
            if not data:
                print("Chiusura dal NAO")
                break

            #data = data.decode()  #per nao

            print("Ricevuto '%s' da NAO" % data)

            print('%s' %data)
            if(data == "INIZIO"):
                print("AVVIO....")
                script_misure = './mediapipeV2_TOR_rilevaCorpo.py'
                # subprocess.run(['python3', script_misure, 'maglia', 'M'])
                taglia = calcolaTaglia(user['vestito'], user['sesso'], user['taglia_succ'])
                print(taglia)
                time.sleep(1)
                script_colore = './prova_colore_medio.py'#Riconoscimento_colore_area/
                frame = scatta_foto()
                colore = ottieni_colore_medio(frame)
            



            # messaggio da inviare al CLIENT
            #data = "Da SERVER: " + str(addr) + ". Mi sono connesso al sito: '" + data + "'"

    	    # mando al client.
            #data = data.encode()
            #c.send(data)
        #c.close()
'''