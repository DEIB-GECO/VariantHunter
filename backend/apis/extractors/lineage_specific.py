"""

    DATA EXTRACTORS AND ANALYZER FOR LINEAGE SPECIFIC APIs
    These methods provide access points to the database for lineage specific analyses

"""

import sqlite3
from datetime import datetime

from ..utils.path_manager import db_path
from ..utils.utils import start_date


def get_all_lineages():
    """
    Extract all the possible lineages

    Returns: A list of lineage names

    """
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    query = "SELECT lineage FROM lineages ORDER BY lineage;"
    extracted_lineages = [x[0] for x in cur.execute(query).fetchall()]

    con.close()
    return extracted_lineages


def get_lineages_from_loc_date(location, date):
    """
    Extract the possible lineages for a given location and period.
    The possible lineages are those having sequences for the specified location and last week of the period
    Args:
        location:   Identifier of the location to be considered
        date:       String representing the (ending) date of the 4-weeks period to be considered.

    Returns: Object containing lineages info
            {
                possible_lineages: ['BA.1','BA.2',...]  List of lineage names
                availability:   dictionary describing the availability in the specified period and location,
                                { 'lineage_name': int_num_sequence }
            }

    """
    stop = (datetime.strptime(date, "%Y-%m-%d") - start_date).days  # date to day-diff conversion
    start = stop - 7  # last week only, not the whole period!
    period_start = stop - 28

    con = sqlite3.connect(db_path)
    cur = con.cursor()
    query = '''     SELECT lineage, sum(count)
                    FROM aggr_sequences SQ
                        JOIN lineages LN ON SQ.lineage_id = LN.lineage_id
                    WHERE date > :period_start AND date <= :stop AND location_id = :loc_id
                            AND SQ.lineage_id IN (  SELECT DISTINCT SQ_I.lineage_id
                                                    FROM aggr_sequences AS SQ_I
                                                    WHERE SQ_I.date > :start AND SQ_I.date <= :stop 
                                                        AND SQ_I.location_id = :loc_id )
                    GROUP BY LN.lineage_id
                    ORDER BY lineage;'''
    params = {'start': start, 'stop': stop, 'loc_id': location, 'period_start': period_start}
    res = cur.execute(query, params).fetchall()
    extracted_lineages = {
        'possible_lineages': [x[0] for x in res],
        'availability': {x[0]: x[1] for x in res}
    }

    con.close()
    return extracted_lineages


def get_lineages_from_loc(location):
    """
    Extract the possible lineages for a given location.
    The possible lineages are those having sequences in the location
    Args:
        location:   Identifier of the location to be considered

    Returns: A list of lineage names

    """
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    query = ''' SELECT DISTINCT lineage 
                FROM aggr_sequences SQ
                    JOIN lineages LN ON SQ.lineage_id = LN.lineage_id
                WHERE location_id = :loc_id
                ORDER BY lineage;'''
    extracted_lineages = [x[0] for x in cur.execute(query, {'loc_id': location}).fetchall()]

    con.close()
    return extracted_lineages


def extract_week_seq_counts(location, lineages, w):
    """
    Extract weekly sequence counts for the given location, lineage and weeks
    Args:
        location:   Identifier of the location to be considered
        lineages:    List of string representing the lineages to be considered
        w:          Dictionary describing the weeks to be considered

    Returns:    Array containing for each of the 4 weeks, the total number of sequences
                matching the input parameters.
                [tot_week1, tot_week2, tot_week3, tot_week4]

    """
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    def extract_week_count(start, stop):
        # Count the seq collected daily for a given week, lineage and location
        query = ''' SELECT sum(count) 
                    FROM aggr_sequences SQ
                        JOIN lineages LN on SQ.lineage_id = LN.lineage_id
                    WHERE date > ? AND date <= ? AND location_id = ? 
                        AND lineage in (%s) ''' % ("?," * len(lineages))[:-1] + '''
                    GROUP BY date;'''
        params = [start, stop, location]
        params.extend(lineages)
        return sum([x[0] for x in cur.execute(query, params).fetchall()])  # sum daily counts within the week

    tot_seq_w4 = extract_week_count(w['w4_begin'], w['w4_end'])
    tot_seq_w3 = extract_week_count(w['w3_begin'], w['w3_end'])
    tot_seq_w2 = extract_week_count(w['w2_begin'], w['w2_end'])
    tot_seq_w1 = extract_week_count(w['w1_begin'], w['w1_end'])
    con.close()
    return [tot_seq_w1, tot_seq_w2, tot_seq_w3, tot_seq_w4]


