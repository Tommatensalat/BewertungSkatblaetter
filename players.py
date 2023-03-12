from PIL import Image, ImageTk

from cards import Card, deck
from typing import List, Dict
from collections import defaultdict
import numpy as np
from numpy import genfromtxt
import time
from model import model1

class Player(object):
    
    def __init__(self, name):
        self.name = name # Name
        self.cards = [] # eigene Karten
        self.points = 0 # erhaltene Punkte durch Stiche
        self.skat = [] # karten hinzufügen, wenn Alleinspieler
        self.team = None # Allein- oder Teamspieler
        self.won = False # boolean ob Spiel gewonnen wurde
        self.possible_trump = None # bewertung des eigenen Skatblattes auf Trumpf
        self.value_possible_trump = 0 # berechnung des möglichen Trumpfs auf den Spielwert
        self.state = None
        self.playing_hand = None # Vorder-, Mittel- oder Rückhand
        self.player_index = self.set_player_index() # Player-Index für Listen-Betrachtungen
        
        # Hilfsvariablen für den Spielalgorithmus MCTS
        self.team_points_MCTS = 0  
        self.other_team_points_MCTS = 0
        self.initial_cards = []
        self.n = 0

        # state = 1 is giving, state = 2 is listening, state = 3 is speaking
    
    def resize_card(self, card, play_card):
        '''
        passt die Größe der Karten auf die Oberfläche an
        '''
        card_img = Image.open(card)
        # Abfrage ob Karte gespielt wurde oder noch Teil des Spieler-Blattes ist
        if play_card == False:
            # Abfrage ob Spieler 1, da größer angezeigt werden soll
            if self != player1:
                resized_card_img = card_img.resize((60, 100))
            else:
                resized_card_img = card_img.resize((80, 150))
        else:
            # gespielte Karten in der Mitte sollen groß angezeigt werden
            resized_card_img = card_img.resize((150, 210))
        card_image = ImageTk.PhotoImage(resized_card_img)

        return card_image
    
    def set_player_index(self):
        # setzt den Player-Index im Bezug zum Namen fest
        # Voraussetzung: Spieler heißen Spieler 1, Spieler 2 und Spieler 3
        return int(self.name[-1]) - 1
    
    def take_cards(self, deck):
        '''
        Aufnahme der Karten von den Spielern vom gesamten Blatt
        '''
        self.cards = []
        for card in range(len(deck)):
            # Wenn das Spielerblatt noch nicht vollständig ist
            if len(self.cards) < 10:
                self.cards.append(deck[card])
                self.initial_cards.append(deck[card])
            else:
                # Entnommene Karten aus dem Deck läschen
                for card in self.cards:
                    if card in deck:
                        deck.remove(card)
                break

    def take_skat(self, deck):
        # Aufnahme des Skates durch den Alleinspieler
        self.skat = deck
    
    def increase_points(self, card):
        # erhöht die Punkte eines Spielers, wenn die Karte keine Lusche darstellt
        if card.value != 7 and card.value != 8 and card.value != 9:
            self.points += card.value
          
    def reset_points(self):
        # setzt die Punkte auf den Anfangswert zurück
        self.points = 0
    
    def remove_card(self, card):
        '''
        Entfernt eine Karte aus dem Deck des Spielers
        '''
        for i in range(len(self.cards)):
            if self.cards[i] == card:
                # Kartenindex wird dem Wert None zugeordnet, sonst Probleme mit Indizes
                self.cards[i] = None
                #self.initial_cards[i] = None
                break

    def check_card_suit(self, card, first_card, trump):
        '''
        Spieler müssen der Bedienpflicht folgen beim Spielen
        '''
        # Datentyp des Trumpfes wird entsprechend geändert
        if type(trump) == str:
            trump = self.convert_card_suit_str_to_int(trump)
        
        # Wenn angespielte Karte der Vorderhand Trumpf ist
        if first_card.suit == trump or first_card.value == 2:
            possible_cards = [cards for cards in self.cards if cards != None and (cards.suit == trump or cards.value == 2)]
            if card in possible_cards or not possible_cards:
                return True
            return False
        else:
            possible_cards = [cards for cards in self.cards if cards != None and (cards.suit == first_card.suit and cards.value != 2)]
            if card in possible_cards or not possible_cards:
                return True
            return False
        # Die Farbe muss in beiden Fällen befolgt werden

    def sort_deck(self, trump):
        '''
        Das Blatt wird entsprechend des ermittelten Trumpfes geordnet nach der 
        Länge der jeweiligen Farbe
        Buben werden an den Anfang des Blattes gestellt
        '''
        # Übrigen Karten extrahieren
        indexing_nones = [self.cards.index(card) for card in self.cards if card is None]
        amount_of_nones = len(indexing_nones)
        self.cards = [card for card in self.cards if card is not None]
        
        # Karten in die einzelnen Farben aufteilen (Buben werden extra betrachtet)
        jacks, diamonds, hearts, spades, clubs = self.split_deck()
        all_cards = [jacks, diamonds, hearts, spades, clubs]
        all_cards = [[card for card in suit if card is not None]for suit in all_cards]
        self.cards = []
        # Besitzt der Spieler Buben
        if all_cards[0]:
            for jack in all_cards[0]:
                self.cards.append(jack)
                
        if type(trump) == str:
            trump = self.convert_card_suit_str_to_int(trump)
        
        # Filtern der restlichen Trumpfkarten
        for suit in all_cards[1::]:
            if suit and suit[0].suit == trump:
                for card in suit:
                   self.cards.append(card)
                all_cards.remove(suit)
                break
        
        # Rest wird der Länge nach sortiert
        all_cards[1::] = self.bubble_sort_suit(all_cards[1::], len(all_cards[1::]))
        for suit in all_cards[1::]:
            for card in suit:
                self.cards.append(card)
        
        [self.cards.append(None) for i in range(amount_of_nones)]
        for i in range(len(self.cards)):
            if indexing_nones and i == indexing_nones[0]:
                self.cards[i+1:len(self.cards)] = self.cards[i:len(self.cards) - 1]
                self.cards[i] = None
                indexing_nones.remove(indexing_nones[0])
    
    def indexing_cards(self, card_value):
        # Karten einer Farbe können des Wertes nach sortiert werden
        index_dict = {
            11: 0,
            10: 1,
            4: 2,
            3: 3,
            9: 4,
            8: 5,
            7: 6
        }
        return index_dict[card_value]
    
    def split_deck(self):
        '''
        Aufsplittung des Blattes in die vier Kartenfarben + Buben
        '''
        # Bereitstellen der Indizes
        jacks = [None, None, None, None]
        clubs = [None, None, None, None, None, None, None]
        spades = [None, None, None, None, None, None, None]
        hearts = [None, None, None, None, None, None, None]
        diamonds = [None, None, None, None, None, None, None]
        all_cards = [jacks, diamonds, hearts, spades, clubs]

        # Karten werden an ihren jeweiligen Index der Liste gesetzt
        for card in self.cards:
            if card.value == 2:
                jacks[len(jacks) - card.suit - 1] = card
            else: 
                all_cards[card.suit + 1][self.indexing_cards(card.value)] = card
        
        return jacks, diamonds, hearts, spades, clubs         
        
    def find_possible_trump(self):
        '''
        Das Ziel ist die Bewertung eines Skatblattes mit dem
        Naiven Algorithmus
        '''
        possible_trump = None
        jacks = []
        diamond_cards = []
        heart_cards = []
        spade_cards = []
        club_cards = []
        dict_card_suits = {
            0: diamond_cards,
            1: heart_cards,
            2: spade_cards,
            3: club_cards
        }
        connecting_lists = [diamond_cards, heart_cards, spade_cards, club_cards]
        
        # Aufsplittung der Karten in die einzelnen Kartenfarben + Buben
        # Vernachlässigung der Reihenfolge
        for card in self.cards:
            if card != None and card.value == 2: # jack
                jacks.append(card)
            else:
                dict_card_suits[card.suit].append(card)
        
        connecting_lists = self.removing_jacks(connecting_lists)
        
        # Einzelne Kartenfarben der Länge nach sortieren
        connecting_lists = self.bubble_sort_suit(connecting_lists, len(connecting_lists))
        # Mögliche Trumpffarbe ist die längste vorhandene Kartenfarbe
        possible_trump = connecting_lists[0][0].suit
        
        # Wenn zwei Kartenfarben gleich oft vorhanden sind, dann wird die gewünschte Trumpffarbe erneut abgefragt
        if connecting_lists[0] == connecting_lists[1] and len(connecting_lists[0]) > 3:
            possible_trump = self.bubble_sort_equal_len(connecting_lists, 2)[0].suit
            if possible_trump == connecting_lists[1][0].suit:
                connecting_lists[0], connecting_lists[1] = connecting_lists[1], connecting_lists[0]
        self.possible_trump = possible_trump
        self.possible_trump = self.convert_card_suit_int_to_str(self.possible_trump)
        # Übergabe in die Bewertung des Skatblattes auf Spielbarkeit
        self.bidding_without_learning(connecting_lists, jacks)

    def calculate_power_of_algorithm(self):
        '''
        Der Naive Algorithmus versucht nach klaren Regeln zu bewerten
        1000 Testblätter werden untersucht
        '''
        def read_datas():
            # Daten werden eingelesen
            csvData = genfromtxt("test_data.csv", delimiter = ",")
            return [np.array(list(map(int, testData))) for testData in csvData]
        
        def split_datas(datas):
            # Der Tabellenkopf wird entfernt
            datas.remove(datas[0])
            
        def convert_numbers_to_cards(number1, number2, index):
            # Kartenobjekte werden erstellt
            newCard = Card(number1, number2)
            test_deck[index].append(newCard)
            
        test_datas = read_datas()
        test_datas = test_datas[:1000]
        split_datas(test_datas)
        test_deck = []
        
        # Die Daten werden in die entsprechende Form für die anschließende Vorhersage
        # überführt
        for k in range(len(test_datas)):
            test_deck.append(list())
            for i in range(0, len(test_datas[k])-2,2):
                convert_numbers_to_cards(test_datas[k][i+1], test_datas[k][i], k)
            test_deck[k].append(test_datas[k][-2])
            test_deck[k].append(test_datas[k][-1])
            
        # Enthält die Information über die Spielbarkeit der Karten
        test_data_y = np.empty(len(test_deck))
        for k in range(len(test_deck)):
            test_data_y[k] = test_deck[k][10]
            
        # Ergebnisarray generieren
        proof_y = np.empty(len(test_deck))
        
        # Vorhergesagte Werte durch den Naiven Algorithmus speichern
        for k in range(len(test_deck)):
            self.cards = test_deck[k][:10].copy()
            self.find_possible_trump()
            if type(self.possible_trump) == str:
                self.possible_trump = self.convert_card_suit_str_to_int(self.possible_trump)
            if self.possible_trump == None:
                proof_y[k] = -1
            else:
                proof_y[k] = self.possible_trump
            self.value_possible_trump = 0
            self.possible_trump = None
        
        # beide Arrays miteinader vergleichen
        compared_y = (proof_y == test_data_y)
        count_true = 0
        count_true_playable = 0
        count_false = 0
        count_false_playable = 0
        for i in range(len(compared_y)):
            if compared_y[i] == True:
                count_true += 1
            if compared_y[i] == True and test_deck[i][-2] != -1:
                count_true_playable += 1
            if compared_y[i] == False:
                count_false += 1
            if compared_y[i] == False and test_deck[i][-2] != -1:
                count_false_playable += 1
        print(count_true, count_true_playable, count_false, count_false_playable)
           
    def removing_jacks(self, card_list):
        # entfernt die Buben aus einer Kartenliste
        for suit in range(len(card_list)):
            for card in card_list[suit]:
                if card.value == 2:
                    card_list.remove(card)
        return card_list
    
    def get_jacks_list(self):
        # gibt alle Buben des Spielers in einer Liste zurück
        jacks = [None, None, None, None]
        for card in self.cards:
            if card.value == 2:
                jacks[3 - card.suit] = card
        return jacks
    
    def bubble_sort_suit(self, card_list, number_lists):
        # sortiert die Karten nach der Kartenfarbe
        for all_cards in range(number_lists):
            for remaining_cards in range(number_lists - all_cards - 1):
                if len(card_list[remaining_cards]) < len(card_list[remaining_cards + 1]):
                    card_list[remaining_cards], card_list[remaining_cards + 1] = card_list[remaining_cards + 1], card_list[remaining_cards]
        return card_list
    
    def compare_equal_len(self, card_list, n_equal_lists):
        '''
        ermittelt die höherwertige Kartenfarbe bei gleicher Länge
        '''
        highest_avg_value = 0
        for list_cards in range(n_equal_lists):
            count_cards = 0
            sum_values = 0
            # berechne den Durchschnittswert der Karten einer Farbe
            for card in range(len(list_cards)):
                count_cards += 1
                if not list_cards[card].check_louse():
                    sum_values += list_cards[card].value
            if sum_values/count_cards > highest_avg_value:
                highest_avg_value = sum_values/count_cards
                new_list = card_list[list_cards]
        # gebe die Farbe mit dem höchsten Durchschnittswert zurück
        return new_list
    
    def bidding_with_learning(self, cards):
        # berechnet die vorhergesagte Farbe durch die KI für den Spieler
        possible_trump = model1.run_game(cards)
        if possible_trump == -1:
            self.possible_trump = None
        else:
            self.possible_trump = possible_trump
            self.possible_trump = self.convert_card_suit_int_to_str(self.possible_trump)
    
    def bidding_without_learning(self, card_lists, jacks):
        '''
        bewertet das Blatt mit dem Naiven Algorithmus
        '''
        # Kriterium: Anzahl Buben
        if len(jacks) > 1:
            self.value_possible_trump += 1
        elif not jacks:
            self.value_possible_trump -= 1
        
        # Kriterium: Anzahl Trumpf
        if len(card_lists[0]) + len(jacks) < 5:
            self.value_possible_trump -= 1
        elif len(card_lists[0]) + len(jacks) > 7:
            self.value_possible_trump += 2
        elif len(card_lists[0]) + len(jacks) == 6 or len(card_lists[0]) + len(jacks) == 7:
            self.value_possible_trump += 1
            
        # Kriterium: Beiblatt
        temp_value = 0
        for i in range(1, len(card_lists)):
            for j in range(len(card_lists[i])):
                if card_lists[i][j].value == 10 or card_lists[i][j].value == 11:
                    if len(card_lists[i]) > 1:
                        temp_value += 1
                elif card_lists[i][j] == 10 and len(card_lists[i]) == 1:
                    temp_value -= 1
        if temp_value < 0:
            self.value_possible_trump -= 1
        elif temp_value > 1:
            self.value_possible_trump += 1
          
        # Kriterium: Freifarben  
        if len(card_lists[-1]) > 1:
            self.value_possible_trump -= 1
        
        if len(card_lists[-1]) == 0:
            self.value_possible_trump += 1
        
        if self.value_possible_trump < 0:
            self.possible_trump, self.value_possible_trump = None, float('-inf') 
    
    def MCTS(self, all_cards, temp_played_cards, trump, team_order, first_card_index, initial_cards):
        '''
        Verknüpfung zur Berechnung der gespielten Karte durch den MCTS
        '''
        # Alle noch vorhandenen Karten 
        initial_cards = [card for card in initial_cards if card is not None]
        dict_cards = {0: [card for card in player1.cards if card is not None],
                        1: [card for card in player2.cards if card is not None],
                        2: [card for card in player3.cards if card is not None]}
        players = {0: player1,
                        1: player2,
                        2: player3}
        
        # Initialisieren des Suchbaums
        if dict_cards[int(self.name[-1]) - 1]:
            node = MCTS_Node(players, dict_cards, self.playing_hand, self.playing_hand, temp_played_cards, int(self.name[-1]) - 1, trump, 
                             team_order, first_card_index, parent = None, action = None, weight_is_changed = False)
            best_card = node.best_action()
            return best_card.action
 
    
    def points_players_MCTS(self, team, points):
        '''
        Hilfsmethode für den Suchbaum
        '''
        # Punkte eines Spielers entsprechend des Teams erhöhen
        if team == self.team:
            self.team_points_MCTS += points
        else:
            self.other_team_points_MCTS += points
    
    def get_points_players_MCTS(self):
        # gibt die Punkte der Teams zurück
        return self.team_points_MCTS, self.other_team_points_MCTS


    def reset_point_players_MCTS(self):
        # setzt die Punkte der Teams zurück
        self.team_points_MCTS = 0
        self.other_team_points_MCTS = 0
    
    def convert_card_suit_int_to_str(self, var):
        # wandelt den Datentyp der Kartenfarbe um in einen String
        suit_dict = {
            0: "diamonds",
            1: "hearts",
            2: "spades",
            3: "clubs"
        }
        var = suit_dict[var]
        return var
    
    def convert_card_suit_str_to_int(self, var):
        # wandelt den Datentyp der Kartenfarbe um in einen Integer
        suit_dict = {
            "diamonds": 0,
            "hearts": 1,
            "spades": 2,
            "clubs": 3
        }
        var = suit_dict[var]
        return var
    
    def increase_n(self):
        # erhöht die Anzahl der Besuche der Spielerknoten im Baum
        self.n += 1
    
    def reset_n(self):
        # setzt die Anzahl der Besuche der Spielerknoten im Baum zurück
        self.n = 0

    
