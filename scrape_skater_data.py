import os
import csv
import datetime
import requests
from time import sleep
from random import randint
from bs4 import BeautifulSoup
from skaters import men, ladies, pairs, dance

base_url = "http://skatingscores.com"

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

def all_tes_scores_to_csv(category, category_name):
    for skater in category:
        add_skater_tes_scores_to_csv(skater, "short", category_name)
        add_skater_tes_scores_to_csv(skater, "long", category_name)

def all_tss_scores_to_csv(category, category_name):
    for skater in category:
        add_skater_tss_scores_to_csv(skater, "short", category_name)
        add_skater_tss_scores_to_csv(skater, "long", category_name)

def add_skater_tes_scores_to_csv(skater, segment, category_name):
    skater_links = read_skater_links_from_file(skater, segment)
    file_path = "skater_data/" + category_name + "_tes_scores.csv"
    for link in skater_links:
        print(link)
        competition = get_competition_details(link)
        tes = get_tes_scores(link)

        if not os.path.exists(file_path):
            with open(file_path, "w", newline="", encoding= "utf-8") as csvfile:
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
            with open(file_path, "a", newline="", encoding= "utf-8") as csvfile:
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

def add_skater_tss_scores_to_csv(skater, segment, category_name):
    skater_links = read_skater_links_from_file(skater, segment)
    file_path = "skater_data/" + category_name + "_tss_scores.csv"
    for link in skater_links:
        print(link)
        competition = get_competition_details(link)
        tss_score = get_total_segment_score(link)
        bv_score = get_total_bv(link)
        tes_score = get_total_tes(link)
        pcs_score = get_total_pcs_scores(link)

        if not os.path.exists(file_path):
            with open(file_path, "w", newline="", encoding= "utf-8") as csvfile:
                fieldnames = ["skater_name", "skater_country", "event", "location", "date", "segment", "tss", "bv", "tes", "pcs"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerow({
                    "skater_name" : skater.get("name"),
                    "skater_country": skater.get("country"),
                    "event": competition.get("name"),
                    "location": competition.get("place"),
                    "date": competition.get("date"),
                    "segment": segment,
                    "tss": tss_score,
                    "bv": bv_score,
                    "tes": tes_score,
                    "pcs": pcs_score
                })
            csvfile.close()
        else:
            with open(file_path, "a", newline="", encoding= "utf-8") as csvfile:
                fieldnames = ["skater_name", "skater_country", "event", "location", "date", "segment", "tss", "bv", "tes", "pcs"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writerow({
                    "skater_name" : skater.get("name"),
                    "skater_country": skater.get("country"),
                    "event": competition.get("name"),
                    "location": competition.get("place"),
                    "date": competition.get("date"),
                    "segment": segment,
                    "tss": tss_score,
                    "bv": bv_score,
                    "tes": tes_score,
                    "pcs": pcs_score
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
    sleep(randint(0, 9))
    page = requests.get(link)
    soup = BeautifulSoup(page.text, "lxml")
    competition_link = base_url + soup.find('h1').find('a').get('href')
    sleep(randint(0, 9))
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

# Extract PCS scores from segment tables // DEPRECATED
''' def get_pcs_scores(link):
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
    return program_components '''

# Extract total PCS from table
def get_total_pcs_scores(link):
    table = get_score_table(link, "pcs")
    line = table.find('tr')
    cells = line.findAll('td')
    placement_pcs = cells[1].get_text(strip=True, separator=" ").split(" ")
    return placement_pcs[1]

# Extract total BV from table
def get_total_bv(link):
    table = get_score_table(link, "tbv")
    line = table.find('tr')
    cells = line.findAll('td')
    placement_bv = cells[1].get_text(strip=True, separator=" ").split(" ")
    return placement_bv[1]

# Extract total TES from table
def get_total_tes(link):
    table = get_score_table(link, "ttes")
    line = table.find('tr')
    cells = line.findAll('td')
    placement_tes = cells[1].get_text(strip=True, separator=" ").split(" ")
    return placement_tes[1]

# Extract TSS from table
def get_total_segment_score(link):
    table = get_score_table(link, "tss")
    lines = table.findAll('tr')
    cells = lines[1].findAll('td')
    tss = cells[2].get_text()
    return tss

# Get relevant score table
def get_score_table(link, type_of_score):
    sleep(randint(0, 9))
    page = requests.get(link)
    soup = BeautifulSoup(page.text, "lxml")
    tables = soup.findAll("table", {"class" : "ptab"})
    if type_of_score == "tss":
        return tables[0]
    elif type_of_score == "tes":
        return tables[2]
    elif type_of_score == "tbv":
        return tables[4]
    elif type_of_score == "ttes":
        return tables[5]
    elif type_of_score == "pcs":
        return tables[7]
    else:
        return ""

# all_tss_scores_to_csv(men, "men")
# all_tes_scores_to_csv(men, "men")
all_tss_scores_to_csv(ladies, "ladies")
all_tes_scores_to_csv(ladies, "ladies")
all_tss_scores_to_csv(pairs, "pairs")
all_tes_scores_to_csv(pairs, "pairs")
all_tss_scores_to_csv(dance, "dance")
all_tes_scores_to_csv(dance, "dance")
