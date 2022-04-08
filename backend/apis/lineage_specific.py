"""
    API to perform lineage specific analysis
    Endpoints:
    ├── getLineages
    ├── getAllLineages
    └── getStatistics
"""

from __future__ import print_function

import sqlite3
import time
from datetime import datetime
import numpy as np
import scipy.stats
from flask_restplus import Namespace, Resource

from .explorer import get_lineage_characterization
from .utils.utils import start_date, compute_weeks_from_date

api = Namespace('lineage_specific', description='lineage_specific')
db_name = 'varianthunter.db'

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


def get_all_lineages():
    """
    Extract all the possible values for the lineage from the database
    Returns: An array of lineages

    """
    print("> Extract all lineages ...", end="")
    exec_start = time.time()
    con = sqlite3.connect(db_name)
    cur = con.cursor()

    query = "select distinct * from lineages_characterization;"
    extracted_lineages = [x[0] for x in cur.execute(query).fetchall()]
    con.close()
    extracted_lineages.sort()

    print(f"done in {time.time() - exec_start:.5f} seconds.")
    return extracted_lineages


all_lineages_dict = get_all_lineages()  # At server startup, fetch all the lineages


def get_lineages_from_loc_date(location, date):
    """
    Extract the lineages for a given location and week from the database
    Args:
        location:   String representing the location to be considered
        date:       String representing the (week ending) date to be considered.

    Returns: An array of lineages

    """
    print("\t Extract lineages data given location and date...", end="")
    stop = (datetime.strptime(date, "%Y-%m-%d") - start_date).days
    start = stop - 28

    exec_start = time.time()
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    query = f'''select distinct lineage 
                    from timelocling 
                    where location = '{location}' and date > {start} and date <= {stop};'''
    extracted_lineages = [x[0] for x in cur.execute(query).fetchall()]
    con.close()

    print(f"done in {time.time() - exec_start:.5f} seconds.")
    return extracted_lineages


def get_lineages_from_loc(location):
    """
    Extract the lineages for a given location from the database
    Args:
        location:   String representing the location to be considered

    Returns: An array of lineages

    """
    print("\t Extract lineages data given location...", end="")
    exec_start = time.time()
    con = sqlite3.connect(db_name)
    cur = con.cursor()

    query = f'''    select distinct lineage 
                    from timelocling 
                    where location = '{location}';'''
    extracted_lineages = [x[0] for x in cur.execute(query).fetchall()]
    con.close()

    print(f"done in {time.time() - exec_start:.5f} seconds.")
    return extracted_lineages


def get_lineages_from_date(date):
    """
    Extract the lineages for a given week from the database
    Args:
        date:       String representing the (week ending) date to be considered.

    Returns: An array of lineages

    """
    print("\t Extract lineages data given date...", end="")
    stop = (datetime.strptime(date, "%Y-%m-%d") - start_date).days
    start = stop - 28

    exec_start = time.time()
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    query = f'''select distinct lineage 
                    from timelocling 
                    where date > {start} and date <= {stop};'''
    extracted_lineages = [x[0] for x in cur.execute(query).fetchall()]
    con.close()

    print(f"done in {time.time() - exec_start:.5f} seconds.")
    return extracted_lineages


def compute_pvalue(freq1, freq2):
    """
    Compute p-value for the hypothesis test of independence of the observed frequencies
    Args:
        freq1:  Observed freq 1
        freq2:  Observed freq 2

    Returns: The computed p-value

    """
    try:
        return scipy.stats.chi2_contingency([freq1, freq2])[1]
    except:
        return "NaN"


def extract_week_seq_counts(location, lineage, w):
    """
    Extract weekly sequence counts for the given location, lineage and weeks from the database
    Args:
        location:   String representing the location to be considered
        lineage:    String representing the lineage to be considered
        w:          Weeks to be considered

    Returns: An array of sequence counts

    """
    print("\t Extract number of sequences in the four weeks...", end="")
    exec_start = time.time()
    con = sqlite3.connect(db_name)
    cur = con.cursor()

    def extract_week_count(start, stop):
        query = f'''  select date,location,sum(count) 
                    from timelocling 
                    where date > {start} and date <= {stop} and location = '{location}' and lineage = '{lineage}' 
                    group by date,location,lineage;'''
        return sum([x[2] for x in cur.execute(query).fetchall()])

    tot_seq_w4 = extract_week_count(w['w4_begin'], w['w4_end'])
    tot_seq_w3 = extract_week_count(w['w3_begin'], w['w3_end'])
    tot_seq_w2 = extract_week_count(w['w2_begin'], w['w2_end'])
    tot_seq_w1 = extract_week_count(w['w1_begin'], w['w1_end'])
    con.close()
    print(f'done in {time.time() - exec_start:.5f} seconds.')
    return [tot_seq_w1, tot_seq_w2, tot_seq_w3, tot_seq_w4]


