# Server in python 3
import socket
import time

NUM_B_RECV=2048								#numero di byte da ricevere a volta
server_address = ('192.168.1.97', 22222)	# Assegnare l'indirizzo IP e la porta

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(server_address)

server_socket.listen(1)
print("Server pronto")

def invia(str, attende):    #se attende=False, nn attende che il client gli mandi una ack ma fa continuare l'esecuzione del server, altrimenti attende che il nao finisca di parlare
    client_socket.sendall(str.encode())    #sendall al posto che send manda tutti i dati presenti nel buffer, invece send normale solo il numero di byte indicati ogni volta
    if(attende):
        client_socket.recv(NUM_B_RECV)  #attende che il client abbia finito di parlare

    
def ricevi():			#bloccante fino a quando nn riceve i dati
    data = client_socket.recv(NUM_B_RECV)
    return data.decode()


tipoSport=""
sesso=""
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
                
                #il programma è partito
                invia("Buongiorno, io sono Naoutfit, il tuo assistente personale per la scelta del vestito più adatto per te. Sono qui per aiutarti a trovare l'outfit perfetto per il tuo sport preferito.Non preoccuparti, non sono un robot snob, mi piacciono tutti gli sport.", True)
                invia("Che sport pratichi o vorresti praticare? Sci, running o nuoto? Io sono bravo in tutti e tre, ma non voglio vantarmi.", True)
                tipoSport=ricevi() 

                print(tipoSport)
                invia("Ottimo, mi piace molto questo sport. Per il buon funzionamento del sistema avrei bisogno di sapere il tuo sesso, ma se non vuoi dirmelo non fa nulla. nel caso tu voglia specificarmelo pronuncia maschio se sei un maschio e femmina se sei una femmina altrimenti non voglio specificarlo.", True)
                sesso=ricevi()
                invia("Bene, ora che mi hai detto il tuo sport e il tuo sesso, posso iniziare a cercare il vestito più adatto per te. Per farlo, ho bisogno di fare uno scanning del tuo corpo, così da capire la tua taglia e il tuo colore dei capelli. Non ti preoccupare, è un’operazione veloce e indolore. Ti basterà stare fermo davanti a me per qualche secondo, mentre uso i miei potenti mezzi tecnici per scansionarti. Sei pronto?", True)
                time.sleep(3)   #attende 3 secondi per dare il tempo di sistemarsi
                invia("Scanning in corso…", False)

                #TODO ___________far partire i programmi per la misura__________

                invia("Fatto! Grazie per la tua collaborazione. Ora ho tutte le informazioni necessarie per trovarti il vestito perfetto. Un attimo di pazienza e ti mostrerò il risultato.", False)
                
                #TODO ___________chat?___________
                

                invia("Ecco, ho trovato il vestito perfetto per te. Ti consiglio ... (descrizione del vestito per lo sport scelto). Così potrai praticare il tuo sport con stile e comodità. A meno che non ti piaccia essere scomodo e fuori moda.", False)
                
                #TODO ___________mostrare i vestiti a schermo________

                ricevi()    #attendo che il nao finisca di parlare
                time.sleep(3)
                invia("Spero di esserti stato utile. Se hai bisogno di altro, non esitare a chiedermi. Grazie per aver scelto Naoutfit, il tuo assistente personale per la scelta del vestito più adatto per te. Arrivederci e buona giornata. E ricorda, lo sport fa bene, ma non esagerare. Non vorrei che ti stancassi troppo e mi dimenticassi.",False)
            except socket.error as e:
                print("Errore durante la comunicazione con il client: {}".format(e))    #stampa il tipo di errore che ha riscontrato
                break
        client_socket.close()  
    except socket.error as e:
        print("Errore di connessione: {}".format(e))



        