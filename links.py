import requests
from bs4 import BeautifulSoup
from skaters import skaters

base_url = "http://skatingscores.com"

# FIND SKATER PAGE URL FROM NAME
def get_skater_page(skater):
    skaternames = skater.get("name").lower().split()
    link = base_url + "/unit/" + skater.get("country") + "/" + skaternames[0] + "_" + skaternames[1] + "/"
    return link

# GET ALL SKATER PROGRAM RESULT PAGES LINKS BY NAME AND TYPE (SP/LP)
def get_skater_programs(skater, type_of_program):
    page = requests.get(get_skater_page(skater))
    soup = BeautifulSoup(page.text, "lxml")
    tables = soup.findAll("table", {"class" : "men-tab"})

    competitionlinks = []
    for table in tables:
        for line in table.findAll('tr'):
            tablecells = line.findAll('td')
            if len(tablecells) == 7:
                if type_of_program == "short":
                    competitionlinks.append(base_url + tablecells[1].find('a').get('href'))
                if type_of_program == "long":
                    competitionlinks.append(base_url + tablecells[3].find('a').get('href'))
    
    return competitionlinks


# TEST
print(get_skater_programs(skaters[2], "short"))
print(get_skater_programs(skaters[2], "long"))
