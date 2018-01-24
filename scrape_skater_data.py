import requests
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


all_short_program_scores = get_segment_scores_for_all_skaters("short")
all_long_program_scores = get_segment_scores_for_all_skaters("long")