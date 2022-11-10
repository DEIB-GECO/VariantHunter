"""

    API to retrieve daily sequences counts
    Endpoints:
    ├── getSequenceInfo: endpoint to get the sequence counts for each day
    ├── getLineagesBreakdown: endpoint to get the lineage breakdown info for each day
    ├── getLastUpdate: endpoint to get the date of the last update of the dataset
    └── getLineagesCharacteristics: endpoint to get the characterizing protein mutations of specified lineages

"""

from __future__ import print_function

import sqlite3
import time

from flask import request
from flask_restplus import Namespace, Resource

from .utils.path_manager import db_path
from .utils.utils import compute_date_from_diff, compute_diff_from_date

api = Namespace('explorer', description='explorer')

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


def extract_seq_num(location, lineage):
    """
    Extract from the database the sequence count for the selected params
    Args:
        location:       the location
        lineage:        the lineage

    Returns: an array of (date, seq_count) pairs

    """
    # print("\t Extract number of sequences ...", end="")
    # exec_start = time.time()
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    def execute_query():
        if lineage is not None:
            query = f'''    SELECT date,sum(count) 
                            FROM aggr_sequences SQ
                                JOIN locations LC ON SQ.location_id = LC.location_id
                                JOIN lineages LN ON SQ.lineage_id = LN.lineage_id
                            WHERE location = "{location}" AND lineage = '{lineage}'
                            GROUP BY date, SQ.location_id, SQ.lineage_id;'''
        else:
            query = f'''    SELECT date,sum(count) 
                            FROM aggr_sequences SQ
                                JOIN locations LC ON SQ.location_id = LC.location_id
                            WHERE location = "{location}"
                            GROUP BY date, SQ.location_id;'''
        seqs = cur.execute(query).fetchall()
        return [{'date': x[0], 'seq_count': x[1]} for x in seqs]

    daily_sequence_counts = execute_query()
    con.close()
    # print(f'done in {time.time() - exec_start:.5f} seconds.')
    return daily_sequence_counts


def extract_lineage_breakdown(location, period):
    """
    Extract from the database the lineage breakdown info for the selected params
    Args:
        location:       the location
        period:          the date range

    Returns: an array of (day,data about the lineage breakdown) pairs

    """
    # print("\t Extract lineage breakdown of sequences ...", end="")
    # exec_start = time.time()
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    def extract_lineages():
        query = f'''    SELECT DISTINCT SQ.lineage_id, lineage
                        FROM aggr_sequences SQ
                            JOIN lineages LN ON SQ.lineage_id = LN.lineage_id
                            JOIN locations LC ON SQ.location_id = LC.location_id
                        WHERE location="{location}" AND date>={period['begin']} AND date<={period['end']}
                        ORDER BY lineage;'''
        return {k: v for k, v in cur.execute(query).fetchall()}

    def extract_day_threshold(day):
        query = f'''    SELECT 0.10 * sum(count)
                        FROM aggr_sequences SQ
                            JOIN locations LC ON SQ.location_id = LC.location_id
                        WHERE location="{location}" AND date={day};'''
        day_threshold = cur.execute(query).fetchone()
        return day_threshold[0] if day_threshold[0] is not None else 0

    def extract_lineage_data(lin_id, day):
        query = f'''    SELECT sum(count)
                        FROM aggr_sequences SQ
                            JOIN locations LC ON SQ.location_id = LC.location_id
                        WHERE lineage_id='{lin_id}' AND location="{location}" and date={day}
                        GROUP BY date, lineage_id, SQ.location_id;'''
        day_count = cur.execute(query).fetchone()
        return day_count[0] if day_count is not None else 0

    lineages = extract_lineages()
    lineage_breakdown = {}
    for date in range(period['begin'], period['end'] + 1):
        threshold = extract_day_threshold(date)
        for lineage_id, lineage_name in lineages.items():
            seq_count = extract_lineage_data(lineage_id, date)
            key = lineage_name if seq_count > threshold else 'Others'

            # Lineage already in the dictionary?
            if key in lineage_breakdown.keys():
                # Do we need to accumulate in 'Others'?
                if key == 'Others' and date in lineage_breakdown['Others'].keys():
                    lineage_breakdown[key][date] += seq_count
                else:
                    lineage_breakdown[key][date] = seq_count
            else:
                lineage_breakdown[key] = {date: seq_count}

    con.close()
    # print(f'done in {time.time() - exec_start:.5f} seconds.')
    return lineage_breakdown


def extract_last_update():
    """
    Extract from the database the date of the last sequence

    Returns: tha date of the last update

    """
    # print("> Extract last update date ...", end="")
    # exec_start = time.time()
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    query = f'''    SELECT max(date) 
                    FROM aggr_sequences;'''
    diff = cur.execute(query).fetchall()[0][0]

    con.close()
    # print(f'done in {time.time() - exec_start:.5f} seconds.')
    return compute_date_from_diff(diff) if diff is not None else None


last_update = extract_last_update()  # At server startup, fetch last update


