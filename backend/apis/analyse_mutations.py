from __future__ import print_function

import re
import time
import timeit

import numpy as np
from scipy.stats import fisher_exact, chi2_contingency, kstest
from threading import Timer
from datetime import datetime, timedelta
from flask_restplus import Namespace, Resource
from pymongo import MongoClient
import sqlite3

api = Namespace('analyse_mutations', description='analyse_mutations')

uri = "mongodb://localhost:27017/gcm_gisaid"
client = MongoClient(uri)
db = client.gcm_gisaid
collection_db = db.database_2022_01_07

sqlite_db_name = 'varianthunter.db'

# client = MongoClient(host='test_mongodb',
#                      port=27017,
#                      username='root',
#                      password='pass',
#                      authSource="admin")
# db = client["viruclust_db"]
# collection_db = db.viruclust_db_0

# collection_update_date = db.db_meta
database_name = 'viruclust_db_0'

PATTERN = re.compile("([a-zA-Z0-9]+)_([a-zA-Z~@#$^*()_+=[\]{}|\\,.?: -]+)([\d]+)([a-zA-Z~@#$^*()_+=[\]{}|\\,.?: -]+)")


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


all_geo_dict = {}

def get_all_geo():
    print("Start geo request...", end="")
    startx = time.time()
    con = sqlite3.connect(sqlite_db_name)
    cur = con.cursor()
    array_continent = [x[0] for x in
                       cur.execute("select * from continent_table where continent is not null;").fetchall()]

    array_country = [x[0] for x in
                     cur.execute("select * from country_table where country is not null;").fetchall()]
    array_region = [x[0] for x in
                    cur.execute("select * from region_table where region is not null;").fetchall()]
    con.close()
    list_geo_dict = {'continent': array_continent, 'country': array_country, 'region': array_region}
    all_geo_dict['all_geo'] = list_geo_dict

    print(f"...done in {time.time() - startx:.5f} seconds.")


all_important_mutation_dict = {}


def get_all_important_mutation():
    print("inizio request important mutation")

    pipeline = [
        {"$group": {"_id": '$covv_lineage', "count": {"$sum": 1}}},
    ]

    lin_info = {x['_id']: (x['count'], []) for x in collection_db.aggregate(pipeline, allowDiskUse=True)}

    pipeline = [
        {"$unwind": "$muts"},
        {"$group": {"_id": {'lin': '$covv_lineage',
                            'pro': "$muts.pro",
                            'org': "$muts.org",
                            'loc': "$muts.loc",
                            'alt': "$muts.alt",
                            },
                    "count": {"$sum": 1}}},
    ]

    results = collection_db.aggregate(pipeline, allowDiskUse=True)

    results = (x['_id'] for x in results if x['count'] / lin_info[x['_id']['lin']][0] >= 0.75)

    for x in results:
        ch = f"{x['pro']}_{x['org']}{x['loc']}{x['alt']}"
        lin_info[x['lin']][1].append(ch)

    lin_info = {x: [c, sorted(arr)] for x, (c, arr) in lin_info.items()}

    for lin in lin_info:
        all_important_mutation_dict[lin] = lin_info[lin]

    print("fine request important mutation")
    # x = datetime.today()
    # y = x.replace(day=x.day, hour=2, minute=0, second=0, microsecond=0) + timedelta(days=1)
    # delta_t = y - x
    # secs = delta_t.total_seconds()
    # t1 = Timer(secs, get_all_important_mutation)
    # t1.start()


get_all_geo()
get_all_lineage()
# get_all_important_mutation()


##############################################################################################################


def get_all_geo_last_week(date, granularity, location, lineage, array_results):
    last_week_date = date.replace(day=date.day) - timedelta(days=7)
    where_part = {
        'collection_date': {
            '$lt': date,
            '$gte': last_week_date
        },
        'c_coll_date_prec': {
            '$eq': 2
        },
    }

    # if lineage is not None:
    #     where_part['covv_lineage'] = {'$eq': lineage}
    if granularity != 'world':
        where_part[f'location.{granularity}'] = {'$eq': location}

    result_count = collection_db.count_documents(where_part)

    if result_count > 0:
        print("geo count --> ", result_count)
        get_all_lineage_for_each_geo(date, granularity, location, lineage, result_count, array_results)
    else:
        print("geo count --> 0")


