import random

class Card(object):
    
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit
        
    # returns the value of a card
    def get_value(self):
        return self.value
    
    # returns the suit of a card
    def get_suit(self):
        return self.suit
    
    # checks if the card is a louse
    def check_louse(self):
        if self.value == 7 or self.value == 8 or self.value == 9:
            return True
        return False
    
    def is_trump(self, trump):
        if self.suit == trump or self.value == 2:
            return True
        return False
    
    # represents the output of a card
    def __repr__(self):
        value_name_dict = {
            7: "seven",
            8: "eight",
            9: "nine",
            10: "ten",
            2: "jack",
            3: "queen",
            4: "king",
            11: "ace"
        }
        value_name = value_name_dict[self.value]
            
        suit_name_dict = {
            0: "diamonds",
            1: "hearts",
            2: "spades",
            3: "clubs"
        }
        suit_name = suit_name_dict[self.suit]
        return value_name + "_of_" + suit_name


class Deck(list):
    
    def __init__(self):
        super().__init__()
        
    def create_deck(self):
        #self = []
        suits = list(range(4))
        values_louses = list(range(7, 11))
        value_others = list(range(2, 5))
        [[self.append(Card(value, suit)) for suit in suits] for value in values_louses]
        [[self.append(Card(value, suit)) for suit in suits] for value in value_others]
        value_ace = 11
        [self.append(Card(value_ace, suit)) for suit in suits]
                
    # shuffles the deck
    def shuffle(self):
        random.shuffle(self)

deck = Deck()

