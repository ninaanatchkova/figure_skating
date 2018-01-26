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

def skater_name_to_string(skater):
    skaternames = skater.get("name").lower().split()
    skater_string = skaternames[0] + "_" + skaternames[1]
    return skater_string

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
    prediction = model.predict(end)
    prediction_string = "{0:.2f}".format(prediction[0])
    fig = plt.figure()
    plt.scatter(X, y, color='r')
    plt.plot(X, model.predict(X), color='k')
    plt.xticks(X, dates, rotation='vertical')
    plt.xlabel("Date")
    plt.ylabel(score.upper())
    plt.xlim(xmin=start, xmax=end)

    fig.savefig("skater_data/plots/" + skater_name_to_string(skater) + "_" + segment + "_" + score + "_" + prediction_string + ".png")
    
    #plt.show()

def compare_skater_plot(skater, score, segment, start, end, colour):
    data = pd.read_csv("skater_data/tss_scores.csv")
    data = data.loc[data["skater_name"] == skater.get("name")]
    data = data.loc[data["segment"] == segment]
    data["date_ordinal"] = pd.to_datetime(data["date"]).apply(lambda x: x.toordinal())

    X = data["date_ordinal"].values[:,np.newaxis]
    y = data[score].values
    dates = data["date"]
    
    model = LinearRegression()
    model.fit(X, y)
    prediction = model.predict(end)
    prediction_string = "{0:.2f}".format(prediction[0])
    prediction_statement = skater.get("name") + " predicted " + segment + " " + score + " for Pyongchang is " + prediction_string
    return [X, y, prediction_statement, prediction_string]

def compare_skaters(score, segment, start, end):
    colours = ("#ECDB54", "#E94B3C", "#944743", "#6F9FD8", "#EC9787", "#00A591", "#6B5B95", "#BC70A4", "#2E4A62", "#92B558")
    predictions = []
    i = 0
    for skater in skaters: 
        prediction = compare_skater_plot(skater, score, segment, start, end, colours[i])
        model = LinearRegression()
        model.fit(prediction[0], prediction[1])
        plt.scatter(prediction[0], prediction[1], color=colours[i])
        plt.plot(prediction[0], model.predict(prediction[0]), color=colours[i], label = prediction[3] + " " + skater.get("name"))
        predictions.append(prediction[2])
        i += 1
    plt.xlabel("Time")
    plt.ylabel(score.upper())
    plt.xlim(xmin=start, xmax=end)
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.show()
    f = open("skater_data/plots/" + segment + "_" + score + "_predictions.txt", 'w')
    for prediction in predictions:
        f.write(prediction + "\n")
    f.close()

def generate_regressions_for_all_skaters():
    for skater in skaters:
        skater_regression(skater, "tss", "short", start_of_season_2016_2017, winter_olympics_2018)
        skater_regression(skater, "tss", "long", start_of_season_2016_2017, winter_olympics_2018)
        skater_regression(skater, "pcs", "short", start_of_season_2016_2017, winter_olympics_2018)
        skater_regression(skater, "pcs", "long", start_of_season_2016_2017, winter_olympics_2018)
        skater_regression(skater, "tes", "short", start_of_season_2016_2017, winter_olympics_2018)
        skater_regression(skater, "tes", "long", start_of_season_2016_2017, winter_olympics_2018)
        skater_regression(skater, "bv", "short", start_of_season_2016_2017, winter_olympics_2018)
        skater_regression(skater, "bv", "long", start_of_season_2016_2017, winter_olympics_2018)

# compare_skaters("tss", "short", start_of_season_2016_2017, winter_olympics_2018)
