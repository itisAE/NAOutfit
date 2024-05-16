'''
TOR: Versione ottimizzata utilizzando mediapipe, preso spunto dal codice trovato qui: https://github.com/AnanthaKannan/ai-media-pipe
per la documentazione guardare questo link: https://medium.com/@sreeananthakannan/full-body-tracking-c7c4cf68bb9d 
aggiunte le funzioni 
#?calculateLung(lmList, bodyPartNum1, bodyPartNum2):
prende in input l'array di array delle coordinate  di ogni punto(**float), il punto di partenza(int) e il punto di arrivo (int)
#?mediaValori(misurazioniArto) 
prende in input l'array di misurazioni(*float) e restituisce la media dei valori(float)


PER PROVARE IL PROGRAMMA:
assicurarsi di avere tutte le librerie installate (per mediapipe se si ha Linux come SO verificare la possibilità di tirare su un venv (https://docs.python.org/3/library/venv.html))
eseguire da terminale python3 mediapipeV2_TOR_rilevaCorpo.py

POSIZIONAMENTO FOTOCAMERA
230cm dal soggetto
500cm --> distanza in cui le misurazioni coincidono coi cm #!deprecated

Diverso coefficiente per cui dividere spalle/braccia e gambe causa proporzioni

POSIZIONE FOTOCAMERA PC AD UN ALTEZZA DI 1 METRO CIRCA PER LE GIUSTE PROPORZIONI

'''


import cv2
import mediapipe as mp
import time
import math
import cv2 as cv
import numpy as np
from scipy.stats import iqr
import random


class poseDetector():
    def __init__(self, mode=False, smooth=True, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.smooth = smooth
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.pTime = 0

        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(static_image_mode=self.mode,
                                smooth_landmarks=self.smooth,
                                min_detection_confidence=self.detectionCon,
                                min_tracking_confidence=self.trackCon)

    def findPose(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)

        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS)
        return img

    def getPosition(self, img):
        self.lmList = []
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.lmList.append([id, cx, cy])
        return self.lmList

    def showFps(self, img):
        cTime = time.time()
        #print(cTime, self.pTime)
        fbs = 1 / (cTime - self.pTime)
        self.pTime = cTime
        cv2.putText(img, str(int(fbs)), (70, 80), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 0), 3)

    def findAngle(self, img, p1, p2, p3, draw=True):
        # Get the landmark
        x1, y1 = self.lmList[p1][1:]
        x2, y2 = self.lmList[p2][1:]
        x3, y3 = self.lmList[p3][1:]

        # Calculate the angle
        angle = math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2))
        # some time this angle comes zero, so below conditon we added
        if angle < 0:
            angle += 360

        # Draw
        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 3)
            cv2.line(img, (x3, y3), (x2, y2), (255, 255, 255), 3)
            cv2.circle(img, (x1, y1), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x1, y1), 15, (0, 0, 255), 1)
            cv2.circle(img, (x2, y2), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (0, 0, 255), 1)
            cv2.circle(img, (x3, y3), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x3, y3), 15, (0, 0, 255), 1)
            # cv2.putText(img, str(int(angle)), (x2 - 20, y2 + 50), cv2.FONT_HERSHEY_SIMPLEX,
            #             1, (0, 0, 255), 2)
        return angle

def calculateLung(lmList, bodyPartNum1, bodyPartNum2):
    xArt1 = lmList[bodyPartNum1][1]
    yArt1 = lmList[bodyPartNum1][2]
    xArt2 = lmList[bodyPartNum2][1]
    yArt2 = lmList[bodyPartNum2][2]
    lung = math.sqrt((xArt1 - xArt2)**2 + (yArt1 - yArt2)**2)
    return lung

