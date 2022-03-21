"""
    API to retrieve daily sequences counts
    Endpoints:
    ├── getLineageBreakdown
    └── getSequenceInfo
"""

from __future__ import print_function

import sqlite3
import time

from flask_restplus import Namespace, Resource

from .utils.utils import compute_date_from_diff, compute_weeks_from_date

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


def extract_lineage_breakdown(granularity, location):
    """
    Extract from the database the lineage breakdown info for the selected params
    Args:
        granularity:    the granularity
        location:       the location

    Returns: an array of (day,data about the lineage breakdown) pairs

    """
    print("\t Extract lineage breakdown of sequences ...", end="")
    exec_start = time.time()
    con = sqlite3.connect(db_name)
    cur = con.cursor()

    def extract_dates():
        query = f'''    select distinct date
                        from timelocling
                        order by date;'''
        dates = cur.execute(query).fetchall()
        return [x[0] for x in dates]

    def extract_lineages_from_date(date):
        query = f'''    select lineage, sum(count)
                        from timelocling
                        where date='{date}'  and location='{location}' 
                        group by location, lineage, date
                        order by lineage;'''
        lin_bd = cur.execute(query).fetchall()
        return [{'name': lin, 'count': count} for lin, count in lin_bd]

    days = extract_dates()
    lineage_breakdown = []
    for day in days:
        lineage_breakdown.append({
            'date': day,
            'data': extract_lineages_from_date(day)
        })

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


def get_lineages_mutations(mutations, location, date):
    """
    Extract from the database the lineages' classification info for the selected mutations
    Args:
        mutations:       an array of protein_mutation elements

    Returns: an array of (lineage, mutations list) pairs

    """
    print("\t Extract lineage classification ...", end="")
    exec_start = time.time()
    con = sqlite3.connect(db_name)
    cur = con.cursor()

    w = compute_weeks_from_date(date)

    def extract_lineages_from_mut(mut):
        query = f'''    select distinct lineage
                        from mutsg
                        where mut = '{mut}' and location = '{location}' and 
                        date > {w['w1_begin']} and date <= {w['w4_end']}
                        order by lineage;'''
        mut_classes = cur.execute(query).fetchall()
        return [x[0] for x in mut_classes]

    classification = {}
    for m in mutations:
        for lineage in extract_lineages_from_mut(m):
            if lineage in classification.keys():
                classification[lineage].append(m)
            else:
                classification[lineage] = [m]

    con.close()
    print(f'done in {time.time() - exec_start:.5f} seconds.')
    return classification


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

        info = extract_lineage_breakdown(granularity, location)
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


@api.route('/getLineagesMutations')
class FieldList(Resource):
    @api.doc('get_lineages_mutations')
    def post(self):
        """
        Endpoint to get the lineages' classification for the mutations
        of a certain location and period
        @return:    A list of (lineage, mutation list) pairs
        """
        location = api.payload['location']
        date = api.payload['date']
        mutations = api.payload['mutations']

        return get_lineages_mutations(mutations, location, date)
