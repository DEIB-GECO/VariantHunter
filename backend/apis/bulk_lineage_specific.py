"""

    API to perform bulk lineage specific analysis
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
from .utils.path_manager import db_path
from .utils.utils import start_date, compute_weeks_from_date, produce_statistics

api = Namespace('lineage_specific', description='lineage_specific')

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


def get_all_lineages():
    """
    Extract all the possible values for the lineage from the database
    Returns: An array of lineages

    """
    # print("> Extract all lineages ...", end="")
    # exec_start = time.time()
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    query = "SELECT lineage FROM lineages ORDER BY lineage;"
    extracted_lineages = [x[0] for x in cur.execute(query).fetchall()]
    con.close()

    # print(f"done in {time.time() - exec_start:.5f} seconds.")
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
    # print("\t Extract lineages data given location and date...", end="")
    stop = (datetime.strptime(date, "%Y-%m-%d") - start_date).days
    start = stop - 5

    # exec_start = time.time()
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    query = f'''    SELECT DISTINCT lineage 
                    FROM aggr_sequences SQ
                        JOIN lineages LN ON SQ.lineage_id = LN.lineage_id
                        JOIN locations LC ON SQ.location_id = LC.location_id
                    WHERE location = "{location}" AND date > {start} AND date <= {stop}
                    ORDER BY lineage;'''
    extracted_lineages = [x[0] for x in cur.execute(query).fetchall()]
    con.close()

    # print(f"done in {time.time() - exec_start:.5f} seconds.")
    return extracted_lineages


def get_lineages_from_loc(location):
    """
    Extract the lineages for a given location from the database
    Args:
        location:   String representing the location to be considered

    Returns: An array of lineages

    """
    # print("\t Extract lineages data given location...", end="")
    # exec_start = time.time()
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    query = f'''    SELECT DISTINCT lineage 
                    FROM aggr_sequences SQ
                        JOIN lineages LN ON SQ.lineage_id = LN.lineage_id
                        JOIN locations LC ON SQ.location_id = LC.location_id
                    WHERE location = "{location}"
                    ORDER BY lineage;'''
    extracted_lineages = [x[0] for x in cur.execute(query).fetchall()]
    con.close()

    # print(f"done in {time.time() - exec_start:.5f} seconds.")
    return extracted_lineages


def get_lineages_from_date(date):
    """
    Extract the lineages for a given week from the database
    Args:
        date:       String representing the (week ending) date to be considered.

    Returns: An array of lineages

    """
    # print("\t Extract lineages data given date...", end="")
    stop = (datetime.strptime(date, "%Y-%m-%d") - start_date).days
    start = stop - 5

    exec_start = time.time()
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    query = f'''    SELECT DISTINCT lineage 
                    FROM aggr_sequences SQ
                        JOIN lineages LN ON SQ.lineage_id = LN.lineage_id
                    WHERE date > {start} and date <= {stop}
                    ORDER BY lineage;'''
    extracted_lineages = [x[0] for x in cur.execute(query).fetchall()]
    con.close()

    # print(f"done in {time.time() - exec_start:.5f} seconds.")
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
    # print("\t Extract number of sequences in the four weeks...", end="")
    # exec_start = time.time()
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    def extract_week_count(start, stop):
        query = f'''    SELECT sum(count) 
                        FROM aggr_sequences SQ
                            JOIN locations LC on SQ.location_id = LC.location_id
                            JOIN lineages LN on SQ.lineage_id = LN.lineage_id
                        WHERE date > {start} and date <= {stop} and location = "{location}" and lineage = '{lineage}' 
                        GROUP BY date, SQ.location_id, SQ.lineage_id;'''
        return sum([x[0] for x in cur.execute(query).fetchall()])

    tot_seq_w6 = extract_week_count(w['w6_begin'], w['w6_end'])
    tot_seq_w5 = extract_week_count(w['w5_begin'], w['w5_end'])
    tot_seq_w4 = extract_week_count(w['w4_begin'], w['w4_end'])
    tot_seq_w3 = extract_week_count(w['w3_begin'], w['w3_end'])
    tot_seq_w2 = extract_week_count(w['w2_begin'], w['w2_end'])
    tot_seq_w1 = extract_week_count(w['w1_begin'], w['w1_end'])
    con.close()
    # print(f'done in {time.time() - exec_start:.5f} seconds.')
    return [tot_seq_w1, tot_seq_w2, tot_seq_w3, tot_seq_w4, tot_seq_w5, tot_seq_w6]


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
    # print("\t Extract mutation data for the four weeks...", end="")
    # exec_start = time.time()
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    def extract_week_mutation(start, stop, is_target=False):
        having_clause = f" HAVING sum(count) >= {min_sequences} "
        query = f'''    SELECT protein, mut, sum(count) 
                        FROM aggr_aa_substitutions SB
                            JOIN proteins PR ON SB.protein_id = PR.protein_id
                            JOIN locations LC ON SB.location_id = LC.location_id
                            JOIN lineages LN ON SB.lineage_id = LN.lineage_id
                        WHERE date > {start} AND date <= {stop} AND location = "{location}" 
                            AND lineage = '{lineage}'
                        GROUP BY SB.protein_id, mut 
                        {having_clause if is_target else ""};'''
        return {p + '_' + m: c for p, m, c in cur.execute(query).fetchall()}

    muts_w6 = extract_week_mutation(w['w6_begin'], w['w6_end'], is_target=True)
    muts_w5 = extract_week_mutation(w['w5_begin'], w['w5_end'])
    muts_w4 = extract_week_mutation(w['w4_begin'], w['w4_end'])
    muts_w3 = extract_week_mutation(w['w3_begin'], w['w3_end'])
    muts_w2 = extract_week_mutation(w['w2_begin'], w['w2_end'])
    muts_w1 = extract_week_mutation(w['w1_begin'], w['w1_end'])
    con.close()
    # print(f'done in {time.time() - exec_start:.5f} seconds.')
    return [muts_w1, muts_w2, muts_w3, muts_w4, muts_w5, muts_w6]


def extract_specific_mutation_data(location, lineage, protein_mut, w):
    """
        Extract weekly mutation data for the given location, lineage and weeks from the database
        Args:
            location:       String representing the location to be considered
            lineage:        String representing the lineage to be considered
            protein_mut:            String representing the mutation
            w:              The weeks

        Returns: Data of the mutation

        """
    # print("\t Extract mutation data for the four weeks...", end="")
    # exec_start = time.time()
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    protein,mut=protein_mut.split("_")

    def extract_week_mutation(start, stop):
        query = f'''    SELECT protein, mut, sum(count) 
                        FROM aggr_aa_substitutions SB
                            JOIN proteins PR ON SB.protein_id = PR.protein_id
                            JOIN locations LC ON SB.location_id = LC.location_id
                            JOIN lineages LN ON SB.lineage_id = LN.lineage_id
                        WHERE date > {start} AND date <= {stop} AND location = "{location}" 
                            AND lineage = '{lineage}' AND protein="{protein}" AND mut="{mut}"
                        GROUP BY SB.protein_id, mut;'''
        return {p + '_' + m: c for p, m, c in cur.execute(query).fetchall()}

    muts_w6 = extract_week_mutation(w['w6_begin'], w['w6_end'])
    muts_w5 = extract_week_mutation(w['w5_begin'], w['w5_end'])
    con.close()
    # print(f'done in {time.time() - exec_start:.5f} seconds.')
    return [muts_w5, muts_w6]


def produce_bulk_statistics(location, week_sequence_counts, mutation_data):
    """
    Process the statistics values by properly formatting them
    Args:
        location:               Location name
        week_sequence_counts:   Week sequences data
        mutation_data:          Mutation data

    Returns:    An array of statistics

    """
    statistics = []
    tot_seq_w1, tot_seq_w2, tot_seq_w3, tot_seq_w4, tot_seq_w5, tot_seq_w6 = week_sequence_counts
    mut_w1, mut_w2, mut_w3, mut_w4, mut_w5, mut_w6 = mutation_data

    for mut, c6 in mut_w6.items():
        c1 = mut_w1.get(mut, 0)
        c2 = mut_w2.get(mut, 0)
        c3 = mut_w3.get(mut, 0)
        c4 = mut_w4.get(mut, 0)
        c5 = mut_w5.get(mut, 0)
        f1 = (c1 / tot_seq_w1) * 100 if tot_seq_w1 > 0 else 0
        f2 = (c2 / tot_seq_w2) * 100 if tot_seq_w2 > 0 else 0
        f3 = (c3 / tot_seq_w3) * 100 if tot_seq_w3 > 0 else 0
        f4 = (c4 / tot_seq_w4) * 100 if tot_seq_w4 > 0 else 0
        f5 = (c5 / tot_seq_w5) * 100 if tot_seq_w5 > 0 else 0
        # f6 = (c6 / tot_seq_w6) * 100 if tot_seq_w6 > 0 else 0

        statistics.append({
            'location': location,
            'protein_mut': mut,
            'f1': f1,
            'f2': f2,
            'f3': f3,
            'f4': f4,
            'f5': f5,
            'w6': c6,
            'tot_seq_w6': tot_seq_w6
        })

    return statistics


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
        print("\t /getAllLineages processing...done.")
        return all_lineages


@api.route('/getLineages')
class FieldList(Resource):
    @api.doc('get_lineages')
    def post(self):
        """
        Endpoint to obtain the lineages for a given location and week (if specified)
        @return:    An array of lineages
        """
        print("\t /getLineages processing...", end="")
        exec_start = time.time()
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

        print(f'done in {time.time() - exec_start:.5f} seconds.')
        return lineages


@api.route('/getStatistics')
class FieldList(Resource):
    @api.doc('get_statistics')
    def post(self):
        """
        Endpoint to perform a lineage specific analysis
        @return:    An object including the results and the support info
        """
        print("\t /getStatistics processing...", end="")
        exec_start = time.time()
        location = api.payload['location']
        lineage = api.payload['lineage']
        date = api.payload['date']

        w = compute_weeks_from_date(date)

        week_sequence_counts = extract_week_seq_counts(location, lineage, w)

        min_sequences = int(week_sequence_counts[-1] * 0.005 + 1)
        mutation_data = extract_mutation_data(location, lineage, w, min_sequences)

        statistics = produce_statistics(location, week_sequence_counts, mutation_data)
        characterizing_muts = get_lineage_characterization([lineage])

        print(f'done in {time.time() - exec_start:.5f} seconds.')
        return {'rows': statistics, 'tot_seq': week_sequence_counts, 'characterizing_muts': characterizing_muts}