def get_all_lineage_for_each_geo(date, granularity, location, lineage, result_count, array_results):
    last_week_date = date.replace(day=date.day) - timedelta(days=7)

    query = []
    where_part = {
        "$match": {
            'collection_date': {
                '$lt': date,
                '$gte': last_week_date
            },
            'c_coll_date_prec': {
                '$eq': 2
            },
        },
    }

    if lineage is not None:
        where_part["$match"]['covv_lineage'] = {'$eq': lineage}
    if granularity != 'world':
        where_part['$match'][f'location.{granularity}'] = {'$eq': location}

    group_part = {
        "$group": {"_id": {'lineage': '$covv_lineage'},
                   "count": {"$sum": 1}
                   }
    }

    sort_part = {"$sort":
                     {"count": -1}
                 }

    query.append(where_part)
    query.append(group_part)
    query.append(sort_part)

    results = collection_db.aggregate(query, allowDiskUse=True)
    list_geo_lineage_dict = []
    for single_item in results:
        # FILTER
        # if single_item['count'] / result_count > 0.01:  # and single_item['count'] > 10:
        single_item_remodel = {'lineage': single_item['_id']['lineage'],
                               'count': single_item['count']}
        list_geo_lineage_dict.append(single_item_remodel)
    print("all_lineages count --> ", list_geo_lineage_dict)
    get_all_mutation_for_lineage_for_each_geo_previous_week(date, granularity, location,
                                                            list_geo_lineage_dict, array_results)


def lineage_growth(date, granularity, location, lineage):
    last_week_date = date.replace(day=date.day) - timedelta(days=7)
    previous_week_date = last_week_date.replace(day=last_week_date.day) - timedelta(days=7)
    query = {
        'c_coll_date_prec': {
            '$eq': 2
        },
        'covv_lineage': {
            '$ne': lineage
        }
    }
    if granularity != 'world':
        query[f'location.{granularity}'] = {'$eq': location}

    query_this_week = query.copy()
    query_prev_week = query.copy()
    query_this_week['collection_date'] = {'$lt': date, '$gte': last_week_date}
    query_prev_week['collection_date'] = {'$lt': last_week_date, '$gte': previous_week_date}
    results_this_week = collection_db.count_documents(query_this_week)
    results_prev_week = collection_db.count_documents(query_prev_week)

    result = {
        'denominator_prev_week': results_prev_week,
        'denominator_this_week': results_this_week,
    }

    return result


def get_all_mutation_not_characteristics(date, granularity, location, lineage):
    last_week_date = date.replace(day=date.day) - timedelta(days=7)
    # previous_week_date = last_week_date.replace(day=last_week_date.day) - timedelta(days=7)

    query_count = {
        'c_coll_date_prec': {
            '$eq': 2
        },
        'collection_date': {
            '$lt': date,
            '$gte': last_week_date
        },
        'covv_lineage': {
            '$eq': lineage
        },
    }

    if granularity != 'world':
        query_count[f'location.{granularity}'] = {'$eq': location}

    denominator_lineage = collection_db.count_documents(query_count)

    pipeline = []

    where_part = {"$match": {
        'c_coll_date_prec': {
            '$eq': 2
        },
        'collection_date': {
            '$lt': date,
            '$gte': last_week_date
        },
        'covv_lineage': {
            '$eq': lineage
        },
    }}

    if granularity != 'world':
        where_part['$match'][f'location.{granularity}'] = {'$eq': location}

    pipeline.append(where_part)

    unwind_part = {"$unwind": "$muts"}
    pipeline.append(unwind_part)

    group_part = {"$group": {"_id": {'lin': '$covv_lineage',
                                     'pro': "$muts.pro",
                                     'org': "$muts.org",
                                     'loc': "$muts.loc",
                                     'alt': "$muts.alt",
                                     },
                             "count": {"$sum": 1}}}
    pipeline.append(group_part)

    results = collection_db.aggregate(pipeline, allowDiskUse=True)
    ##### FILTER NUMERIC ########
    # results = (x['_id'] for x in results if (0.75 > x['count'] / denominator_lineage > 0.01))  # and x['count'] > 10)

    filtered_results = []
    for x in results:
        mutation = f"{x['_id']['pro']}_{x['_id']['org']}{x['_id']['loc']}{x['_id']['alt']}"
        if 0.75 > (x['count']/denominator_lineage) > 0.01:     # mutation not in all_important_mutation_dict[x['_id']['lin']] and
            filtered_results.append(x['_id'])

    result_array = []
    for x in filtered_results:
        ch = f"{x['pro']}_{x['org']}{x['loc']}{x['alt']}"
        result_array.append(ch)

    return result_array


