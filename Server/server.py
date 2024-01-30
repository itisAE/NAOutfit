# Server in python 3
import socket
import time

NUM_B_RECV=2048								#numero di byte da ricevere a volta
server_address = ('192.168.1.97', 22222)	# Assegnare l'indirizzo IP e la porta

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(server_address)

server_socket.listen(1)
print("Server pronto")

def invia(str, temp):
    client_socket.sendall(str.encode())    #sendall al posto che send manda tutti i dati presenti nel buffer, invece send normale solo il numero di byte indicati ogni volta
    time.sleep(temp)	#tempo che impiega il nao per parlare (si potrebbe fare parte client facendo mandare al server quando a terminato)
def ricevi():			#bloccante fino a quando nn riceve i dati
    data = client_socket.recv(NUM_B_RECV)
    return data.decode()

while True:
    try:
        # Accetta le connessioni
        client_socket, client_address = server_socket.accept()

        while True:
            try:
                data=ricevi()
                if not data:
                    print('Il client si è disconnesso')
                    break
                print('ricevuto "{}", quindi connessione stabilita'.format(data))
                # Risponde
                invia('Per favore mettiti in posizione davanti alla fotocamera, così potrò capire le tue taglie',10)
                
                #TODO ___________far partire i programmi per la misura__________
                
                
                invia('Ho trovato che per la maglia ti sta bene la taglia M, vuoi una taglia in più?',0)
                rx=ricevi()
                print("Risposta alla domanda dal client: " + rx)
                                  
                if rx=="si":
                    invia('Ho aumentato di una taglia', 10)
                else:
                    invia('Hai confermato la taglia', 10)


            except socket.error as e:
                print("Errore durante la comunicazione con il client: {}".format(e))    #stampa il tipo di errore che ha riscontrato
                break
        client_socket.close()  
    except socket.error as e:
        print("Errore di connessione: {}".format(e))



        