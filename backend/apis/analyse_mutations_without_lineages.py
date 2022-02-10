from __future__ import print_function

import re
import timeit
import time

import numpy as np
import scipy.stats
from scipy.stats import fisher_exact, chi2_contingency, kstest
from threading import Timer
from datetime import datetime, timedelta
from flask_restplus import Namespace, Resource
from pymongo import MongoClient
import sqlite3

from .analyse_mutations import collection_db, database_name

api = Namespace('analyse_mutations_without_lineages', description='analyse_mutations_without_lineages')

PATTERN = re.compile("([a-zA-Z0-9]+)_([a-zA-Z~@#$^*()_+=[\]{}|\\,.?: -]+)([\d]+)([a-zA-Z~@#$^*()_+=[\]{}|\\,.?: -]+)")


startdate = datetime.strptime("2020-01-01", "%Y-%m-%d")
sqlite_db_name = 'varianthunter.db'


##############################################################################################################


def get_all_geo_last_week(date, granularity, location, array_results):
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
    if granularity != 'world':
        where_part[f'location.{granularity}'] = {'$eq': location}

    result_count = collection_db.count_documents(where_part)

    if result_count > 0:
        print("geo count --> ", result_count)
        get_all_mutation_for_each_geo_previous_week(date, granularity, location, array_results)
    else:
        print("geo count --> 0")


def growth(date, granularity, location):
    last_week_date = date.replace(day=date.day) - timedelta(days=7)
    previous_week_date = last_week_date.replace(day=last_week_date.day) - timedelta(days=7)
    query = {
        'c_coll_date_prec': {
            '$eq': 2
        },
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


def get_all_mutation_not_characteristics(date, granularity, location):
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
    }

    if granularity != 'world':
        query_count[f'location.{granularity}'] = {'$eq': location}

    denominator = collection_db.count_documents(query_count)

    pipeline = []

    where_part = {"$match": {
        'c_coll_date_prec': {
            '$eq': 2
        },
        'collection_date': {
            '$lt': date,
            '$gte': last_week_date
        },
    }}

    if granularity != 'world':
        where_part['$match'][f'location.{granularity}'] = {'$eq': location}

    pipeline.append(where_part)

    unwind_part = {"$unwind": "$muts"}
    pipeline.append(unwind_part)

    group_part = {"$group": {"_id": {
                                     'pro': "$muts.pro",
                                     'org': "$muts.org",
                                     'loc': "$muts.loc",
                                     'alt': "$muts.alt",
                                     },
                             "count": {"$sum": 1}}}
    pipeline.append(group_part)

    results = collection_db.aggregate(pipeline, allowDiskUse=True)
    ##### FILTER NUMERIC ########
    # results = (x['_id'] for x in results if (0.75 > x['count'] / denominator > 0.01))  # and x['count'] > 10)

    filtered_results = []
    for x in results:
        mutation = f"{x['_id']['pro']}_{x['_id']['org']}{x['_id']['loc']}{x['_id']['alt']}"
        if (x['count']/denominator) > 0.01:     # mutation not in all_important_mutation_dict[x['_id']['lin']] and
            filtered_results.append(x['_id'])

    result_array = []
    for x in filtered_results:
        ch = f"{x['pro']}_{x['org']}{x['loc']}{x['alt']}"
        result_array.append(ch)

    return result_array


