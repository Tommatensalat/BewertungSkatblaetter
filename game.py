from players import player1, player2, player3
from cards import Card
import random

class Game (object):
    
    def __init__(self):
        self.trump = None
        self.bidding_winner = None
        self.player1 = player1
        self.player2 = player2
        self.player3 = player3
        self.total_cards = [player1.cards, player2.cards, player3.cards]
        self.total_points = 0
        self.count_played_cards = 0
        self.playing_order = None
        self.trump_value = float("-inf")
        self.games = 0
    
    # increases the number of games already played
    def increase_number_of_games(self):
        self.games += 1
    
    # sets the trump for the game    
    def set_trump(self, trump):
        trump_dict = {
            "diamonds" : 0,
            "hearts" : 1,
            "spades" : 2,
            "clubs" : 3,
        }
        self.trump = trump_dict[trump]
    
    # sets the order of the playing hands in the game    
    def set_playing_hands(self, first_player):
        if first_player == player1:
            player1.playing_hand, player2.playing_hand, player3.playing_hand = 1, 2, 3
        if first_player == player2:
            player1.playing_hand, player2.playing_hand, player3.playing_hand = 3, 1, 2
        if first_player == player3:
            player1.playing_hand, player2.playing_hand, player3.playing_hand = 2, 3, 1
    
    # compares the value of two cards    
    def compare_higher_value(self, value, so_far_highest_value):
        if value > so_far_highest_value:
            return value
        return so_far_highest_value
    
    # compares the suits of two cards
    def compare_higher_suit(self, suit, so_far_highest_suit):
        if so_far_highest_suit != None:
            if suit >= so_far_highest_suit:
                return suit
            return so_far_highest_suit
        return suit
    
    # compares the three cards    
    def get_temp_winner(self, comb1: tuple(), comb2: tuple(), comb3: tuple()):
        served_suit = comb1[1].suit
        highest_jack_suit = None
        highest_value = 0
        count_trump = 0
        count_jacks = 0
        count_louses = 0
        winner = None
        list_comb = [comb1, comb2, comb3]
        if type(self.trump) == str:
            self.trump = comb1[0].convert_card_suit_str_to_int(self.trump)
        for comb in list_comb:
            if not self.check_trump(comb[1]):
                if comb[1].suit == served_suit and count_trump == 0:
                    if comb[1].check_louse():
                        count_louses += 1
                        if winner != None and highest_value == 7 or highest_value == 8 or highest_value == 9: 
                            highest_value = self.compare_higher_value(comb[1].value, 
                                                        highest_value)
                        elif winner == None:
                            highest_value = comb[1].value
                    else:
                        if winner != None and (highest_value != 7 and highest_value != 8 and highest_value != 9):
                            highest_value = self.compare_higher_value(comb[1].value,
                                                                  highest_value)
                        else:
                            highest_value = comb[1].value        
                    if highest_value == comb[1].value or winner == None:
                        winner = comb[0]
            else:
                count_trump += 1
                if comb[1].value == 2:
                    count_jacks += 1
                    highest_jack_suit = self.compare_higher_suit(comb[1].suit, 
                                                                  highest_jack_suit)       
                    if highest_jack_suit == comb[1].suit:
                        winner = comb[0]  
                        highest_value = comb[1].value
                else:
                    if count_jacks == 0:
                        if not comb[1].check_louse():
                            if count_trump == 1:
                                highest_value = comb[1].value
                            elif winner != None and highest_value != 7 and highest_value != 8 and highest_value != 9:
                                highest_value = self.compare_higher_value(comb[1].value, 
                                                                highest_value)
                            else:
                                highest_value = comb[1].value
                        else:
                            count_louses += 1
                            if count_trump == 1:
                                highest_value = comb[1].value
                            else:
                                if count_louses == count_trump:
                                    highest_value = self.compare_higher_value(comb[1].value,
                                                                              highest_value) 
                        if highest_value == comb[1].value or winner == None:
                            winner = comb[0]
        return winner 
    
    # returns the highest louse
    def get_highest_louse(self, louse, so_far_highest_louse):
        if louse > so_far_highest_louse and not self.check_trump(louse):
            return louse
        return so_far_highest_louse                              
    
    # check if the card is a trump
    def check_trump(self, card):
        if card.suit == self.trump or card.value == 2:
            return True
        return False
        
    # checks the numbers of played cards
    def get_number_of_cards(self, list_comparing_cards):
        if self.frequency_analysis(None, list_comparing_cards) == 0:
            return True
        return False
    
    # calaculates the amount of a var in a list
    def frequency_analysis(self, var, list):
        amount_of_var = 0
        for i in list:
            if i == var:
                amount_of_var += 1
        return amount_of_var
    
    # sets the total points, already played in the game
    def set_total_points(self, points_player1, points_player2, points_player3):
        self.total_points = points_player1 + points_player2 + points_player3
    
    # returns the total points, already played in the game
    def get_total_points(self):
        return self.total_points
    
    # increases the count of played cards
    def increase_count_played_cards(self, value):
        self.count_played_cards += value
        
    # returns the winning player(s)    
    def get_winning_player(self, players_and_cards):
        for player in players_and_cards:
            if not player.team:
                if self.check_winning_points(player):
                    return player
                return [players for players in players_and_cards if players != player]
    
    # checks if the winner has enough points    
    def check_winning_points(self, winner):
        if winner.points > 60:
            return True
        return False

    # resets the count played cards to zero
    def reset_count_played_cards(self):
        self.count_played_cards = 0
    
    # returns if the game is over    
    def is_over(self):
        if self.count_played_cards == 30:
            return True
        return False
    
    # sets the order of playing the game
    def set_game_order(self, players):
        giving_player = random.choice(players)
        giving_player.state = 1
        for i in range(len(players)):
            if players[i] == giving_player:
                players[i - 2].state = 2
                listening_player = players[i - 2]
                players[i - 1].state = 3
                speaking_player = players[i - 1]
                break
        self.playing_order = [listening_player, speaking_player, giving_player]
        listening_player.playing_hand, speaking_player.playing_hand, giving_player.playing_hand = 1, 2, 3
            
    # returns the highest possible trump of the players for getting the game trump
    def get_game_trump(self, player_list):
        multiplicator = 0
        index = 0
        for player in player_list:
            jacks = player.get_jacks_list()
            if jacks[0] != None:
                multiplicator = 1
                index = 1
                while index < 4 and jacks[index] != None:
                    multiplicator += 1
                    index += 1
                multiplicator += 1
            else:
                multiplicator = 5
                for jack in range(1, len(jacks)):
                    if jacks[jack] != None:
                        multiplicator = jack + 1
                        break
            if player.possible_trump != None:            
                player.value_possible_trump = self.get_bidding_value_of_suits(player.possible_trump)
                player.value_possible_trump *= multiplicator
                if player.value_possible_trump > self.trump_value:
                    self.trump, self.trump_value = player.possible_trump, player.value_possible_trump
                    self.bidding_winner = player
            
        return self.trump, self.bidding_winner
    
    # returns the bidding value of a suit        
    def get_bidding_value_of_suits(self, suit):
        dict_bidding_value_of_suits = {
            "diamonds": 9,
            "hearts": 10,
            "spades": 11,
            "clubs": 12
        }
        return dict_bidding_value_of_suits[suit]
    
    # bubble sorts the possible trumps    
    def bubble_sort_trump(self, card_trumps, number_trumps):
        for all_trumps in range(number_trumps):
            for remaining_trumps in range(number_trumps - all_trumps - 1):
                if card_trumps[remaining_trumps][1] < card_trumps[remaining_trumps + 1][1]:
                    card_trumps[remaining_trumps], card_trumps[remaining_trumps + 1] = card_trumps[remaining_trumps + 1], card_trumps[remaining_trumps]
        return [(comb[0], comb[2]) for comb in card_trumps]
    
    # sets the teams of the game after bidding
    def set_teams(self, bidding_winner):
        if player1 == bidding_winner:
            player1.team, player2.team, player3.team = False, True, True
        elif player2 == bidding_winner:
            player1.team, player2.team, player3.team = True, False, True
        elif player3 == bidding_winner:
            player1.team, player2.team, player3.team = True, True, False

game = Game()