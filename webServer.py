import time
import socket 
import webbrowser
from dependencies import *
import urllib


taglie = list(('S', 'M', 'L', 'XL', 'XXL'))

####################################
user = {
    'taglia' : 'M',
    'colore_capelli' : 'marrone_scuro',
    'sesso' : 'M',
    'vestito' : 'maglia',
    'taglia_succ': False,
    'sport' : 'running'
}
####################################

################################################
# Indirizzo SERVER a cui mi collego
SERVER_ADDRESS = '192.168.168.105'
#################################################


SERVER_PORT = 22222

# Creo Socket
s = socket.socket()


s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((SERVER_ADDRESS, SERVER_PORT))
s.listen(5)

print("SERVER avviato... sono in attesa %s. Kill con Ctrl-C" %
     str((SERVER_ADDRESS, SERVER_PORT)))

while True:   
    c, addr = s.accept()

    print("\nConnessione ricevuta da NAO %s" % str(addr)) #per nao

    while True:
        data = c.recv(2048)
        if data:
            data = data.decode()
            print("Ricevuto '%s' da NAO" % data)
            if data == 'FINE':
                print('chiusura dal NAO...')
                c.close()
                with urllib.request.urlopen('http://api.callmebot.com/start.php?user=@Ceseprova100&text=Un+cliente+ha+bisogno+di+un+operatore+al+reparto+sport&lang=it-IT-Standard-B&rpt=5') as response:
                    html = response.read()
                print(html)
                break
            elif data == 'INIZIO':
                data = 'cerchi vestiti per uomo o per donna?'
                webbrowser.open_new_tab('./img/sesso.pdf')#apre il pdf per la scelta del sesso
            elif data == 'donna' or data == 'uomo':
                if data == 'donna':
                    user['sesso'] = 'F'
                else:
                    user['sesso'] = 'M'
                data = 'Per quale sport vuoi prepararti ? SCI, RANNING o NUOTO? Io sono bravo in tutti e tre, ma non voglio vantarmi.'
                webbrowser.open_new_tab('./img/sport.pdf')
            elif data == 'running' or data == 'nuoto' or data == 'sci' :
                user['sport'] = data
                temp = 'Ottimo, mi piace molto questo sport. ora che mi hai detto il tuo sport e il tuo sesso, posso iniziare a cercare il vestito più adatto per te. Per farlo, ho bisogno di fare uno scanning del tuo corpo, così da capire la tua taglia e il tuo colore dei capelli. Non ti preoccupare, è un’operazione veloce e indolore. Ti basterà stare fermo davanti a me per qualche secondo, mentre uso i miei potenti mezzi tecnici per scansionarti. Sei pronto?'
                c.send(temp.encode('utf-8'))
                data = c.recv(2048) # consuma la risposta che arriva dal NAO, per fare un altro invio
                print(data)
                user['taglia'] = calcolaTaglia(user['vestito'], user['sesso'], user['taglia_succ'])
                print(user['taglia'])
                if user['taglia'] == 'Err':
                    user['taglia'] = 'M'
                frame = scatta_foto()
                colore = ottieni_colore_medio(frame)
                user['colore_capelli'] = colore
                data = "ho rilevato che hai la taglia " + user['taglia'] + " e sei "+user['colore_capelli']+" di capelli va bene così?"
                webbrowser.open_new_tab('./img/taglia_'+user['taglia']+'.pdf')#apre la pagina della taglia
            elif data == 'si' or data == 'no':
                if data == 'si':
                    data = 'ora ti propongo dei capi di abbigliamento secondo l\'armocromia che ho rilevato!!'
                    user['taglia_succ'] = False
                else:
                    data = 'ora ti propongo dei capi di abbigliamento secondo l\'armocromia che ho rilevato ma con una taglia in più!!'
                    user['taglia_succ'] = True
                #data = 'ora ti propongo dei capi di abbigliamento secondo l\'armorcomia che ho rilevato!!'
                c.send(data.encode('utf-8'))
                c.recv(2048)#consuma
                print(user['sesso'])
                link = gestisci_utente(user['sesso'], user['sport'], user['colore_capelli'])
                data = ritornaRisposta(link)#ritorna la stringa dal file --> verrà implementato chat gpt
                webbrowser.open_new_tab(link)
                #data viene mandata dal send sotto
            print(data)
            data = data.encode()     
            c.send(data)
    break #!è necessario? il break nel while più interno esce solo dal primo while in teoria, da provare
           #UPDATE: sembrerebbe funzionare, da testare con NAO 
