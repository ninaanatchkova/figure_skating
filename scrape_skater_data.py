import os
import json
import datetime
import requests
from bs4 import BeautifulSoup
from skaters import skaters
from links import skater_total_segment_data


# GET ALL DATA FROM SEGMENT
def get_segment_data(link):
    page = requests.get(link)
    soup = BeautifulSoup(page.text, "lxml")
    competition_link = base_url + soup.find('h1').find('a').get('href')
    competition_details = get_competition_details(competition_link)
    tables = soup.findAll("table", {"class" : "ptab ptab2"})
    competition_data = {
        "details" : competition_details,
        "tes" : get_tes_scores(tables[1]),
        "pcs" : get_pcs_scores(tables[2])
    }
    return competition_data   

# GET COMPETITION NAME AND DATE
def get_competition_details(competition_link):
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
def get_tes_scores(table):
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

# Extract component scores from segment tables
def get_pcs_scores(table):
    lines = table.findAll('tr')
    length = len(lines)
    index = 1
    program_components = []
    while index < length - 1:
        tablecells = lines[index].findAll('td')
        rowlength = len(tablecells)
        component_placement_score = tablecells[rowlength - 1].getText()
        component_label = tablecells[0].getText().lower().split(" ")
        label = component_label[0]
        if len(component_label) > 1:
            label += "_" + component_label[1]
        component = {
            "label" : label,
            "score" : component_placement_score[1:len(component_placement_score)]
        }
        program_components.append(component)
        index += 1
    return program_components

def skater_total_segment_data(skater, segment):
    competition_links = get_skater_programs(skater, segment)
    skater_segment_data = []
    for link in competition_links:
        segment_data = get_segment_data(link)
        skater_segment_data.append(segment_data)
    return skater_segment_data

yuzu = skater_total_segment_data(skaters[0], "short")



# Add all short/long segment scores for each skater in an array
def get_segment_scores_for_all_skaters(segment):
    all_segment_scores = []
    for skater in skaters:
        segment_scores = {
            "skater" : skater,
            "segment_scores" : skater_total_segment_data(skater, segment)
        }
        all_segment_scores.append(segment_scores)
    return all_segment_scores



create_project_dir("data")

write_file("data/short_program_scores.txt", "All short program scores from the 2016/2017 and 2017/2018 seasons for the top 10 men singles skaters participating at the 2018 Olympics \n")
all_short_program_scores = get_segment_scores_for_all_skaters("short")
append_to_file("data/short_program_scores.txt", all_short_program_scores)

write_file("data/long_program_scores.txt", "All long program scores from the 2016/2017 and 2017/2018 seasons for the top 10 men singles skaters participating at the 2018 Olympics \n")
all_long_program_scores = get_segment_scores_for_all_skaters("long")
append_to_file("data/long_program_scores.txt", all_long_program_scores)


