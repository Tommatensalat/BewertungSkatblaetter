import random

class Card(object):
    
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit
        
    def get_value(self):
        # gibt den Wert einer Karte zurück
        return self.value
    
    def get_suit(self):
        # gibt die Farbe einer Karte zurück
        return self.suit
    
    def check_louse(self):
        # gibt zurück, ob die Karte eine Lusche ist
        if self.value == 7 or self.value == 8 or self.value == 9:
            return True
        return False
    
    def is_trump(self, trump):
        # gibt zurück, ob die Karte Teil des Trumpfes ist 
        if self.suit == trump or self.value == 2:
            return True
        return False
    
    def __repr__(self):
        # repräsentiert die Darstellung der Karte
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
        # eine Sammlung von Karten
        super().__init__()
        
    def create_deck(self):
        '''
        dem Deck werden alle Karten zugefügt
        '''
        # Mögliche Kartenfarben
        suits = list(range(4))
        # Werte der Luschen + Wert der Karte 10 und Ass
        values_louses = list(range(7, 12))
        # Werte der anderen Karten
        value_others = list(range(2, 5))
        # Kreuzung und Hinzufügen
        [[self.append(Card(value, suit)) for suit in suits] for value in values_louses]
        [[self.append(Card(value, suit)) for suit in suits] for value in value_others]
                
    def shuffle(self):
        # mischt die Karten zufällig
        random.shuffle(self)

deck = Deck()

