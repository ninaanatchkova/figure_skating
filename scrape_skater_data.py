import os
import csv
import datetime
import requests
from bs4 import BeautifulSoup
from skaters import skaters
from links import base_url, skater_name_to_string

def all_tes_scores_to_csv():
    for skater in skaters:
        add_skater_tes_scores_to_csv(skater, "short")
        add_skater_tes_scores_to_csv(skater, "long")

def all_pcs_scores_to_csv():
    for skater in skaters:
        add_skater_pcs_scores_to_csv(skater, "short")
        add_skater_pcs_scores_to_csv(skater, "long")

def add_skater_tes_scores_to_csv(skater, segment):
    skater_links = read_skater_links_from_file(skater, segment)
    for link in skater_links:
        competition = get_competition_details(link)
        tes = get_tes_scores(link)

        if not os.path.exists("skater_data/tes_scores.csv"):
            with open("skater_data/tes_scores.csv", "w", newline="", encoding= "utf-8") as csvfile:
                fieldnames = ["skater_name", "skater_country", "event", "location", "date", "segment", "tech_element", "info", "bv", "goe"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for tes_score in tes:
                    writer.writerow({
                        "skater_name" : skater.get("name"),
                        "skater_country": skater.get("country"),
                        "event": competition.get("name"),
                        "location": competition.get("place"),
                        "date": competition.get("date"),
                        "segment": segment,
                        "tech_element": tes_score.get("label"),
                        "info": tes_score.get("info"),
                        "bv": tes_score.get("BV"),
                        "goe": tes_score.get("GOE")
                        })
            csvfile.close()
        else:
            with open("skater_data/tes_scores.csv", "a", newline="", encoding= "utf-8") as csvfile:
                fieldnames = ["skater_name", "skater_country", "event", "location", "date", "segment", "tech_element", "info", "bv", "goe"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                for tes_score in tes:
                    writer.writerow({
                        "skater_name" : skater.get("name"),
                        "skater_country": skater.get("country"),
                        "event": competition.get("name"),
                        "location": competition.get("place"),
                        "date": competition.get("date"),
                        "segment": segment,
                        "tech_element": tes_score.get("label"),
                        "info": tes_score.get("info"),
                        "bv": tes_score.get("BV"),
                        "goe": tes_score.get("GOE")
                    })
            csvfile.close()

def add_skater_pcs_scores_to_csv(skater, segment):
    skater_links = read_skater_links_from_file(skater, segment)
    for link in skater_links:
        competition = get_competition_details(link)
        pcs_score = get_pcs_scores(link)

        if not os.path.exists("skater_data/pcs_scores.csv"):
            with open("skater_data/pcs_scores.csv", "w", newline="", encoding= "utf-8") as csvfile:
                fieldnames = ["skater_name", "skater_country", "event", "location", "date", "segment", "skating_skills", "transitions", "performance", "composition", "interpretation"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerow({
                    "skater_name" : skater.get("name"),
                    "skater_country": skater.get("country"),
                    "event": competition.get("name"),
                    "location": competition.get("place"),
                    "date": competition.get("date"),
                    "segment": segment,
                    "skating_skills": pcs_score.get("skating_skills"),
                    "transitions": pcs_score.get("transitions"),
                    "performance": pcs_score.get("performance"),
                    "composition": pcs_score.get("composition"),
                    "interpretation": pcs_score.get("interpretation")
                    })
            csvfile.close()
        else:
            with open("skater_data/pcs_scores.csv", "a", newline="", encoding= "utf-8") as csvfile:
                fieldnames = ["skater_name", "skater_country", "event", "location", "date", "segment", "skating_skills", "transitions", "performance", "composition", "interpretation"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writerow({
                    "skater_name" : skater.get("name"),
                    "skater_country": skater.get("country"),
                    "event": competition.get("name"),
                    "location": competition.get("place"),
                    "date": competition.get("date"),
                    "segment": segment,
                    "skating_skills": pcs_score.get("skating_skills"),
                    "transitions": pcs_score.get("transitions"),
                    "performance": pcs_score.get("performance"),
                    "composition": pcs_score.get("composition"),
                    "interpretation": pcs_score.get("interpretation")
                })
            csvfile.close()
       

# READ SKATER LINKS FROM FILE
def read_skater_links_from_file(skater, segment):
    skater_links = []
    file_name = skater_name_to_string(skater) + "_" + segment + "_links.txt"
    path = "skater_data/links/" + file_name
    if os.path.exists(path):
        skater_links = [line.strip() for line in open(path)]
    return skater_links


# Get competition name, place, date
def get_competition_details(link):
    page = requests.get(link)
    soup = BeautifulSoup(page.text, "lxml")
    competition_link = base_url + soup.find('h1').find('a').get('href')
    page =  requests.get(competition_link)
    soup = BeautifulSoup(page.text, "lxml")
    competition_name = soup.find('h1').getText()
    competition_place_date = soup.findAll('h2')
    competition_dates = competition_place_date[1].getText().split(" - ")
    competition_details = {
        "name" : competition_name,
        "place" : competition_place_date[0].getText(),
        "date" : competition_dates[1]
    }
    return competition_details

# Extract TES scores from segment tables
def get_tes_scores(link):
    table = get_score_table(link, "tes")
    lines = table.findAll('tr')
    length = len(lines)
    index = 1
    tech_elements = []
    while index < length - 1:
        tablecells = lines[index].findAll('td')
        element = {
            "label" : tablecells[1].getText(),
            "info" : tablecells[2].getText(),
            "BV" : tablecells[3].getText(),
            "GOE" : tablecells[5].getText()
        }
        tech_elements.append(element)
        index += 1
    return tech_elements

# Extract PCS scores from segment tables
def get_pcs_scores(link):
    table = get_score_table(link, "pcs")
    lines = table.findAll('tr')
    length = len(lines)
    index = 1
    program_components = {}
    while index < length - 1:
        tablecells = lines[index].findAll('td')
        rowlength = len(tablecells)
        component_placement_score = tablecells[rowlength - 1].getText()
        component_label = tablecells[0].getText().lower().split(" ")
        label = component_label[0]
        if len(component_label) > 1:
            label += "_" + component_label[1]
        program_components.update({label : component_placement_score[1:len(component_placement_score)]})
        index += 1
    return program_components

# Get relevant score table
def get_score_table(link, type_of_score):
    page = requests.get(link)
    soup = BeautifulSoup(page.text, "lxml")
    tables = soup.findAll("table", {"class" : "ptab ptab2"})
    if type_of_score == "tes":
        return tables[1]
    elif type_of_score == "pcs":
        return tables[2]
    else:
        return ""