def mediaValori(misurazioniArto):#accetta in input l'array del dizionario (es: dictArrDistance["braccia"])

    #TOR PARTE DI CALCOLO DEI DATI
    moltiplicatore = 2
    misurazioni = np.array(misurazioniArto)
    q1 = np.percentile(misurazioni, 25) #calcolo il primo quartile (valore sottoi lquale si trova il 25% dei dati)
    q3 = np.percentile(misurazioni, 75) #calcolo il terzo quartile 

    iqr_value = iqr(misurazioni) #calcolo il valore dell'interquartile

    soglia_inf = q1 - moltiplicatore * iqr_value #imposto soglia maggiore e soglia inferiore per gli outlier
    soglia_sup = q3 + moltiplicatore * iqr_value

    #li filtro
    misurazioni_filtrate = misurazioni[(misurazioni >= soglia_inf) & (misurazioni <= soglia_sup)]

    return np.mean(misurazioni_filtrate) #faccio la media tra tutti i valori dell'array

dictDistance = {
    "spalle" : 0,
    "braccia" : 0,
    "gambe" : 0,
    "vita" : 0
}

#dizionario con insieme di misure da calcolare
dictArrDistance = {
    "spalle" : [],
    "braccia" : [],
    "gambe" : [],
    "vita" : []
}

####################################################################################
#CONFIGURAZIONE TAGLIE
min_h_S = 0
max_h_S = 0
min_h_M = 0
max_h_M = 0
min_h_L = 0
max_h_L = 0
min_h_XL =0
max_h_XL = 0
#####################################################################################
dividendo_misurazioni = 2.1  #73913043 #coefficiente per cui dividere per la proporzione in cm

dividendo_gambe=1.35


def calcolaTaglia(arg1, arg2, arg3):
    print("Mettiti in posizione")
    #time.sleep(3)
    detector = poseDetector()
    ################################
    cap = cv2.VideoCapture(4)
    if not cap.isOpened():
        cap = cv2.VideoCapture(0)
    ################################
    start_time = time.time()
    durata_programma = 10
    #while True: #--originale
    while (cv.waitKey(1) < 0)and(time.time() - start_time < durata_programma):
        success, img = cap.read()
        img = detector.findPose(img)
        lmList = detector.getPosition(img)
        if  len(lmList):
           dictArrDistance["spalle"].append(calculateLung(lmList, 11, 12)/dividendo_misurazioni)
           temp = calculateLung(lmList, 11, 13)/dividendo_misurazioni
           dictArrDistance["braccia"].append((temp+calculateLung(lmList, 11, 15))/dividendo_misurazioni) #braccio destro
           temp = calculateLung(lmList, 12, 14)/dividendo_misurazioni
           dictArrDistance["braccia"].append((temp+calculateLung(lmList, 14, 16))/dividendo_misurazioni)#braccio sinistro
           temp = calculateLung(lmList, 24, 26)/dividendo_misurazioni
           dictArrDistance["gambe"].append((temp+ calculateLung(lmList, 26,28))/dividendo_gambe)#gamba sinistra
           temp = calculateLung(lmList, 23, 25)/dividendo_misurazioni
           dictArrDistance["gambe"].append((temp+ calculateLung(lmList, 25,27))/dividendo_gambe) #gamba destra
           dictArrDistance["vita"].append((temp+ calculateLung(lmList,24,23))/dividendo_misurazioni) #vita 
           #print(str(dictArrDistance["spalle"])+ "\n")
        #else:
            #print('lmList = '+str(lmList))
        detector.showFps(img)
        cv2.imshow("Image", img)
        cv2.waitKey(1)

    cap.release()
    cv2.destroyAllWindows()
    if not dictArrDistance["spalle"]:
        fp = open("result.txt", "w")
        fp.write(str(dictDistance))
    elif not dictArrDistance["gambe"]:
        fp = open("result.txt", "w")
        fp.write(str(dictDistance))
    elif not dictArrDistance["braccia"]:
        fp = open("result.txt", "w")
        fp.write(str(dictDistance))
    else:
        dictDistance["spalle"] = mediaValori(dictArrDistance["spalle"])
        #print("rilevazioni gambe"+str(dictArrDistance["gambe"]))
        dictDistance["gambe"] = mediaValori(dictArrDistance["gambe"])
        dictDistance["braccia"] = mediaValori(dictArrDistance["braccia"])
        dictDistance["vita"] = mediaValori(dictArrDistance["vita"])
        #print(dictDistance)
    
   


    if (arg1 == 'maglia'):
        spalle = dictDistance["spalle"] * 2.7
        lungBraccio = dictDistance["braccia"]
        tagliaSpalle = convertiTaglie(spalle, arg1, arg2, arg3)
        print("circonferenza spalle"+str(spalle))
        
        return tagliaSpalle

    elif (arg1 == 'pantaloni'):
        vita = dictDistance["vita"] * 2.2
        lungGambe = dictDistance["gambe"]
        tagliaGambe = convertiTaglie(vita, arg1, arg2, arg3)
        print("circonferenza vita"+str(vita))
        return tagliaGambe
    
    

