import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import csv
import os
from skaters import men, ladies, pairs, dance

def skater_means(category_name, skater):
    file_path = "skater_data/" + category_name + "_tss_scores.csv"
    data = pd.read_csv(file_path)
    data = data.loc[data["skater_name"] == skater.get("name")]
    data_short = data.loc[data["segment"] == "short"]
    data_long = data.loc[data["segment"] == "long"]
    short_tes_mean = data_short["tes"].mean()
    long_tes_mean = data_long["tes"].mean()
    short_pcs_mean = data_short["pcs"].mean()
    long_pcs_mean = data_long["pcs"].mean()
    short_bv_mean = data_short["bv"].mean()
    long_bv_mean = data_long["bv"].mean()
    short_tss_mean = data_short["tss"].mean()
    long_tss_mean = data_long["tss"].mean()
    write_file_path = "skater_data/" + category_name + "_mean_scores.csv"
    if not os.path.exists(write_file_path):
        with open(write_file_path, "w", newline="", encoding= "utf-8") as csvfile:
            fieldnames = ["skater_name", "short_tes", "long_tes", "short_pcs", "long_pcs", "short_bv", "long_bv", "short_tss", "long_tss"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow({
                    "skater_name" : skater.get("name"),
                    "short_tes": short_tes_mean,
                    "long_tes": long_tes_mean,
                    "short_pcs": short_pcs_mean,
                    "long_pcs": long_pcs_mean,
                    "short_bv": short_bv_mean,
                    "long_bv": long_bv_mean,
                    "short_tss": short_tss_mean,
                    "long_tss": long_tss_mean
                    })
        csvfile.close()
    else:
        with open(write_file_path, "a", newline="", encoding= "utf-8") as csvfile:
            fieldnames = ["skater_name", "short_tes", "long_tes", "short_pcs", "long_pcs", "short_bv", "long_bv", "short_tss", "long_tss"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow({
                    "skater_name" : skater.get("name"),
                    "short_tes": short_tes_mean,
                    "long_tes": long_tes_mean,
                    "short_pcs": short_pcs_mean,
                    "long_pcs": long_pcs_mean,
                    "short_bv": short_bv_mean,
                    "long_bv": long_bv_mean,
                    "short_tss": short_tss_mean,
                    "long_tss": long_tss_mean
                    })
        csvfile.close()


def generate_means_dataset(category, category_name):
    for skater in category:
        skater_means(category_name, skater)



def plot_skater_data(x, y, category_name):
    df = pd.read_csv("skater_data/" + category_name + "_mean_scores.csv")
    fig = plt.figure()
    plt.scatter(df[x], df[y], marker='o')

    for i, name in enumerate(df['skater_name']):
        plt.annotate(name, (df[x][i], df[y][i]))
    
    plt.xlabel(x)
    plt.ylabel(y)
    
    fig.savefig("skater_data/plots/" + category_name + "_" + x + "_vs_" + y, bbox_inches='tight')
    # plt.show()


################################ Execute functions ######################

# generate_means_dataset(men, "men")

# plot_skater_data("long_tss", "short_tss", "men")
# plot_skater_data("short_pcs", "short_tes", "men")
# plot_skater_data("long_pcs", "long_tes", "men")
# plot_skater_data("long_bv", "long_tes", "men")