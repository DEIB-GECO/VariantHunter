"""

    DATA EXTRACTORS AND ANALYZER FOR EXPLORER APIs
    These methods provide access points to the database for dataset exploration capabilities

"""

import sqlite3

from ..utils.path_manager import db_path
from ..utils.utils import compute_date_from_diff


def extract_seq_num(location, lineages):
    """
    Extract from the database the sequence count for the selected location and lineage
    Args:
        location:   The location identifier to be considered
        lineages:   The list of lineage names to be considered

    Returns:    List of dictionaries representing the sequences.
                [
                    {
                        'date':         number of days since the reference date
                        'seq_count':    number of sequences collected in the day for the specified parameters
                    }, ...
                ]

    """
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    def execute_query():
        params = [location]
        if lineages is not None and len(lineages) > 0:
            # Count how many seq have been collected for each day, matching given location and lineage
            query = ''' SELECT date,sum(count) 
                        FROM aggr_sequences SQ
                            JOIN lineages LN ON SQ.lineage_id = LN.lineage_id
                        WHERE location_id = ? AND
                            lineage IN (%s) ''' % ("?," * len(lineages))[:-1] + '''
                        GROUP BY date;'''
            params.extend(lineages)
        else:
            # Count how many seq have been collected for each day, matching given location
            query = ''' SELECT date,sum(count) 
                        FROM aggr_sequences SQ
                        WHERE location_id = ?
                        GROUP BY date;'''
        seqs = cur.execute(query, params).fetchall()
        return [{'date': x[0], 'seq_count': x[1]} for x in seqs]

    daily_sequence_counts = execute_query()
    con.close()
    return daily_sequence_counts


def extract_lineage_breakdown(location, period):
    """
    Extract from the database the lineage breakdown info for the selected params
    Args:
        location:       The location identifier
        period:         Dictionary defining 'begin' and 'end' date

    Returns:    Hashmap with lineage names as the key and an object as
                the value. That object is a hashmap that has the days (defined as the number
                of days since the reference date) as the key and the number of sequences assigned
                to that lineage collected on that day as the value.
                For each day, only lineages that affected at least 10% of the collected sequences
                on that date are considered; the others are counted under 'Others'.
                Example: {'BA.5':{'876':1, '878':3}, ... ,'Others':{'873':14, '874':3}}

    """
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    def extract_lineages():
        # Extract lineages present in the given location and period
        query = ''' SELECT DISTINCT SQ.lineage_id, lineage
                    FROM aggr_sequences SQ
                        JOIN lineages LN ON SQ.lineage_id = LN.lineage_id
                    WHERE location_id=:loc_id AND date>=:begin AND date<=:end
                    ORDER BY lineage;'''
        res = cur.execute(query, {'loc_id': location, 'begin': period['begin'], 'end': period['end']}).fetchall()
        return {k: v for k, v in res}

    def extract_day_threshold(day):
        # Given a day, extracts how much is 10% of the sequences collected on that day
        query = ''' SELECT 0.10 * sum(count)
                    FROM aggr_sequences SQ
                    WHERE location_id=:loc_id AND date=:day;'''
        day_threshold = cur.execute(query, {'loc_id': location, 'day': day}).fetchone()
        return day_threshold[0] if day_threshold[0] is not None else 0

    def extract_lineage_data(lin_id, day):
        # Extracts the number of sequences associated with a given lineage on a given day,
        # for the location considered
        query = ''' SELECT sum(count)
                    FROM aggr_sequences SQ
                    WHERE lineage_id=:lin_id AND location_id=:loc_id and date=:day
                    GROUP BY date, lineage_id, SQ.location_id;'''
        day_count = cur.execute(query, {'lin_id': lin_id, 'loc_id': location, 'day': day}).fetchone()
        return day_count[0] if day_count is not None else 0

    lineages = extract_lineages()  # extract the lineages to be considered for the loc and period
    lineage_breakdown = {}
    # Iterate over the days in the considered period
    for date in range(period['begin'], period['end'] + 1):
        threshold = extract_day_threshold(date)  # extract minimum number of seq to appear in the result

        # Iterate over the lineages in the period
        for lineage_id, lineage_name in lineages.items():
            seq_count = extract_lineage_data(lineage_id, date)  # extract the count
            # Decide whether it appears as standalone or under others
            key = lineage_name if seq_count > threshold else 'Others'

            # Lineage already in the dictionary?
            if key in lineage_breakdown.keys():
                # Do we need to accumulate in 'Others'?
                if key == 'Others' and date in lineage_breakdown['Others'].keys():
                    lineage_breakdown[key][date] += seq_count
                else:
                    lineage_breakdown[key][date] = seq_count
            else:
                lineage_breakdown[key] = {date: seq_count}

    con.close()
    return lineage_breakdown