#giro petto = 93
#vita = 82
#bacino  = 106
    

###############################################################################################
###############################################################################################
###############################################################################################
###############################################################################################
###############################################################################################


""" apre il collegamento con la fotocamera scatta una foto che salva nella cartella foto, crea un'altra foto
con area 'area_centrale' e crea un foto con il colore medio"""

"""

TOR
def distanza_colore(color1, color2):
Questa funzione calcola la distanza euclidea tra due vettori di colore RGB. 
La distanza euclidea è una misura della lunghezza del vettore che connette due punti in uno spazio a tre dimensioni (nel nostro caso, uno spazio colore RGB).
La formula per la distanza euclidea tra due vettori  è:

distanza=sqrt((a1-b1)**2+(a2-b2)**2+(a3-b3)**2)

olor1 e color2 sono due vettori di colore RGB, e np.linalg.norm() calcola la norma euclidea di color1-color2, che è la distanza euclidea tra i due colori."""


def scatta_foto(percorso_immagine = './prova.jpg'):#foto/
    # Apri la connessione con la telecamera (0 indica la telecamera predefinita)(2 fotocamera esterna test)
    #controlla se è aperta la telecamera altrimenti apre la default e non genera errore
    cap = cv2.VideoCapture(2)
    if not cap.isOpened():
        cap = cv2.VideoCapture(0)

    # Verifica se la telecamera è stata aperta correttamente
    if cap.isOpened() == False:
        print("Impossibile aprire la telecamera.")
        return

    # Cattura un singolo frame dalla telecamera
    corretto, frame = cap.read()

    # Controlla se il frame è stato catturato correttamente
    if not corretto:
        print("Impossibile catturare il frame.")
        return

    cv2.imwrite(percorso_immagine, frame)

    # Chiudi la telecamera
    cap.release()

    return frame

def ottieni_colore_medio(frame, percorso_immagine_area = './prova_area.jpg'):#foto/
    altezza, larghezza = frame.shape[:2]
    dimensione_area = 20
    centro_x = larghezza // 2
    centro_y = altezza // 2
    area_centrale = frame[centro_y - dimensione_area:centro_y + dimensione_area, centro_x - dimensione_area:centro_x + dimensione_area]
    cv2.imwrite(percorso_immagine_area, area_centrale)
    colore_medio = np.mean(area_centrale, axis=(0, 1))
    colore_medio_rgb = (int(colore_medio[2]), int(colore_medio[1]), int(colore_medio[0]))
    dimensioni = (65, 65)
    colore_immagine = np.zeros((dimensioni[0], dimensioni[1], 3), dtype=np.uint8)
    colore_immagine[:, :] = colore_medio
    cv2.imwrite('./prova_colore.jpg', colore_immagine)#foto/
    colori_riferimento = {
        #'bianco': [255, 255, 255],
        'rasato': [255, 182, 193],
        'moro': [165, 129, 76],
        #'marrone_scuro': [92, 64, 51],
        #'nero': [0, 0, 0],
        'biondo': [255, 222, 173],
        #'rosso': [255, 0, 0]
    }
    #leggi header
    def distanza_colore(color1, color2):
        return np.linalg.norm(np.array(color1) - np.array(color2))
    colore_classificato = min(colori_riferimento.keys(), key=lambda colore: distanza_colore(colore_medio_rgb, colori_riferimento[colore]))
    print(f"Colore medio dell'area centrale: {colore_medio_rgb}")
    print(f"Colore classificato: {colore_classificato}")
    return colore_classificato
