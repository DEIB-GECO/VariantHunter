"""
    API to retrieve daily sequences counts
    Endpoints:
    ├── getLineagesMutations
    ├── getLineageBreakdown
    └── getSequenceInfo
"""

from __future__ import print_function

import sqlite3
import time

from flask_restplus import Namespace, Resource

from .utils.utils import compute_date_from_diff, compute_weeks_from_date, compute_diff_from_date

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


def extract_lineage_breakdown(granularity, location, period):
    """
    Extract from the database the lineage breakdown info for the selected params
    Args:
        granularity:    the granularity
        location:       the location
        period:          the date range

    Returns: an array of (day,data about the lineage breakdown) pairs

    """
    print("\t Extract lineage breakdown of sequences ...", end="")
    exec_start = time.time()
    con = sqlite3.connect(db_name)
    cur = con.cursor()

    def extract_lineages():
        query = f'''    select distinct lineage
                        from timelocling
                        where location='{location}' and date>={period['begin']} and date<={period['end']}
                        order by lineage;'''
        lineages_list = cur.execute(query).fetchall()
        return [x[0] for x in lineages_list]

    def extract_day_threshold(day):
        query = f'''    select 0.10 * sum(count)
                        from timelocling as t2
                        where location='{location}' and date={day};'''
        day_threshold = cur.execute(query).fetchone()
        return day_threshold[0] if day_threshold[0] is not None else 0

    def extract_lineage_data(lin, day):
        query = f'''    select sum(count)
                        from timelocling
                        where lineage='{lin}' and location='{location}' and date={day}
                        group by lineage, location, date;'''
        day_count = cur.execute(query).fetchone()
        return day_count[0] if day_count is not None else 0

    lineages = extract_lineages()
    lineage_breakdown = {}
    for date in range(period['begin'],period['end']+1):
        threshold = extract_day_threshold(date)
        for lineage in lineages:
            seq_count = extract_lineage_data(lineage,date)
            key = lineage if seq_count > threshold else 'Others'

            # Lineage already in the dictionary?
            if key in lineage_breakdown.keys():
                # Do we need to accumulate in 'Others'?
                if key == 'Others' and date in lineage_breakdown['Others'].keys():
                    lineage_breakdown[key][date] += seq_count
                else:
                    lineage_breakdown[key][date] = seq_count
            else:
                lineage_breakdown[key] = { date : seq_count}

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
    con = sqlite3.connect(db_name)
    cur = con.cursor()

    query = f'''    select max(date) 
                    from timelocling;'''
    diff = cur.execute(query).fetchall()[0][0]

    con.close()
    print(f'done in {time.time() - exec_start:.5f} seconds.')
    return compute_date_from_diff(diff)


lastUpdate = extract_last_update()


def get_lineage_characterization(lineages):
    """
    Extract from the database the characterizing mutations of specified lineages
    Args:
        lineages:    array of lineages to be considered

    Returns: an array of characterizing mutations

    """
    print("\t Extract lineage characterization  ...", end="")
    exec_start = time.time()
    con = sqlite3.connect(db_name)
    cur = con.cursor()

    def extract_muts_from_lineage():
        query = f'''    select distinct mut
                        from lineages_characterization
                        where lineage in (%s) ''' % ("?," * len(lineages))[:-1] + '''
                        order by mut;'''
        muts = cur.execute(query,lineages).fetchall()
        return [x[0] for x in muts]

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
        granularity = api.payload['granularity']
        location = api.payload['location']
        lineage = api.payload['lineage']

        info = extract_seq_num(granularity, location, lineage)
        return info


@api.route('/getLineageBreakdown')
class FieldList(Resource):
    @api.doc('get_lineage_breakdown')
    def post(self):
        """
        Endpoint to get the lineage breakdown info for each day
        @return:    An array of describing the breakdown
        """
        granularity = api.payload['granularity']
        location = api.payload['location']
        range = {
            'begin': compute_diff_from_date(api.payload['range'][0])+1,
            'end': compute_diff_from_date(api.payload['range'][1]),
        }

        info = extract_lineage_breakdown(granularity, location, range)
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


@api.route('/getLineagesCharacterization')
class FieldList(Resource):
    @api.doc('get_lineages_characterization')
    def post(self):
        """
        Endpoint to get the characterization of specified lineages
        @return:    A list of characterizing mutations
        """
        lineages = api.payload['lineages']

        return get_lineage_characterization(lineages)
