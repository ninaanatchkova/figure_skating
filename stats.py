import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt 
from skaters import ladies, men, pairs, dance


def read_skater_data(category_name, skater, segment, type_of_score):
    data = pd.read_csv("skater_data/" + category_name + "_tss_scores.csv")
    data = data.loc[data["skater_name"] == skater.get("name")]
    data = data.loc[data["segment"] == segment]
    return data[type_of_score].tolist()

def all_skaters_data(category, category_name, segment, type_of_score):
    all_data = []
    for skater in category:
        data = read_skater_data(category_name, skater, segment, type_of_score)
        all_data.append(data)
    return all_data


def create_boxplots(category, category_name, segment, type_of_score):
    to_plot = all_skaters_data(category, category_name, segment, type_of_score)
    fig = plt.figure(1, figsize=(9, 6))
    ax = fig.add_subplot(111)
    bp = ax.boxplot(to_plot)
    skater_names = []
    for skater in category:
        name = skater.get("name")
        skater_names.append(name)
    plt.xticks([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], skater_names, rotation='vertical')
    plt.title(category_name.upper() + " " + segment.upper() + " " + type_of_score.upper() + " score".upper())
    # plt.show()
    # Save the figure
    fig.savefig("skater_data/plots/box_plots_" + category_name + "_" + segment + "_" + type_of_score, bbox_inches='tight')


# unfinished
def get_skater_quads(skater):
    data = pd.read_csv("skater_data/men_tes_scores.csv")
    data = data.loc[data["skater_name"] == skater.get("name")]
    data = data[data["tech_element"].str.startswith("4", na=False)]
    print(data)
    i = 0
    data_size = 0 # find it
    competition = ""
    quad_stats = {}
    while i < data_size:
        jump_count = 0
        jump_total_worth = 0
        if competition != data.iloc[[i]]["event"]:
            if jump_count != 0:
                quad_stats.update({ jump_count : jump_total_worth})
            competition = data.iloc[[i]]["event"]
            jump_count = 1
            jump_total_worth = data.iloc[[i]]["bv"] + data.iloc[[i]]["goe"]
        else:
            jump_count += 1
            jump_total_worth += data.iloc[[i]]["bv"] 
            jump_total_worth += data.iloc[[i]]["goe"]
        i += 0
    return quad_stats

# plot averages


#################################### Execute functions #######################################

# create_boxplots(men, "men", "long", "tss")