###############################################################################################
###############################################################################################
###############################################################################################
###############################################################################################
###############################################################################################
    #gestisciLink

# Creazione della tabella di mapping
#MMS =  maschi mori sci
#FBR =  femmine bionde running
#FMN = femmine more nuoto

pagine_da_aprire_MMS = ['https://www.decathlon.it/p/giacca-snowboard-uomo-snb100-grigia-e-nera/_/R-p-349323?mc=8827795&c=grigio', 'https://www.decathlon.it/p/giacca-sci-uomo-patrol-rossa/_/R-p-335336?mc=8667071&c=rosso', 'https://www.decathlon.it/p/piumino-sci-uomo-900-warm-azzurro/_/R-p-339367?mc=8802780&c=blu']
pagine_da_aprire_MMR = ['https://www.decathlon.it/p/maglia-manica-lunga-running-uomo-warm-regul/_/R-p-311855?mc=8642366&c=nero', 'https://www.decathlon.it/p/maglia-termica-running-uomo-kiprun-skincare-grigia/_/R-p-307913?mc=8588361&c=grigio', 'https://www.decathlon.it/p/gilet-running-uomo-run-wind/_/R-p-121436?mc=8487907&c=nero', 'https://www.decathlon.it/p/mp/gsclosure/t-shirt-uomo-bioattiva-tecnologia-raggi-infrarossi-lontani-bluabyss/_/R-p-523995e1-5f6d-4fdc-bd4e-14a30678d96e?mc=523995e1-5f6d-4fdc-bd4e-14a30678d96e_c8&c=blu', 'https://www.decathlon.it/p/giacca-impermeabile-running-uomo-kiprun-rain-nera/_/R-p-329263?mc=8649262&c=nero']
pagine_da_aprire_MMN = ['https://www.decathlon.it/p/costume-boxer-uomo-speedo-trick-nero-verde/_/R-p-X8815018?mc=8815018&c=nero', 'https://www.decathlon.it/p/costume-slip-uomo-arena-icons-rosso-bianco/_/R-p-X8821727?mc=8821727&c=rosso_bianco', 'https://www.decathlon.it/p/costume-slip-uomo-arena-icons-rosso-bianco/_/R-p-X8821727?mc=8821727&c=rosso']

pagine_da_aprire_MBS = ['https://www.decathlon.it/p/giacca-sci-uomo-900/_/R-p-339432?mc=8801961&c=verde']
pagine_da_aprire_MBR = ['https://www.decathlon.it/p/maglia-running-uomo-dry-breath-rossa/_/R-p-326372?mc=964110&c=nero', 'https://www.decathlon.it/p/maglia-manica-lunga-running-uomo-sun-protect-nera/_/R-p-145872?mc=8398867&c=nero']
pagine_da_aprire_MBN = ['https://www.decathlon.it/p/mp/guggen-mountain/guggen-mountain-2335-costume-da-bagno-da-uomo-stampa-di-alta-qualita/_/R-p-ba3ba99b-7e11-475b-bb1a-b79636a08445?mc=ba3ba99b-7e11-475b-bb1a-b79636a08445_c22.c1&c=giallo', 'https://www.decathlon.it/p/mp/guggen-mountain/guggen-mountainzm1609-costume-da-bagno-da-uomo-a-quadri-stampa-di-alta-qualita/_/R-p-c207ff72-4ff3-41f6-889c-d66708c0f485?mc=c207ff72-4ff3-41f6-889c-d66708c0f485_c4.c251&c=bianco', 'https://www.decathlon.it/p/costume-boxer-lungo-uomo/_/R-p-122525?mc=8616021&c=nero']


