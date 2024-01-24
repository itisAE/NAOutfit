import socket
import time

class MyClass(GeneratedClass):
    command=""
    def __init__(self):
        GeneratedClass.__init__(self)

    def onLoad(self):
        pass

    def onUnload(self):
        pass

    def onInput_onStart(self):
        pass

    def onInput_onStop(self):
        self.onUnload()
        self.onStopped()

    def onInput_userCommand(self, user_word):
        self.command = user_word
        self.log(user_word)
        self.processing()

    def processing(self):
        SERVER_ADDRESS = '192.168.1.97'  	# IP del server
        SERVER_PORT = 22222  				# Porta del server

        if self.command == "INIZIO":
            data = 'INIZIO'  # Dati inviati al server

            self.log("Connessione... ")
            c = socket.socket()

            try:
                c.connect((SERVER_ADDRESS, SERVER_PORT))
                self.log("Connessione al SERVER STABILITA")

                c.sendall(data)  # Invia i dati
                
                data = c.recv(2048)  # Riceve i dati
                datastr = str(data)
                self.log("Start della misurazione")
                self.log("Risposta da server: " + datastr)
                self.outStr(datastr)
                
                
                #il recv è bloccante quindi no delay
                data = c.recv(2048)  # Riceve i dati
                datastr = str(data)
                self.log("Domande all'utente")
                self.log("Risposta da server: " + datastr)
                self.parlaAscolta(datastr)#utilizza un uscita "speciale" pk dopo aver utilizzato la funzione che parla uso il suo bang di fine comando
                
                while True:		#while true per aspettare che il comando che arriva sia corretto 
                    data = self.command  # Assegna il valore a data pk così dopo fuori dal while posso utilizzarla
                    if data=="no" or data=="si":
                        break  # Esce dal ciclo se la condizione è vera
                    time.sleep(0.1)  # Aspetta per un breve periodo di tempo per non sovraccaricare la cpu
                    
                c.sendall(data)  # Invia i dati
                
                data = c.recv(2048)  # Riceve i dati
                datastr = str(data)
                self.log("Risposta finale")
                self.log("Risposta da server: "+datastr)
                self.outStr(datastr)
                self.log("Connessione al SERVER TERMINATA")
            except socket.error as e:
                self.log("Connessione fallita (SERVER OFFLINE), continuo il programma")
                return

            c.close()
        self.onStopped()