player1 = Player("Player 1")
player2 = Player("Player 2")
player3 = Player("Player 3")

#player1.calculate_power_of_algorithm()


P = Player # type for players
C = Card # type for cards

class MCTS_Node:
   
    def __init__(self, players: P, current_state: Dict[str, P], playing_hand: int, 
                 player_playing_hand: int, temp_played_cards: List[C], 
                 player_index: int, trump, team_order: List, first_card_index: int, parent = None, 
                 action = None, weight_is_changed = False):
        
        self.players = players # drei Spieler
        self.player = self.players[player_index] # aktueller Spieler
        self.current_state = current_state
        self.player_playing_hand = player_playing_hand # Vorhand, Mittelhand und Rückhand des Spielers
        self.playing_hand = playing_hand # Vorhand, Mittelhand und Rückhand des Knotens
        self.player_index = player_index # Index eines Spielers
        self.player_playing_index = int(self.player.name[-1]) - 1 # Index des aktuellen Spieler des Knotens
        self.temp_played_cards = temp_played_cards # Liste für den Stich
        self.trump = trump # Trumpf
        if type(self.trump) == str:
            # umwandeln in einen Integer
            self.trump = self.player.convert_card_suit_str_to_int(trump)
        
        self.first_card_index = first_card_index # Index der Vorhand
        self.parent = parent # Elternknoten
        self.action = action # gespielte Karte
        self.children = [] # Kindsknoten
        self.number_of_visits = 0 # Anzahl der Besuche
        self.possible_moves = None # alle Karten, die urch Kiindsknoten gespielt werden können
        self.possible_moves = self.get_possible_moves()
        self.outcomes = defaultdict(int)
        self.outcomes[1] = 0 # Gewinn
        self.outcomes[-1] = 0 # Verlust
        self.team_order = team_order # Reihenfolge der Teamverteilung
        # ursprünglichen Karten des Stiches, 
        # benötigt wegen Playout-Phase
        self.initial_card_index_1 = self.temp_played_cards[0]
        self.initial_card_index_2 = self.temp_played_cards[1]
        self.initial_card_index_3 = self.temp_played_cards[2]
        self.bool_expanding = True
        self.weight_is_changed = weight_is_changed
     
    def is_winnable_game(self, mode):
        '''
        überprüft ob der aktuelle Stich gewonnen werden kann
        '''
        played_cards = [self.temp_played_cards[0], self.temp_played_cards[1],
                        self.temp_played_cards[2]]
        # Ziel: eigenes Team gewinnt den Stich
        # Hinterhand
        if played_cards.count(None) == 1:
            for move in self.possible_moves:
                played_cards[self.player_index] = move
                winner_card, points = self.three_cards_winner(played_cards)
                if (mode == 1 and self.team_order[played_cards.index(winner_card)] == self.player.team) or (mode == 2 and self.team_order[played_cards.index(winner_card)] != self.player.team):
                    return False
            return True
             
        # Mittelhand       
        elif played_cards.count(None) == 2:
            for move in self.possible_moves:
                played_cards[self.player_index] = move
                for next_move in self.set_possible_moves(played_cards[self.first_card_index], 
                                                         self.current_state[self.player_index + 1] if self.player_index < 2 else self.current_state[self.player_index - 2]):
                    played_cards[self.player_index - 2] = next_move
                    winner_card, points = self.three_cards_winner(played_cards)
                    if (mode == 1 and self.team_order[played_cards.index(winner_card)] == self.player.team) or (mode == 2 and self.team_order[played_cards.index(winner_card)] != self.player.team):
                        return False
            return True
            
    def get_possible_moves(self):
        # gibt die möglichen Karten der Kindsknoten zurück
        return self.set_possible_moves(self.temp_played_cards[self.first_card_index], self.current_state[self.player_index])
       
    def get_player_position(self):
        # gibt zurück, ob ein Spieler in Vor-, Mittel- oder Hinterhand sitzt
        count = 0
        for card in self.temp_played_cards:
            if card != None:
                count += 1
        return count

    def get_n_visits(self):
        # gibt die Anzahl der Knotenbesuche zurück
        return self.number_of_visits
    
    def difference_wins_losses(self):
        # berechnet die Differenz zwischen dem Gewinn und dem Verlust
        return self.outcomes[1] - self.outcomes[-1]
    
    def set_possible_moves(self, first_card, card_list):
        '''
        berechnet die möglichen Karten der Kindsknoten
        '''
        
        card_list = [card for card in card_list if card is not None]
        # wenn Vorhand, werden stehen alle Karten zur Verfügung
        if not first_card:
            return card_list
        else:
            possible_moves = []
            suits = [card.suit for card in card_list if card.value != 2]
            values = [card.value for card in card_list]
            
            # Fall 1: Kein Trumpf angespielt durch die Vorhand
            if first_card.suit != self.trump and first_card.value != 2:
                if first_card.suit not in suits:
                    return card_list
                possible_moves = [card for card in card_list if card.suit == first_card.suit and card.value != 2]
                return possible_moves
            
            else:
                # Fall 2: Bube oder Trumpf angespielt
                if first_card.value == 2 or first_card.suit == self.trump:
                    # Bube oder Trumpfkarte vorhanden
                    if self.trump in suits or 2 in values:
                        possible_moves = [card for card in card_list if card.suit == self.trump or card.value == 2]
                        return possible_moves
                    else:
                        return card_list
                # Fall 3: Farbe kann bedient werden
                elif first_card.suit in suits:
                    possible_moves = [card for card in card_list if card.suit == first_card.suit]
                    return possible_moves
                return card_list
        
    def no_moves_left(self):
        # gibt zurück ob weitere Karten gespielt werden können
        return len(self.possible_moves) == 0
    
    def is_game_over(self, liste):
        # gibt zurück ob das Spiel beendet ist
        if len(liste) == 0:
            return True
        return False
    
    def is_leaf_node(self):
        # gibt zurück ob der aktuelle Knoten ein Blattknoten ist
        if not self.children:
            return True
        return False

    def expand(self):
        '''
        expandiert den Baum um eine weitere Knotentiefe in einem Pfad,
        die einzelnen Fälle der Spielzustände werden unterschieden, Attribute der
        neuen Knoten unterscheiden sich leicht
        '''
        self.possible_moves = self.get_possible_moves()
        if self.get_possible_moves():
            for card in self.possible_moves:
                # wenn in Vorderhand
                if not None in self.temp_played_cards:
                    child = MCTS_Node(self.players, self.current_state, 1, 
                                    self.player_playing_hand, self.temp_played_cards, 
                                    self.first_card_index, self.trump, 
                                    self.team_order, self.first_card_index, 
                                    parent = self, action = card, weight_is_changed = False)
                # in Mittelhand
                elif self.playing_hand < 3:
                    # nicht Spieler 3
                    if self.player_index < 2:
                        child = MCTS_Node(self.players, self.current_state, self.playing_hand + 1, 
                                        self.player_playing_hand, self.temp_played_cards, 
                                        self.player_index + 1, self.trump,
                                        self.team_order, self.first_card_index,
                                        parent = self, action = card, weight_is_changed = False)
                    else:
                        # Spieler 3
                        child = MCTS_Node(self.players, self.current_state, self.playing_hand + 1,
                                        self.player_playing_hand, self.temp_played_cards, 0,
                                        self.trump, self.team_order, self.first_card_index,
                                        parent = self, action = card, weight_is_changed = False)
                else:
                    # in Hinterhand
                    # nicht Spieler 3
                    if self.player_index < 2:
                        child = MCTS_Node(self.players, self.current_state, 1, self.player_playing_hand, 
                                        self.temp_played_cards, self.player_index + 1, self.trump, 
                                        self.team_order, self.first_card_index,
                                        parent = self, action = card, weight_is_changed = False)
                    else:
                        # Spieler 3
                        child = MCTS_Node(self.players, self.current_state, 1, self.player_playing_hand,
                                        self.temp_played_cards, 0, self.trump, self.team_order, self.first_card_index, 
                                        parent = self, action = card, weight_is_changed = False)
                self.children.append(child)
            # erster Kindsknoten wird zurückgegeben
            return self.children[0]
        self.bool_expanding = False
        return self
        
    def backpropagate(self, outcome, position):
        '''
        geht den Pfad entlang und verändert die Ergebnisse, nachdem eine 
        Playout-Phase beendet wurde
        '''
        # Stichkarten werden zurückgesetzt
        self.temp_played_cards[0] = self.initial_card_index_1
        self.temp_played_cards[1] = self.initial_card_index_2
        self.temp_played_cards[2] = self.initial_card_index_3
        self.number_of_visits += 1
        self.outcomes[position] += outcome
        # Elternknoten wird besucht
        if self.action:
            self.parent.current_state = self.current_state
            self.parent.bool_expanding = self.bool_expanding
            self.parent.current_state[self.parent.player_index].append(self.action)
            self.parent.backpropagate(outcome, position)
    
    def rollout(self):
        '''
        auch Playout genannt, spielt das Spiel vom aktuellen Knoten mit
        zufällig gewählten Karten zu Ende
        '''
        # Anfangswerte werden festgelegt
        current_rollout_state = self.current_state.copy()
        initial_rollout_state = {0: [],
                                 1: [],
                                 2: []}
        initial_playing_hand = self.playing_hand
        initial_player_index = self.player_index
        initial_player_playing_hand = self.player_playing_hand
        initial_first_card_index = self.first_card_index
        # solange das Ende des Spiels nicht erreicht ist und am Ende wieder der Anfangsspieler gesetzt wurde (zweite Bedingung ist notwendig,
        # sonst wird zu früh abgebrochen)
        while not (self.is_game_over(current_rollout_state[self.player_index]) and self.playing_hand == 1):
            # ermittle die möglichen Züge
            self.possible_moves = self.set_possible_moves(self.temp_played_cards[self.first_card_index], current_rollout_state[self.player_index])
            # gespielter Zug wird ausgewählt
            action = self.rollout_policy(self.possible_moves)
            # Karte entfernen
            if action is not None:
                current_rollout_state[self.player_index].remove(action)
                initial_rollout_state[self.player_index].append(action)
                self.move(action, self.player_index)
            else:
                break
        # Werte zurücksetzen
        self.current_state = initial_rollout_state
        self.playing_hand = initial_playing_hand
        self.player_playing_hand = initial_player_playing_hand
        self.player_index = initial_player_index
        self.first_card_index = initial_first_card_index
        self.temp_played_cards[0] = self.initial_card_index_1
        self.temp_played_cards[1] = self.initial_card_index_2
        self.temp_played_cards[2] = self.initial_card_index_3
            
        return self.game_result()
           
    def best_child(self, c_param = 2):
        '''
        wendet die UCB1-Formel an
        '''
        # ermittle ob der Stich gewonnen werden kann oder nicht
        is_not_winnable = self.is_winnable_game(1)
        is_winnable = self.is_winnable_game(2)
        # Berechnung der UCB1-Formel der Kindsknoten
        choices_weight = [(c.difference_wins_losses()) + c_param * np.sqrt(np.log(self.parent.number_of_visits if self.parent else self.number_of_visits)/self.number_of_visits) for c in self.children]
        # Werte werden entsprechend der Beobachtungen und den möglichen Fällen optimiert
        for i in range(len(choices_weight)):
            # wenn: Stich ist gewonnen, Bube wird gespielt
            if is_winnable and self.children[i].action.value == 2:
                choices_weight[i] *= 0.28
            # wenn: Stich wird nicht gewonnen und Lusche wird gespielt
            if is_not_winnable and self.children[i].action.check_louse():
                # Alleinspieler
                if not self.player.team:
                    choices_weight[i] *= 3.36
                else:
                    choices_weight[i] *= 3.46
            # Trumpfkarte wird angespielt
            if self.children[i].action.is_trump(self.trump):
                # Alleinspieler
                if not self.player.team:
                    choices_weight[i] *= 2.79
                else:
                    choices_weight[i] *= 0.61
        return self.children[np.argmax(choices_weight)]
    
    def rollout_policy(self, possible_moves):
        # wähle eine zufällige Karte aus
        if possible_moves:
            return possible_moves[np.random.randint(0, len(possible_moves))]
        
    def tree_policy(self):
        '''
        Übergang von Selektions- in Expansionsphase
        '''
        current_node = self
        # bis Blattknoten erreicht ist
        while not current_node.is_leaf_node():
            # bester Knoten selektieren
            if current_node.checking_children():
                current_node = current_node.best_child()
            else:
                current_node = current_node.get_first_possible_child()
            
            # Stichkarten vom Elternknoten übernommen
            current_node.temp_played_cards[0] = current_node.parent.temp_played_cards[0]
            current_node.temp_played_cards[1] = current_node.parent.temp_played_cards[1]
            current_node.temp_played_cards[2] = current_node.parent.temp_played_cards[2]
            
            # Stichkarte aktueller Spieler gesetzt
            current_node.temp_played_cards[current_node.parent.player_index] = current_node.action
            
            # wenn Stich vollendet
            if None not in current_node.temp_played_cards:
                current_node.increase_team_points()
                current_node.temp_played_cards = [None, None, None]
            # Vorhand neu bestimmen
                current_node.player_index = current_node.first_card_index
            # Spielstatus vom Elternknoten übernehmen
            if current_node.parent:
                current_node.current_state = current_node.parent.current_state
            # aktualisieren
            if current_node.action is not None and current_node.action in current_node.current_state[current_node.parent.player_index]:
                current_node.current_state[current_node.parent.player_index].remove(current_node.action)
       # noch nicht besucht, sofort in rollout phase
        if current_node.get_n_visits() == 0:
            return current_node
        else:
            # expandieren
            current_node = current_node.expand()
            # werte des neuen knotens initialisieren
            if current_node.bool_expanding:
                current_node.initial_card_index_1 = current_node.temp_played_cards[0]
                current_node.initial_card_index_2 = current_node.temp_played_cards[1]
                current_node.initial_card_index_3 = current_node.temp_played_cards[2]
                
                current_node.move_expansion(current_node.action, current_node.parent.player_index)
                current_node.current_state[current_node.parent.player_index].remove(current_node.action)
            return current_node
       
    def checking_children(self):
        # überprüfen ob alle Kinder bereits besucht wurden
        children_visits = [child.number_of_visits for child in self.children]
        if 0 in children_visits:
            return False
        return True
    
    def get_first_possible_child(self):
        # gibt das erste Kinde zurück was nicht besucht wurde
        for child in self.children:
            if child.number_of_visits == 0:
                return child
        
    def move(self, action, playing_index):
        # spielt eine Karte für den Spieler im Stich, um den Zutand des des Knotens zu aktualisieren
        self.temp_played_cards[playing_index] = action
        # wenn der Knoten in Hinterhand gespielt
        if not None in self.temp_played_cards:
            self.increase_team_points()
            self.temp_played_cards = [None, None, None]
            self.player_index = self.first_card_index
        else:
            # Folgende gespielte Hand setzen
            if self.playing_hand < 3:
                self.playing_hand += 1
            if self.player_index < 2:
                self.player_index += 1
            else:
                self.player_index = 0
          
    def move_expansion(self, action, playing_index):
        # leicht abgeänderte move-Methode für die Expansionsphase, 
        # playing hand wird nicht aktualisiert
        self.temp_played_cards[playing_index] = action
        if not None in self.temp_played_cards:
            self.increase_team_points()
            self.temp_played_cards = [None, None, None]
            self.player_index = self.first_card_index
    
    def is_time_over(self):
        # Zeitintervall vergleichen
        global start_time
        end_time = time.time()
        if end_time - start_time >= 1:
            return True
        return False
    
    def best_action(self):
        '''
        Für die Baum-Traversierung verantwortlich, von Spielerklasse 
        aufgerufen
        '''
        global start_time
        simulations = 0
        start_time = time.time()
        #must_playing_card = self.is_not_winnable_game()
        while not self.is_time_over():
            simulations += 1
            # Punkte und Besuche des Spielers zurücksetzen, für Hilfsmethoden
            # wichtig
            self.player.reset_n()
            self.player.reset_point_players_MCTS()
            # aktuellen Knoten in die Baumtraversierung "geben"
            node = self.tree_policy()
            # rollout Phase beginnen, wenn expandiert wurde
            if self.bool_expanding:
                results, position = node.rollout()
            # den Pfad rückpropagieren
            node.backpropagate(results, position)
        # beste Karte finden
        best_action = self.best_child(c_param = 2)
        return best_action
    
    def three_cards_winner(self, cards):
        '''
        Stichgewinner herausfinden, äquivalent zur
        get_temp_winner-Methode in game.py
        '''
        winner_card = None
        points = 0
        cards_playing_order = self.get_correct_playing_order(cards)
        served_suit = cards_playing_order[0].suit
        highest_jack_suit = None
        highest_value = 0
        count_trump = 0
        count_jacks = 0
        count_louses = 0
        
        for card in cards_playing_order:
            if not card.check_louse():
                points += card.value
            
            if not self.check_card_trump(card):
                if card.suit == served_suit and count_trump == 0:
                    if card.check_louse():
                        count_louses += 1
                        if winner_card != None and (highest_value == 7 or highest_value == 8 or highest_value == 9):
                            highest_value = self.compare_higher_value(card.value, highest_value)
                        elif winner_card == None:
                            highest_value = card.value
                    else:
                        if winner_card != None and (highest_value != 7 and highest_value != 8 and highest_value != 9):
                            highest_value = self.compare_higher_value(card.value, highest_value)
                        else:
                            highest_value = card.value 
                    if highest_value == card.value or winner_card == None:
                        winner_card = card
            else:
                count_trump += 1
                if card.value == 2:
                    count_jacks += 1
                    highest_jack_suit = self.compare_higher_suit(card.suit, highest_jack_suit)
                    if highest_jack_suit == card.suit:
                        winner_card = card
                        highest_value = card.value
                else:
                    if count_jacks == 0:
                        if not card.check_louse():
                            if count_trump == 1:
                                highest_value = card.value
                            elif winner_card != None and (highest_value != 7 and highest_value != 8 and highest_value != 9):
                                highest_value = self.compare_higher_value(card.value, highest_value)
                            else:
                                highest_value = card.value
                        else:
                            count_louses += 1
                            if count_trump == 1:
                                highest_value = card.value
                            else:
                                if count_louses == count_trump:
                                    highest_value = self.compare_higher_value(card.value, highest_value)
                        if highest_value == card.value or winner_card == None:
                            winner_card = card
        return winner_card, points
    
    def increase_team_points(self):
        '''
        erhäht die Punte der jeweilgen Spieler, nach einem Stichgewinn
        '''
        # Gewinner finden
        winner_card, points = self.three_cards_winner([self.temp_played_cards[0], 
                                               self.temp_played_cards[1],
                                               self.temp_played_cards[2]])
        
        for i in range(len(self.temp_played_cards)):
            if i == self.player_playing_index:
                for j in range(len(self.temp_played_cards)):
                    # wenn untersuchter Spieler gewonnen hat
                    if self.temp_played_cards[j] == winner_card:
                        # Punkte erhöhen
                        self.player.points_players_MCTS(self.team_order[j], points)
                        self.first_card_index = j
                        self.player_index = j
                        if i == j:
                            self.player_playing_hand = 1
                        if i == j + 1 or i == j - 2:
                            self.player_playing_hand = 2
                        if i == j + 2 or i == j - 1:
                            self.player_playing_hand = 3
                        self.playing_hand = 1
                        break
                       
    def check_card_trump(self, card):
        # überprüft ob eine Karte dem Trumpf angehört
        if card.suit == self.trump or card.value == 2:
            return True
        return False
     
    def compare_higher_value(self, value, so_far_highest_value):
        # vergleicht die Kartenwerte zweier Karten
        if value > so_far_highest_value:
            return value
        return so_far_highest_value
    
    def compare_higher_suit(self, suit, so_far_highest_suit):
        # vergleicht die Farbe zweier Karten
        if so_far_highest_suit != None:
            if suit >= so_far_highest_suit:
                return suit
            return so_far_highest_suit
        return suit

    def get_correct_playing_order(self, temp_played_cards):
        # setzt die Spielordnung in die gewünschte Reihenfolge
        cards_playing_order = []
        # abhängig vom Index der Vorderhand
        if self.first_card_index == 0:
            cards_playing_order.append(temp_played_cards[0])
            cards_playing_order.append(temp_played_cards[1])
            cards_playing_order.append(temp_played_cards[2])
        elif self.first_card_index == 1:
            cards_playing_order.append(temp_played_cards[1])
            cards_playing_order.append(temp_played_cards[2])
            cards_playing_order.append(temp_played_cards[0])
        else:
            cards_playing_order.append(temp_played_cards[2])
            cards_playing_order.append(temp_played_cards[0])
            cards_playing_order.append(temp_played_cards[1])
        return cards_playing_order
       
    def game_result(self):
        '''
        berechnet das Spielergebnis am Ende eines Pfades
        '''
        own_team_points, other_team_points = self.player.get_points_players_MCTS()
        # fragt die einzelnen Fälle ab (TEamspieler/Alleinspieler, gewonnen/verloren)
        if self.team_order[self.player_playing_index] == True:
            if own_team_points > 60:
                return own_team_points, 1
            else:
                return other_team_points, -1
        else:
            if own_team_points >= 60:
                return own_team_points, 1
            return other_team_points, -1