def get_all_mutation_for_lineage_for_each_geo_previous_week(date, granularity, real_location,
                                                            list_geo_lineage_dict, array_results):
    last_week_date = date.replace(day=date.day) - timedelta(days=7)
    previous_week_date = last_week_date.replace(day=last_week_date.day) - timedelta(days=7)

    for lineage_obj in list_geo_lineage_dict:
        lineage = lineage_obj['lineage']

        lineage_growth_result = lineage_growth(date, granularity, real_location, lineage)

        denominator_prev_week_with_mut = lineage_growth_result['denominator_prev_week']
        denominator_this_week_with_mut = lineage_growth_result['denominator_this_week']
        denominator_prev_week_without_mut = lineage_growth_result['denominator_prev_week']
        denominator_this_week_without_mut = lineage_growth_result['denominator_this_week']

        all_mutations_dict = get_all_mutation_not_characteristics(date, granularity, real_location, lineage)
        mut_dict = all_mutations_dict
        mut_len = len(mut_dict)
        kk = 0
        for mut in mut_dict:
            kk = kk + 1
            num_mut_perc = (kk / mut_len) * 100
            # FILTER SPIKE
            if '*' not in mut and '_-' not in mut:  # and 'Spike' in mut:

                print("", real_location, "-", lineage, "-", date, "-", mut, " --> ", num_mut_perc, " % ")
                # print("mut analysis ---> ", date, real_location, lineage, mut)

                m = PATTERN.fullmatch(mut)
                if m:
                    protein, orig, loc, alt = m.groups()
                    orig = orig.replace('stop', '*')
                    alt = alt.replace('stop', '*')

                    loc = int(loc)
                    if orig == 'ins':
                        orig = '-' * len(alt)
                        t = 'INS'
                    elif alt == 'del':
                        alt = '-'
                        t = 'DEL'
                    else:
                        t = 'SUB'

                    length = len(alt)
                    new_mut = {'pro': protein, 'org': orig,
                               'loc': loc, 'alt': alt,
                               'typ': t, 'len': length}

                    query = {
                        'c_coll_date_prec': {
                            '$eq': 2
                        },
                        'covv_lineage': {
                            '$eq': lineage
                        },
                    }

                    if granularity != 'world':
                        query[f'location.{granularity}'] = {'$eq': real_location}

                    query_with_mut_this_week = query.copy()
                    query_with_mut_prev_week = query.copy()
                    query_without_mut_this_week = query.copy()
                    query_without_mut_prev_week = query.copy()

                    query_with_mut_this_week['muts'] = {'$elemMatch': {
                        'pro': new_mut['pro'],
                        'loc': new_mut['loc'],
                        'alt': new_mut['alt'],
                        'org': new_mut['org'],
                    }
                    }
                    query_with_mut_this_week['collection_date'] = {'$lt': date, '$gte': last_week_date}
                    query_with_mut_prev_week['muts'] = {'$elemMatch': {
                        'pro': new_mut['pro'],
                        'loc': new_mut['loc'],
                        'alt': new_mut['alt'],
                        'org': new_mut['org'],
                    }
                    }
                    query_with_mut_prev_week['collection_date'] = {'$lt': last_week_date,
                                                                   '$gte': previous_week_date}
                    results_with_mut_this_week = collection_db.count_documents(query_with_mut_this_week)
                    results_with_mut_prev_week = collection_db.count_documents(query_with_mut_prev_week)

                    query_without_mut_this_week['muts'] = {'$not': {'$elemMatch': {
                        'pro': new_mut['pro'],
                        'loc': new_mut['loc'],
                        'alt': new_mut['alt'],
                        'org': new_mut['org'],
                    }
                    }
                    }
                    query_without_mut_this_week['collection_date'] = {'$lt': date, '$gte': last_week_date}
                    query_without_mut_prev_week['muts'] = {'$not': {'$elemMatch': {
                        'pro': new_mut['pro'],
                        'loc': new_mut['loc'],
                        'alt': new_mut['alt'],
                        'org': new_mut['org'],
                    }
                    }
                    }
                    query_without_mut_prev_week['collection_date'] = {'$lt': last_week_date,
                                                                      '$gte': previous_week_date}
                    results_without_mut_this_week = collection_db.count_documents(query_without_mut_this_week)
                    results_without_mut_prev_week = collection_db.count_documents(query_without_mut_prev_week)

                    if (results_with_mut_prev_week + results_without_mut_prev_week) != 0:
                        perc_with_mut_prev_week = (
                                                          results_with_mut_prev_week /
                                                          (results_with_mut_prev_week + results_without_mut_prev_week)) \
                                                  * 100
                    else:
                        perc_with_mut_prev_week = 0
                    if (results_with_mut_this_week + results_without_mut_this_week) != 0:
                        perc_with_mut_this_week = (
                                                          results_with_mut_this_week /
                                                          (results_with_mut_this_week + results_without_mut_this_week)) \
                                                  * 100
                    else:
                        perc_with_mut_this_week = 0
                    diff_perc_with_mut = perc_with_mut_this_week - perc_with_mut_prev_week

                    if (results_with_mut_prev_week + results_without_mut_prev_week) != 0:
                        perc_without_mut_prev_week = \
                            (results_without_mut_prev_week /
                             (results_with_mut_prev_week + results_without_mut_prev_week)) * 100
                    else:
                        perc_without_mut_prev_week = 0
                    if (results_with_mut_this_week + results_without_mut_this_week) != 0:
                        perc_without_mut_this_week = \
                            (results_without_mut_this_week /
                             (results_with_mut_this_week + results_without_mut_this_week)) * 100
                    else:
                        perc_without_mut_this_week = 0
                    diff_perc_without_mut = perc_without_mut_this_week - perc_without_mut_prev_week

                    if granularity != 'world':
                        location = real_location
                    else:
                        location = 'World'

                    table_with_mutation = [[results_with_mut_prev_week, results_with_mut_this_week],
                                           [denominator_prev_week_with_mut, denominator_this_week_with_mut]]
                    odds_with_mut, p_with_mut = fisher_exact(table_with_mutation)

                    table_without_mutation = [[results_without_mut_prev_week, results_without_mut_this_week],
                                              [denominator_prev_week_without_mut, denominator_this_week_without_mut]]
                    odds_without_mut, p_without_mut = fisher_exact(table_without_mutation)

                    table_comparative_mutation = [
                        [results_with_mut_prev_week, results_with_mut_this_week],
                        [results_without_mut_prev_week, results_without_mut_this_week]]
                    odds_comparative_mut, p_comparative_mut = fisher_exact(table_comparative_mutation)

                    to_float = perc_with_mut_this_week
                    format_float = "{:.2f}".format(to_float)
                    perc_with_absolute_number = format_float + f'  ({results_with_mut_this_week})'

                    full_object = {f'{granularity}': location,
                                   'lineage': lineage,
                                   'mut': mut,
                                   'muts': [new_mut],
                                   'total_seq_pop_prev_week_with_mut': denominator_prev_week_with_mut,
                                   'total_seq_pop_this_week_with_mut': denominator_this_week_with_mut,
                                   'total_seq_pop_prev_week_without_mut': denominator_prev_week_without_mut,
                                   'total_seq_pop_this_week_without_mut': denominator_this_week_without_mut,
                                   'count_with_mut_prev_week': results_with_mut_prev_week,
                                   'count_with_mut_this_week': results_with_mut_this_week,
                                   'perc_with_mut_prev_week': perc_with_mut_prev_week,
                                   'perc_with_mut_this_week': perc_with_mut_this_week,
                                   'diff_perc_with_mut': diff_perc_with_mut,
                                   'p_value_with_mut': p_with_mut,
                                   'count_without_mut_prev_week': results_without_mut_prev_week,
                                   'count_without_mut_this_week': results_without_mut_this_week,
                                   'perc_without_mut_prev_week': perc_without_mut_prev_week,
                                   'perc_without_mut_this_week': perc_without_mut_this_week,
                                   'diff_perc_without_mut': diff_perc_without_mut,
                                   'p_value_without_mut': p_without_mut,
                                   'p_value_comparative_mut': p_comparative_mut,
                                   'analysis_date': date.strftime("%Y-%m-%d"),
                                   'granularity': granularity,
                                   'location': location,
                                   'perc_with_absolute_number': perc_with_absolute_number,
                                   }

                    array_results.append(full_object)

                else:
                    print('======> ERROR', mut)

    print("fine all_mutation all_lineages")


