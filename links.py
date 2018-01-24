import requests
from bs4 import BeautifulSoup
from dateutil import parser
from skaters import skaters

base_url = "http://skatingscores.com"

# FIND SKATER PAGE URL FROM NAME
def get_skater_page(skater):
    skaternames = skater.get("name").lower().split()
    link = base_url + "/unit/" + skater.get("country") + "/" + skaternames[0] + "_" + skaternames[1] + "/"
    return link

# GET ALL SKATER PROGRAM RESULT PAGES LINKS BY NAME AND TYPE (SP/LP)
def get_skater_programs(skater, segment):
    page = requests.get(get_skater_page(skater))
    soup = BeautifulSoup(page.text, "lxml")
    tables = soup.findAll("table", {"class" : "men-tab"})

    competitionlinks = []
    for table in tables:
        for line in table.findAll('tr'):
            tablecells = line.findAll('td')
            if len(tablecells) == 7:
                if segment == "short":
                    competitionlinks.append(base_url + tablecells[1].find('a').get('href'))
                if segment == "long":
                    competitionlinks.append(base_url + tablecells[3].find('a').get('href'))
    return competitionlinks

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
        "date" : parser.parse(competition_dates[1])
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
        component = {
            "label" : tablecells[0].getText(),
            "score" : component_placement_score[1:len(component_placement_score)]
        }
        program_components.append(component)
        index += 1
    return program_components

def skater_total_segment_data(skater, segment):
    competition_links = get_skater_programs(skater, segment)
    print(competition_links)
    skater_segment_data = []
    for link in competition_links:
        segment_data = get_segment_data(link)
        print(segment_data)
        skater_segment_data.append(segment_data)
    return skater_segment_data

# TEST
print(skater_total_segment_data(skaters[2], "short"))