pagine_da_aprire_FMS = ['https://www.decathlon.it/p/giacca-snowboard-donna-compatibile-ziprotec-snb-500-grigia/_/R-p-332260?mc=8758695&c=grigio', 'https://www.decathlon.it/p/mp/siroko/giacca-da-snowboard-da-donna-sport-invernali-w2-w-cerro-siroko-beige/_/R-p-cbae01ca-53a8-4bdf-8c81-87961457ee35?mc=cbae01ca-53a8-4bdf-8c81-87961457ee35_c30&c=beige', 'https://www.decathlon.it/p/mp/siroko/giacca-da-snowboard-da-donna-sport-invernali-w1-w-crystal-siroko-nero/_/R-p-4c55f510-f23e-4865-beea-531eddabe722?mc=4c55f510-f23e-4865-beea-531eddabe722_c1.c5&c=nero']
pagine_da_aprire_FMR = ['https://www.decathlon.it/p/maglia-manica-lunga-running-donna-run-warm-nera/_/R-p-152557?mc=8394789&c=nero','https://www.decathlon.it/p/maglia-termica-running-donna-kiprun-skincare/_/R-p-336832?mc=8809905&c=blu','https://www.decathlon.it/p/maglia-manica-lunga-running-donna-kiprun-skincare/_/R-p-327200?mc=8809835&c=rosso_arancione', 'https://www.decathlon.it/p/pantaloncini-ciclisti-running-donna-run-500-comfort-neri/_/R-p-340075?mc=8820453&c=verde']
pagine_da_aprire_FMN = ['https://www.decathlon.it/p/mp/adidas/bikini-neckholder/_/R-p-a8f59e26-1faf-4858-a769-fa079081f336?mc=a8f59e26-1faf-4858-a769-fa079081f336_c1.c4&c=nero', 'https://www.decathlon.it/p/costume-intero-donna-heva-li/_/R-p-306354?mc=8547548&c=rosa', 'https://www.decathlon.it/p/costume-intero-donna-kamiye/_/R-p-333202?mc=8788455&c=blu']

pagine_da_aprire_FBS = ['https://www.decathlon.it/p/mp/cortina/giacca-invernale-da-donna-ice-imbottita-con-cappuccio-fondazione-cortina/_/R-p-789724d5-b817-4ea3-a951-1dff0f2b3a37?mc=789724d5-b817-4ea3-a951-1dff0f2b3a37_c2&c=grigio']
pagine_da_aprire_FBR = ['https://www.decathlon.it/p/mp/tca/top-con-collo-a-imbuto-da-donna/_/R-p-4f336b17-e75e-4f59-a3a7-ffcd306a4cac?mc=4f336b17-e75e-4f59-a3a7-ffcd306a4cac_c1&c=nero']
pagine_da_aprire_FBN = ['https://www.decathlon.it/p/costume-intero-donna-vega-light-hot/_/R-p-306386?mc=8647529&c=nero', 'https://www.decathlon.it/p/costume-intero-donna-kamyli/_/R-p-332968?mc=8645312&c=blu', 'https://www.decathlon.it/p/costume-intero-donna-kamiye-lazo/_/R-p-3930?mc=8579338&c=nero']

#sport: sci, running, nuoto

sport = ['sci', 'running', 'nuoto']

