import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt 
from sklearn.linear_model import LinearRegression
import datetime
import operator
import os
from skaters import men, ladies, pairs, dance

# important dates
start_of_season_2016_2017 = datetime.datetime(2016,7,1,0,0,0).toordinal()
end_of_season_2016_2017 = datetime.datetime(2017,6,30,0,0,0).toordinal()
start_of_season_2017_2018 = datetime.datetime(2017,7,1,0,0,0).toordinal()
end_of_season_2017_2018 = datetime.datetime(2018,6,30,0,0,0).toordinal()
winter_olympics_2018=datetime.datetime(2018,2,9,0,0,0).toordinal()

# Convert skater names to url string
def skater_name_to_string(skater):
    skaternames = skater.get("name").lower().split()
    skater_string = skaternames[0]
    i = 1
    while i < len(skaternames):
        skater_string += "_"
        skater_string += skaternames[i]
        i += 1
    return skater_string

# Get a prediction for a skater score in a given segment for the END date
def skater_score_regression(category_name, skater, score, segment, start, end):
    data = pd.read_csv("skater_data/" + category_name + "_tss_scores.csv")
    data = data.loc[data["skater_name"] == skater.get("name")]
    data = data.loc[data["segment"] == segment]
    data["date_ordinal"] = pd.to_datetime(data["date"]).apply(lambda x: x.toordinal())

    X = data["date_ordinal"].values[:,np.newaxis]
    y = data[score].values
    model = LinearRegression()
    model.fit(X, y)
    prediction = model.predict(end)

    return prediction

# Plot regression for a skater score in a given segment
def skater_plot_score_regression(category_name, skater, score, segment, start, end):
    data = pd.read_csv("skater_data/" + category_name + "_tss_scores.csv")
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

    # Prepare skater plot for comparison
def skater_plot_for_comparison(category_name, skater, score, segment, start, end, colour):
    data = pd.read_csv("skater_data/" + category_name + "_tss_scores.csv")
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

    # Comparison plot for all skaters in category
def compare_skaters_plot(category, score, segment, start, end):
    colours = ("#ECDB54", "#E94B3C", "#944743", "#6F9FD8", "#EC9787", "#00A591", "#6B5B95", "#BC70A4", "#2E4A62", "#92B558")
    predictions = []
    i = 0
    for skater in category: 
        prediction = skater_plot_for_comparison(category_name, skater, score, segment, start, end, colours[i])
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

def generate_regressions_for_all_skaters(category, category_name):
    for skater in category:
        skater_plot_score_regression(category_name, skater, "tss", "short", start_of_season_2016_2017, winter_olympics_2018)
        skater_plot_score_regression(category_name, skater, "tss", "long", start_of_season_2016_2017, winter_olympics_2018)
        skater_plot_score_regression(category_name, skater, "pcs", "short", start_of_season_2016_2017, winter_olympics_2018)
        skater_plot_score_regression(category_name, skater, "pcs", "long", start_of_season_2016_2017, winter_olympics_2018)
        skater_plot_score_regression(category_name, skater, "tes", "short", start_of_season_2016_2017, winter_olympics_2018)
        skater_plot_score_regression(category_name, skater, "tes", "long", start_of_season_2016_2017, winter_olympics_2018)
        skater_plot_score_regression(category_name, skater, "bv", "short", start_of_season_2016_2017, winter_olympics_2018)
        skater_plot_score_regression(category_name, skater, "bv", "long", start_of_season_2016_2017, winter_olympics_2018)

# Outputs predicted ranking in txt file
def generate_skater_ranking(category, category_name, start, end):
    skater_index = 0
    scores_list = {}
    for skater in category:
        short_tes = float(skater_score_regression(category_name, skater, "tes", "short", start, end))
        short_pcs = float(skater_score_regression(category_name, skater, "pcs", "short", start, end))
        long_tes = float(skater_score_regression(category_name, skater, "tes", "long", start, end))
        long_pcs = float(skater_score_regression(category_name, skater, "pcs", "long", start, end))
        final_estimation = short_tes + short_pcs + long_tes + long_pcs
        print(final_estimation)
        scores_list.update({skater_index : final_estimation})
        skater_index += 1
    print(scores_list)
    
    create_project_dir("skater_data/rankings")
    file_name = category_name + "_ranking.txt"
    path = "skater_data/rankings/" + file_name
    delete_file_contents(path)
    f = open(path, 'w')
    i = 1
    for key, value in sorted(scores_list.items(), key=operator.itemgetter(1), reverse=True):
        skater_name = category[key].get("name")
        skater_country = category[key].get("country")
        score = "{0:.2f}".format(value)
        f.write(str(i) + ". " + skater_name + " " + skater_country + " " + str(score) + "\n")
        i += 1
    f.close()
    

# Delete file contents
def delete_file_contents(path):
    with open(path, 'w'):
        pass

# Create folder for files
def create_project_dir(directory):
    if not os.path.exists(directory):
        print('Creating folder ' + directory)
        os.makedirs(directory)


####################### Execute functions ##########################################

# generate_skater_ranking(men, "men", start_of_season_2016_2017, winter_olympics_2018)
# generate_skater_ranking(ladies, "ladies", start_of_season_2016_2017, winter_olympics_2018)
# generate_skater_ranking(pairs, "pairs", start_of_season_2016_2017, winter_olympics_2018)
# generate_skater_ranking(dance, "dance", start_of_season_2016_2017, winter_olympics_2018)
