"""

    APIS MIXINS
    General purpose functions shared by the APIs

"""

from datetime import datetime, timedelta

import numpy as np
import scipy.stats

start_date = datetime.strptime("2020-01-01", "%Y-%m-%d")
""" 
Reference date for database dates 
"""


def compute_weeks_from_date(date):
    """
    Compute weeks values starting from the date string of the last day of the 4th week
    Args:
        date: String representing the date of the last day of the 4th week

    Returns: A dictionary identifying all the 4 weeks

    """
    w = {}
    w['w4_end'] = (datetime.strptime(date, "%Y-%m-%d") - start_date).days
    w['w4_begin'] = w['w4_end'] - 7
    w['w3_end'] = w['w4_begin']
    w['w3_begin'] = w['w3_end'] - 7
    w['w2_end'] = w['w3_begin']
    w['w2_begin'] = w['w2_end'] - 7
    w['w1_end'] = w['w2_begin']
    w['w1_begin'] = w['w1_end'] - 7
    return w


def compute_diff_from_date(date):
    """
    Compute diff from the start_date from date
    Args:
        date: String representing the date to be considered

    Returns: Difference from the start date

    """
    diff = (datetime.strptime(date, "%Y-%m-%d") - start_date).days
    return diff


def compute_date_from_diff(diff):
    """
    Compute date value from diff from the start_date
    Args:
        diff: Difference from the start date

    Returns: A string representing the date

    """
    date = start_date + timedelta(days=diff)
    return date.strftime("%Y-%m-%d")


def compute_pvalue(freq1, freq2):
    """
    Compute p-value for the hypothesis test of independence of the observed frequencies
    Args:
        freq1:  Observed freq 1
        freq2:  Observed freq 2

    Returns: The computed p-value

    """
    try:
        return scipy.stats.chi2_contingency([freq1, freq2])[1]
    except:
        return "NaN"


def produce_statistics(location, week_sequence_counts, mutation_data):
    """
    Process the statistics values by properly formatting them
    Args:
        location:               Location name
        week_sequence_counts:   Week sequences data
        mutation_data:          Mutation data

    Returns:    An array of statistics

    """
    statistics = []
    tot_seq_w1, tot_seq_w2, tot_seq_w3, tot_seq_w4 = week_sequence_counts
    mut_w1, mut_w2, mut_w3, mut_w4 = mutation_data

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

    return statistics
