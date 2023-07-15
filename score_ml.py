import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split


class Generate_Score :
    def __init__(self, c_debt=0, c_credit=0, c_score=0):
        self.c_debt = c_debt
        self.c_credit = c_credit
        self.c_score = c_score

    def loadDataset(self):
        self.dataset = pd.read_csv('data.csv')
        self.X = self.dataset.iloc[:, 1:-1].values
        self.y = self.dataset.iloc[:, -1].values
    
    def train(self):
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, self.y, test_size = 0.2, random_state = 0)
        self.regressor = RandomForestRegressor(n_estimators = 10, random_state = 0)
        self.regressor.fit(self.X_train, self.y_train)
        # self.regressor.predict([[6.5]])

    def test(self):
        pass
    
    def predictScore(self):
        self.regressor.fit()