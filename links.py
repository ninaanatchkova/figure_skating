import requests
import os
from skaters import men, ladies, pairs, dance
from bs4 import BeautifulSoup

base_url = "http://skatingscores.com"

# Find skater page at skatingscores.com by name
def get_skater_page(skater):
    skaternames = skater.get("name").lower().split()
    link = base_url + "/unit/" + skater.get("country") + "/" + skater_name_to_string(skater) + "/"
    return link

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

# Get competition links by segment
def get_skater_programs(category_name, skater, segment):
    tab_name = {"men": "men-tab", "ladies" : "ladies-tab", "pairs" : "pairs-tab", "dance" : "dance-tab"}
    tab = tab_name.get(category_name, "default")
    page = requests.get(get_skater_page(skater))
    soup = BeautifulSoup(page.text, "lxml")
    tables = soup.findAll("table", {"class" : tab})

    competitionlinks = []
    for table in tables:
        for line in table.findAll('tr'):
            tablecells = line.findAll('td')
            if len(tablecells) == 7:
                if segment == "short":
                    competitionlinks.append(base_url + tablecells[1].find('a').get('href'))
                if segment == "long":
                    competitionlinks.append(base_url + tablecells[3].find('a').get('href'))
    print(competitionlinks)
    return competitionlinks

# Create folder for files
def create_project_dir(directory):
    if not os.path.exists(directory):
        print('Creating folder ' + directory)
        os.makedirs(directory)

# Delete file contents
def delete_file_contents(path):
    with open(path, 'w'):
        pass

# Get and save segment links to file
def save_skater_links_to_file(category_name, skater, segment):
    links = get_skater_programs(category_name, skater, segment)
    create_project_dir("skater_data/links")
    file_name = skater_name_to_string(skater) + "_" + segment + "_links.txt"
    path = "skater_data/links/" + file_name
    delete_file_contents(path)
    f = open(path, 'w')
    for link in links:
        f.write(link + "\n")
    f.close()

# Save links for all skaters in a category
def save_all_category_links(category, category_name):
    for skater in category:
        save_skater_links_to_file(category_name, skater, "short")
        save_skater_links_to_file(category_name, skater, "long")


################### execute #######################

# save_all_category_links(men, "men")
# save_all_category_links(ladies, "ladies")
# save_all_category_links(pairs, "pairs")
# save_all_category_links(dance, "dance")