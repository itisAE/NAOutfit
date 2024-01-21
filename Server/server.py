"""
python2 e python3.
"""

#Testato per aprire il file di rilevamento misure corpo e rilevamento colore


import time
import socket
from flask import Flask
import subprocess
import webbrowser
import urllib.request



################################################
# Indirizzo IP del server
SERVER_ADDRESS = '172.20.10.2'
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
        print("\nConnessione ricevuta da NAO %s" % str(addr)) 

        
        data = c.recv(2048) 	#aspetta inizio
        data = data.decode()
            
        print("Ricevuto '%s' da NAO" % data)

        print('%s' %data)
        if(data[0] == "INIZIO"):
            
            print("Inizio misure")
            script_misure = './mediapipeV2_TOR_rilevaCorpo.py'
            subprocess.run(['python3', script_misure, 'maglia', 'M'])
            time.sleep(1)
            script_colore = './prova_colore_medio.py'#Riconoscimento_colore_area/
            subprocess.run(['python3', script_colore])
            print("Fine misure")
            
            data=["parla ascolta","La taglia che ho riconosciuto è L, confermi: "]
            data = data.encode()	#manda i dati
            c.send(data)
            data = c.recv(2048) 	#riceve la risposta
            data = data.decode()
            if(data[0]=="rx" and data[1]=="si"):
                data=["parla","hai accettato"]
            elif(data[0]=="rx" and data[1]=="no"):
                data=["parla","hai annullato"]
            data = data.encode()
            c.send(data)
            data = c.recv(2048) 	#riceve la risposta
            data = data.decode()
            data=["fine"]
            data = data.encode()
            c.send(data)
            
        c.close()
