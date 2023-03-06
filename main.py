from cards import deck, Deck
from players import player1, player2, player3
from game import game
from tkinter import *
import time
#from model import Model
import numpy as np
from numpy import genfromtxt

def show_images():
    '''
    passt die Kartengröße auf die Labels an
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
    # sortiert die Blätter der Spieler nach dem Trumpf
    player1.sort_deck(game.trump)
    player2.sort_deck(game.trump)
    player3.sort_deck(game.trump)
    
def check_number_of_cards(player, card):
    '''
    überprüft ob ein Stich vollendet ist
    '''
    global state_comparing_cards, b36
    comb = (player, card)
    state_comparing_cards[int(is_playing.name[-1]) - 1] = comb
    # wurden 3 Karten angespielt
    if game.get_number_of_cards(state_comparing_cards):
        # berechne Stichgewinner
        winner = game.get_temp_winner(state_comparing_cards[first_card_index],
                        state_comparing_cards[first_card_index - 2],
                        state_comparing_cards[first_card_index - 1])
        # Zeige Button an, um Stich zu beenden
        b36 = Button(window, text = "Increase Points", bg = "grey", 
                        command = lambda: b_click_collect(winner, state_comparing_cards))
        b36.place(x = 900, y = 450, width = 200, height = 50)

def b_click_collect(winner, list_player_and_cards):
    '''
    sammelt die drei Stichkarten ein und überschreibt die Werte der Variablen
    '''
    global l33, l34, l35, l36, l37, l38, l39, b36
    global is_playing, state_comparing_cards
    global list_players, first_card_index
    # Punkte dem Stichgewinner zuschreiben
    for comb in list_player_and_cards:
        winner.increase_points(comb[1])
    # Kartenanzahl erhöhen
    game.increase_count_played_cards(3)
    # Labels zurücksetzen
    clear_image(l33), time.sleep(0.2)
    clear_image(l34), time.sleep(0.2)
    clear_image(l35), time.sleep(0.2)      
    b36.place_forget()
    change_label_player_text(is_playing)
    # Stich zurücksetzen
    state_comparing_cards = [None, None, None]
    game.set_total_points(player1.points, player2.points, player3.points)
    # wenn Spiel vorbei ist
    if game.is_over():
        # Labels verschwinden lassen
        l33.place_forget(), l34.place_forget(), l35.place_forget()
        l37.place_forget(), l38.place_forget(), l39.place_forget()
        l36.place_forget()
        list_players = [player1, player2, player3]
        # Gewinner des Spiels ermitteln
        game_winner = game.get_winning_player(list_players)
        # Gewinner anzeigen
        show_winner(game_winner)
    # sonst Vorhand, Mittelhand und Hinterhand überschreiben
    else:
        is_playing = winner
        game.set_playing_hands(winner)
        first_card_index = winner.player_index
        #if first_card_index != 0:
        # Berechnung der neuen Karte für den neuen Stich
        automated_card_choice(winner, dict_labels_player[first_card_index], dict_buttons_player[first_card_index])

def clear_image(l):
    # lässt das Bild in einem Image verschwinden
    l.config(image = None)
    l.image = None

def show_winner(winner):
    '''
    Anzeige für den Gewinner eines Spiels
    '''
    l40 = Label(window, text = "", font = ("Helvetica", 30), bg = "green")
    l40.place(x = 500, y = 300, width = 700, height = 80)
    # wenn die Teamspieler gewonnen haben
    if type(winner) == list:
        l40.config(text = f"{winner[0].name} and {winner[1].name} win the game")
    # wenn der Alleinspieler gewonnen hat
    else:
        l40.config(text = f"{winner.name} wins the game")
    time.sleep(1)
    window.destroy()
    # neues Spiel mit nächster Trumpffarbe beginnen
    print(player1.points, player2.points, player3.points)
    start()
     
def change_label_player_text(player):
    # verändert den Text im Label des aktuell spielenden Spielers in einem Stich
    global l36
    l36.config(text = f"{player.name} plays")
  
def amount_analysis(var, list):
    # berechnet wie oft ein Element in einer Liste vorkommt
    amount_of_var = 0
    for i in list:
        if i == var:
            amount_of_var += 1
    return amount_of_var

# initializes the important parameters for running the algorithm and 
# returns the value to the b_click function
def automated_card_choice(player, player_labels_liste, player_buttons_liste):
    '''
    initialisiert die Variablen, die für die Berechnung der zu spielenden Karten
    benötigt werden
    '''
    all_players = [player1, player2, player3]
    all_cards = []
    # aktueller Stich ohne Spielerobjekte dargestellt
    temp_played_cards = [None, None, None]
    for i in range(len(state_comparing_cards)):
        if state_comparing_cards[i] != None:
            temp_played_cards[i] = state_comparing_cards[i][1]  
    # alle Karten festhalten
    for players in all_players:
        for card in players.cards:
            all_cards.append(card)
    team_order = [player1.team, player2.team, player3.team]
    # Aufrufen der Methode in der Spieler-Klasse zur Berechnung der gespielten Karte
    playing_card = player.MCTS(all_cards, temp_played_cards, game.trump, team_order, first_card_index, player.cards)
    # konvertiere den Typ des Trumpfes in einen Integer
    if type(game.trump) == int:
        game.trump = player.convert_card_suit_int_to_str(game.trump)
    # Karte anzeigen lassen
    if playing_card:
        b_click(playing_card, dict_labels_player[player.player_index][player.cards.index(playing_card)], player, dict_buttons_player[player.player_index][player.cards.index(playing_card)])

def b_click(card, l, player,  b):
    '''
    gespielte Karte wird angezeigt und Variablen für den nächsten Spieler überschrieben
    '''
    global l33, l34, l35
    global is_playing, state_comparing_cards#, b36
    global first_card_index
    global liste_Labels_player1, liste_Labels_player2, liste_Labels_player3
    global list_buttons_player1, list_buttons_player2, list_buttons_player3
    players_list = [player1, player2, player3]
    labels_list = [l33, l34, l35]
    # wenn der Spieler noch nicht alle Karten gespielt hat
    if amount_analysis(None, player.cards) < 10:
        # wenn der Spieler in Vorhand ist oder die angespielte Karte im Bezug zur 
        # Karte der Vorhand und dem eigenen Blatt übereinstimmt
        if (amount_analysis(None, state_comparing_cards) == 3 or player.check_card_suit(card, state_comparing_cards[first_card_index][1], game.trump)) and amount_analysis(None, state_comparing_cards) != 0:
            
            if card in player.cards:
                # Bildgröße neu anpassen
                player_handed_card = player.resize_card(f"assets/{card}.png", True)
                labels_list[player.player_index].config(image = player_handed_card)
                labels_list[player.player_index].image = player_handed_card
                # Kartenbild aus dem Spielerdeck entfernen
                b.place_forget(), l.place_forget()
                # Kartenobjekt aus dem Blatt entfernen
                player.remove_card(card)
                check_number_of_cards(player, card)
                if amount_analysis(None, state_comparing_cards) != 0:
                    # Vaktueller Spieler wird geändert
                    is_playing = players_list[players_list.index(player) - 2]
                    change_label_player_text(is_playing)
                
                    # ggf. Index der Vorhand anpassen
                    if amount_analysis(None, state_comparing_cards) == 2:
                        first_card_index = player.player_index
                    time.sleep(1)
                
                    #if is_playing.player_index != 0:
                    automated_card_choice(is_playing, dict_labels_player[is_playing.player_index], dict_buttons_player[is_playing.player_index])
 
deck1 = Deck()        
# shows the starting state of the game
def start():
    global deck1
    import bidding
    #print(game.games)
    if game.games == 0:
        deck = Deck()
        deck.create_deck()
        deck.shuffle()
        deck1 = deck.copy()
    else:
        deck = deck1
    # zuerst Reizen
    bidding.start_bidding(deck)
    game.increase_number_of_games()
    
    global window
    window = Tk()
    window.geometry("1400x900")
    window.title ("Skat Game!")
    window.configure(background = "green")

    global l1, l2, l3, l4, l5, l6, l7, l8, l9, l10 
    global l11, l12, l13, l14, l15, l16, l17, l18, l19, l20
    global l21, l22, l23, l24, l25, l26, l27, l28, l29, l30
    global l33, l34, l35, l36, l37, l38, l39, l40, l41, l42
    global list_buttons_player1, list_buttons_player2, list_buttons_player3
    global dict_labels_player, dict_buttons_player
    global first_card_index
    if not game.trump:
        window.destroy()
    hand_the_deck()
    global is_playing, state_comparing_cards
    # Stichkarten
    state_comparing_cards = [None, None, None]
    # aktuell spielender Spieler
    is_playing = game.playing_order[0]
    if type(game.trump) == str:
        game.set_trump(game.trump)

    # Vorhand Index festlegen und Punkte zurücksetzen
    first_card_index = int(is_playing.name[-1]) - 1
    player1.reset_points()
    player2.reset_points()
    player3.reset_points()
    game.reset_count_played_cards()
    player1.increase_points(deck[0])
    player1.increase_points(deck[1])
    
    #create Labels
    #l40 = Label(window, text = "Human Player")
    #l40.place(x = 50, y = 600, width = 100, height = 50)
    # Labels Player 1
    
    # Labels einstellen
    l1 = Label(window, text = "", bg = "green")
    l2 = Label(window, text = "", bg = "green")
    l3 = Label(window, text = "", bg = "green")
    l4 = Label(window, text = "", bg = "green")
    l5 = Label(window, text = "", bg = "green")
    l6 = Label(window, text = "", bg = "green")
    l7 = Label(window, text = "", bg = "green")
    l8 = Label(window, text = "", bg = "green")
    l9 = Label(window, text = "", bg = "green")
    l10 = Label(window, text = "", bg = "green")

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
    
    liste_Labels_player1 = [l1, l2, l3, l4, l5, l6, l7 ,l8, l9, l10]
    
    # Labels Player 2
    #l41 = Label(window, text = "KI Player")
    #l41.place(x = 50, y = 160, width = 100, height = 50)
    l11 = Label(window, text = "", bg = "green")
    l12 = Label(window, text = "", bg = "green")
    l13 = Label(window, text = "", bg = "green")
    l14 = Label(window, text = "", bg = "green")
    l15 = Label(window, text = "", bg = "green")
    l16 = Label(window, text = "", bg = "green")
    l17 = Label(window, text = "", bg = "green")
    l18 = Label(window, text = "", bg = "green")
    l19 = Label(window, text = "", bg = "green")
    l20 = Label(window, text = "", bg = "green")

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
    
    liste_Labels_player2 = [l11, l12, l13, l14, l15, l16, l17, l18, l19, l20]
    
    # Labels Player 3
    #l42 = Label(window, text = "Naive Player")
    #l42.place(x = 700, y = 160, width = 100, height = 50)
    l21 = Label(window, text = "", bg = "green")
    l22 = Label(window, text = "", bg = "green")
    l23 = Label(window, text = "", bg = "green")
    l24 = Label(window, text = "", bg = "green")
    l25 = Label(window, text = "", bg = "green")
    l26 = Label(window, text = "", bg = "green")
    l27 = Label(window, text = "", bg = "green")
    l28 = Label(window, text = "", bg = "green")
    l29 = Label(window, text = "", bg = "green")
    l30 = Label(window, text = "", bg = "green")

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
    
    liste_Labels_player3 = [l21, l22, l23, l24, l25, l26, l27, l28, l29, l30]

    # Labels Skat
    
    # Labels Comparing Cards
    l33 = Label(window, text = "", bg = "black")
    l34 = Label(window, text = "", bg = "black")
    l35 = Label(window, text = "", bg = "black")
    l33.place(x = 300, y = 310, width = 150, height = 210)
    l34.place(x = 500, y = 310, width = 150, height = 210)
    l35.place(x = 700, y = 310, width = 150, height = 210)
    
    l37 = Label(window, text = "Card Player 1", font = ("Helvetica", 20))
    l37.place(x = 300, y = 520, width = 150, height = 50)
    l38 = Label(window, text = "Card Player 2", font = ("Helvetica", 20))
    l38.place(x = 500, y = 520, width = 150, height = 50)
    l39 = Label(window, text = "Card Player 3", font = ("Helvetica", 20))
    l39.place(x = 700, y = 520, width = 150, height = 50)

    # Buttons to hand cards
    b1 = Button(window, text = "+", command = lambda: b_click(player1.cards[0], l1, player1, b1))
    b2 = Button(window, text = "+", command = lambda: b_click(player1.cards[1], l2, player1, b2))
    b3 = Button(window, text = "+", command = lambda: b_click(player1.cards[2], l3, player1, b3))
    b4 = Button(window, text = "+", command = lambda: b_click(player1.cards[3], l4, player1, b4))
    b5 = Button(window, text = "+", command = lambda: b_click(player1.cards[4], l5, player1, b5))
    b6 = Button(window, text = "+", command = lambda: b_click(player1.cards[5], l6, player1, b6))
    b7 = Button(window, text = "+", command = lambda: b_click(player1.cards[6], l7, player1, b7))
    b8 = Button(window, text = "+", command = lambda: b_click(player1.cards[7], l8, player1, b8))
    b9 = Button(window, text = "+", command = lambda: b_click(player1.cards[8], l9, player1, b9))
    b10 = Button(window, text = "+", command = lambda: b_click(player1.cards[9], l10, player1, b10))
    
    list_buttons_player1 = [b1, b2, b3, b4, b5, b6, b7, b8, b9, b10]
    
    b1.place(x = 50, y = 860, width = 80, height = 30)
    b2.place(x = 130, y = 860, width = 80, height = 30)
    b3.place(x = 210, y = 860, width = 80, height = 30)
    b4.place(x = 290, y = 860, width = 80, height = 30)
    b5.place(x = 370, y = 860, width = 80, height = 30)
    b6.place(x = 450, y = 860, width = 80, height = 30)
    b7.place(x = 530, y = 860, width = 80, height = 30)
    b8.place(x = 610, y = 860, width = 80, height = 30)
    b9.place(x = 690, y = 860, width = 80, height = 30)
    b10.place(x = 770, y = 860, width = 80, height = 30)

    b11 = Button(window, text = "+")
    b12 = Button(window, text = "+")
    b13 = Button(window, text = "+")
    b14 = Button(window, text = "+")
    b15 = Button(window, text = "+")
    b16 = Button(window, text = "+")
    b17 = Button(window, text = "+")
    b18 = Button(window, text = "+")
    b19 = Button(window, text = "+")
    b20 = Button(window, text = "+")
    
    list_buttons_player2 = [b11, b12, b13, b14, b15, b16, b17, b18, b19, b20]

    b21 = Button(window, text = "+")
    b22 = Button(window, text = "+")
    b23 = Button(window, text = "+")
    b24 = Button(window, text = "+")
    b25 = Button(window, text = "+")
    b26 = Button(window, text = "+")
    b27 = Button(window, text = "+")
    b28 = Button(window, text = "+")
    b29 = Button(window, text = "+")
    b30 = Button(window, text = "+")
    
    list_buttons_player3 = [b21, b22, b23, b24, b25, b26, b27, b28, b29, b30]
    
    l36 = Label(window, text = f"{is_playing.name} begins", bg = "green", font = ("Helvetica", 20))
    l36.place(x = 1000, y = 300, width = 200, height = 50)
    
    dict_labels_player = {0 : liste_Labels_player1,
                          1 : liste_Labels_player2,
                          2 : liste_Labels_player3}
    dict_buttons_player = {0 : list_buttons_player1,
                           1 : list_buttons_player2,
                           2 : list_buttons_player3}
    
    # create Labels
    show_images()
    
    first_card_index = is_playing.player_index
    #if first_card_index != 0:
    automated_card_choice(is_playing, dict_labels_player[is_playing.player_index], dict_buttons_player[is_playing.player_index])
    window.mainloop()
start()

def read_datas(filename):
    # Daten aus einer csv-Datei auslesen
    csvData = genfromtxt(filename, delimiter = ",")
    return csvData

def write_datas(test_datas):
    '''
    Daten in die Trainingsdaten csv-Datei schreiben
    '''
    # lesen und in eine Liste umwandeln
    tmp = read_datas("datas.csv")
    tmp = tmp.tolist()
    len_tmp = len(tmp)

    # in die entsprechende Form als Zahlenwerte bringen
    for i in range(len(test_datas)):
        tmp.append(list())
        for k in range(len(test_datas[i]) - 2):
            tmp[i+len_tmp].append(test_datas[i][k].suit)
            tmp[i+len_tmp].append(test_datas[i][k].value)
        tmp[i+len_tmp].append(test_datas[i][-2])
        tmp[i+len_tmp].append(test_datas[i][-1])   
    np.savetxt("datas.csv", tmp, delimiter = ",")

# creates a test data set or training data set
def create_data_set():
    '''
    lässt mehrmals durchspielen, um ein großen Datensatz in einer kleinen Zeitspanne zu generieren
    '''
    test_datas = []
    deck = Deck()
    for i in range(300):
        print(i)
        # Kartendeck erstellen
        deck.create_deck()
        deck.shuffle()
        deck1 = deck.copy()
        # für jede Trumpffarbe durchspielen
        for j in range(3,-1,-1):
            deck = Deck()
            deck = deck1.copy()
            player1.possible_trump = j
            results = []
            datas = deck[0:10]
            datas.append(None)
            datas.append(None)
            # jede Farbe wird 10x durchgespielt
            for k in range(10):
                start()
                results.append(player1.points)
                player1.reset_points()
                player2.reset_points()
                player3.reset_points()
                game.reset_count_played_cards()
                deck = deck1.copy()
            # extremale Werte aus der Betrachtung entfernen
            results.remove(max(results))
            results.remove(min(results))
            # durchschnitt aus den Ergebnissen bilden
            # entscheiden ob Blatt spielbar oder nicht
            average = sum(results)/8
            if average > 60:
                datas[-1] = 1
                datas[-2] = j
            else:
                datas[-1]  = 0
                datas[-2] = j
            test_datas.append(datas)
        deck = Deck()
    write_datas(test_datas)
    
        
    
#create_data_set()
