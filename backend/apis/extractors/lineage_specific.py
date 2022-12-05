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
    The possible lineages are those having sequences in the period and location
    Args:
        location:   Identifier of the location to be considered
        date:       String representing the (ending) date of the 4-weeks period to be considered.

    Returns: A list of lineage names

    """
    stop = (datetime.strptime(date, "%Y-%m-%d") - start_date).days  # date to day-diff conversion
    start = stop - 7

    con = sqlite3.connect(db_path)
    cur = con.cursor()
    query = '''    SELECT DISTINCT lineage 
                    FROM aggr_sequences SQ
                        JOIN lineages LN ON SQ.lineage_id = LN.lineage_id
                    WHERE date > :start AND date <= :stop AND location_id = :loc_id
                    ORDER BY lineage;'''
    params = {'start': start, 'stop': stop, 'loc_id': location}
    extracted_lineages = [x[0] for x in cur.execute(query, params).fetchall()]

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


def extract_week_seq_counts(location, lineage, w):
    """
    Extract weekly sequence counts for the given location, lineage and weeks
    Args:
        location:   Identifier of the location to be considered
        lineage:    String representing the lineage to be considered
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
                    WHERE date > :start AND date <= :stop AND location_id = :loc_id AND lineage = :lineage
                    GROUP BY date, SQ.location_id, SQ.lineage_id;'''
        params = {'start': start, 'stop': stop, 'loc_id': location, 'lineage': lineage}
        return sum([x[0] for x in cur.execute(query, params).fetchall()])  # sum daily counts within the week

    tot_seq_w4 = extract_week_count(w['w4_begin'], w['w4_end'])
    tot_seq_w3 = extract_week_count(w['w3_begin'], w['w3_end'])
    tot_seq_w2 = extract_week_count(w['w2_begin'], w['w2_end'])
    tot_seq_w1 = extract_week_count(w['w1_begin'], w['w1_end'])
    con.close()
    return [tot_seq_w1, tot_seq_w2, tot_seq_w3, tot_seq_w4]


def extract_mutation_data(location, lineage, w, min_sequences=0):
    """
    Extract weekly mutation data for the given location, lineage and weeks
    Args:
        location:       Identifier of the location to be considered
        lineage:        String representing the lineage to be considered
        w:              Dictionary describing the weeks to be considered
        min_sequences:  Minimum number of sequence required for the mutations appearing in week 4
                        to be considered in the result

    Returns: A list describing the mutations for each week

    """
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    def extract_week_mutation(start, stop, is_target=False):
        having_clause = "HAVING sum(count) >= :min_seq"
        query = f'''    SELECT protein, mut, sum(count) 
                        FROM aggr_aa_substitutions SB
                            JOIN proteins PR ON SB.protein_id = PR.protein_id
                            JOIN lineages LN ON SB.lineage_id = LN.lineage_id
                        WHERE date > :start AND date <= :stop AND location_id = :loc_id
                            AND lineage = :lineage
                        GROUP BY SB.protein_id, mut 
                        {having_clause if is_target else ""};'''
        params = {'start': start, 'stop': stop, 'loc_id': location, 'lineage': lineage, 'min_seq': min_sequences}
        return {p + '_' + m: c for p, m, c in cur.execute(query, params).fetchall()}

    muts_w4 = extract_week_mutation(w['w4_begin'], w['w4_end'], is_target=True)  # extract muts having tot>min_seq
    muts_w3 = extract_week_mutation(w['w3_begin'], w['w3_end'])  # extract all muts
    muts_w2 = extract_week_mutation(w['w2_begin'], w['w2_end'])  # extract all muts
    muts_w1 = extract_week_mutation(w['w1_begin'], w['w1_end'])  # extract all muts
    con.close()
    return [muts_w1, muts_w2, muts_w3, muts_w4]
