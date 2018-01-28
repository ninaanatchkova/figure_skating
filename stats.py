import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt 
from skaters import skaters


def read_skater_data(skater, segment, type_of_score):
    data = pd.read_csv("skater_data/tss_scores.csv")
    data = data.loc[data["skater_name"] == skater.get("name")]
    data = data.loc[data["segment"] == segment]
    return data[type_of_score].tolist()

def all_skaters_data(segment, type_of_score):
    all_data = []
    for skater in skaters:
        data = read_skater_data(skater, segment, type_of_score)
        all_data.append(data)
    return all_data


def create_boxplots(segment, type_of_score):
    to_plot = all_skaters_data(segment, type_of_score)
    fig = plt.figure(1, figsize=(9, 6))
    ax = fig.add_subplot(111)
    bp = ax.boxplot(to_plot)
    skater_names = []
    for skater in skaters:
        name = skater.get("name")
        skater_names.append(name)
    plt.xticks([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], skater_names, rotation='vertical')
    plt.show()
    # Save the figure
    # fig.savefig('fig1.png', bbox_inches='tight')

create_boxplots("short", "tss")
create_boxplots("long", "tss")
