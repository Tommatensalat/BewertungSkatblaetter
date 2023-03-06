from tkinter import *
from players import player1, player2, player3
from game import game


def show_images():
    '''
    passt die Größe der Karten an und zeigt sie an
    '''
    
     # Images Player 1
    player1_image1 = player1.resize_card(f"assets/{player1.cards[0]}.png", False)
    l1.config(image = player1_image1)
    l1.image = player1_image1

    player1_image2 = player1.resize_card(f"assets/{player1.cards[1]}.png", False)
    l2.config(image = player1_image2)
    l2.image = player1_image2

    player1_image3 = player1.resize_card(f"assets/{player1.cards[2]}.png", False)
    l3.config(image = player1_image3)
    l3.image = player1_image3

    player1_image4 = player1.resize_card(f"assets/{player1.cards[3]}.png", False)
    l4.config(image = player1_image4)
    l4.image = player1_image4

    player1_image5 = player1.resize_card(f"assets/{player1.cards[4]}.png", False)
    l5.config(image = player1_image5)
    l5.image = player1_image5

    player1_image6 = player1.resize_card(f"assets/{player1.cards[5]}.png", False)
    l6.config(image = player1_image6)
    l6.image = player1_image6

    player1_image7 = player1.resize_card(f"assets/{player1.cards[6]}.png", False)
    l7.config(image = player1_image7)
    l7.image = player1_image7

    player1_image8 = player1.resize_card(f"assets/{player1.cards[7]}.png", False)
    l8.config(image = player1_image8)
    l8.image = player1_image8

    player1_image9 = player1.resize_card(f"assets/{player1.cards[8]}.png", False)
    l9.config(image = player1_image9)
    l9.image = player1_image9

    player1_image10 = player1.resize_card(f"assets/{player1.cards[9]}.png", False)
    l10.config(image = player1_image10)
    l10.image = player1_image10


    # Images Player 2
    player2_image1 = player2.resize_card(f"assets/{player2.cards[0]}.png", False)
    l11.config(image = player2_image1)
    l11.image = player2_image1

    player2_image2 = player2.resize_card(f"assets/{player2.cards[1]}.png", False)
    l12.config(image = player2_image2)
    l12.image = player2_image2

    player2_image3 = player2.resize_card(f"assets/{player2.cards[2]}.png", False)
    l13.config(image = player2_image3)
    l13.image = player2_image3

    player2_image4 = player2.resize_card(f"assets/{player2.cards[3]}.png", False)
    l14.config(image = player2_image4)
    l14.image = player2_image4

    player2_image5 = player2.resize_card(f"assets/{player2.cards[4]}.png", False)
    l15.config(image = player2_image5)
    l15.image = player2_image5

    player2_image6 = player2.resize_card(f"assets/{player2.cards[5]}.png", False)
    l16.config(image = player2_image6)
    l16.image = player2_image6

    player2_image7 = player2.resize_card(f"assets/{player2.cards[6]}.png", False)
    l17.config(image = player2_image7)
    l17.image = player2_image7

    player2_image8 = player2.resize_card(f"assets/{player2.cards[7]}.png", False)
    l18.config(image = player2_image8)
    l18.image = player2_image8

    player2_image9 = player2.resize_card(f"assets/{player2.cards[8]}.png", False)
    l19.config(image = player2_image9)
    l19.image = player2_image9

    player2_image10 = player2.resize_card(f"assets/{player2.cards[9]}.png", False)
    l20.config(image = player2_image10)
    l20.image = player2_image10

    # Images Player 3
    player3_image1 = player3.resize_card(f"assets/{player3.cards[0]}.png", False)
    l21.config(image = player3_image1)
    l21.image = player3_image1

    player3_image2 = player3.resize_card(f"assets/{player3.cards[1]}.png", False)
    l22.config(image = player3_image2)
    l22.image = player3_image2

    player3_image3 = player3.resize_card(f"assets/{player3.cards[2]}.png", False)
    l23.config(image = player3_image3)
    l23.image = player3_image3

    player3_image4 = player3.resize_card(f"assets/{player3.cards[3]}.png", False)
    l24.config(image = player3_image4)
    l24.image = player3_image4

    player3_image5 = player3.resize_card(f"assets/{player3.cards[4]}.png", False)
    l25.config(image = player3_image5)
    l25.image = player3_image5

    player3_image6 = player3.resize_card(f"assets/{player3.cards[5]}.png", False)
    l26.config(image = player3_image6)
    l26.image = player3_image6

    player3_image7 = player3.resize_card(f"assets/{player3.cards[6]}.png", False)
    l27.config(image = player3_image7)
    l27.image = player3_image7

    player3_image8 = player3.resize_card(f"assets/{player3.cards[7]}.png", False)
    l28.config(image = player3_image8)
    l28.image = player3_image8

    player3_image9 = player3.resize_card(f"assets/{player3.cards[8]}.png", False)
    l29.config(image = player3_image9)
    l29.image = player3_image9

    player3_image10 = player3.resize_card(f"assets/{player3.cards[9]}.png", False)
    l30.config(image = player3_image10)
    l30.image = player3_image10
    

