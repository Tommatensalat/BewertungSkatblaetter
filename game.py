from players import player1, player2, player3
from cards import Card
import random

class Game (object):
    
    def __init__(self):
        self.trump = None # Trumpffarbe
        self.bidding_winner = None # Gewinner beim Reizen, Alleinspieler
        self.player1 = player1
        self.player2 = player2
        self.player3 = player3
        self.total_cards = [player1.cards, player2.cards, player3.cards]
        self.total_points = 0
        self.count_played_cards = 0
        self.playing_order = None # Reihenfolge in der gespielt wird
        self.trump_value = float("-inf")
        self.games = 0 # Anzahl der Spiele, die unter dieser Verteilung gespielt wurden
    
    def increase_number_of_games(self): # erhöht die Anzahl der gespielten Spiele
        self.games += 1
    
    def set_trump(self, trump):
        # legt den Zahlenwert für den Trumpf fest
        trump_dict = {
            "diamonds" : 0,
            "hearts" : 1,
            "spades" : 2,
            "clubs" : 3,
        }
        self.trump = trump_dict[trump]
        
    def set_playing_hands(self, first_player):
        # die Reihenfolge, in der ein Stich gespielt wird, wird festgelegt
        if first_player == player1:
            player1.playing_hand, player2.playing_hand, player3.playing_hand = 1, 2, 3
        if first_player == player2:
            player1.playing_hand, player2.playing_hand, player3.playing_hand = 3, 1, 2
        if first_player == player3:
            player1.playing_hand, player2.playing_hand, player3.playing_hand = 2, 3, 1
       
    def compare_higher_value(self, value, so_far_highest_value):
        # vergleicht die Werte von zwei Karten
        if value > so_far_highest_value:
            return value
        return so_far_highest_value
    
    def compare_higher_suit(self, suit, so_far_highest_suit):
        # vergleicht die Farben von zwei Karten
        if so_far_highest_suit != None:
            if suit >= so_far_highest_suit:
                return suit
            return so_far_highest_suit
        return suit
    
    def get_temp_winner(self, comb1: tuple(), comb2: tuple(), comb3: tuple()):
        '''
        gibt den Stichgewinner zurück
        '''
        served_suit = comb1[1].suit # farbe der Karte von der Vorhand
        highest_jack_suit = None # höchster angespielter Bube
        highest_value = 0 # höchster angespielter Wert
        count_trump = 0 # Anzahl der angespielten Trumpfkarten
        count_jacks = 0 # Anzahl der angespielten Buben
        count_louses = 0 # Anzahl der angespielten Luschen
        winner = None # Stichgewinner
        list_comb = [comb1, comb2, comb3]
        # Umwandlung Trumpf in einen Integer
        if type(self.trump) == str:
            self.trump = comb1[0].convert_card_suit_str_to_int(self.trump)
        for comb in list_comb:
            # wenn kein Trumpf vom untersuchten Spieler angespielt wurde
            if not self.check_trump(comb[1]):
                # wenn Farbe bedient wurde und noch kein Trumpf angespielt wurde
                if comb[1].suit == served_suit and count_trump == 0:
                    # wenn eine Lusche angespielt wurde vom untersuchten Spieler
                    if comb[1].check_louse():
                        count_louses += 1
                        # wenn untersuchter Spieler in Mittelhand und Hinterhand sitzt
                        # und die aktuell höchste Karte eine Lusche ist
                        if winner != None and (highest_value == 7 or highest_value == 8 or highest_value == 9): 
                            # verlgeiche beide angespielten Karten miteinander
                            highest_value = self.compare_higher_value(comb[1].value, 
                                                        highest_value)
                        # wenn untersuchter Spieler in Vorhand sitzt
                        elif winner == None:
                            # automatisch temporärer Gewinner
                            highest_value = comb[1].value
                    else:
                        # wenn vom untersuchten Spieler keine Lusche angespielt wurde
                        # wenn untersuchter Spieler in Mittelhand oder Hinterhand sitzt
                        # und die aktuell höchste Karte keine Lusche ist
                        if winner != None and (highest_value != 7 and highest_value != 8 and highest_value != 9):
                            highest_value = self.compare_higher_value(comb[1].value,
                                                                  highest_value)
                        else:
                            highest_value = comb[1].value
                    # wenn die Karte des untersuchten Spielers die temüorär höchste Karte darstellt
                    # wird der Gewinner überschrieben      
                    if highest_value == comb[1].value or winner == None:
                        winner = comb[0]
            # wenn eine Trumpfkarte vom untersuchten Spieler angespielt wurde
            else:
                count_trump += 1
                # wenn ein Bube angespielt wurde
                if comb[1].value == 2:
                    count_jacks += 1
                    # vergleiche den Buben mit dem aktuell höchsten Buben
                    highest_jack_suit = self.compare_higher_suit(comb[1].suit, 
                                                                  highest_jack_suit) 
                    # wenn neuer Bube höher ist, Gewinner überschreiben      
                    if highest_jack_suit == comb[1].suit:
                        winner = comb[0]  
                        highest_value = comb[1].value
                # normale Trumpfkarte wurde angespielt, kein Bube
                else:
                    # bisher noch kein Bube angespielt
                    if count_jacks == 0:
                        # keine Lusche angespielt
                        if not comb[1].check_louse():
                            # der einzig angespielte Trumpf
                            if count_trump == 1:
                                highest_value = comb[1].value
                            # verlgeiche beide Karten miteinander, wenn aktueller Gewinner keine Lusche angespielt hat
                            elif winner != None and highest_value != 7 and highest_value != 8 and highest_value != 9:
                                highest_value = self.compare_higher_value(comb[1].value, 
                                                                highest_value)
                            else:
                                highest_value = comb[1].value
                        # wenn vom untersuchten Spieler eine Lusche angespielt wurde
                        else:
                            count_louses += 1
                            if count_trump == 1:
                                highest_value = comb[1].value
                            else:
                                # wenn alle angespielten Trumpfkarten Luschen sind
                                if count_louses == count_trump:
                                    highest_value = self.compare_higher_value(comb[1].value,
                                                                              highest_value) 
                        if highest_value == comb[1].value or winner == None:
                            winner = comb[0]
        return winner 
    
    def get_highest_louse(self, louse, so_far_highest_louse):
        # gibt die höhere Lusche zurück, wenn kein Trumpf angespielt wurde
        if louse > so_far_highest_louse and not self.check_trump(louse):
            return louse
        return so_far_highest_louse                              
    
    def check_trump(self, card):
        # gibt zurück, ob ein Trumpf angespielt wurde
        if card.suit == self.trump or card.value == 2:
            return True
        return False
        
    def get_number_of_cards(self, list_comparing_cards):
        # gibt zurück, ob alle Karten im aktuellen Stich angespielt wurden
        if self.frequency_analysis(None, list_comparing_cards) == 0:
            return True
        return False
    
    def frequency_analysis(self, var, list):
        '''
        untersucht die Anzahl eines Elementes in einer Liste
        '''
        amount_of_var = 0
        for i in list:
            if i == var:
                amount_of_var += 1
        return amount_of_var
    
    def set_total_points(self, points_player1, points_player2, points_player3):
        # legt die insgesamt im Spiel erhaltenen Punkte fest
        self.total_points = points_player1 + points_player2 + points_player3

    def get_total_points(self):
        # gibt die Anzahl aller Punkte zurück
        return self.total_points
    
    def increase_count_played_cards(self, value):
        # erhöht die Anzahl der gespielten Karten um einen bestimmten Wert
        self.count_played_cards += value
        
    def get_winning_player(self, players_and_cards):
        # gibt die Spieler zurück, die das Spiel gewonnen haben
        for player in players_and_cards:
            if not player.team:
                if self.check_winning_points(player):
                    return player
                return [players for players in players_and_cards if players != player]
       
    def check_winning_points(self, winner):
        # überprüft ob der Gewinner genügend Punkte gesammelt hat
        if winner.points > 60:
            return True
        return False

    def reset_count_played_cards(self):
        # setzt die Anzahl der gespielten Karten zurück
        self.count_played_cards = 0
      
    def is_over(self):
        # gibt zurück, ob das Spiel vorbei ist
        if self.count_played_cards == 30:
            return True
        return False
    
    def set_game_order(self, players):
        '''
        legt die Reihenfolge beim Spielen fest
        '''
        # zufällig ausgewählter Spieler modelliert den Gegner
        giving_player = random.choice(players)
        giving_player.state = 1
        
        # Reihenfolge wird Geben->Hören->Sagen wird aufbauen darauf festeglegt
        for i in range(len(players)):
            if players[i] == giving_player:
                players[i - 2].state = 2
                listening_player = players[i - 2]
                players[i - 1].state = 3
                speaking_player = players[i - 1]
                break
        self.playing_order = [listening_player, speaking_player, giving_player]
        # spielende Hand wird gesetzt
        listening_player.playing_hand, speaking_player.playing_hand, giving_player.playing_hand = 1, 2, 3
            
    def get_game_trump(self, player_list):
        '''
        vergleicht die angegebenen gewünschten Trumpffarben zweier Spieler
        auf Grundlage ihrer Kartenkonstellation
        '''
        multiplicator = 0 # Multiplikator initialisieren
        index = 0
        for player in player_list:
            # die Buben eines Spielers werden anegegeben
            jacks = player.get_jacks_list()
            # wenn der Kreuz Bube vorhanden ist
            if jacks[0] != None:
                multiplicator = 1
                index = 1
                # führe die Schleife solange fort, bis die Bubenreihe unterbrochen ist
                while index < 4 and jacks[index] != None:
                    multiplicator += 1
                    index += 1
                # Multiplkator ein letztes Mal erhöhen
                multiplicator += 1
            # wenn der Kreuz Bube nicht vorhanden ist
            else:
                multiplicator = 5
                for jack in range(1, len(jacks)):
                    # Multiplikator wird entsprechend des ersten vorhandenen Buben gesetzt
                    if jacks[jack] != None:
                        multiplicator = jack + 1
                        break
            # wenn die Rolle als Alleinspieler vom Spieler gewünscht ist
            # (wenn die Algorithmen ein spielbares Blatt vorhergesagt haben)
            if player.possible_trump != None:            
                player.value_possible_trump = self.get_bidding_value_of_suits(player.possible_trump)
                player.value_possible_trump *= multiplicator
                # vergleicht den gewünschten Trumpf des Spielers mit dem aktuell
                # höchsten Trumpf im Spiel
                if player.value_possible_trump > self.trump_value:
                    self.trump, self.trump_value = player.possible_trump, player.value_possible_trump
                    self.bidding_winner = player
            
        return self.trump, self.bidding_winner
          
    def get_bidding_value_of_suits(self, suit):
        # gibt die Reizfarbe als Integer zurück
        dict_bidding_value_of_suits = {
            "diamonds": 9,
            "hearts": 10,
            "spades": 11,
            "clubs": 12
        }
        return dict_bidding_value_of_suits[suit]
    
    def set_teams(self, bidding_winner):
        # legt die Allein- und Teamspieler fest
        if player1 == bidding_winner:
            player1.team, player2.team, player3.team = False, True, True
        elif player2 == bidding_winner:
            player1.team, player2.team, player3.team = True, False, True
        elif player3 == bidding_winner:
            player1.team, player2.team, player3.team = True, True, False

game = Game()