def create_unique_array_results(array_results, today_date, array_date):
    result_dict = {}
    for single_res in array_results:
        single_obj = {}
        if single_res['location'] is None:
            location = 'none'
        else:
            location = single_res['location']
        if single_res['lineage'] is None:
            lineage = 'none'
        else:
            lineage = single_res['lineage']
        if single_res['mut'] is None:
            mut = 'none'
        else:
            mut = single_res['mut']
        if single_res['granularity'] is None:
            granularity = 'none'
        else:
            granularity = single_res['granularity']
        id_single_obj = location + granularity + lineage + mut
        if id_single_obj not in result_dict:
            analysis_date = single_res['analysis_date']
            for key in single_res:
                if key == 'p_value_comparative_mut' or \
                        key == 'p_value_without_mut' or \
                        key == 'diff_perc_without_mut' or \
                        key == 'perc_without_mut_this_week' or \
                        key == 'perc_without_mut_prev_week' or \
                        key == 'count_without_mut_this_week' or \
                        key == 'count_without_mut_prev_week' or \
                        key == 'p_value_with_mut' or \
                        key == 'diff_perc_with_mut' or \
                        key == 'perc_with_mut_this_week' or \
                        key == 'perc_with_mut_prev_week' or \
                        key == 'count_with_mut_this_week' or \
                        key == 'count_with_mut_prev_week' or \
                        key == 'perc_with_absolute_number':
                    new_key = key + '_' + analysis_date
                    single_obj[new_key] = single_res[key]
                elif key == 'total_seq_pop_this_week_with_mut':
                    new_key = 'total_seq_pop_this_week' + '_' + analysis_date
                    single_obj[new_key] = single_res[key]
                elif key == 'total_seq_pop_prev_week_with_mut':
                    new_key = 'total_seq_pop_prev_week' + '_' + analysis_date
                    single_obj[new_key] = single_res[key]
                elif key == 'analysis_date':
                    single_obj[key] = single_res[key]   # str(today_date.strftime('%Y-%m-%d'))
                elif key == 'mut':
                    single_obj['protein'] = single_res[key].split('_')[0]
                    single_obj[key] = single_res[key].split('_')[1]
                else:
                    if key != 'total_seq_world_prev_week' and \
                            key != 'total_seq_world_this_week':
                        single_obj[key] = single_res[key]
                key_lineage_1 = 'total_seq_lineage_this_week' + '_' + analysis_date
                single_obj[key_lineage_1] = single_res['count_with_mut_this_week'] \
                                            + single_res['count_without_mut_this_week']
                key_lineage_2 = 'total_seq_lineage_prev_week' + '_' + analysis_date
                single_obj[key_lineage_2] = single_res['count_with_mut_prev_week'] \
                                            + single_res['count_without_mut_prev_week']
                key_diff = 'diff_perc' + '_' + analysis_date
                if single_obj[key_lineage_1] != 0:
                    factor_1 = single_res['count_with_mut_this_week'] / single_obj[key_lineage_1]
                else:
                    factor_1 = 0
                if single_obj[key_lineage_2] != 0:
                    factor_2 = single_res['count_with_mut_prev_week'] / single_obj[key_lineage_2]
                else:
                    factor_2 = 0
                single_obj[key_diff] = (factor_1 - factor_2) * 100

            result_dict[id_single_obj] = single_obj
        else:
            analysis_date = single_res['analysis_date']
            for key in single_res:
                if key == 'p_value_comparative_mut' or \
                        key == 'p_value_without_mut' or \
                        key == 'diff_perc_without_mut' or \
                        key == 'perc_without_mut_this_week' or \
                        key == 'perc_without_mut_prev_week' or \
                        key == 'count_without_mut_this_week' or \
                        key == 'count_without_mut_prev_week' or \
                        key == 'p_value_with_mut' or \
                        key == 'diff_perc_with_mut' or \
                        key == 'perc_with_mut_this_week' or \
                        key == 'perc_with_mut_prev_week' or \
                        key == 'count_with_mut_this_week' or \
                        key == 'count_with_mut_prev_week' or \
                        key == 'perc_with_absolute_number':
                    new_key = key + '_' + analysis_date
                    result_dict[id_single_obj][new_key] = single_res[key]
                elif key == 'total_seq_pop_this_week_with_mut':
                    new_key = 'total_seq_pop_this_week' + '_' + analysis_date
                    result_dict[id_single_obj][new_key] = single_res[key]
                elif key == 'total_seq_pop_prev_week_with_mut':
                    new_key = 'total_seq_pop_prev_week' + '_' + analysis_date
                    result_dict[id_single_obj][new_key] = single_res[key]
                key_lineage_1 = 'total_seq_lineage_this_week' + '_' + analysis_date
                result_dict[id_single_obj][key_lineage_1] = single_res['count_with_mut_this_week'] \
                                                            + single_res['count_without_mut_this_week']
                key_lineage_2 = 'total_seq_lineage_prev_week' + '_' + analysis_date
                result_dict[id_single_obj][key_lineage_2] = single_res['count_with_mut_prev_week'] \
                                                            + single_res['count_without_mut_prev_week']
                key_diff = 'diff_perc' + '_' + analysis_date
                if result_dict[id_single_obj][key_lineage_1] != 0:
                    factor_1 = single_res['count_with_mut_this_week'] / result_dict[id_single_obj][key_lineage_1]
                else:
                    factor_1 = 0
                if result_dict[id_single_obj][key_lineage_2] != 0:
                    factor_2 = single_res['count_with_mut_prev_week'] / result_dict[id_single_obj][key_lineage_2]
                else:
                    factor_2 = 0
                result_dict[id_single_obj][key_diff] = (factor_1 - factor_2) * 100

    array_to_del = []
    for elem in result_dict:
        json_obj = result_dict[elem]
        i = 0
        array_x_polyfit = []
        array_y_polyfit = []
        count = 0

        table_with_mutation = [[], []]
        table_without_mutation = [[], []]
        table_comparative_mutation = [[], []]

        table_with_mut_chi2 = []
        table_without_mutation_chi2 = []
        table_comparative_mutation_chi2 = []

        for single_date in array_date:
            array_x_polyfit.append(float(i))
            i = i + 1
            key = 'perc_with_mut_this_week' + '_' + single_date
            # key = 'p_value_comparative_mut' + '_' + single_date
            if key in json_obj:
                count = count + 1
                array_y_polyfit.append(json_obj[key])
            # else:
            #     array_y_polyfit.append(1.0)

            if i == 1:
                key_count_with_mut_prev_week = 'count_with_mut_prev_week' + '_' + single_date
                key_denom_with_mut_prev_week = 'total_seq_pop_prev_week' + '_' + single_date
                key_count_without_mut_prev_week = 'count_without_mut_prev_week' + '_' + single_date
                key_denom_without_mut_prev_week = 'total_seq_pop_prev_week' + '_' + single_date

                arr_chi2 = []
                if key_count_with_mut_prev_week in json_obj:
                    table_with_mutation[0].append(json_obj[key_count_with_mut_prev_week])
                    arr_chi2.append(json_obj[key_count_with_mut_prev_week])
                # else:
                #     table_with_mutation[0].append(0)
                # arr_chi2.append(0)
                if key_denom_with_mut_prev_week in json_obj:
                    table_with_mutation[1].append(json_obj[key_denom_with_mut_prev_week])
                    arr_chi2.append(json_obj[key_denom_with_mut_prev_week])
                # else:
                #     table_with_mutation[1].append(0)
                # arr_chi2.append(0)
                if len(arr_chi2) > 0:
                    table_with_mut_chi2.append(arr_chi2)

                arr_chi2 = []
                if key_count_without_mut_prev_week in json_obj:
                    table_without_mutation[0].append(json_obj[key_count_without_mut_prev_week])
                    arr_chi2.append(json_obj[key_count_without_mut_prev_week])
                # else:
                #     table_without_mutation[0].append(0)
                # arr_chi2.append(0)
                if key_denom_without_mut_prev_week in json_obj:
                    table_without_mutation[1].append(json_obj[key_denom_without_mut_prev_week])
                    arr_chi2.append(json_obj[key_denom_without_mut_prev_week])
                # else:
                #     table_without_mutation[1].append(0)
                # arr_chi2.append(0)
                if len(arr_chi2) > 0:
                    table_without_mutation_chi2.append(arr_chi2)

                arr_chi2 = []
                if key_count_with_mut_prev_week in json_obj:
                    table_comparative_mutation[0].append(json_obj[key_count_with_mut_prev_week])
                    arr_chi2.append(json_obj[key_count_with_mut_prev_week])
                # else:
                #     table_without_mutation[0].append(0)
                # arr_chi2.append(0)
                if key_count_without_mut_prev_week in json_obj:
                    table_comparative_mutation[1].append(json_obj[key_count_without_mut_prev_week])
                    arr_chi2.append(json_obj[key_count_without_mut_prev_week])
                # else:
                #     table_comparative_mutation[1].append(0)
                # arr_chi2.append(0)
                if len(arr_chi2) > 0:
                    table_comparative_mutation_chi2.append(arr_chi2)

            key_count_with_mut_this_week = 'count_with_mut_this_week' + '_' + single_date
            key_denom_with_mut_this_week = 'total_seq_pop_this_week' + '_' + single_date
            key_count_without_mut_this_week = 'count_without_mut_this_week' + '_' + single_date
            key_denom_without_mut_this_week = 'total_seq_pop_this_week' + '_' + single_date

            arr_chi2 = []
            if key_count_with_mut_this_week in json_obj:
                table_with_mutation[0].append(json_obj[key_count_with_mut_this_week])
                arr_chi2.append(json_obj[key_count_with_mut_this_week])
            # else:
            #     table_with_mutation[0].append(0)
            # arr_chi2.append(0)
            if key_denom_with_mut_this_week in json_obj:
                table_with_mutation[1].append(json_obj[key_denom_with_mut_this_week])
                arr_chi2.append(json_obj[key_denom_with_mut_this_week])
            # else:
            #     table_with_mutation[1].append(0)
            # arr_chi2.append(0)
            if len(arr_chi2) > 0:
                table_with_mut_chi2.append(arr_chi2)

            arr_chi2 = []
            if key_count_without_mut_this_week in json_obj:
                table_without_mutation[0].append(json_obj[key_count_without_mut_this_week])
                arr_chi2.append(json_obj[key_count_without_mut_this_week])
            # else:
            #     table_without_mutation[0].append(0)
            # arr_chi2.append(0)
            if key_denom_without_mut_this_week in json_obj:
                table_without_mutation[1].append(json_obj[key_denom_without_mut_this_week])
                arr_chi2.append(json_obj[key_denom_without_mut_this_week])
            # else:
            #     table_without_mutation[1].append(0)
            # arr_chi2.append(0)
            if len(arr_chi2) > 0:
                table_without_mutation_chi2.append(arr_chi2)

            arr_chi2 = []
            if key_count_with_mut_this_week in json_obj:
                table_comparative_mutation[0].append(json_obj[key_count_with_mut_this_week])
                arr_chi2.append(json_obj[key_count_with_mut_this_week])
            # else:
            #     table_comparative_mutation[0].append(0)
            # arr_chi2.append(0)
            if key_count_without_mut_this_week in json_obj:
                table_comparative_mutation[1].append(json_obj[key_count_without_mut_this_week])
                arr_chi2.append(json_obj[key_count_without_mut_this_week])
            # else:
            #     table_comparative_mutation[1].append(0)
            # arr_chi2.append(0)
            if len(arr_chi2) > 0:
                table_comparative_mutation_chi2.append(arr_chi2)

        # odds_with_mut, p_with_mut = fisher_exact(table_with_mutation)
        # odds_without_mut, p_without_mut = fisher_exact(table_without_mutation)
        # odds_comparative_mut, p_comparative_mut = fisher_exact(table_comparative_mutation)

        # print("QUI1", table_with_mut_chi2)
        # print("QUI2", table_without_mutation_chi2)
        # print("QUI3", table_comparative_mutation_chi2)

        min_count = (len(array_date) / 2) + 1
        if count >= min_count:
            stat, p_with_mut, dof, expected = chi2_contingency(table_with_mut_chi2)
            stat, p_without_mut, dof, expected = chi2_contingency(table_without_mutation_chi2)
            stat, p_comparative_mut, dof, expected = chi2_contingency(table_comparative_mutation_chi2)

            # stat1, p_with_mut = kstest(table_with_mutation[0], table_with_mutation[1])
            # stat2, p_without_mut = kstest(table_without_mutation[0], table_without_mutation[1])
            # stat3, p_comparative_mut = kstest(table_comparative_mutation[0], table_comparative_mutation_chi2[1])

            json_obj['p_value_with_mut_total'] = p_with_mut
            json_obj['p_value_without_mut_total'] = p_without_mut
            json_obj['p_value_comparative_mut_total'] = p_comparative_mut

        array_x_polyfit = []
        j = 0
        while j < len(array_y_polyfit):
            array_x_polyfit.append(float(j))
            j = j + 1

        # print("qui", array_x_polyfit, array_y_polyfit)
        if len(array_x_polyfit) > 1:
            z = np.polyfit(array_x_polyfit, array_y_polyfit, 1)
            json_obj['polyfit_slope'] = z[0]

            to_float = z[1]
            format_float = "{:.2f}".format(to_float)
            json_obj['polyfit_intercept'] = format_float
        else:
            json_obj['polyfit_slope'] = 0
            json_obj['polyfit_intercept'] = 0

        min_count = (len(array_date) / 2) + 1
        if count < min_count:
            array_to_del.append(elem)

    for el in array_to_del:
        del result_dict[el]

    return result_dict


