"""
    API to perform lineage independent analysis
    Endpoints:
    ├── getStatistics
    └── getLineages
"""

from __future__ import print_function
import sqlite3
import time
import numpy as np
from flask_restplus import Namespace, Resource
from .lineage_specific import compute_pvalue
from .utils.utils import compute_weeks_from_date

api = Namespace('lineage_independent', description='lineage_independent')
db_name = 'varianthunter.db'

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


def extract_week_seq_counts(location, w, mut=None):
    """
    Extract weekly sequence counts for the given location and weeks from the database
    Args:
        location:   String representing the location to be considered
        w:          Weeks to be considered
        mut:        If set, the counts consider only the sequences with a given mutation

    Returns: An array of sequence counts

    """
    print("\t Extract number of sequences in the four weeks...", end="")
    exec_start = time.time()
    con = sqlite3.connect(db_name)
    cur = con.cursor()

    def extract_week_count(start, stop):
        if mut is not None:
            # count the seq collected for a given week and location having a given mutation
            query = f'''    select sum(count)
                            from  mutsg
                            where date > {start} and date <= {stop} and location = '{location}' and mut='{mut}' 
                            group by date,location;'''
        else:
            # count the seq collected for a given week and location
            query = f'''    select sum(count)
                            from  timelocling
                            where date > {start} and date <= {stop} and location = '{location}' 
                            group by date,location;'''
        return sum([x[0] for x in cur.execute(query).fetchall()])

    tot_seq_w4 = extract_week_count(w['w4_begin'], w['w4_end'])
    tot_seq_w3 = extract_week_count(w['w3_begin'], w['w3_end'])
    tot_seq_w2 = extract_week_count(w['w2_begin'], w['w2_end'])
    tot_seq_w1 = extract_week_count(w['w1_begin'], w['w1_end'])
    con.close()
    print(f'done in {time.time() - exec_start:.5f} seconds.')
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
    print("\t Extract mutation data for the four weeks...", end="")
    exec_start = time.time()
    con = sqlite3.connect(db_name)
    cur = con.cursor()

    def extract_week_mutation(start, stop, is_target=False):
        having_clause = f"having sum(count) >= {min_sequences}"
        query = f'''    select mut, sum(count) 
                        from mutsg 
                        where date > {start} and date <= {stop} and location = '{location}' and mut !=''
                        group by mut 
                        {having_clause if is_target else ""};'''
        return {k: v for k, v in cur.execute(query).fetchall()}

    muts_w4 = extract_week_mutation(w['w4_begin'], w['w4_end'], is_target=True)
    muts_w3 = extract_week_mutation(w['w3_begin'], w['w3_end'])
    muts_w2 = extract_week_mutation(w['w2_begin'], w['w2_end'])
    muts_w1 = extract_week_mutation(w['w1_begin'], w['w1_end'])
    con.close()
    print(f'done in {time.time() - exec_start:.5f} seconds.')
    return [muts_w1, muts_w2, muts_w3, muts_w4]


def extract_lineages_data(location, mut, w):
    """
    Extract lineages data for the given location, mutation and weeks from the database
    Args:
        location:   String representing the location to be considered
        mut:        String representing the protein and the mutation to be considered
        w:          Weeks to be considered

    Returns:

    """
    print("\t Extract lineages data in the four weeks for mutation...", end="")
    exec_start = time.time()
    con = sqlite3.connect(db_name)
    cur = con.cursor()

    week_sequence_counts = extract_week_seq_counts(location, w, mut=mut)
    tot_seq_w1, tot_seq_w2, tot_seq_w3, tot_seq_w4 = week_sequence_counts
    print(week_sequence_counts)
    print(extract_week_seq_counts(location, w))

    def extract_all_lineages(start, stop):
        query = f'''    select distinct lineage 
                        from    mutsg
                        where   date > {start} and date <= {stop} and 
                                location = '{location}' and mut = '{mut}';'''
        all_lineages = cur.execute(query).fetchall()
        return [x[0] for x in all_lineages]

    def extract_week_info(lineage, start, stop):
        query = f'''    select sum(count) 
                        from    mutsg 
                        where   date > {start} and date <= {stop} and location = '{location}' and 
                                lineage = '{lineage}'  and mut='{mut}'
                        group by date,location,mut,lineage;'''
        seqs = cur.execute(query).fetchall()
        return sum([x[0] for x in seqs])

    lineages = extract_all_lineages(w['w1_begin'], w['w4_end'])
    lineages.sort()
    lineages_data = []
    for lineage_name in lineages:
        lin_w4 = extract_week_info(lineage_name, w['w4_begin'], w['w4_end'])
        lin_w3 = extract_week_info(lineage_name, w['w3_begin'], w['w3_end'])
        lin_w2 = extract_week_info(lineage_name, w['w2_begin'], w['w2_end'])
        lin_w1 = extract_week_info(lineage_name, w['w1_begin'], w['w1_end'])
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
    print(f'done in {time.time() - exec_start:.5f} seconds.')
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
        # granularity = api.payload['granularity']
        location = api.payload['location']
        date = api.payload['date']

        w = compute_weeks_from_date(date)

        week_sequence_counts = extract_week_seq_counts(location, w)
        tot_seq_w1, tot_seq_w2, tot_seq_w3, tot_seq_w4 = week_sequence_counts

        mutation_data = extract_mutation_data(location, w, min_sequences=int(tot_seq_w4 * 0.005 + 1))
        mut_w1, mut_w2, mut_w3, mut_w4 = mutation_data

        statistics = []
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
            statistics.append({
                'location': location,
                'protein': protein,
                'mut': mutation,
                'slope': slope,
                'f1': f1,
                'f2': f2,
                'f3': f3,
                'f4': f4,
                'w1': c1,
                'w2': c2,
                'w3': c3,
                'w4': c4,
                'p_value_with_mut':
                    compute_pvalue([c1, c2, c3, c4], week_sequence_counts),
                'p_value_without_mut':
                    compute_pvalue(
                        [tot_seq_w1 - c1, tot_seq_w2 - c2, tot_seq_w3 - c3, tot_seq_w4 - c4],
                        week_sequence_counts),
                'p_value_comp':
                    compute_pvalue(
                        [c1, c2, c3, c4],
                        [tot_seq_w1 - c1, tot_seq_w2 - c2, tot_seq_w3 - c3, tot_seq_w4 - c4]),
            })

        return {'rows': statistics, 'tot_seq': week_sequence_counts}


@api.route('/getLineages')
class FieldList(Resource):
    @api.doc('get_lineages')
    def post(self):
        """
        Endpoint to obtain info about lineages for given mutation, location and date
        @return:    An object including the results
        """
        location = api.payload['location']
        date = api.payload['date']
        mut = api.payload['prot_mut']

        w = compute_weeks_from_date(date)

        return extract_lineages_data(location, mut, w)
