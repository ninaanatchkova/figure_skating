import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt 
from sklearn.linear_model import LinearRegression
import datetime
from skaters import skaters

# important dates
start_of_season_2016_2017 = datetime.datetime(2016,7,1,0,0,0).toordinal()
end_of_season_2016_2017 = datetime.datetime(2017,6,30,0,0,0).toordinal()
start_of_season_2017_2018 = datetime.datetime(2017,7,1,0,0,0).toordinal()
end_of_season_2017_2018 = datetime.datetime(2018,6,30,0,0,0).toordinal()
winter_olympics_2018=datetime.datetime(2018,2,9,0,0,0).toordinal()

def skater_regression(skater, score, segment, start, end):
    data = pd.read_csv("skater_data/tss_scores.csv")
    data = data.loc[data["skater_name"] == skater.get("name")]
    data = data.loc[data["segment"] == segment]
    data["date_ordinal"] = pd.to_datetime(data["date"]).apply(lambda x: x.toordinal())

    X = data["date_ordinal"].values[:,np.newaxis]
    y = data[score].values
    dates = data["date"]
    
    model = LinearRegression()
    model.fit(X, y)
    print(model.predict(end))
    plt.scatter(X, y, color='r')
    plt.plot(X, model.predict(X), color='k')
    plt.xticks(X, dates, rotation='vertical')
    plt.xlabel("Date")
    plt.ylabel(score.upper())
    plt.xlim(xmin=start, xmax=end)
    plt.show()

skater_regression(skaters[0], "tss", "long", start_of_season_2016_2017, winter_olympics_2018)

