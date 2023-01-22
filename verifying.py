import numpy as np
from model import model1
from scipy import stats
import seaborn as sns; sns.set()
from sklearn import svm
from players import player1

daten = {2 : {1000 : 950, 2000 : 850,
                     3000 : 550, 4000 : 2550,
                     5000 : 150, 6000 : 850,
                     7000 : 150, 8000 : 650,
                     9000 : 450, 10000 : 250},
         3 : {1000 : 450, 2000 : 1550,
              3000 : 1250, 4000 : 350,
              5000 : 250, 6000 : 250,
              7000 : 350, 8000 : 350,
              9000 : 650, 10000 : 250},
         6 : {1000 : 950, 2000 : 1050,
              3000 : 1550, 4000 : 550,
              5000 : 850, 6000 : 650,
              7000 : 1900, 8000 : 3000,
              9000 : 3900, 10000 : 3350}}

def model(kernel_degree, amount_datas):
    dataset = model1.datas
    X = dataset[:amount_datas, :8]
    y = dataset[:amount_datas, 8:].ravel()
    poly_svc = svm.SVC(kernel = "poly", C = daten[kernel_degree][amount_datas], degree = kernel_degree).fit(X, y)
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
player1.calculate_power_of_algorithm()



