"""

    API to perform lineage independent analysis
    Endpoints:
    ├── getStatistics: endpoint to perform a lineage independent analysis
    └── getLineagesStatistics: endpoint to obtain statistics about lineages for given protein, mutation, location and date

"""

from __future__ import print_function

import sqlite3
import time

from flask_restplus import Namespace, Resource

from .utils.path_manager import db_path
from .utils.utils import compute_weeks_from_date, produce_statistics

api = Namespace('lineage_independent', description='lineage_independent')

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


def extract_week_seq_counts(location, w, prot=None, mut=None):
    """
    Extract weekly sequence counts for the given location and weeks from the database
    Args:
        location:   String representing the location to be considered
        w:          Weeks to be considered
        prot:       If set, the counts consider only the sequences with a given protein
        mut:        If set, the counts consider only the sequences with a given mutation

    Returns: An array of sequence counts

    """
    # print("\t Extract number of sequences in the four weeks...", end="")
    # exec_start = time.time()
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    def extract_week_count(start, stop):
        if prot is not None and mut is not None:
            # count the seq collected for a given week and location having a given mutation
            query = f'''    SELECT sum(count)
                            FROM  aggr_aa_substitutions SB
                                JOIN locations LC ON SB.location_id = LC.location_id
                                JOIN proteins PR ON SB.protein_id = PR.protein_id
                            WHERE date > {start} AND date <= {stop} AND location = "{location}" 
                                AND mut='{mut}' AND protein='{prot}' 
                            GROUP BY date, SB.location_id;'''
        else:
            # count the seq collected for a given week and location
            query = f'''    SELECT sum(count)
                            FROM  aggr_sequences SQ
                                JOIN locations LC ON SQ.location_id = LC.location_id
                            WHERE date > {start} AND date <= {stop} AND location = "{location}" 
                            GROUP BY date, SQ.location_id;'''
        return sum([x[0] for x in cur.execute(query).fetchall()])

    tot_seq_w4 = extract_week_count(w['w4_begin'], w['w4_end'])
    tot_seq_w3 = extract_week_count(w['w3_begin'], w['w3_end'])
    tot_seq_w2 = extract_week_count(w['w2_begin'], w['w2_end'])
    tot_seq_w1 = extract_week_count(w['w1_begin'], w['w1_end'])
    con.close()
    # print(f'done in {time.time() - exec_start:.5f} seconds.')
    return [tot_seq_w1, tot_seq_w2, tot_seq_w3, tot_seq_w4]


def extract_mutation_data(location, w, min_sequences=0):
    """
    Extract weekly mutation data for the given location and weeks from the database
    Args:
        location:       String representing the location to be considered
        w:              Weeks to be considered
        min_sequences:  Minimum number of sequence

    Returns: An array describing the mutations for each week

    """
    # print("\t Extract mutation data for the four weeks ...", end="")
    # exec_start = time.time()
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    def extract_week_mutation(start, stop, is_target=False):
        having_clause = f"HAVING sum(count) >= {min_sequences}"
        query = f'''    SELECT protein, mut, sum(count) 
                        FROM aggr_aa_substitutions SB
                            JOIN proteins PR ON SB.protein_id = PR.protein_id
                            JOIN locations LC ON SB.location_id = LC.location_id
                        WHERE date > {start} AND date <= {stop} AND location = "{location}"
                        GROUP BY SB.protein_id, mut 
                        {having_clause if is_target else ""};'''
        return {p + '_' + m: c for p, m, c in cur.execute(query).fetchall()}

    muts_w4 = extract_week_mutation(w['w4_begin'], w['w4_end'], is_target=True)
    muts_w3 = extract_week_mutation(w['w3_begin'], w['w3_end'])
    muts_w2 = extract_week_mutation(w['w2_begin'], w['w2_end'])
    muts_w1 = extract_week_mutation(w['w1_begin'], w['w1_end'])
    con.close()
    # print(f'done in {time.time() - exec_start:.5f} seconds.')
    return [muts_w1, muts_w2, muts_w3, muts_w4]