##############################################################################################################


@api.route('/getAllGeo')
class FieldList(Resource):
    @api.doc('get_all_geo')
    def get(self):
        all_geo = all_geo_dict['all_geo']
        return all_geo


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
        granularity = payload['granularity']
        location = payload['value']
        lineage = payload['lineage']
        date = payload['date']
        num_week = payload['numWeek']

        i = 0
        array_date = []
        date_1 = date
        start = timeit.default_timer()
        array_date_2 = []
        while i < num_week:
            translated_date = datetime.strptime(date_1, '%Y-%m-%d')
            array_date.append(date_1)
            array_date_2.insert(0, date_1)
            previous_week_date = translated_date.replace(day=translated_date.day) - timedelta(days=7)
            date_1 = previous_week_date.strftime("%Y-%m-%d")
            i = i + 1

        array_results = []
        for single_date in array_date:
            print("DATE ", single_date)
            specific_date = datetime.strptime(single_date, '%Y-%m-%d')
            get_all_geo_last_week(specific_date, granularity, location, lineage, array_results)

        result_dict = create_unique_array_results(array_results, datetime.strptime(date, '%Y-%m-%d'), array_date_2)
        array_to_return = list(result_dict.values())
        end = timeit.default_timer()
        print("TIMER ", end - start)
        return array_to_return