def hand_the_deck():
    # teilt die Blätter an die Spieler aus
    global deck
    player1.take_cards(deck)
    player2.take_cards(deck)
    player3.take_cards(deck)
    if game.games == 0:
        game.set_game_order([player1, player2, player3])
    #player2.find_possible_trump()
    #player3.bidding_with_learning(player3.cards)
    
    

# shows the game trump in a label
def show_trump():
    global deck
    '''
    für die Trumpfanzeige der Spieler verantwortlich
    '''
    #game.trump, bidding_winner = game.get_game_trump([game.playing_order[0], game.playing_order[1]])
    #if bidding_winner == game.playing_order[0]:
    #    game.trump, bidding_winner = game.get_game_trump([game.playing_order[2], game.playing_order[1]])
    #elif bidding_winner == game.playing_order[1]:
    #    game.trump, bidding_winner = game.get_game_trump([game.playing_order[2], game.playing_order[1]])
    game.trump = player1.possible_trump
    bidding_winner = player1
    # zeigt die erhaltenen Reizwerte an
    l32 = Label(fenster, text = f"{player1.value_possible_trump}")
    l32.place(x = 200, y = 650, width = 50, height = 40)
    l33 = Label(fenster, text = f"{player2.value_possible_trump}")
    l33.place(x = 100, y = 160, width = 50, height = 40)
    l34 = Label(fenster, text = f"{player3.value_possible_trump}")
    l34.place(x = 800, y = 160, width = 50, height = 40)
    # zeigt den Reizgewinner an
    if game.trump != None:
        game.set_teams(bidding_winner)
        [bidding_winner.increase_points(card) for card in deck]
        l31.config(bg = "black", text = f"{bidding_winner.name} plays {game.trump}")
        b1 = Button(fenster, text = "Play", bg = "grey", command = lambda: fenster.destroy())
        b1.place(x = 700, y = 550, width = 80, height = 50)
    else:
        l31.config(bg = "black", text = "Nobody wants to play the game")
        b1 = Button(fenster, text = "End the game", bg = "grey", command = lambda: fenster.destroy())
        b1.place(x = 700, y = 550, width = 100, height = 50)
        
def confirm_choice(suit):
    '''
    Benutzer bestätigt die Eingabe
    '''
    confirm = Button(fenster, text = "Confirm", command = lambda: set_player_trump(suit))
    confirm.place(x = 700, y = 550, width = 100, height = 50)
    
def set_player_trump(suit):
    # gibt die Trumpffarbe von Spieler 1 an
    if suit == "":
        player1.possible_trump = None
    else:
        player1.possible_trump = suit
    show_trump()