def extract_lineages_data(location, prot, mut, w):
    """
    Extract lineages data for the given location, mutation and weeks from the database
    Args:
        location:   String representing the location to be considered
        prot:       String representing the protein to be considered
        mut:        String representing the mutation to be considered
        w:          Weeks to be considered

    Returns:

    """
    # print("\t Extract lineages data in the four weeks for mutation...", end="")
    # exec_start = time.time()
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    week_sequence_counts = extract_week_seq_counts(location, w, prot, mut)
    tot_seq_w1, tot_seq_w2, tot_seq_w3, tot_seq_w4 = week_sequence_counts

    def extract_all_lineages(start, stop):
        # get the lineages for the considered period, location, prot and mut
        query = f'''    SELECT DISTINCT SB.lineage_id, lineage
                        FROM aggr_aa_substitutions SB
                            JOIN lineages LN ON SB.lineage_id = LN.lineage_id
                            JOIN locations LC ON SB.location_id = LC.location_id
                            JOIN proteins PR ON SB.protein_id = PR.protein_id
                        WHERE date > {start} AND date <= {stop} AND location = "{location}" 
                            AND protein = '{prot}' AND mut = '{mut}'
                        ORDER BY lineage;'''
        return {k: v for k, v in cur.execute(query).fetchall()}

    def extract_week_info(lin_id, start, stop):
        query = f'''    SELECT sum(count) 
                        FROM aggr_aa_substitutions SB
                            JOIN locations LC ON SB.location_id = LC.location_id
                            JOIN proteins PR ON SB.protein_id = PR.protein_id
                        WHERE date > {start} AND date <= {stop} AND location = "{location}" 
                            AND lineage_id = '{lin_id}' AND protein = '{prot}' AND mut = '{mut}'
                        GROUP BY date, SB.location_id, SB.protein_id, mut, lineage_id;'''
        return sum([x[0] for x in cur.execute(query).fetchall()])

    lineages = extract_all_lineages(w['w1_begin'], w['w4_end'])
    lineages_data = []
    for lineage_id, lineage_name in lineages.items():
        lin_w4 = extract_week_info(lineage_id, w['w4_begin'], w['w4_end'])
        lin_w3 = extract_week_info(lineage_id, w['w3_begin'], w['w3_end'])
        lin_w2 = extract_week_info(lineage_id, w['w2_begin'], w['w2_end'])
        lin_w1 = extract_week_info(lineage_id, w['w1_begin'], w['w1_end'])
        lineages_data.append({
            'name': lineage_name,
            'f1': (lin_w1 / tot_seq_w1) * 100 if tot_seq_w1 > 0 else 0,
            'f2': (lin_w2 / tot_seq_w2) * 100 if tot_seq_w2 > 0 else 0,
            'f3': (lin_w3 / tot_seq_w3) * 100 if tot_seq_w3 > 0 else 0,
            'f4': (lin_w4 / tot_seq_w4) * 100 if tot_seq_w4 > 0 else 0,
            'w1': lin_w1,
            'w2': lin_w2,
            'w3': lin_w3,
            'w4': lin_w4
        })
    con.close()
    # print(f'done in {time.time() - exec_start:.5f} seconds.')
    return lineages_data


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""                               ENDPOINTS                             """""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


@api.route('/getStatistics')
class FieldList(Resource):
    @api.doc('get_statistics')
    def post(self):
        """
        Endpoint to perform a lineage independent analysis
        @return:    An object including the results and the support info
        """
        print("\t /getStatistics processing...", end="")
        exec_start = time.time()
        location = api.payload['location']
        date = api.payload['date']

        w = compute_weeks_from_date(date)

        week_sequence_counts = extract_week_seq_counts(location, w)

        min_sequences = int(week_sequence_counts[-1] * 0.005 + 1)
        mutation_data = extract_mutation_data(location, w, min_sequences)

        statistics = produce_statistics(location, week_sequence_counts, mutation_data)

        print(f'done in {time.time() - exec_start:.5f} seconds.')
        return {'rows': statistics, 'tot_seq': week_sequence_counts}


@api.route('/getLineagesStatistics')
class FieldList(Resource):
    @api.doc('get_lineages_statistics')
    def post(self):
        """
        Endpoint to obtain statistics about lineages for given protein, mutation, location and date
        @return:    An object including the results
        """
        print("\t /getLineagesStatistics processing...", end="")
        exec_start = time.time()
        location = api.payload['location']
        date = api.payload['date']
        prot = api.payload['prot']
        mut = api.payload['mut']

        w = compute_weeks_from_date(date)
        lineage_data = extract_lineages_data(location, prot, mut, w)

        print(f'done in {time.time() - exec_start:.5f} seconds.')
        return lineage_data