def extract_dataset_info():
    """
    Extract information about the dataset in use

    Returns:    A dictionary as follows
                {
                    'last_update': date of the most recent sequence in the database. Takes format YYYY-mm-dd.
                    'file_type': provider of the dataset. Either 'gisaid' or 'nextstrain'
                    'filtered_countries': list of countries the dataset has been restricted to, 'all' otherwise
                    'begin_date': start date of the time period the dataset was restricted to, 'beginning' otherwise
                    'end_date': end date of the time period the dataset was restricted to, 'end' otherwise
                    'parsed_on': date on which the dataset was uploaded to VariantHunter. Takes format YYYY-mm-dd
                    'version': running backend version of VariantHunter
                } 

    """
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    def extract_last_update():
        # Fetch date of the most recent sequence in the database
        query = ''' SELECT max(date) 
                    FROM aggr_sequences;'''
        diff = cur.execute(query).fetchone()[0]
        return compute_date_from_diff(diff) if diff is not None else None

    def extract_parsing_info():
        # Fetch metadata from info table
        query = ''' SELECT file_type, filtered_countries, beginning_date, end_date, parse_date, version
                    FROM  info;'''
        return cur.execute(query).fetchone()

    parsing_info = extract_parsing_info()  # extract metadata
    info = {
        'last_update': extract_last_update(),  # extract last sequence
        'file_type': parsing_info[0],
        'filtered_countries': parsing_info[1] if len(parsing_info[1]) > 0 else "all",
        'begin_date': parsing_info[2],
        'end_date': parsing_info[3],
        'parsed_on': parsing_info[4],
        'version': parsing_info[5]
    }

    con.close()
    return info


def extract_lineage_characterization(lineages):
    """
    Extracts the characterizing mutations of specified lineages.
    A mutation is defined as characterizing if it affects at least 50% of the lineage sequences.
    Args:
        lineages:   List of lineage names to be considered

    Returns:    List of characterizing mutation for the lineages

    """
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    def extract_muts_from_lineage():
        # Extract the mutations directly from the lineage_characteristics table
        query = ''' SELECT DISTINCT protein, mut
                    FROM lineages_characteristics LC
                        JOIN lineages LN ON LC.lineage_id = LN.lineage_id
                        JOIN proteins PR ON LC.protein_id = PR.protein_id
                    WHERE lineage in (%s) ''' % ("?," * len(lineages))[:-1] + '''
                    ORDER BY protein, mut;'''
        return [x[0] + '_' + x[1] for x in cur.execute(query, lineages).fetchall()]

    characterizing_muts = extract_muts_from_lineage()

    con.close()
    return characterizing_muts


def extract_characterized_lineages(prot, mut):
    """
    Given a protein_mutation pair it retrieves the lineages characterized by that pair
    Args:
        prot:   The name of the protein of interest
        mut:    The mutation of interest

    Returns:    List of all lineages that have been characterized by the given mutation 
                (such that at least 50 percent of the lineage sequences have the mutation)

    """
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    query = ''' SELECT L.lineage
                FROM lineages_characteristics AS LC
                    JOIN proteins AS P  ON P.protein_id=LC.protein_id
                    JOIN lineages AS L ON L.lineage_id=LC.lineage_id
                WHERE P.protein=:prot AND LC.mut=:mut
                ORDER BY  L.lineage;'''
    lineages = [lineage for [lineage] in cur.execute(query, {'prot': prot, 'mut': mut}).fetchall()]

    con.close()
    return lineages


def extract_mutation_history(prot, mut):
    """
    Given a protein_mutation pair it computes the percentage at which that pair appeared in each lineage, if >0.
    Args:
        prot:   The name of the protein of interest
        mut:    The mutation of interest

    Returns:    Hashmap in which: keys are names of lineages in which the mutation was found;
                values are objects of the form {abs, percentage} representing the number of
                sequences in absolute value and percentage.
                Example: {'BA.2':{'abs':12, 'percentage':53.4},...}

    """
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    # Extract the list of lineages and the number of seq having the given mutation
    query = ''' SELECT L.lineage, SUM(AA.count)
                FROM aggr_aa_substitutions AS AA
                    JOIN proteins AS P  ON P.protein_id = AA.protein_id
                    JOIN lineages AS L ON AA.lineage_id = L.lineage_id
                WHERE P.protein=:prot AND AA.mut=:mut
                GROUP BY L.lineage
                HAVING SUM(AA.count)>0
                ORDER BY SUM(AA.count) DESC ;'''

    history = {}
    total = 0
    for lineage, count in cur.execute(query, {'prot': prot, 'mut': mut}).fetchall():
        total += count  # accumulate total number of sequences having the mutation of interest
        history[lineage] = {'abs': count}

    # Compute the percentage of appearance
    for lineage in history:
        history[lineage]['percentage'] = 100 * history[lineage]['abs'] / total

    con.close()
    return history
