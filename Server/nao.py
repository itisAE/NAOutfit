import socket
class MyClass(GeneratedClass):
    command=""
    def __init__(self):
        GeneratedClass.__init__(self)

    def onLoad(self):
        #put initialization code here
        pass

    def onUnload(self):
        #put clean-up code here
        pass

    def onInput_onStart(self):
        #self.onStopped() #activate the output of the box
        pass

    def onInput_onStop(self):
        self.onUnload() #it is recommended to reuse the clean-up as the box is stopped
        self.onStopped() #activate the output of the box

    def onInput_userCommand(self, user_word):
        self.command = user_word
        self.log(user_word)
        self.processing()

    def processing(self):
		SERVER_ADDRESS = '192.168.1.55'  # ip del pc su cui gira il server
		SERVER_PORT = 22222
        NUMBYTE=2048 #numero max di byte che riceve alla volta
		self.log(self.command)

		if self.command == "INIZIO":
			data = 'INIZIO'  # stringa inviata al server

			self.log("Connessione... ")
			c = socket.socket()

			try:
				c.connect((SERVER_ADDRESS, SERVER_PORT))
				self.log("Connessione al SERVER STABILITA")
				
				while True:
                    self.log("Invio i dati")
					data = data.encode()	#invia i dati
					c.send(data)
					data = c.recv(NUMBYTE)		#riceve i dati
					data = data.decode()
					datastr = str(data)
                    if(datastr[0]=="parla"):
                        self.OutputDaServer(datastr[1])
                        data=["ack"]
                        self.log("parlo")
                        while(not self.strOnStopped):
                            self.log("esecuzione cmd da server...")
                    elif(datastr[0]=="ascolta"):
                        self.spr(1)
                        data=["rx",self.command]
                        self.log("ascolto")
                        while(not self.strOnStopped):
                            self.log("esecuzione cmd da server...")
                    elif(datastr[1]=="parla ascolta"):
                        self.OutputDaServer(datastr[1])
                        self.log("parlo")
                        self.spr(1)
                        while(not self.strOnStopped):
                            self.log("esecuzione cmd da server...")
                        data=["rx",self.command]
                        self.log("ascolto")
                        while(not self.strOnStopped):
                            self.log("esecuzione cmd da server...")
                    elif(datastr[1]=="ascolta parla"):
                        self.spr(1)
                        data=["rx",self.command]
                        self.log("ascolto")
                        while(not self.strOnStopped):
                            self.log("esecuzione cmd da server...")
                        self.OutputDaServer(datastr[1])
                        self.log("parlo")
                        while(not self.strOnStopped):
                            self.log("esecuzione cmd da server...")
                    elif(data[0]=="fine"):
                        self.log("comunicazione terminata (cmd ricevuto dal server)")
                        break

			except socket.error as e:
				self.log("Connessione fallita, continuo il programma")
				return
				
			c.close()
	self.onStopped()