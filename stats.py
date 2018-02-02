import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import csv
import os
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
    fig.savefig("skater_data/plots/box_plots_" + category_name + "_" + segment + "_" + type_of_score, bbox_inches='tight')


# generate quad statistics csv
def get_skater_quads(skater):
    data = pd.read_csv("skater_data/men_tes_scores.csv")
    data = data.loc[data["skater_name"] == skater.get("name")]
    data = data[data["tech_element"].str.startswith("4", na=False)]
    i = 0
    data_size = data.shape[0]
    competition = ""
    competition_list = []
    while i < data_size:
        row = data.iloc[i]
        current_comp = str(row["event"])
        if competition != current_comp:
            if current_comp in competition_list:
                pass
            else:
                competition_list.append(current_comp)
            competition = current_comp
        else:
            pass
        i += 1
    for competition in competition_list:
        comp_data = data.loc[data["event"] == competition]
        jumps_count = comp_data.shape[0]
        jumps_total_value = comp_data["bv"].sum() + comp_data["goe"].sum()
        if not os.path.exists("skater_data/quad_stats.csv"):
            with open("skater_data/quad_stats.csv", "w", newline="", encoding= "utf-8") as csvfile:
                fieldnames = ["skater_name", "competition", "quads", "total_quad_value"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerow({
                        "skater_name" : skater.get("name"),
                        "competition": competition,
                        "quads": jumps_count,
                        "total_quad_value": jumps_total_value
                        })
            csvfile.close()
        else:
            with open("skater_data/quad_stats.csv", "a", newline="", encoding= "utf-8") as csvfile:
                fieldnames = ["skater_name", "competition", "quads", "total_quad_value"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writerow({
                        "skater_name" : skater.get("name"),
                        "competition": competition,
                        "quads": jumps_count,
                        "total_quad_value": jumps_total_value
                        })
            csvfile.close()

def all_quad_stats():
    for skater in men:
        get_skater_quads(skater)


# plot quad statistics
def plot_quad_averages():
    data = pd.read_csv("skater_data/quad_stats.csv")

    avg_quads = []
    avg_quad_values = []
    name_list = []

    for skater in men:
        name_list.append(skater.get("name"))
        current_data = data.loc[data["skater_name"] == skater.get("name")]
        quads = current_data["quads"].mean()
        avg_quads.append(int(quads))
        quad_value = current_data["total_quad_value"].mean()
        avg_quad_values.append(quad_value)

    fig = plt.figure()

    i = 0
    for name in name_list:
        plt.annotate(name, (avg_quads[i], avg_quad_values[i]))
        i += 1

    plt.scatter(avg_quads, avg_quad_values, marker='o')
    plt.xticks(avg_quads, avg_quads, rotation='vertical')   
    plt.xlabel("Average quads per competition")
    plt.ylabel("Average score per quad")

    fig.savefig("skater_data/plots/quad_stats.png", bbox_inches='tight')
    # plt.show()


#################################### Execute functions #######################################

# create_boxplots(men, "men", "long", "tss")

# all_quad_stats()

# plot_quad_averages()