def get_lineage_characterization(lineages):
    """
    Extract from the database the characterizing mutations of specified lineages
    Args:
        lineages:    array of lineages to be considered

    Returns: an array of characterizing mutations

    """
    # print("\t Extract lineage characterization  ...", end="")
    # exec_start = time.time()
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    def extract_muts_from_lineage():
        query = f'''    SELECT DISTINCT protein, mut
                        FROM lineages_characteristics LC
                            JOIN lineages LN ON LC.lineage_id = LN.lineage_id
                            JOIN proteins PR ON LC.protein_id = PR.protein_id
                        WHERE lineage in (%s) ''' % ("?," * len(lineages))[:-1] + '''
                        ORDER BY protein, mut;'''
        return [x[0] + '_' + x[1] for x in cur.execute(query, lineages).fetchall()]

    characterizing_muts = extract_muts_from_lineage()

    con.close()
    # print(f'done in {time.time() - exec_start:.5f} seconds.')
    return characterizing_muts


def extract_characterized_lineages(prot, mut):
    """
    Given a protein mutation pair it retrieves the lineages characterized by that pair
    Args:
        prot:   The name of the protein of interest
        mut:    The mutation of interest

    Returns:    List of characterized lineage names

    """
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    query = ''' SELECT L.lineage
                FROM lineages_characteristics AS LC
                    JOIN proteins AS P  ON P.protein_id=LC.protein_id
                    JOIN lineages AS L ON L.lineage_id=LC.lineage_id
                WHERE P.protein=:prot AND LC.mut=:mut;'''
    lineages = [lineage for [lineage] in cur.execute(query, {'prot': prot, 'mut': mut}).fetchall()]

    con.close()
    return lineages


def extract_mutation_history(prot, mut):
    """
    Given a protein,mutation pair it computes the percentage at which that pair appeared in each lineage, if >0.
    Args:
        prot:   The name of the protein of interest
        mut:    The mutation of interest

    Returns:    A dictionary of lineages storing the percentage of appearance in each lineage, in all times.

    """
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    query = ''' SELECT L.lineage, SUM(AA.count)
                FROM aggr_aa_substitutions AS AA
                    JOIN proteins AS P  ON P.protein_id = AA.protein_id
                    JOIN lineages AS L ON AA.lineage_id = L.lineage_id
                WHERE P.protein=:prot AND AA.mut=:mut
                GROUP BY L.lineage
                HAVING SUM(AA.count)>0
                ORDER BY SUM(AA.count) DESC ;'''

    history = {}
    total = 0
    for lineage, count in cur.execute(query, {'prot': prot, 'mut': mut}).fetchall():
        total += count
        history[lineage] = {'abs' : count}

    for lineage in history:
        history[lineage]['percentage'] = 100 * history[lineage]['abs'] / total

    con.close()
    return history


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""                             ENDPOINTS                               """""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


@api.route('/getSequenceInfo')
class FieldList(Resource):
    @api.doc('get_sequence_info')
    def get(self):
        """
        Endpoint to get the sequence counts for each day
        @return:    An array of (date,seq_count) pairs
        """
        print("\t /getSequenceInfo processing...", end="")
        exec_start = time.time()
        args = request.args
        location = args.get('location')
        lineage = args.get('lineage')

        info = extract_seq_num(location, lineage)
        print(f'done in {time.time() - exec_start:.5f} seconds.')
        return info


@api.route('/getLineagesBreakdown')
class FieldList(Resource):
    @api.doc('get_lineage_breakdown')
    def get(self):
        """
        Endpoint to get the lineage breakdown info for each day
        @return:    An array of describing the breakdown
        """
        print("\t /getLineagesBreakdown processing...", end="")
        exec_start = time.time()
        args = request.args
        location = args.get('location')
        period = {
            'begin': compute_diff_from_date(args.get('begin')) + 1,
            'end': compute_diff_from_date(args.get('end')),
        }

        info = extract_lineage_breakdown(location, period)
        print(f'done in {time.time() - exec_start:.5f} seconds.')
        return info


@api.route('/getLastUpdate')
class FieldList(Resource):
    @api.doc('get_last_update')
    def get(self):
        """
        Endpoint to get the date of the last update of the dataset
        @return:    The date of the last sequence collected
        """
        print("\t /getLastUpdate processing...done.")
        return last_update


@api.route('/getLineagesCharacteristics')
class FieldList(Resource):
    @api.doc('get_lineages_characteristics')
    def get(self):
        """
        Endpoint to get the characterizing protein mutations of specified lineages
        @return:    A list of characterizing mutations
        """
        print("\t /getLineagesCharacteristics processing...", end="")
        exec_start = time.time()
        args = request.args
        lineages = args.getlist('lineages')
        print(lineages)

        characterization = get_lineage_characterization(lineages)
        print(f'done in {time.time() - exec_start:.5f} seconds.')
        return characterization


@api.route('/getMutationHistory')
class FieldList(Resource):
    @api.doc('get_mutation_history')
    def get(self):
        """
        Endpoint to obtain statistics about history of a given mutation
        @return:    An object including the results
        """
        print("\t /getMutationHistory processing...", end="")
        exec_start = time.time()
        args = request.args
        protein = args.get('protein')
        mut = args.get('mut')

        mutation_history = extract_mutation_history(prot=protein, mut=mut)
        characterized_lineages = extract_characterized_lineages(prot=protein, mut=mut)

        print(f'done in {time.time() - exec_start:.5f} seconds.')
        return {'history': mutation_history, 'characterized_lineages':characterized_lineages}
