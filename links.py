import requests
import os
from skaters import skaters
from bs4 import BeautifulSoup

base_url = "http://skatingscores.com"

# FIND SKATER PAGE URL FROM NAME
def get_skater_page(skater):
    skaternames = skater.get("name").lower().split()
    link = base_url + "/unit/" + skater.get("country") + "/" + skater_name_to_string(skater) + "/"
    return link

def skater_name_to_string(skater):
    skaternames = skater.get("name").lower().split()
    skater_string = skaternames[0] + "_" + skaternames[1]
    return skater_string

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

# CREATE PROJECT FOLDER
def create_project_dir(directory):
    if not os.path.exists(directory):
        print('Creating folder ' + directory)
        os.makedirs(directory)

# DELETE THE CONTENTS OF A FILE
def delete_file_contents(path):
    with open(path, 'w'):
        pass

# SAVE SKATER SEGMENT LINKS TO FILE
def save_skater_links_to_file(skater, segment):
    links = get_skater_programs(skater, segment)
    create_project_dir("skater_data/links")
    file_name = skater_name_to_string(skater) + "_" + segment + "_links.txt"
    path = "skater_data/links/" + file_name
    delete_file_contents(path)
    f = open(path, 'w')
    for link in links:
        f.write(link + "\n")
    f.close()

# SAVE ALL SKATER LINKS
for skater in skaters:
    save_skater_links_to_file(skater, "short")
    save_skater_links_to_file(skater, "long")