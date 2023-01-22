from players import player1, player2, player3
from game import game
from model import model1
import numpy as np
from numpy import genfromtxt
from cards import Card

csvTestData = []
data = []
deck_of_cards = []
results_ki = []
results_naive_algorithm = []

def read_datas():
    global data
    csvTestData = genfromtxt("test_data.csv", delimiter = ",")
    data = [np.array(list(map(int, csvTestData[i]))) for i in range(21)]
    data = data[1:]

def convert_numbers_to_cards():
    for i in range(len(data)):
        deck_of_cards.append(list())
        for j in range(0, len(data[i])-2, 2):
            newCard = Card(data[i][j+1], data[i][j])
            deck_of_cards[i].append(newCard)
        deck_of_cards[i].append(data[i][-2])
        deck_of_cards[i].append(data[i][-1])

def get_results_of_ki():
    for i in range(len(deck_of_cards)):
        trump = model1.run_game(deck_of_cards[i][:len(deck_of_cards[i])-2])
        model1.initial_datas = []
        model1.datas = None
        model1.headline = []
        model1.trump = None
        model1.deck = []
        results_ki.append(trump)
        
def get_results_of_naive_algorithm():
    for i in range(len(deck_of_cards)):
        player1.cards = deck_of_cards[i][:len(deck_of_cards[i])-2]
        player1.find_possible_trump()
        results_naive_algorithm.append(player1.possible_trump)
         
def convert_card_suit_int_to_str(number):
    suits = {-1 : "None",
             0 : "diamonds",
             1 : "hearts",
             2 : "spades",
             3 : "clubs"}
    return suits[number]

def create_txt_file():
    datei = open("comparison.txt", "w")
    datei.write("Karten \n")
    for i in range(len(data)):
        deck_of_cards[i][-2] = convert_card_suit_int_to_str(deck_of_cards[i][-2])
        datei.write(f"{deck_of_cards[i][:len(deck_of_cards[i])-2]} \n")
    datei.write("\nResults KI \t Results Naive Algorithm \t Correct Results \n")
    for i in range(len(data)):
        results_ki[i] = convert_card_suit_int_to_str(results_ki[i])
        datei.write(f"{results_ki[i]} \t\t\t\t\t {results_naive_algorithm[i]}\t\t\t\t\t {deck_of_cards[i][-2]} \n")

def calculate():
    global deck_of_cards
    read_datas(), convert_numbers_to_cards()
    get_results_of_ki(), get_results_of_naive_algorithm()
    deck_of_cards = []
    convert_numbers_to_cards()
    create_txt_file()
calculate()
    
    