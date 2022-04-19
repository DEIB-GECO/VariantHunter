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
    print("\t Extract number of sequences ...", end="")
    exec_start = time.time()
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    def execute_query():
        if lineage is not None:
            query = f'''    SELECT date,sum(count) 
                            FROM aggr_sequences SQ
                                JOIN locations LC ON SQ.location_id = LC.location_id
                                JOIN lineages LN ON SQ.lineage_id = LN.lineage_id
                            WHERE location = '{location}' AND lineage = '{lineage}'
                            GROUP BY date, SQ.location_id, SQ.lineage_id;'''
        else:
            query = f'''    SELECT date,sum(count) 
                            FROM aggr_sequences SQ
                                JOIN locations LC ON SQ.location_id = LC.location_id
                            WHERE location = '{location}'
                            GROUP BY date, SQ.location_id;'''
        seqs = cur.execute(query).fetchall()
        return [{'date': x[0], 'seq_count': x[1]} for x in seqs]

    daily_sequence_counts = execute_query()
    con.close()
    print(f'done in {time.time() - exec_start:.5f} seconds.')
    return daily_sequence_counts


def extract_lineage_breakdown(location, period):
    """
    Extract from the database the lineage breakdown info for the selected params
    Args:
        location:       the location
        period:          the date range

    Returns: an array of (day,data about the lineage breakdown) pairs

    """
    print("\t Extract lineage breakdown of sequences ...", end="")
    exec_start = time.time()
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    def extract_lineages():
        query = f'''    SELECT DISTINCT SQ.lineage_id, lineage
                        FROM aggr_sequences SQ
                            JOIN lineages LN ON SQ.lineage_id = LN.lineage_id
                            JOIN locations LC ON SQ.location_id = LC.location_id
                        WHERE location='{location}' AND date>={period['begin']} AND date<={period['end']}
                        ORDER BY lineage;'''
        return {k: v for k, v in cur.execute(query).fetchall()}

    def extract_day_threshold(day):
        query = f'''    SELECT 0.10 * sum(count)
                        FROM aggr_sequences SQ
                            JOIN locations LC ON SQ.location_id = LC.location_id
                        WHERE location='{location}' AND date={day};'''
        day_threshold = cur.execute(query).fetchone()
        return day_threshold[0] if day_threshold[0] is not None else 0

    def extract_lineage_data(lin_id, day):
        query = f'''    SELECT sum(count)
                        FROM aggr_sequences SQ
                            JOIN locations LC ON SQ.location_id = LC.location_id
                        WHERE lineage_id='{lin_id}' AND location='{location}' and date={day}
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
    print(f'done in {time.time() - exec_start:.5f} seconds.')
    return lineage_breakdown


def extract_last_update():
    """
    Extract from the database the date of the last sequence

    Returns: tha date of the last update

    """
    print("> Extract last update date ...", end="")
    exec_start = time.time()
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    query = f'''    SELECT max(date) 
                    FROM aggr_sequences;'''
    diff = cur.execute(query).fetchall()[0][0]

    con.close()
    print(f'done in {time.time() - exec_start:.5f} seconds.')
    return compute_date_from_diff(diff) if diff is not None else None


last_update = extract_last_update()  # At server startup, fetch last update


def get_lineage_characterization(lineages):
    """
    Extract from the database the characterizing mutations of specified lineages
    Args:
        lineages:    array of lineages to be considered

    Returns: an array of characterizing mutations

    """
    print("\t Extract lineage characterization  ...", end="")
    exec_start = time.time()
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
    print(f'done in {time.time() - exec_start:.5f} seconds.')
    return characterizing_muts


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""                             ENDPOINTS                               """""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


@api.route('/getSequenceInfo')
class FieldList(Resource):
    @api.doc('get_sequence_info')
    def post(self):
        """
        Endpoint to get the sequence counts for each day
        @return:    An array of (date,seq_count) pairs
        """
        location = api.payload['location']
        lineage = api.payload['lineage']

        info = extract_seq_num(location, lineage)
        return info


@api.route('/getLineagesBreakdown')
class FieldList(Resource):
    @api.doc('get_lineage_breakdown')
    def post(self):
        """
        Endpoint to get the lineage breakdown info for each day
        @return:    An array of describing the breakdown
        """
        location = api.payload['location']
        period = {
            'begin': compute_diff_from_date(api.payload['range'][0]) + 1,
            'end': compute_diff_from_date(api.payload['range'][1]),
        }

        info = extract_lineage_breakdown(location, period)
        return info


@api.route('/getLastUpdate')
class FieldList(Resource):
    @api.doc('get_last_update')
    def get(self):
        """
        Endpoint to get the date of the last update of the dataset
        @return:    The date of the last sequence collected
        """
        return last_update


@api.route('/getLineagesCharacteristics')
class FieldList(Resource):
    @api.doc('get_lineages_characteristics')
    def post(self):
        """
        Endpoint to get the characterizing protein mutations of specified lineages
        @return:    A list of characterizing mutations
        """
        lineages = api.payload['lineages']

        return get_lineage_characterization(lineages)
