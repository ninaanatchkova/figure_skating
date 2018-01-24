import os
import json
import datetime
from skaters import skaters
from links import skater_total_segment_data

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

# create project folder
def create_project_dir(directory):
    if not os.path.exists(directory):
        print('Creating folder ' + directory)
        os.makedirs(directory)

# create a new file
def write_file(path, data):
    f = open(path, 'w')
    f.write(data)
    f.close()

# add data onto an existing file
def append_to_file(path, data):
    with open(path, 'a') as outfile:
        json.dump(data, outfile)

# delete the contents of a file
def delete_file_contents(path):
    with open(path, 'w'):
        pass

create_project_dir("data")

write_file("data/short_program_scores.txt", "All short program scores from the 2016/2017 and 2017/2018 seasons for the top 10 men singles skaters participating at the 2018 Olympics \n")
all_short_program_scores = get_segment_scores_for_all_skaters("short")
append_to_file("data/short_program_scores.txt", all_short_program_scores)

write_file("data/long_program_scores.txt", "All long program scores from the 2016/2017 and 2017/2018 seasons for the top 10 men singles skaters participating at the 2018 Olympics \n")
all_long_program_scores = get_segment_scores_for_all_skaters("long")
append_to_file("data/long_program_scores.txt", all_long_program_scores)