combinazioni_funzioni = {
    ('M', sport[0], 'moro'): random.choice(pagine_da_aprire_MMS),
    ('M', sport[1], 'moro'): random.choice(pagine_da_aprire_MMR),
    ('M', sport[2], 'moro'): random.choice(pagine_da_aprire_MMN),

    ('M', sport[0], 'rasato'): random.choice(pagine_da_aprire_MMS),
    ('M', sport[1], 'rasato'): random.choice(pagine_da_aprire_MMR),
    ('M', sport[2], 'rasato'): random.choice(pagine_da_aprire_MMN),

    ('M', sport[0], 'biondo'): random.choice(pagine_da_aprire_MBS),
    ('M', sport[1], 'biondo'): random.choice(pagine_da_aprire_MBR),
    ('M', sport[2], 'biondo'): random.choice(pagine_da_aprire_MBN),

    ('F', sport[0], 'moro'): random.choice(pagine_da_aprire_FMS),
    ('F', sport[1], 'moro'): random.choice(pagine_da_aprire_FMR),
    ('F', sport[2], 'moro'): random.choice(pagine_da_aprire_FMN),
    
    ('F', sport[0], 'biondo'): random.choice(pagine_da_aprire_FBS),
    ('F', sport[1], 'biondo'): random.choice(pagine_da_aprire_FBR),
    ('F', sport[2], 'biondo'): random.choice(pagine_da_aprire_FBN)
}


def gestisci_utente(sesso, sport, colore_capelli):
    # Cerca la funzione corrispondente nella tabella di mapping
    funzione = combinazioni_funzioni.get((sesso, sport, colore_capelli))
    
    # Chiamala e restituisci il risultato
    return funzione

###############################################################################################
###############################################################################################
###############################################################################################
###############################################################################################
###############################################################################################

def trova_riga_successiva(parola_cercata, nome_file):
    with open(nome_file, 'r') as file:
        linee = file.readlines()

        for i in range(len(linee)):
            # Rimuovi il carattere newline (\n) dalla fine di ogni riga
            linee[i] = linee[i].rstrip('\n')

            # Verifica se la parola cercata è presente nella riga
            if parola_cercata in linee[i]:
                # Verifica se la riga successiva esiste
                if i + 1 < len(linee):
                    return linee[i + 1]
                else:
                    return "Fine del file, nessuna riga successiva disponibile."

    return "Parola non trovata nel file."

def ritornaRisposta(link):
    # Esempio di utilizzo
    file_da_esaminare = "legginao.txt"  # Sostituisci con il percorso corretto del tuo file

    risultato = trova_riga_successiva(link, file_da_esaminare)
    with open ("risposta.txt", "w") as file:
        file.write(risultato)

    with open("risposta.txt", "r") as file:
        risposta = file.read()

    return risposta


