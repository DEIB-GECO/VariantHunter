from __future__ import print_function

import re
import timeit

import numpy as np
from scipy.stats import fisher_exact
from threading import Timer
from datetime import datetime, timedelta
from flask_restplus import Namespace, Resource
from pymongo import MongoClient

api = Namespace('analyse_mutations', description='analyse_mutations')

uri = "mongodb://localhost:27017/gcm_gisaid"
client = MongoClient(uri)
db = client.gcm_gisaid
collection_db = db.viruclust_db_0
collection_update_date = db.db_meta

# client = MongoClient(host='test_mongodb',
#                      port=27017,
#                      username='root',
#                      password='pass',
#                      authSource="admin")
# db = client["viruclust_db"]
# collection_db = db.viruclust_db_0
# database_name = 'viruclust_db_0'

PATTERN = re.compile("([a-zA-Z0-9]+)_([a-zA-Z~@#$^*()_+=[\]{}|\\,.?: -]+)([\d]+)([a-zA-Z~@#$^*()_+=[\]{}|\\,.?: -]+)")


##############################################################################################################


all_lineage_dict = {}


def get_all_lineage():
    print("inizio request lineage")
    start_date = datetime.strptime("2019-01-01", '%Y-%m-%d')
    query = [
        {
            "$match": {
                'collection_date': {
                    '$gte': start_date
                },
                'c_coll_date_prec': {
                    '$eq': 2
                },
                'covv_lineage': {
                    '$ne': ''
                },
            },
        },
        {"$group": {"_id": {'lineage': '$covv_lineage',
                            },
                    }
         },
    ]

    results = collection_db.aggregate(query, allowDiskUse=True)

    array_results = []
    for single_item in results:
        array_results.append(single_item['_id']['lineage'])

    array_results.sort()

    all_lineage_dict['all_lineage'] = array_results
    print("fine request lineage")
    # x = datetime.today()
    # y = x.replace(day=x.day, hour=2, minute=0, second=0, microsecond=0) + timedelta(days=1)
    # delta_t = y - x
    # secs = delta_t.total_seconds()
    # t4 = Timer(secs, get_all_lineage)
    # t4.start()


all_geo_dict = {}


def get_all_geo():
    print("inizio request geo")
    start_date = datetime.strptime("2019-01-01", '%Y-%m-%d')
    query = [
        {
            "$match": {
                'collection_date': {
                    '$gte': start_date
                },
                'c_coll_date_prec': {
                    '$eq': 2
                },
                'covv_lineage': {
                    '$ne': ''
                },
            },
        },
        {"$group": {"_id": {'geo_group': '$location.geo_group',
                            'country': "$location.country",
                            'region': "$location.region",
                            },
                    }
         },
    ]

    results = collection_db.aggregate(query, allowDiskUse=True)

    array_continent = []
    array_country = []
    array_region = []
    for single_item in results:
        if single_item['_id']['geo_group'] not in array_continent:
            array_continent.append(single_item['_id']['geo_group'])
        if single_item['_id']['country'] not in array_country:
            array_country.append(single_item['_id']['country'])
        if single_item['_id']['region'] not in array_region:
            array_region.append(single_item['_id']['region'])
    list_geo_dict = {'continent': array_continent, 'country': array_country, 'region': array_region}

    all_geo_dict['all_geo'] = list_geo_dict
    print("fine request geo")
    # x = datetime.today()
    # y = x.replace(day=x.day, hour=2, minute=0, second=0, microsecond=0) + timedelta(days=1)
    # delta_t = y - x
    # secs = delta_t.total_seconds()
    # t4 = Timer(secs, get_all_geo)
    # t4.start()


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
        for mut in mut_dict:
            if '*' not in mut and '_-' not in mut:  # and 'Spike' in mut:

                print("mut analysis ---> ", date, real_location, lineage, mut)

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

                    if denominator_prev_week_with_mut != 0:
                        perc_with_mut_prev_week = (
                                                          results_with_mut_prev_week / denominator_prev_week_with_mut) * 100
                    else:
                        perc_with_mut_prev_week = 0
                    if denominator_this_week_with_mut != 0:
                        perc_with_mut_this_week = (
                                                          results_with_mut_this_week / denominator_this_week_with_mut) * 100
                    else:
                        perc_with_mut_this_week = 0
                    diff_perc_with_mut = perc_with_mut_this_week - perc_with_mut_prev_week

                    if denominator_prev_week_without_mut != 0:
                        perc_without_mut_prev_week = \
                            (results_without_mut_prev_week / denominator_prev_week_without_mut) * 100
                    else:
                        perc_without_mut_prev_week = 0
                    if denominator_this_week_without_mut != 0:
                        perc_without_mut_this_week = \
                            (results_without_mut_this_week / denominator_this_week_without_mut) * 100
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
                                   'location': location
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
                        key == 'count_with_mut_prev_week':
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
                        key == 'count_with_mut_prev_week':
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
        for single_date in array_date:
            array_x_polyfit.append(float(i))
            i = i + 1
            key = 'p_value_comparative_mut' + '_' + single_date
            if key in json_obj:
                count = count + 1
                array_y_polyfit.append(json_obj[key])
            else:
                array_y_polyfit.append(1.0)
        print("qui", array_x_polyfit, array_y_polyfit)
        z = np.polyfit(array_x_polyfit, array_y_polyfit, 1)
        json_obj['polyfit'] = z[0]

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
