"""
    API to retrieve daily sequences counts
    Endpoints:
    └── getSequenceInfo
"""

from __future__ import print_function
import sqlite3
import time
from flask_restplus import Namespace, Resource
from .utils.utils import compute_date_from_diff

api = Namespace('explorer', description='explorer')
db_name = 'varianthunter.db'

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


def extract_seq_num(granularity, location, lineage):
    """
    Extract from the database the sequence count for the selected params
    Args:
        granularity:    the granularity
        location:       the location
        lineage:        the lineage

    Returns: an array of (date, seq_count) pairs

    """
    print("\t Extract number of sequences ...", end="")
    exec_start = time.time()
    con = sqlite3.connect(db_name)
    cur = con.cursor()

    def execute_query():
        if lineage is not None:
            query = f'''    select date,sum(count) 
                            from timelocling 
                            where location = '{location}' and lineage = '{lineage}'
                            group by date,location,lineage;'''
        else:
            query = f'''    select date,sum(count) 
                            from timelocling 
                            where location = '{location}' 
                            group by date,location;'''
        seqs = cur.execute(query).fetchall()
        return [{'date': x[0], 'seq_count': x[1]} for x in seqs]

    daily_sequence_counts = execute_query()
    con.close()
    print(f'done in {time.time() - exec_start:.5f} seconds.')
    return daily_sequence_counts


def extract_last_update():
    """
    Extract from the database the date of the last sequence

    Returns: tha date of the last update

    """
    print("> Extract last update date ...", end="")
    exec_start = time.time()
    con = sqlite3.connect(db_name)
    cur = con.cursor()

    query = f'''    select max(date) 
                    from timelocling;'''
    diff = cur.execute(query).fetchall()[0][0]

    con.close()
    print(f'done in {time.time() - exec_start:.5f} seconds.')
    return compute_date_from_diff(diff)


lastUpdate = extract_last_update()


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
        granularity = api.payload['granularity']
        location = api.payload['location']
        lineage = api.payload['lineage']

        info = extract_seq_num(granularity, location, lineage)
        return info


@api.route('/getLastUpdate')
class FieldList(Resource):
    @api.doc('get_last_update')
    def get(self):
        """
        Endpoint to get the date of the last update of the dataset
        @return:    The date of the last sequence collected
        """
        return lastUpdate