def get_all_mutation_for_each_geo_previous_week(date, granularity, real_location, array_results):
    last_week_date = date.replace(day=date.day) - timedelta(days=7)
    previous_week_date = last_week_date.replace(day=last_week_date.day) - timedelta(days=7)

    growth_result = growth(date, granularity, real_location)

    denominator_prev_week_with_mut = growth_result['denominator_prev_week']
    denominator_this_week_with_mut = growth_result['denominator_this_week']
    denominator_prev_week_without_mut = growth_result['denominator_prev_week']
    denominator_this_week_without_mut = growth_result['denominator_this_week']

    all_mutations_dict = get_all_mutation_not_characteristics(date, granularity, real_location)
    mut_dict = all_mutations_dict
    mut_len = len(mut_dict)
    kk = 0
    for mut in mut_dict:
        kk = kk + 1
        num_mut_perc = (kk / mut_len) * 100
        # FILTER ON SPIKE
        if '*' not in mut and '_-' not in mut:  # and 'Spike' in mut:

            print("", real_location, "-", date, "-", mut, " --> ", num_mut_perc, " % ")
            # print("mut analysis ---> ", date, real_location, mut)

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

                to_float = perc_with_mut_this_week
                format_float = "{:.2f}".format(to_float)
                perc_with_absolute_number = format_float + f'  ({results_with_mut_this_week})'

                full_object = {'mut': mut,
                               'lineage': None,
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

    print("fine all_mutation")


def create_unique_array_results(array_results, today_date, array_date, function):
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
                if function != 'selectedMuts':
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
                if function != 'selectedMuts':
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

    if function != 'selectedMuts':
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
                if key in json_obj:
                    count = count + 1
                    array_y_polyfit.append(json_obj[key])
                # else:
                #     array_y_polyfit.append(0.0)

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

def extract_cumulative_data(location, w1_begin, w1_end, w2_begin, w2_end, w3_begin, w3_end, w4_begin, w4_end):
    print("Extract number of sequences in the four weeks...", end="")
    startex = time.time()
    con = sqlite3.connect(sqlite_db_name)
    cur = con.cursor()

    def execute_query(start, stop):
        cur.execute(f'''select date,location,sum(count) 
                        from timelocling 
                        where date > {start} and date <= {stop} and location = '{location}' 
                        group by date,location;''')
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

def extract_mutation_data(location, w1_begin, w1_end, w2_begin, w2_end, w3_begin, w3_end, w4_begin, w4_end, min_sequences = 0):
    print("Extract mutation data for the four weeks...", end="")
    startex = time.time()

    con = sqlite3.connect(sqlite_db_name)
    cur = con.cursor()

    def execute_query(start, stop, is_target = False):
        having_clause = f"having sum(count) >= {min_sequences}"
        cur.execute(f'''select mut, sum(count) from mutsg 
                        where date > {start} and date <= {stop} and location = '{location}'
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

def compute_pvalue(freq1, freq2):
    try:
        return scipy.stats.chi2_contingency([freq1, freq2])[1]
    except:
        return "NaN"

##############################################################################################################


@api.route('/getStatistics')
class FieldList(Resource):
    @api.doc('get_statistics')
    def post(self):
        print("inside get statistics")
        payload = api.payload
        granularity = payload['granularity']
        location = payload['value']
        date = payload['date']

        w4_end = (datetime.strptime(date, "%Y-%m-%d") - startdate).days
        w4_begin = w4_end - 7
        w3_end = w4_begin - 1
        w3_begin = w3_end - 7
        w2_end = w3_begin - 1
        w2_begin = w2_end - 7
        w1_end = w2_begin - 1
        w1_begin = w1_end - 7

        week_sequence_counts = extract_cumulative_data(location,
                                                       w1_begin,w1_end,
                                                       w2_begin,w2_end,
                                                       w3_begin,w3_end,
                                                       w4_begin,w4_end)
        mutation_data = extract_mutation_data(location,
                                              w1_begin, w1_end,
                                              w2_begin, w2_end,
                                              w3_begin, w3_end,
                                              w4_begin, w4_end,
                                              min_sequences=int(week_sequence_counts[-1]*0.005 +1))

        tot_seq_w1, tot_seq_w2, tot_seq_w3, tot_seq_w4 = week_sequence_counts
        mut_w1, mut_w2, mut_w3, mut_w4 = mutation_data
        print(mut_w1)
        array_to_return = []
        for mut, c4 in mut_w4.items():
            protein, mutation = mut.split("_")
            c1 = mut_w1.get(mut, 0)
            c2 = mut_w2.get(mut, 0)
            c3 = mut_w3.get(mut, 0)
            f1 = (c1 / tot_seq_w1)*100
            f2 = (c2 / tot_seq_w2)*100
            f3 = (c3 / tot_seq_w3)*100
            f4 = (c4 / tot_seq_w4)*100
            slope, intercept = np.polyfit([0, 1, 2, 3], [f1, f2, f3, f4], 1)
            array_to_return.append({
                'location': location,
                'protein' : protein,
                'mut' : mutation,
                'polyfit_slope': f'{slope:2.4f}',
                'polyfit_intercept' : f'{intercept:2.4f}',
                'w4': f'{f4:.3f} ({c4})',
                'w3': f'{f3:.3f} ({c3})',
                'w2': f'{f2:.3f} ({c2})',
                'w1': f'{f1:.3f} ({c1})',
                'f1': f1,
                'f2': f2,
                'f3': f3,
                'f4': f4,
                'p_value_with_mut_total' : compute_pvalue([c1,c2,c3,c4], week_sequence_counts),
                'p_value_without_mut_total': compute_pvalue([tot_seq_w1-c1, tot_seq_w2-c2, tot_seq_w3-c3, tot_seq_w4-c4],
                                                            week_sequence_counts),
                'p_value_comparative_mut_total': compute_pvalue([c1, c2, c3, c4],
                                                                [tot_seq_w1-c1, tot_seq_w2-c2, tot_seq_w3-c3, tot_seq_w4-c4]),
            })

        return array_to_return


@api.route('/analyzePeriodSelectedMuts')
class FieldList(Resource):
    @api.doc('analyze_period_selected_muts')
    def post(self):
        payload = api.payload
        granularity = payload['granularity']
        location = payload['location']
        date = payload['date']
        num_week = payload['numWeek']
        list_of_muts = payload['listOfMutations']

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
            analysis_date = datetime.strptime(single_date, '%Y-%m-%d')
            last_week_date = analysis_date.replace(day=analysis_date.day) - timedelta(days=7)
            mut_len = len(list_of_muts)
            kk = 0
            for mut in list_of_muts:
                kk = kk + 1
                num_mut_perc = (kk / mut_len) * 100
                print("", location, "-", single_date, "-", mut, " --> ", num_mut_perc, " % ")

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
                    }

                    if granularity != 'world':
                        query[f'location.{granularity}'] = {'$eq': location}

                    query_with_mut_this_week = query.copy()
                    query_without_mut_this_week = query.copy()

                    query_with_mut_this_week['muts'] = {'$elemMatch': {
                        'pro': new_mut['pro'],
                        'loc': new_mut['loc'],
                        'alt': new_mut['alt'],
                        'org': new_mut['org'],
                    }
                    }
                    query_with_mut_this_week['collection_date'] = {'$lt': analysis_date, '$gte': last_week_date}

                    results_with_mut_this_week = collection_db.count_documents(query_with_mut_this_week)

                    query_without_mut_this_week['muts'] = {'$not': {'$elemMatch': {
                        'pro': new_mut['pro'],
                        'loc': new_mut['loc'],
                        'alt': new_mut['alt'],
                        'org': new_mut['org'],
                    }
                    }
                    }
                    query_without_mut_this_week['collection_date'] = {'$lt': analysis_date, '$gte': last_week_date}

                    results_without_mut_this_week = collection_db.count_documents(query_without_mut_this_week)

                    denominator_this_week_with_mut = results_with_mut_this_week + results_without_mut_this_week

                    if denominator_this_week_with_mut != 0:
                        perc_with_mut_this_week = (
                                                          results_with_mut_this_week / denominator_this_week_with_mut) * 100
                    else:
                        perc_with_mut_this_week = 0

                    full_object = {f'{granularity}': location,
                                   'mut': mut,
                                   'muts': [new_mut],
                                   'count_with_mut_this_week': results_with_mut_this_week,
                                   'perc_with_mut_this_week': perc_with_mut_this_week,
                                   'count_without_mut_this_week': results_without_mut_this_week,
                                   'analysis_date': analysis_date.strftime("%Y-%m-%d"),
                                   'granularity': granularity,
                                   'location': location,
                                   'lineage': None
                                   }

                    array_results.append(full_object)

                else:
                    print('======> ERROR', mut)

        function2 = 'selectedMuts'
        result_dict = create_unique_array_results(array_results, datetime.strptime(date, '%Y-%m-%d'), array_date_2, function2)
        array_to_return = list(result_dict.values())
        end = timeit.default_timer()
        print("TIMER ", end - start)
        return array_to_return
