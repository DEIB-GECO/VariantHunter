"""
This script performs automatically the lineage specific analysis for every
geographical area (at every granularity level) and every lineage and store
in a .csv file the mutations satisfying the some conditions

Remember that: lineage specific search extract all and only the mutations
detected in the last week of the considered analysis period.
Only mutations affecting at least 0.5% of the sequences collected in the week are shown.

"""
import csv
import sqlite3
from datetime import datetime
import time
from functools import partial
from json import dump
from math import inf as infinity
from os.path import exists
from types import SimpleNamespace

from apis.explorer import get_lineage_characterization
from apis.lineage_specific import get_lineages_from_loc_date, extract_week_seq_counts, extract_mutation_data
from apis.utils.path_manager import db_path, create_directory
from apis.utils.utils import compute_weeks_from_date, start_date, produce_adv_statistics

# ################## CONFIGURATION ##################
#     use math.inf or -math.inf to remove filters

c = {}
c['end_date'] = "2022-05-10"

c['slope_min'] = 1.5  # min slope value
c['f1_max'] = 25  # max frequency for the 1st week
c['ignore_characterizing'] = True  # ignore the characterizing mutations

c['p_value_with_mut_max'] = infinity  # max value for the p-value-with-mut
c['p_value_without_mut_max'] = infinity  # max value for the p-value-without-mut
c['p_value_comp_max'] = 0.05  # max value for the p-value-comp
# NaN p-values values are included in all the cases

c['w1_min'] = 0  # min number of sequences for the 1st week
c['w2_min'] = 0  # min number of sequences for the 2nd week
c['w3_min'] = 1  # min number of sequences for the 3rd week
c['w4_min'] = 1  # min number of sequences for the 4th week

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


characterizations_dic = {}


def is_characterizing(item, lineage):
    if not (lineage in characterizations_dic):
        characterizations_dic[lineage] = get_lineage_characterization([lineage])
    return (item["protein"] + "_" + item["mut"]) in characterizations_dic[lineage]


def check_requirements(mut, lineage):
    is_compliant = \
        mut["slope"] >= c.slope_min and \
        mut["f1"] <= c.f1_max and \
        mut["w1"] >= c.w1_min and mut["w2"] >= c.w2_min and \
        mut["w3"] >= c.w3_min and mut["w4"] >= c.w4_min and \
        (mut["p_value_with_mut"] == 'NaN' or float(mut["p_value_with_mut"]) <= c.p_value_with_mut_max) and \
        (mut["p_value_without_mut"] == 'NaN' or float(mut["p_value_without_mut"]) <= c.p_value_without_mut_max) and \
        (mut["p_value_comp"] == 'NaN' or float(mut["p_value_comp"]) <= c.p_value_comp_max) and \
        not is_characterizing(mut, lineage)

    return is_compliant


def run_auto_analyzer():
    print("\n***** Automatic analyzer started  *****")
    all_locations = fetch_all_locations(c.end_date)
    tot_mut = 0

    print("\nProcessing started:")
    exec_start = time.time()
    dir_name = 'auto_analyzer_' + c.end_date.replace('-', '_')

    i = 0
    while exists(f"{i if i>0 else ''}{dir_name}"):
        i += 1

    create_directory(f"{i if i>0 else ''}{dir_name}")

    with open(f"{i if i>0 else ''}{dir_name}/config.txt", 'w', encoding='UTF8') as f:
        dump(vars(c), f)

    with open(f"{i if i>0 else ''}{dir_name}/mutations.csv", 'w', encoding='UTF8') as f:
        fieldnames = ['location', 'lineage', 'protein', 'mut', 'slope','std_dev',
                      'f1', 'w1', 'f2', 'w2', 'f3', 'w3', 'f4', 'w4',
                      'tot_seq', 'slope123', 'slope134', 'slope234',
                      'p_value_with_mut', 'p_value_without_mut', 'p_value_comp']
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
                statistics = produce_adv_statistics(location, week_sequence_counts, mutation_data)
                # filter and map
                statistics = list(filter(partial(check_requirements, lineage=lineage), statistics))
                statistics = [dict(item, lineage=lineage) for item in statistics]
                print(", added " + str(len(statistics)) + " rows")
                tot_mut += len(statistics)
                writer.writerows(statistics)
    print(f"\ndone in {time.time() - exec_start:.5f} seconds.")
    print("******************************************************* tot_mut=" + str(tot_mut))
