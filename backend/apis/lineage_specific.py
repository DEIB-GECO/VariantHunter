"""
    API to perform lineage dependent analysis

    Endpoints:
    ├── getGeoLineages
    ├── getAllLineage
    └── getStatistics
"""

from __future__ import print_function

import sqlite3
import time
from datetime import datetime
import numpy as np
import scipy.stats
from flask_restplus import Namespace, Resource

api = Namespace('lineage_specific', description='lineage_specific')
sqlite_db_name = 'varianthunter.db'
start_date = datetime.strptime("2020-01-01", "%Y-%m-%d")


##############################################################################################################

all_lineage_dict = {}


def get_all_lineage():
    print("Start lineage request...", end="")
    startx = time.time()
    con = sqlite3.connect(sqlite_db_name)
    cur = con.cursor()
    array_results = [x[0] for x in
                     cur.execute("select * from lineage_table where lineage is not null;").fetchall()]

    array_results.sort()
    all_lineage_dict['all_lineage'] = array_results
    con.close()
    print(f"...done in {time.time() - startx:.5f} seconds.")


def get_geo_lineages(geo, date):
    stop = (datetime.strptime(date, "%Y-%m-%d") - start_date).days
    start = stop - 7
    con = sqlite3.connect(sqlite_db_name)
    cur = con.cursor()
    cur.execute(f'''select distinct lineage 
                    from timelocling 
                    where location = '{geo}' and date > {start} and date <= {stop}
        ''')
    return [x[0] for x in cur.fetchall()]


get_all_lineage()


def compute_pvalue(freq1, freq2):
    try:
        return scipy.stats.chi2_contingency([freq1, freq2])[1]
    except:
        return "NaN"

##############################################################################################################

def extract_mutation_data(location, lineage, w1_begin, w1_end, w2_begin, w2_end, w3_begin, w3_end, w4_begin, w4_end, min_sequences = 0):
    print("Extract mutation data for the four weeks...", end="")
    startex = time.time()

    con = sqlite3.connect(sqlite_db_name)
    cur = con.cursor()

    def execute_query(start, stop, is_target = False):
        having_clause = f"having sum(count) >= {min_sequences}"
        cur.execute(f'''select mut, sum(count) from mutsg 
                        where date > {start} and date <= {stop} and location = '{location}' and lineage = '{lineage}' 
                        group by mut 
                        {having_clause if is_target else ""};''')
        muts = cur.fetchall()
        return {k: v for k, v in muts}

    muts_w4 = execute_query(w4_begin, w4_end, is_target=True)
    muts_w3 = execute_query(w3_begin, w3_end)
    muts_w2 = execute_query(w2_begin, w2_end)
    muts_w1 = execute_query(w1_begin, w1_end)
    con.close()
    week_mut_data = [muts_w1, muts_w2, muts_w3, muts_w4]
    print(f'done in {time.time() - startex:.5f} seconds.')
    return week_mut_data


def extract_cumulative_data(location, lineage, w1_begin, w1_end, w2_begin, w2_end, w3_begin, w3_end, w4_begin, w4_end):
    print("Extract number of sequences in the four weeks...", end="")
    startex = time.time()
    con = sqlite3.connect(sqlite_db_name)
    cur = con.cursor()

    def execute_query(start, stop):
        cur.execute(f'''select date,location,sum(count) 
                        from timelocling 
                        where date > {start} and date <= {stop} and location = '{location}' and lineage = '{lineage}' 
                        group by date,location,lineage;''')
        seqs = cur.fetchall()
        return sum([x[2] for x in seqs])

    tot_seq_w4 = execute_query(w4_begin, w4_end)
    tot_seq_w3 = execute_query(w3_begin, w3_end)
    tot_seq_w2 = execute_query(w2_begin, w2_end)
    tot_seq_w1 = execute_query(w1_begin, w1_end)
    con.close()
    week_sequence_counts = [tot_seq_w1, tot_seq_w2, tot_seq_w3, tot_seq_w4]
    print(f'done in {time.time() - startex:.5f} seconds.')
    return week_sequence_counts


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""                             ENDPOINTS                               """""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


@api.route('/getGeoLineages')
class FieldList(Resource):
    @api.doc('get_geo_lineages')
    def post(self):
        return get_geo_lineages(api.payload['geo'], api.payload['date'])


@api.route('/getAllLineage')
class FieldList(Resource):
    @api.doc('get_all_lineage')
    def get(self):
        all_lineage = all_lineage_dict['all_lineage']
        return all_lineage


@api.route('/getStatistics')
class FieldList(Resource):
    @api.doc('get_statistics')
    def post(self):
        payload = api.payload
        location = payload['value']
        lineage = payload['lineage']
        date = payload['date']

        w4_end = (datetime.strptime(date, "%Y-%m-%d") - start_date).days
        w4_begin = w4_end - 7
        w3_end = w4_begin - 1
        w3_begin = w3_end - 7
        w2_end = w3_begin - 1
        w2_begin = w2_end - 7
        w1_end = w2_begin - 1
        w1_begin = w1_end - 7

        week_sequence_counts = extract_cumulative_data(location, lineage,
                                                       w1_begin, w1_end,
                                                       w2_begin, w2_end,
                                                       w3_begin, w3_end,
                                                       w4_begin, w4_end)

        mutation_data = extract_mutation_data(location, lineage,
                                              w1_begin, w1_end,
                                              w2_begin, w2_end,
                                              w3_begin, w3_end,
                                              w4_begin, w4_end,
                                              min_sequences=int(week_sequence_counts[-1] * 0.005 + 1))

        tot_seq_w1, tot_seq_w2, tot_seq_w3, tot_seq_w4 = week_sequence_counts
        mut_w1, mut_w2, mut_w3, mut_w4 = mutation_data
        array_to_return = []
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
            array_to_return.append({
                'location': location,
                'protein': protein,
                'lineage' : lineage,
                'mut': mutation,
                'polyfit_slope': slope,
                'w4': c4,
                'w3': c3,
                'w2': c2,
                'w1': c1,
                'f1': f1,
                'f2': f2,
                'f3': f3,
                'f4': f4,
                'p_value_with_mut': compute_pvalue([c1, c2, c3, c4], week_sequence_counts),
                'p_value_without_mut': compute_pvalue(
                    [tot_seq_w1 - c1, tot_seq_w2 - c2, tot_seq_w3 - c3, tot_seq_w4 - c4],
                    week_sequence_counts),
                'p_value_comparative_mut': compute_pvalue([c1, c2, c3, c4],
                                                          [tot_seq_w1 - c1, tot_seq_w2 - c2, tot_seq_w3 - c3,
                                                           tot_seq_w4 - c4]),
            })

        return {'rows': array_to_return, 'tot_seq': [tot_seq_w1, tot_seq_w2,tot_seq_w3, tot_seq_w4]}
