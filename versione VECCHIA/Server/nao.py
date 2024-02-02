import socket
import time

class MyClass(GeneratedClass):
    command = ""
    is_fine_cmd_received = False

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

    def onInput_fineCmd(self):
        self.is_fine_cmd_received = True  # Imposta la flag quando arriva l'input "fineCmd"
    def fineCmd(self):
    # Restituisci True se un "bang" è stato ricevuto
        return self.is_fine_cmd_received

    def processing(self):
        SERVER_ADDRESS = '192.168.1.97'      # IP del server
        SERVER_PORT = 22222                  # Porta del server

        if self.command == "INIZIO":
            data = 'INIZIO'  # Dati inviati al server

            self.log("Connessione... ")
            c = socket.socket()

            try:
                c.connect((SERVER_ADDRESS, SERVER_PORT))
                self.log("Connessione al SERVER STABILITA")
                c.sendall(data)  #fa partire il programma sul server
                

                data = c.recv(2048)  # Riceve i dati da dire
                datastr = str(data)
                self.outStr(datastr)    #parla
                while True:
                    if  self.fineCmd():
                        c.sendall("fine")  #fa partire continuare il programma sul server
                        break  # Esce dal ciclo se la condizione è vera
                    time.sleep(0.1)  # Aspetta per un breve periodo di tempo per non sovraccaricare la cpu
                


                data = c.recv(2048)  # Riceve i dati
                datastr = str(data)
                self.parlaAscolta(datastr)#utilizza un uscita "speciale" pk dopo aver utilizzato la funzione che parla uso il suo bang di fine comando
                while True:        #while true per aspettare che il comando che arriva sia corretto 
                    data = self.command  # Assegna il valore a data pk così dopo fuori dal while posso utilizzarla
                    if data=="sci" or data=="running" or data=="nuoto":
                        c.sendall(data)  # Invia i dati
                        break  # Esce dal ciclo se la condizione è vera
                    time.sleep(0.1)  # Aspetta per un breve periodo di tempo per non sovraccaricare la cpu
               


                data = c.recv(2048)  # Riceve i dati
                datastr = str(data)
                self.parlaAscolta(datastr)#utilizza un uscita "speciale" pk dopo aver utilizzato la funzione che parla uso il suo bang di fine comando
                while True:        #while true per aspettare che il comando che arriva sia corretto 
                    data = self.command  # Assegna il valore a data pk così dopo fuori dal while posso utilizzarla
                    if data=="maschio" or data=="femmina" or data=="non voglio specificarlo":
                        c.sendall(data)  # Invia i dati
                        break  # Esce dal ciclo se la condizione è vera
                    time.sleep(0.1)  # Aspetta per un breve periodo di tempo per non sovraccaricare la cpu
                



                data = c.recv(2048)  # Riceve i dati da dire
                datastr = str(data)
                self.outStr(datastr)    #parla
                while True:
                    if not self.fineCmd():
                        c.sendall("fine")  #fa partire continuare il programma sul server
                        break  # Esce dal ciclo se la condizione è vera
                    time.sleep(0.1)  # Aspetta per un breve periodo di tempo per non sovraccaricare la cpu
                
                
                data = c.recv(2048)  # Riceve i dati da dire
                datastr = str(data)
                self.outStr(datastr)    #parla
                
                
                data = c.recv(2048)  # Riceve i dati da dire
                datastr = str(data)
                self.outStr(datastr)    #parla
                
                
                data = c.recv(2048)  # Riceve i dati da dire
                datastr = str(data)
                self.outStr(datastr)    #parla
                while True:
                    if not self.fineCmd():
                        c.sendall("fine")  #fa partire continuare il programma sul server
                        break  # Esce dal ciclo se la condizione è vera
                    time.sleep(0.1)  # Aspetta per un breve periodo di tempo per non sovraccaricare la cpu
                

                self.log("Connessione al SERVER TERMINATA")
            except socket.error as e:
                self.log("Connessione fallita (SERVER OFFLINE), continuo il programma")
                self.onStopped()
                return

            c.close()
        self.onStopped()