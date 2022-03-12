"""
    API to retrieve daily sequences counts
    Endpoints:
    └── getSequenceInfo
"""

from __future__ import print_function
import sqlite3
import time
from flask_restplus import Namespace, Resource

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
    print("Extract number of sequences ...", end="")
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
