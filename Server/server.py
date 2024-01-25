# Python 3
import socket
import time

# Creare un socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Assegnare l'indirizzo IP e la porta
server_address = ('192.168.168.100', 22222)
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

                #TODO ___________far partire i programmi per la misura__________
                
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
