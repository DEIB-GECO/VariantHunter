"""

    API to perform lineage specific analysis
    Endpoints:
    ├── getAllLineages: endpoint to obtain all the possible lineages
    ├── getLineages: endpoint to obtain the lineages for a given location and week (if specified)
    └── getStatistics: endpoint to perform a lineage specific analysis

"""

from __future__ import print_function

import sqlite3
import time
from datetime import datetime

from flask_restplus import Namespace, Resource

from .explorer import get_lineage_characterization
from .utils.utils import start_date, compute_weeks_from_date, produce_statistics

api = Namespace('lineage_specific', description='lineage_specific')
db_name = 'db/varianthunter.db'

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

    query = "SELECT lineage FROM lineages ORDER BY lineage;"
    extracted_lineages = [x[0] for x in cur.execute(query).fetchall()]
    con.close()

    print(f"done in {time.time() - exec_start:.5f} seconds.")
    return extracted_lineages


all_lineages = get_all_lineages()  # At server startup, fetch all the lineages


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
    start = stop - 7

    exec_start = time.time()
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    query = f'''    SELECT DISTINCT lineage 
                    FROM aggr_sequences SQ
                        JOIN lineages LN ON SQ.lineage_id = LN.lineage_id
                        JOIN locations LC ON SQ.location_id = LC.location_id
                    WHERE location = '{location}' AND date > {start} AND date <= {stop};'''
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

    query = f'''    SELECT DISTINCT lineage 
                    FROM aggr_sequences SQ
                        JOIN lineages LN ON SQ.lineage_id = LN.lineage_id
                        JOIN locations LC ON SQ.location_id = LC.location_id
                    WHERE location = '{location}';'''
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
    start = stop - 7

    exec_start = time.time()
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    query = f'''    SELECT DISTINCT lineage 
                    FROM aggr_sequences SQ
                        JOIN lineages LN ON SQ.lineage_id = LN.lineage_id
                    WHERE date > {start} and date <= {stop};'''
    extracted_lineages = [x[0] for x in cur.execute(query).fetchall()]
    con.close()

    print(f"done in {time.time() - exec_start:.5f} seconds.")
    return extracted_lineages


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
        query = f'''    SELECT sum(count) 
                        FROM aggr_sequences SQ
                            JOIN locations LC on SQ.location_id = LC.location_id
                            JOIN lineages LN on SQ.lineage_id = LN.lineage_id
                        WHERE date > {start} and date <= {stop} and location = '{location}' and lineage = '{lineage}' 
                        GROUP BY date, SQ.location_id, SQ.lineage_id;'''
        return sum([x[0] for x in cur.execute(query).fetchall()])

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
        having_clause = f" HAVING sum(count) >= {min_sequences} "
        query = f'''    SELECT protein, mut, sum(count) 
                        FROM aggr_aa_substitutions SB
                            JOIN proteins PR ON SB.protein_id = PR.protein_id
                            JOIN locations LC ON SB.location_id = LC.location_id
                            JOIN lineages LN ON SB.lineage_id = LN.lineage_id
                        WHERE date > {start} AND date <= {stop} AND location = '{location}' 
                            AND lineage = '{lineage}'
                        GROUP BY SB.protein_id, mut 
                        {having_clause if is_target else ""};'''
        return {p + '_' + m: c for p, m, c in cur.execute(query).fetchall()}

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
        return all_lineages


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
            lineages = all_lineages
        elif date is None:
            lineages = get_lineages_from_loc(location)
        elif location is None:
            lineages = get_lineages_from_date(date)
        else:
            lineages = get_lineages_from_loc_date(location, date)
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

        min_sequences = int(week_sequence_counts[-1] * 0.005 + 1)
        mutation_data = extract_mutation_data(location, lineage, w, min_sequences)

        statistics = produce_statistics(location, week_sequence_counts, mutation_data)
        characterizing_muts = get_lineage_characterization([lineage])

        return {'rows': statistics, 'tot_seq': week_sequence_counts, 'characterizing_muts': characterizing_muts}
