import numpy as np

class SimpleLinearRegression:
    def __init__(self):
        self.slope = None
        self.intercept = None

    def fit(self, X, y):
        X_mean = np.mean(X)
        y_mean = np.mean(y)
        self.slope = np.sum((X - X_mean) * (y - y_mean)) / np.sum((X - X_mean) ** 2)
        self.intercept = y_mean - (self.slope * X_mean)
        return self

    def predict(self, X):
        return self.slope * X + self.intercept

    def score(self, X, y):
        y_pred = self.predict(X)
        ss_total = np.sum((y - np.mean(y)) ** 2)
        ss_residual = np.sum((y - y_pred) ** 2)
        return 1 - (ss_residual / ss_total)
