"""
This script performs automatically the lineage specific analysis for every
geographical area (at every granularity level) and every lineage and store
in a .csv file the mutations

"""
import csv
import sqlite3
from datetime import datetime
import time
from json import dump
from os.path import exists
from types import SimpleNamespace

from apis.bulk_lineage_specific import extract_mutation_data, produce_bulk_statistics, extract_week_seq_counts, get_lineages_from_loc_date
from apis.utils.path_manager import db_path, create_directory
from apis.utils.utils import start_date

# ################## CONFIGURATION ##################
#     use math.inf or -math.inf to remove filters

c = {}
c['end_date'] = "2022-05-10"
c = SimpleNamespace(**c)


# ####################################################


def fetch_all_locations(date):
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    stop = (datetime.strptime(date, "%Y-%m-%d") - start_date).days
    start = stop - 7

    print(">Fetching all locations...", end="")
    query = f''' SELECT DISTINCT location 
                 FROM locations JOIN aggr_sequences AGS on locations.location_id = AGS.location_id
                 WHERE location is not null AND date > {start} AND date <= {stop}
                 ORDER BY location;'''
    locs = [x[0] for x in cur.execute(query).fetchall()]
    con.close()
    print("done.")
    return locs


def compute_weeks_from_date(date):
    """
    Compute weeks values starting from the date string of the last day of the analysis period
    Args:
        date: String representing the date of the last day of the 4th week

    Returns: A dictionary identifying all the six 5-days periods

    """
    w = {}
    w['w6_end'] = (datetime.strptime(date, "%Y-%m-%d") - start_date).days
    w['w6_begin'] = w['w6_end'] - 5
    w['w5_end'] = w['w6_begin']
    w['w5_begin'] = w['w5_end'] - 5
    w['w4_end'] = w['w5_begin']
    w['w4_begin'] = w['w4_end'] - 5
    w['w3_end'] = w['w4_begin']
    w['w3_begin'] = w['w3_end'] - 5
    w['w2_end'] = w['w3_begin']
    w['w2_begin'] = w['w2_end'] - 5
    w['w1_end'] = w['w2_begin']
    w['w1_begin'] = w['w1_end'] - 5

    return w


def run_bulk_analyzer():
    print("\n***** Bulk analyzer started  *****")
    all_locations = fetch_all_locations(c.end_date)
    tot_mut = 0

    print("\nProcessing started:")
    exec_start = time.time()
    dir_name = 'bulk_analyzer_' + c.end_date.replace('-', '_')

    i = 0
    while exists(f"{i if i>0 else ''}{dir_name}"):
        i += 1

    create_directory(f"{i if i>0 else ''}{dir_name}")

    with open(f"{i if i>0 else ''}{dir_name}/config.txt", 'w', encoding='UTF8') as f:
        dump(vars(c), f)

    with open(f"{i if i>0 else ''}{dir_name}/mutations.csv", 'w', encoding='UTF8') as f:
        fieldnames = ['location', 'lineage', 'protein_mut',
                      'f1', 'f2', 'f3', 'f4', 'f5', 'w6','tot_seq_w6']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for index, location in enumerate(all_locations):
            print("\t> Current location[" + str(index + 1) + "/" + str(len(all_locations)) + "]: " + location)
            all_lineages = get_lineages_from_loc_date(location=location, date=c.end_date)
            if len(all_lineages) == 0:
                print("\t\t> No lineages for this location")

            for idx, lineage in enumerate(all_lineages):
                print("\t\t> Current lineage[" + str(idx + 1) + "/" + str(len(all_lineages)) + "]: " + lineage, end="")

                w = compute_weeks_from_date(c.end_date)
                week_sequence_counts = extract_week_seq_counts(location, lineage, w)

                min_sequences = int(week_sequence_counts[-1] * 0.005 + 1)
                mutation_data = extract_mutation_data(location, lineage, w, min_sequences)

                # list of dictionaries, each representing a mutation
                statistics = produce_bulk_statistics(location, week_sequence_counts, mutation_data)
                # map
                statistics = [dict(item, lineage=lineage) for item in statistics]
                print(", added " + str(len(statistics)) + " rows")
                tot_mut += len(statistics)
                writer.writerows(statistics)
    print(f"\ndone in {time.time() - exec_start:.5f} seconds.")
    print("******************************************************* tot_mut=" + str(tot_mut))
