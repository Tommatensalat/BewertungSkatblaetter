import numpy as np
from numpy import genfromtxt

from scipy import stats
import seaborn as sns; sns.set()
from sklearn import svm
from sklearn.model_selection import train_test_split
from cards import Card, Deck

class Model:
    
    def __init__(self):
        self.initial_datas = [] # ausgelesene datensätze
        self.datas = None # konvertierte datensätze
        self.headline = [] # kopfzeile
        self.trump = None # trumpf
        self.deck = [] # # kartendecks
        self.test_deck = [] # testdecks
        self.initial_test_datas = [] # ausgelesene testdatensätze
        self.test_datas = None # konvertierte Testdatensätze
    
    def read_datas(self):
        '''
        Auslesen der Trainings- und Testdatensätze aus einer csv-Datei
        '''
        csvData = genfromtxt("datas.csv", delimiter = ",")
        self.initial_datas = [np.array(list(map(int, datas))) for datas in csvData]
        
        csvTestData = genfromtxt("test_data.csv", delimiter = ",")
        self.initial_test_datas = [np.array(list(map(int, testDatas))) for testDatas in csvTestData]
        
    def write_datas(self):
        # schreibt neue Daten in die csv-Datei
        np.savetxt("datas.csv", self.deck, delimiter = ",")
    
    def split_datas(self):
        # entnimmt die Kopfzeile aus den Daten
        self.initial_datas.remove(self.initial_datas[0])
        self.initial_test_datas.remove(self.initial_test_datas[0])
    
    def get_distribution_of_datas_4steps(self):
        '''
        gibt die Verteilung zwischen spielbaren und nicht-spielbaren Händen zurück
        in 4er Schritten, da 4 Datensätze ein Blatt beschreiben
        '''
        self.read_datas()
        self.split_datas()
        playable_hands = 0
        not_playable_hands = 0
        for i in range(0, 10000, 4):
            # wenn eines der Blätter spielbar ist
            if self.initial_datas[i][21] == 1 or self.initial_datas[i+1][21] == 1 or self.initial_datas[i+2][21] == 1 or self.initial_datas[i+3][21] == 1:
                playable_hands += 1
            else:
                not_playable_hands += 1
            if (i+4) % 100 == 0 and i != 0:
                print(i, playable_hands, not_playable_hands)
    
    # returns the distribution of playable hands and not playable hands
    # every deck counts for itself
    def get_distribution_of_datas_1step(self):
        '''
        gibt die Verteilung zwischen spielbaren und nicht-spielbaren Händen
        in 1er Schritten, jedes Blatt steht für sich alleine
        '''
        self.read_datas()
        self.split_datas()
        playable_hands = 0
        not_playable_hands = 0
        for i in range(0, 10000, 1):
            # wenn Blatt spielbar ist
            if self.initial_datas[i][21] == 1:
                playable_hands += 1
            else:
                not_playable_hands += 1
            if (i+1) % 100 == 0 and i != 0:
                print(i, playable_hands, not_playable_hands, playable_hands / (i+1), not_playable_hands / (i+1))
    
    def model(self):
        '''
        führt die Untersuchung zur Optimierung der KI durch
        '''
        dataset = self.datas
        # Anzahl der einbezogenen Trainingsdaten
        amount_datas = 3000
        # Aufteilung der Trainingsdaten in Merkmale und Label
        X = dataset[:amount_datas, :8]
        y = dataset[:amount_datas, 8:].ravel()
        count_list = []
        # Schleifeniterationen zur Anpassung des Regularisierungskoeffizienten
        for j in range(3050, 6050, 100):
            print(j)
            # Initialisierung des Merkmalsraums mit Einordnung der Diskriminanz-
            # funktion
            # Werte werden für die Untersuchung jeweils verändert
            rbf_svc = svm.SVC(C = j).fit(X, y)
            test_dataset = self.test_datas
            # Aufteilung der zu vergleichenden Testdaten in Merkmale und Label
            test_x = test_dataset[:, :, :8]
            test_final_y = test_dataset[:, :, 8]
            # Initialisierung des Arrays, um die Ergebnisse der KI festzuhalten
            proof_y = np.empty(shape = (len(self.test_datas),4))
            # Vorhersage der Testdaten durchführen
            for k in range (len(test_x)):
                tmp_y = rbf_svc.predict(test_x[k])
                for l in range(4):
                    # Füllen des Arrays mit den Werten
                    if 1 in tmp_y:
                        proof_y[k][l] = 3 - np.argmax(tmp_y == 1)
                    else:
                        proof_y[k][l] = -1
            # beide Arrays miteinander vergleichen
            compared_y = (proof_y == test_final_y)
            countTrue = 0 # Anzahl der richtig klassifizierten Blätter
            countTruePlayable = 0 # Anzahl der richtig klassifizierten spielbaren Blätter
            countFalse = 0 # Anzahl der falsch klassifizierten Blätter
            countFalsePlayable = 0 # Anzahl der falsch klassifizierten spielbaren Blätter
            for k in range(len(compared_y)):
                # Blatt ist richtig klassifiziert und spielbar
                if compared_y[k][0] == True and test_final_y[k][0] != -1:
                    countTruePlayable +=1
                # Blatt ist richtig klassifiziert
                if compared_y[k][0] == True:
                    countTrue += 1
                # Blatt ist falsch klassifiziert und spielbar
                if compared_y[k][0] == False and test_final_y[k][0] != -1:
                    countFalsePlayable += 1
                # Blatt ist falsch klassifiziert
                if compared_y[k][0] == False:
                    countFalse += 1
            count_list.append((countTrue, countTruePlayable, countFalse, countFalsePlayable, j))
        print(count_list)
        
    def calculating_features(self, cards):
        '''
        Berechnung der Merkmale eines Blattes
        '''
        def feature1(self):
            # Anzahl der Buben
            jacks = [card for card in cards if card.value == 2]
            return len(jacks)       
        
        def feature2(self):
            # Anzahl der anderen Trümpfe
            other_trumps = [card for card in cards if card.suit == self.trump and card.value != 2]
            return len(other_trumps)   
             
        def feature3(self):
            # Anzahl der 10er und Asse (10 nur, wenn Ass in der gleichen Farbe)
            suits = [[], [], [], []]
            [suits[card.suit].append(card) for card in cards if card.value == 11 and card.suit != self.trump]
            [suits[card.suit].append(card) for card in cards if (card.value == 10 and len(suits[card.suit]) == 1) and card.suit != self.trump]
            amount_of_cards = 0
            for suit in suits:
                amount_of_cards += len(suit)
            return amount_of_cards   
            
        def feature4(self):
            # Gesamtpunkte des eigenen Blattes
            value_of_deck = 0
            for card in cards:
                if not card.check_louse():
                    value_of_deck += card.value
            return value_of_deck        
        
        def feature5(self):
            # Anzahl der Freifarben
            suits = [[], [], [], []]
            [suits[card.suit].append(card) for card in cards]
            amount_of_suits = 0
            for suit in suits:
                if suit:
                    amount_of_suits += 1
            return 4 - amount_of_suits
        
        def feature6(self):
            # Anzahl der 10er außer Trumpf, nur wenn ass nicht in der gleichen Farbe
            suits = [[], [], [], []]
            [suits[card.suit].append(card) for card in cards if (card.value == 11 or card.value == 10) and card.suit != self.trump]
            amount_of_cards = 0
            for suit in suits:
                if len(suit) == 1 and suit[0].value == 10:
                    amount_of_cards += 1
            return amount_of_cards        
        
        def feature7(self):
            # Gewichtung der Buben
            value_jacks = 0
            jacks = [card for card in cards if card.value == 2]
            for jack in jacks:
                value_jacks += jack.suit + 1
            return value_jacks        
        
        def feature8(self):
            # Gewichtung der anderen Trumpfkarten
            other_trumps = [convert_value_card(self, card) for card in cards if card.suit == self.trump and card.value != 2]
            return sum(other_trumps)
        
        def convert_value_card(self, card):
            # gibt den Wert einer Karte zurück, benötigt für Merkmal 8
            values = {
                11 : 5,
                10 : 4,
                4 : 3,
                3 : 2,
                9 : 1,
                8 : 1,
                7 : 1}
            return values[card.value]
        
        return feature1(self), feature2(self), feature3(self), feature4(self), feature5(self), feature6(self), feature7(self), feature8(self)    
    
    def convert_numbers_to_cards(self, number1, number2, index, testDatas):
        '''
        wandelt die Zahlen in den csv-Dateien in Kartenobjekte um
        '''
        newCard = Card(number1, number2)
        if not testDatas:
            self.deck[index].append(newCard)
        else:
            self.test_deck[index].append(newCard)
          
    def run_game(self, cards):
        '''
        sagt die Trumpffarbe für ein spezifisches Blatt vor
        '''
        
        self.read_datas()
        self.split_datas()
        
        # Trainingsdaten in Kartendecks konvertieren
        for k in range(len(self.initial_datas)):
            self.deck.append(list())
            for i in range(0,len(self.initial_datas[k])-2,2):
                self.convert_numbers_to_cards(self.initial_datas[k][i+1], self.initial_datas[k][i], k, False)
            self.deck[k].append(self.initial_datas[k][-2])
            self.deck[k].append(self.initial_datas[k][-1])   
        self.datas = np.empty(shape = (len(self.deck),9))
        
        # Merkmale zu den Trainingsdaten berechnen
        for k in range(len(self.deck)):
            self.trump = self.initial_datas[k][-2]
            features = self.calculating_features(self.deck[k][:len(self.deck[k])-2:])
            self.datas[k, :8:] = features
            self.datas[k, 8] = self.deck[k][-1]
        self.predict_game(cards)
        
    
    def predict_game(self, cards):
        # Array bereitstellen
        new_datas = np.empty(shape = (4, 8))
        # Merkmale entsprechend der Trumpffarbe berechnen
        for i in range(3, -1, -1):
            self.trump = i
            features = self.calculating_features(cards)
            new_datas[3-i] = features
        X = self.datas[:3000, :8]
        y = self.datas[:3000, 8].ravel()
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size = 0.4, random_state = 0
        )
        # Modell einstellen und Blatt vorhersagen
        poly_svc = svm.SVC(kernel = 'poly', degree = 2, C = 550).fit(X_train, y_train)
        new_datas_y = poly_svc.predict(new_datas)
        if 1 in new_datas_y:
            return 3 - np.argmax(new_datas_y == 1)
        return -1
         
    def run_datas(self):
        '''
        Umwandlung der Trainings- und Testdaten in Skatblätter mit Labels
        '''
        self.read_datas()
        self.split_datas()
        # Trainingsdatensatz: Umwandlung Zahlen in Karten und Blätter
        for k in range(len(self.initial_datas)):
            self.deck.append(list())
            for i in range(0,len(self.initial_datas[k])-2,2):
                self.convert_numbers_to_cards(self.initial_datas[k][i+1], self.initial_datas[k][i], k, False)
            self.deck[k].append(self.initial_datas[k][-2])
            self.deck[k].append(self.initial_datas[k][-1])   
        self.datas = np.empty(shape = (len(self.deck),9))
        # Merkmale berechnen
        for k in range(len(self.deck)):
            self.trump = self.initial_datas[k][-2]
            features = self.calculating_features(self.deck[k][:len(self.deck[k])-2:])
            self.datas[k, :8:] = features
            self.datas[k, 8] = self.deck[k][-1]
            
        # Testdatensatz: Umwandlung Zahlen in Karten und Blätter
        for k in range(len(self.initial_test_datas)):
            self.test_deck.append(list())
            for i in range(0, len(self.initial_test_datas[k])-2,2):
                self.convert_numbers_to_cards(self.initial_test_datas[k][i+1], self.initial_test_datas[k][i], k, True)
            self.test_deck[k].append(self.initial_test_datas[k][-2])
            self.test_deck[k].append(self.initial_test_datas[k][-1])
        self.test_datas = np.empty(shape = (len(self.test_deck),4,10))
        # Merkmale berechnen
        for k in range(len(self.test_deck)):
            for i in range(3,-1,-1):
                self.trump = i
                features = self.calculating_features(self.test_deck[k][:len(self.test_deck[k])-2:])
                self.test_datas[k,3-i,:8:] = features
                self.test_datas[k,3-i,8] = self.test_deck[k][-2]
                self.test_datas[k,3-i,9] = self.test_deck[k][-1]
        #self.model()


model1 = Model()
#model1.get_distribution_of_datas_1step()
#model1.read_datas()
#model1.split_datas()
#model1.run_datas()
#model1.model()
#model1.run()

