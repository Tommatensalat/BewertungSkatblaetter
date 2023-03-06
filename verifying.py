import numpy as np
from model import model1
from scipy import stats
import seaborn as sns; sns.set()
from sklearn import svm
from players import player1
from cards import Card

daten = {1 : {100 : 350, 200 : 250, 
              300 : 1850, 400 : 250, 
              500 : 150, 600 : 250,
              700 : 350, 800 : 50,
              900 : 150, 1000 : 50, 
              2000 : 50, 3000 : 5150,
              4000 : 50, 5000 : 1350,
              6000 : 1150, 7000 : 1050},
        2 : {100 : 550, 200 : 50, 
              300 : 1350, 400 : 4750,
              500 : 750, 600 : 650,
              700 : 1450, 800 : 1350,
              900 : 850, 1000 : 950, 2000 : 850,
                     3000 : 550, 4000 : 2550,
                     5000 : 150, 6000 : 850,
                     7000 : 150},
         3 : {100 : 50, 200 : 1850, 
              300 : 250, 400 : 1350, 
              500 : 250, 600 : 2650,
              700 : 2750, 800 : 850, 900 : 1550,
              1000 : 450, 2000 : 1550,
              3000 : 1250, 4000 : 350,
              5000 : 250, 6000 : 250,
              7000 : 350},
         6 : {100 : 50, 200 : 150,
              300 : 1250, 400 : 850,
              500 : 5550, 600 : 2550,
              700 : 2050, 800 : 2850, 900 : 750,
              1000 : 950, 2000 : 1050,
              3000 : 1550, 4000 : 550,
              5000 : 850, 6000 : 650,
              7000 : 1900}}

def model(kernel_degree, amount_datas):
    '''
    gibt die Werte für die einzelnen Merkmalsräume und optimale
    C-Parameter an, Funktionen sind entsprechend den Methoden
    in model.py, zusammengefasst in einer Methode
    '''
    dataset = model1.datas
    X = dataset[:amount_datas, :8]
    y = dataset[:amount_datas, 8:].ravel()
    if kernel_degree != 1:
        poly_svc = svm.SVC(kernel = "poly", C = daten[kernel_degree][amount_datas], degree = kernel_degree).fit(X, y)
    else:
        poly_svc = svm.SVC(C = daten[1][amount_datas]).fit(X, y)
    test_dataset = model1.test_datas
    test_x = test_dataset[:, :, :8]
    test_final_y = test_dataset[:, :, 8]
    proof_y = np.empty(shape = (len(model1.test_datas), 4))
    for k in range(len(test_x)):
        tmp_y = poly_svc.predict(test_x[k])
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
            countTruePlayable += 1
        if compared_y[k][0] == True:
            countTrue += 1
        if compared_y[k][0] == False and test_final_y[k][0] != -1:
            countFalsePlayable += 1
        if compared_y[k][0] == False:
            countFalse += 1
    print(countTrue, countTruePlayable, countFalse, countFalsePlayable)

model1.run_datas()
model(2, 1000)
print()
#player1.calculate_power_of_algorithm()
#player1.cards = [Card(2, 2), Card(2, 0), Card(11, 3), Card(10, 3), Card(4, 3), Card(9, 3), Card(11, 2),
#                 Card(10, 2), Card(4, 2), Card(10, 1)]
#print(model1.run_game(player1.cards))