def start_bidding(deck1):
    '''
    Hauptfunktion für das Reizen
    '''
    
    #print("im bidding", deck)
    global fenster
    fenster = Tk()
    fenster.geometry("1400x900")
    fenster.title("Skat Game!")
    fenster.configure(background = "green")
    #print(deck1)
    
    global l1, l2, l3, l4, l5, l6, l7, l8, l9, l10 
    global l11, l12, l13, l14, l15, l16, l17, l18, l19, l20
    global l21, l22, l23, l24, l25, l26, l27, l28, l29, l30
    global l31, l40, l41, l42
    global deck
    deck = deck1
    l31 = Label(fenster, text = "", font = ("Helvetica", 40), bg = "green")
    l31.place(x = 400, y = 400, width = 600, height = 60)
    hand_the_deck()
    player1.cards = player1.initial_cards
    player2.cards = player2.initial_cards
    player3.cards = player3.initial_cards
    print(deck)
    player1.take_skat(deck)
    
    
    # Initialisieren der Labels
    l40 = Label(fenster, text = "Human Player")
    l40.place(x = 350, y = 630, width = 100, height = 50)
     
    l1 = Label(fenster, text = "", bg = "green")
    l2 = Label(fenster, text = "", bg = "green")
    l3 = Label(fenster, text = "", bg = "green")
    l4 = Label(fenster, text = "", bg = "green")
    l5 = Label(fenster, text = "", bg = "green")
    l6 = Label(fenster, text = "", bg = "green")
    l7 = Label(fenster, text = "", bg = "green")
    l8 = Label(fenster, text = "", bg = "green")
    l9 = Label(fenster, text = "", bg = "green")
    l10 = Label(fenster, text = "", bg = "green")

    l1.place(x = 50, y = 700, width = 80, height = 150)
    l2.place(x = 130, y = 700, width = 80, height = 150)
    l3.place(x = 210, y = 700, width = 80, height = 150)
    l4.place(x = 290, y = 700, width = 80, height = 150)
    l5.place(x = 370, y = 700, width = 80, height = 150)
    l6.place(x = 450, y = 700, width = 80, height = 150)
    l7.place(x = 530, y = 700, width = 80, height = 150)
    l8.place(x = 610, y = 700, width = 80, height = 150)
    l9.place(x = 690, y = 700, width = 80, height = 150)
    l10.place(x = 770, y = 700, width = 80, height = 150)
    

    # Labels Player 2
    l41 = Label(fenster, text = "KI Player")
    l41.place(x = 350, y = 160, width = 100, height = 50)
    l11 = Label(fenster, text = "", bg = "green")
    l12 = Label(fenster, text = "", bg = "green")
    l13 = Label(fenster, text = "", bg = "green")
    l14 = Label(fenster, text = "", bg = "green")
    l15 = Label(fenster, text = "", bg = "green")
    l16 = Label(fenster, text = "", bg = "green")
    l17 = Label(fenster, text = "", bg = "green")
    l18 = Label(fenster, text = "", bg = "green")
    l19 = Label(fenster, text = "", bg = "green")
    l20 = Label(fenster, text = "", bg = "green")

    l11.place(x = 50, y = 50, width = 60, height = 100)
    l12.place(x = 110, y = 50, width = 60, height = 100)
    l13.place(x = 170, y = 50, width = 60, height = 100)
    l14.place(x = 230, y = 50, width = 60, height = 100)
    l15.place(x = 290, y = 50, width = 60, height = 100)
    l16.place(x = 350, y = 50, width = 60, height = 100)
    l17.place(x = 410, y = 50, width = 60, height = 100)
    l18.place(x = 470, y = 50, width = 60, height = 100)
    l19.place(x = 530, y = 50, width = 60, height = 100)
    l20.place(x = 590, y = 50, width = 60, height = 100)

    # Labels Player 3
    l42 = Label(fenster, text = "Naive Player")
    l42.place(x = 900, y = 160, width = 100, height = 50)
    l21 = Label(fenster, text = "", bg = "green")
    l22 = Label(fenster, text = "", bg = "green")
    l23 = Label(fenster, text = "", bg = "green")
    l24 = Label(fenster, text = "", bg = "green")
    l25 = Label(fenster, text = "", bg = "green")
    l26 = Label(fenster, text = "", bg = "green")
    l27 = Label(fenster, text = "", bg = "green")
    l28 = Label(fenster, text = "", bg = "green")
    l29 = Label(fenster, text = "", bg = "green")
    l30 = Label(fenster, text = "", bg = "green")

    l21.place(x = 700, y = 50, width = 60, height = 100)
    l22.place(x = 760, y = 50, width = 60, height = 100)
    l23.place(x = 820, y = 50, width = 60, height = 100)
    l24.place(x = 880, y = 50, width = 60, height = 100)
    l25.place(x = 940, y = 50, width = 60, height = 100)
    l26.place(x = 1000, y = 50, width = 60, height = 100)
    l27.place(x = 1060, y = 50, width = 60, height = 100)
    l28.place(x = 1120, y = 50, width = 60, height = 100)
    l29.place(x = 1180, y = 50, width = 60, height = 100)
    l30.place(x = 1240, y = 50, width = 60, height = 100)
    
    # Auswahl für Spieler 1
    diamonds = Button(fenster, text = "Diamonds", command = lambda: confirm_choice("diamonds"))
    hearts = Button(fenster, text = "Hearts", command = lambda: confirm_choice("hearts"))
    spades = Button(fenster, text = "Spades", command = lambda: confirm_choice("spades"))
    clubs = Button(fenster, text = "Clubs", command = lambda: confirm_choice("clubs"))
    none = Button(fenster, text = "None", command = lambda: confirm_choice(""))
    
    
    diamonds.place(x = 150, y = 550, width = 100, height = 50)
    hearts.place(x = 250, y = 550, width = 100, height = 50)
    spades.place(x = 350, y = 550, width = 100, height = 50)
    clubs.place(x = 450, y = 550, width = 100, height = 50)
    none.place(x = 550, y = 550, width = 100, height = 50)
    
    player1.possible_trump = 3 - game.games
    confirm_choice(player1.convert_card_suit_int_to_str(player1.possible_trump))
    set_player_trump(player1.convert_card_suit_int_to_str(player1.possible_trump))
    
    show_images()
    
    fenster.mainloop()
    
# start_bidding()

    
    