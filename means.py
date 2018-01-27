import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import csv
import os
from skaters import skaters
from sklearn.cluster import KMeans 

def skater_means(skater):
    data = pd.read_csv("skater_data/tss_scores.csv")
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
    if not os.path.exists("skater_data/mean_scores.csv"):
        with open("skater_data/mean_scores.csv", "w", newline="", encoding= "utf-8") as csvfile:
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
        with open("skater_data/mean_scores.csv", "a", newline="", encoding= "utf-8") as csvfile:
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


def generate_means_dataset():
    for skater in skaters:
        skater_means(skater)

# generate_means_dataset()


def plot_skater_data(x, y):
    df = pd.read_csv("skater_data/mean_scores.csv")
    fig, ax = plt.subplots()
    ax.scatter(df[x], df[y], marker='o')

    for i, name in enumerate(df['skater_name']):
        ax.annotate(name, (df[x][i], df[y][i]))
    
    plt.xlabel(x)
    plt.ylabel(y)

    plt.show()

plot_skater_data("long_tss", "short_tss")
plot_skater_data("short_pcs", "short_tes")
plot_skater_data("long_pcs", "long_tes")
plot_skater_data("long_bv", "long_tes")