def extract_mutation_data(location, lineage, w, min_sequences=0):
    """
        Extract weekly mutation data for the given location, lineage and weeks from the database
        Args:
            location:       String representing the location to be considered
            lineage:        String representing the lineage to be considered
            w:              Weeks to be considered
            min_sequences:  Minimum number of sequence

        Returns: An array describing the mutations for each week

        """
    print("\t Extract mutation data for the four weeks...", end="")
    exec_start = time.time()
    con = sqlite3.connect(db_name)
    cur = con.cursor()

    def extract_week_mutation(start, stop, is_target=False):
        having_clause = f"having sum(count) >= {min_sequences}"
        query = f'''  select mut, sum(count) 
                    from mutsg 
                    where date > {start} and date <= {stop} and location = '{location}' and lineage = '{lineage}' and mut !=''
                    group by mut 
                    {having_clause if is_target else ""};'''
        return {k: v for k, v in cur.execute(query).fetchall()}

    muts_w4 = extract_week_mutation(w['w4_begin'], w['w4_end'], is_target=True)
    muts_w3 = extract_week_mutation(w['w3_begin'], w['w3_end'])
    muts_w2 = extract_week_mutation(w['w2_begin'], w['w2_end'])
    muts_w1 = extract_week_mutation(w['w1_begin'], w['w1_end'])
    con.close()
    print(f'done in {time.time() - exec_start:.5f} seconds.')
    return [muts_w1, muts_w2, muts_w3, muts_w4]


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""                               ENDPOINTS                             """""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


@api.route('/getAllLineages')
class FieldList(Resource):
    @api.doc('get_all_lineages')
    def get(self):
        """
        Endpoint to obtain all the possible lineages
        @return:    An array of lineages
        """
        return all_lineages_dict


@api.route('/getLineages')
class FieldList(Resource):
    @api.doc('get_lineages')
    def post(self):
        """
        Endpoint to obtain the lineages for a given location and week (if specified)
        @return:    An array of lineages
        """
        location = api.payload['location']
        date = api.payload['date']

        if location is None and date is None:
            lineages = all_lineages_dict
        elif date is None:
            lineages = get_lineages_from_loc(location)
        elif location is None:
            lineages = get_lineages_from_date(date)
        else:
            lineages = get_lineages_from_loc_date(location,date)
        return lineages


@api.route('/getStatistics')
class FieldList(Resource):
    @api.doc('get_statistics')
    def post(self):
        """
        Endpoint to perform a lineage specific analysis
        @return:    An object including the results and the support info
        """
        location = api.payload['location']
        lineage = api.payload['lineage']
        date = api.payload['date']

        w = compute_weeks_from_date(date)

        week_sequence_counts = extract_week_seq_counts(location, lineage, w)
        tot_seq_w1, tot_seq_w2, tot_seq_w3, tot_seq_w4 = week_sequence_counts

        mutation_data = extract_mutation_data(location, lineage, w,
                                              min_sequences=int(week_sequence_counts[-1] * 0.005 + 1))
        mut_w1, mut_w2, mut_w3, mut_w4 = mutation_data

        statistics = []
        for mut, c4 in mut_w4.items():
            protein, mutation = mut.split("_")
            c1 = mut_w1.get(mut, 0)
            c2 = mut_w2.get(mut, 0)
            c3 = mut_w3.get(mut, 0)
            f1 = (c1 / tot_seq_w1) * 100 if tot_seq_w1 > 0 else 0
            f2 = (c2 / tot_seq_w2) * 100 if tot_seq_w2 > 0 else 0
            f3 = (c3 / tot_seq_w3) * 100 if tot_seq_w3 > 0 else 0
            f4 = (c4 / tot_seq_w4) * 100 if tot_seq_w4 > 0 else 0
            slope, intercept = np.polyfit([0, 1, 2, 3], [f1, f2, f3, f4], 1)
            statistics.append({
                'location': location,
                'protein': protein,
                'mut': mutation,
                'slope': slope,
                'f1': f1,
                'f2': f2,
                'f3': f3,
                'f4': f4,
                'w1': c1,
                'w2': c2,
                'w3': c3,
                'w4': c4,
                'p_value_with_mut':
                    compute_pvalue([c1, c2, c3, c4], week_sequence_counts),
                'p_value_without_mut':
                    compute_pvalue(
                        [tot_seq_w1 - c1, tot_seq_w2 - c2, tot_seq_w3 - c3, tot_seq_w4 - c4],
                        week_sequence_counts),
                'p_value_comp':
                    compute_pvalue(
                        [c1, c2, c3, c4],
                        [tot_seq_w1 - c1, tot_seq_w2 - c2, tot_seq_w3 - c3, tot_seq_w4 - c4]),
            })

        characterizing_muts = get_lineage_characterization([lineage])

        return {'rows': statistics, 'tot_seq': week_sequence_counts, 'characterizing_muts': characterizing_muts}