def extract_mutation_data(location, lineages, w, min_sequences=0):
    """
    Extract weekly mutation data for the given location, lineage and weeks
    Args:
        location:       Identifier of the location to be considered
        lineages:        List of string representing the lineages to be considered
        w:              Dictionary describing the weeks to be considered
        min_sequences:  Minimum number of sequence required for the mutations appearing in week 4
                        to be considered in the result

    Returns: A list describing the mutations for each week

    """
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    def extract_week_mutation(start, stop, is_target=False):
        having_clause = "HAVING sum(count) >= ?"
        query = '''     SELECT protein, mut, sum(count) 
                        FROM aggr_aa_substitutions SB
                            JOIN proteins PR ON SB.protein_id = PR.protein_id
                            JOIN lineages LN ON SB.lineage_id = LN.lineage_id
                        WHERE date > ? AND date <= ? AND location_id = ?
                           AND lineage in (%s) ''' % ("?," * len(lineages))[:-1] + f'''
                        GROUP BY SB.protein_id, mut 
                        {having_clause if is_target else ""};'''
        params = [start, stop, location]
        params.extend(lineages)
        if is_target:
            params.append(min_sequences)
        return {p + '_' + m: c for p, m, c in cur.execute(query, params).fetchall()}

    muts_w4 = extract_week_mutation(w['w4_begin'], w['w4_end'], is_target=True)  # extract muts having tot>min_seq
    muts_w3 = extract_week_mutation(w['w3_begin'], w['w3_end'])  # extract all muts
    muts_w2 = extract_week_mutation(w['w2_begin'], w['w2_end'])  # extract all muts
    muts_w1 = extract_week_mutation(w['w1_begin'], w['w1_end'])  # extract all muts
    con.close()
    return [muts_w1, muts_w2, muts_w3, muts_w4]


def parse_lineages(location, stop, lineages):
    """
    Given a set of lineages possibly in star notation, it categorizes them in items, groups and all
    Args:
        location:       Identifier of the location to be considered
        stop:           End date (as diff from reference date) of the analysis period to be considered
        lineages:       List of string representing the lineages to be considered

    Returns: items, groups and all

    """
    items = list()  # well-defined lineages
    group_names = list()  # star-notation lineages
    groups = {}  # mapping star-notation lineages
    all_lineages = list()  # overall summary

    # Divide items (well-defined lineages) from groups (lineages in star notation)
    for el in lineages:
        if el[-1] != '*':
            items.append(el)
        else:
            group_names.append(el)
    items.sort()
    all_lineages.extend(items)

    # Compute the lineages of the group, if any
    if len(group_names) > 0:
        start = stop - 7  # last week only, not the whole period!

        con = sqlite3.connect(db_path)
        cur = con.cursor()
        for group in group_names:
            query = ''' SELECT DISTINCT LN.lineage
                        FROM aggr_sequences AS SQ
                            JOIN lineages LN ON SQ.lineage_id = LN.lineage_id 
                        WHERE SQ.date > :start AND SQ.date <= :stop AND SQ.location_id = :loc_id
                             AND (LN.lineage LIKE :group OR LN.lineage=:father)
                        ORDER BY LN.lineage; '''
            params = {'start': start, 'stop': stop, 'loc_id': location,
                      'group': group[:-2] + '.%', 'father': group[:-2]}
            res = [row[0] for row in cur.execute(query, params).fetchall()]
            all_lineages.extend(res)  # update summary
            groups[group] = res  # update mapping
        con.close()
    return items, groups, all_lineages
