import numpy as np
from numpy import genfromtxt

from scipy import stats
import seaborn as sns; sns.set()
from sklearn import svm
from sklearn.model_selection import train_test_split
from cards import Card, Deck

class Model:
    
    def __init__(self):
        self.initial_datas = []
        self.datas = None
        self.headline = []
        self.trump = None
        self.deck = []
        self.test_deck = []
        self.initial_test_datas = []
        self.test_datas = None
    
    # reads the datas from the csv file
    def read_datas(self):
        csvData = genfromtxt("datas.csv", delimiter = ",")
        self.initial_datas = [np.array(list(map(int, datas))) for datas in csvData]
        
        csvTestData = genfromtxt("test_data.csv", delimiter = ",")
        self.initial_test_datas = [np.array(list(map(int, testDatas))) for testDatas in csvTestData]
        
    # writes the datas in a csv file
    def write_datas(self):
        np.savetxt("datas.csv", self.deck, delimiter = ",")
    
    # splits the headline from the datas
    def split_datas(self):
        self.initial_datas.remove(self.initial_datas[0])
        self.initial_test_datas.remove(self.initial_test_datas[0])
    
    # returns the distribution of playable hands and not playable hands
    # every four decks will be put together
    def get_distribution_of_datas_4steps(self):
        self.read_datas()
        self.split_datas()
        playable_hands = 0
        not_playable_hands = 0
        for i in range(0, 10000, 4):
            if self.initial_datas[i][21] == 1 or self.initial_datas[i+1][21] == 1 or self.initial_datas[i+2][21] == 1 or self.initial_datas[i+3][21] == 1:
                playable_hands += 1
            else:
                not_playable_hands += 1
            if (i+4) % 100 == 0 and i != 0:
                print(i, playable_hands, not_playable_hands)
    
    # returns the distribution of playable hands and not playable hands
    # every deck counts for itself
    def get_distribution_of_datas_1step(self):
        self.read_datas()
        self.split_datas()
        playable_hands = 0
        not_playable_hands = 0
        for i in range(0, 10000, 1):
            if self.initial_datas[i][21] == 1:
                playable_hands += 1
            else:
                not_playable_hands += 1
            if (i+1) % 100 == 0 and i != 0:
                print(i, playable_hands, not_playable_hands, playable_hands / (i+1), not_playable_hands / (i+1))
    
    # runs the model
    def model(self):
        dataset = self.datas
        amount_datas = 10000
        X = dataset[:amount_datas, :8]
        y = dataset[:amount_datas, 8:].ravel()
        count_list = []
        for j in range(50, 550, 100):
            print(j)
            rbf_svc = svm.SVC(kernel = "poly", C = j, degree = 2).fit(X, y)
            test_dataset = self.test_datas
            test_x = test_dataset[:, :, :8]
            test_final_y = test_dataset[:, :, 8]
            proof_y = np.empty(shape = (len(self.test_datas),4))
            for k in range (len(test_x)):
                tmp_y = rbf_svc.predict(test_x[k])
                for l in range(4):
                    if 1 in tmp_y:
                        proof_y[k][l] = 3 - np.argmax(tmp_y == 1)
                    else:
                        proof_y[k][l] = -1
            compared_y = (proof_y == test_final_y)
            countTrue = 0
            countTruePlayable = 0
            countFalse = 0
            countFalsePlayable = 0
            for k in range(len(compared_y)):
                if compared_y[k][0] == True and test_final_y[k][0] != -1:
                    countTruePlayable +=1
                if compared_y[k][0] == True:
                    countTrue += 1
                if compared_y[k][0] == False and test_final_y[k][0] != -1:
                    countFalsePlayable += 1
                if compared_y[k][0] == False:
                    countFalse += 1
            count_list.append((countTrue, countTruePlayable, countFalse, countFalsePlayable, j))
        print(count_list)
        
    # calculates all the necessary value of features of a deck
    def calculating_features(self, cards):
        # amount of jacks
        def feature1(self):
            jacks = [card for card in cards if card.value == 2]
            return len(jacks)       
        # amount trumps without jacks
        def feature2(self):
            other_trumps = [card for card in cards if card.suit == self.trump and card.value != 2]
            return len(other_trumps)        
        # amount of aces and tens (tens only when ace is there in same suit)
        def feature3(self):
            suits = [[], [], [], []]
            [suits[card.suit].append(card) for card in cards if card.value == 11 and card.suit != self.trump]
            [suits[card.suit].append(card) for card in cards if (card.value == 10 and len(suits[card.suit]) == 1) and card.suit != self.trump]
            amount_of_cards = 0
            for suit in suits:
                amount_of_cards += len(suit)
            return amount_of_cards       
        # points of all cards
        def feature4(self):
            value_of_deck = 0
            for card in cards:
                if not card.check_louse():
                    value_of_deck += card.value
            return value_of_deck        
        # amount of suits which are not there
        def feature5(self):
            suits = [[], [], [], []]
            [suits[card.suit].append(card) for card in cards]
            amount_of_suits = 0
            for suit in suits:
                if suit:
                    amount_of_suits += 1
            return 4 - amount_of_suits
        # amount of tens which are not trump and no aces in same suit are there
        def feature6(self):
            suits = [[], [], [], []]
            [suits[card.suit].append(card) for card in cards if (card.value == 11 or card.value == 10) and card.suit != self.trump]
            amount_of_cards = 0
            for suit in suits:
                if len(suit) == 1 and suit[0].value == 10:
                    amount_of_cards += 1
            return amount_of_cards        
        # value of jacks
        def feature7(self):
            value_jacks = 0
            jacks = [card for card in cards if card.value == 2]
            for jack in jacks:
                value_jacks += jack.suit + 1
            return value_jacks        
        # value of the other trumphs
        def feature8(self):
            other_trumps = [convert_value_card(self, card) for card in cards if card.suit == self.trump and card.value != 2]
            return sum(other_trumps)
        
        # converts the value of the cards for feature 8
        def convert_value_card(self, card):
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
    
    # converts the numbers from the csv file back into a card
    def convert_numbers_to_cards(self, number1, number2, index, testDatas):
        newCard = Card(number1, number2)
        if not testDatas:
            self.deck[index].append(newCard)
        else:
            self.test_deck[index].append(newCard)
    
    # calculates the best possible trump for the game        
    def run_game(self, cards):
        new_datas = np.empty(shape = (4, 8))
        for i in range(3, -1, -1):
            self.trump = i
            features = self.calculating_features(cards)
            new_datas[3-i] = features
        self.read_datas()
        self.split_datas()
        for k in range(len(self.initial_datas)):
            #print(self.initial_datas[k])
            self.deck.append(list())
            for i in range(0,len(self.initial_datas[k])-2,2):
                self.convert_numbers_to_cards(self.initial_datas[k][i+1], self.initial_datas[k][i], k, False)
            self.deck[k].append(self.initial_datas[k][-2])
            self.deck[k].append(self.initial_datas[k][-1])   
        self.datas = np.empty(shape = (len(self.deck),9))
        #print(self.initial_datas)
        for k in range(len(self.deck)):
            self.trump = self.initial_datas[k][-2]
            features = self.calculating_features(self.deck[k][:len(self.deck[k])-2:])
            self.datas[k, :8:] = features
            self.datas[k, 8] = self.deck[k][-1]
        
        X = self.datas[:10000, :8]
        y = self.datas[:10000, 8].ravel()
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size = 0.4, random_state = 0
        )
        poly_svc = svm.SVC(kernel = "poly", degree = 2, C = 250).fit(X_train, y_train)
        new_datas_y = poly_svc.predict(new_datas)
        if 1 in new_datas_y:
            return 3 - np.argmax(new_datas_y == 1)
        return -1
    
    # runs the model      
    def run_datas(self):
        self.read_datas()
        self.split_datas()
        for k in range(len(self.initial_datas)):
            self.deck.append(list())
            for i in range(0,len(self.initial_datas[k])-2,2):
                self.convert_numbers_to_cards(self.initial_datas[k][i+1], self.initial_datas[k][i], k, False)
            self.deck[k].append(self.initial_datas[k][-2])
            self.deck[k].append(self.initial_datas[k][-1])   
        self.datas = np.empty(shape = (len(self.deck),9))
        for k in range(len(self.deck)):
            self.trump = self.initial_datas[k][-2]
            features = self.calculating_features(self.deck[k][:len(self.deck[k])-2:])
            self.datas[k, :8:] = features
            self.datas[k, 8] = self.deck[k][-1]
            
        for k in range(len(self.initial_test_datas)):
            self.test_deck.append(list())
            for i in range(0, len(self.initial_test_datas[k])-2,2):
                self.convert_numbers_to_cards(self.initial_test_datas[k][i+1], self.initial_test_datas[k][i], k, True)
            self.test_deck[k].append(self.initial_test_datas[k][-2])
            self.test_deck[k].append(self.initial_test_datas[k][-1])
        self.test_datas = np.empty(shape = (len(self.test_deck),4,10))
        for k in range(len(self.test_deck)):
            for i in range(3,-1,-1):
                self.trump = i
                features = self.calculating_features(self.test_deck[k][:len(self.test_deck[k])-2:])
                self.test_datas[k,3-i,:8:] = features
                self.test_datas[k,3-i,8] = self.test_deck[k][-2]
                self.test_datas[k,3-i,9] = self.test_deck[k][-1]
        #print(self.test_datas)
        #self.model()

#m1 = Model()
#m1.get_distribution_of_datas()
"""
deck1 = Deck()
deck1.create_deck()
deck1.shuffle()
deck1 = deck1[:12]
skat = deck1[10::]
deck1 = deck1[:10]
print(deck1)
trump = int(input("Wähle den Trumph aus"))
model1 = Model(trump)
model1.datas = model1.calculating_features(deck1)
datas = [[]]
for data in model1.datas:
    datas[0].append(data)
datas[0].append(trump)
model1.datas = datas
print(model1.datas)
model1.write_datas()"""
#csvData = np.genfromtxt("datas.csv", delimiter = ",")
#model = Model(1)
#for deck in csvData[1::]:
#    for i in range(0, len(deck)-1, 2):
#        model.convert_numbers_to_cards(int(deck[i+1]), int(deck[i]))
#print(model.deck)
model1 = Model()
#model1.get_distribution_of_datas_1step()
#model1.read_datas()
#model1.split_datas()
#model1.run_datas()
#model1.model()
#model1.run()

