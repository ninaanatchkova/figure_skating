import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt 
from sklearn.linear_model import LinearRegression
import datetime

data = pd.read_csv("skater_data/tes_scores.csv")
epoch_0=datetime.datetime(2016,7,1,0,0,0)

data["date"] = (pd.to_datetime(data["date"])-epoch_0) / np.timedelta64(1, 's')
data.head()

X = data["date"].values[:,np.newaxis]
y = data["bv"].values

model = LinearRegression()
model.fit(X, y)

plt.scatter(X, y,color='r')
plt.plot(X, model.predict(X), color='k')

plt.show()