#se tagliaSuccessiva è True allora il programma restituirà la misura successiva a quella attuale
def convertiTaglie(dato, vestito, sesso, tagliaSuccessiva):
    if sesso=='M':
        if vestito=='maglia':
            #rispetto al giro petto
            if dato>86 and dato<92:
                if(tagliaSuccessiva):
                    return 'M'
                return 'S'
            elif dato>=92 and dato<98:
                if(tagliaSuccessiva):
                    return 'L'
                return 'M'
            elif dato>=98 and dato<104:
                if(tagliaSuccessiva):
                    return 'XL'
                return 'L'
            elif dato>=104 and dato<114:
                if(tagliaSuccessiva):
                    return 'XL'
                return 'XL'
            elif dato>=114 and dato<124:
                if(tagliaSuccessiva):
                    return 'XL'
                return 'XL'
            elif dato>=124 and dato<134:
                if(tagliaSuccessiva):
                    return 'XL'
                return 'XL'
            else:
                return 'Err'  #errore
        elif vestito=='pantaloni':
            if dato>88 and dato<92:
                if(tagliaSuccessiva):
                    return ["IT 44", "EU 40"]
                return ["IT 42", "EU 38"]
            elif dato>=92 and dato<96:
                if(tagliaSuccessiva):
                    return ["IT 46", "EU 42"]
                return ["IT 44", "EU 40"]
            elif dato>=96 and dato<100:
                if(tagliaSuccessiva):
                    return ["IT 48", "EU 44"]
                return ["IT 46", "EU 42"]
            elif dato>=100 and dato<105:
                if(tagliaSuccessiva):
                    return ["IT 50", "EU 46"]
                return ["IT 48", "EU 44"]
            elif dato>=105 and dato<109:
                if(tagliaSuccessiva):
                    return ["IT 52", "EU 48"]
                return ["IT 50", "EU 46"]
            elif dato>=109 and dato<114:
                if(tagliaSuccessiva):
                    return ["IT 54", "EU 50"]
                return ["IT 52", "EU 48"]
            elif dato>=114 and dato<119:
                if(tagliaSuccessiva):
                    return ["IT 56", "EU 52"]
                return ["IT 54", "EU 50"]
            elif dato>=119 and dato<124:
                if(tagliaSuccessiva):
                    return ["IT 58", "EU 54"]
                return ["IT 56", "EU 52"]
            elif dato>=124 and dato<129:
                if(tagliaSuccessiva):
                    return 'Err'
                return ["IT 58", "EU 54"]
            else:
                return 'Err'  #errore
    elif sesso=='F':
        if vestito=='maglia':
            #rispetto a giro vita
            if dato>68 and dato<71:
                if(tagliaSuccessiva):
                    return 'S'
                return 'XS'
            elif dato>=71 and dato<74:
                if(tagliaSuccessiva):
                    return 'S'
                return 'S'
            elif dato>=74 and dato<77:
                if(tagliaSuccessiva):
                    return 'S'
                return 'S'
            elif dato>=77 and dato<89:
                if(tagliaSuccessiva):
                    return 'S'
                return 'S'
            elif dato>=89 and dato<101:
                if(tagliaSuccessiva):
                    return 'M'
                return 'S'
            elif dato>=101 and dato<113:
                if(tagliaSuccessiva):
                    return 'M'
                return 'M'
            elif dato>=113 and dato<125:
                if(tagliaSuccessiva):
                    return 'M'
                return 'M'
            else:
                return 'Err'  #errore
        elif vestito=='pantaloni':
            if dato>58 and dato<62:
                if(tagliaSuccessiva):
                    return 'XS'
                return '2XS'
            elif dato>=62 and dato<65:
                if(tagliaSuccessiva):
                    return 'S'
                return 'XS'
            elif dato>=65 and dato<69:
                if(tagliaSuccessiva):
                    return 'M'
                return 'S'
            elif dato>=69 and dato<73:
                if(tagliaSuccessiva):
                    return 'L'
                return 'M'
            elif dato>=73 and dato<77:
                if(tagliaSuccessiva):
                    return 'L'
                return 'M/L'
            elif dato>=77 and dato<84:
                if(tagliaSuccessiva):
                    return 'XL'
                return 'L'
            elif dato>=84 and dato<90:
                if(tagliaSuccessiva):
                    return 'XL'
                return 'L/XL'
            elif dato>=90 and dato<96:
                if(tagliaSuccessiva):
                    return '2XL'
                return 'XL'
            elif dato>=96 and dato<102:
                if(tagliaSuccessiva):
                    return '2XL'
                return 'XL/2XL'
            elif dato>=102 and dato<108:
                if(tagliaSuccessiva):
                    return '3XL'
                return '2XL'
            elif dato>=108 and dato<114:
                if(tagliaSuccessiva):
                    return '3XL'
                return '2XL/3XL'
            elif dato>=114 and dato<120:
                if(tagliaSuccessiva):
                    return '4XL'
                return '3XL'
            elif dato>=120 and dato<128:
                if(tagliaSuccessiva):
                    return '4XL'
                return '3XL/4XL'
            elif dato>=128 and dato<132:
                if(tagliaSuccessiva):
                    return '5XL'
                return '4XL'
            elif dato>=132 and dato<139:
                if(tagliaSuccessiva):
                    return '5XL'
                return '4XL/5XL'
            elif dato>=139 and dato<145:
                if(tagliaSuccessiva):
                    return 'Err'
                return '5XL'
            else:
                return 'Err'  #errore
    else:
        return 'Err parametri'
