"""

    APIS MIXINS
    General purpose functions shared by the APIs

"""
from datetime import datetime, timedelta

import numpy as np
import scipy.stats
import statsmodels.api as sm

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
    w['w4_end'] = (datetime.strptime(date, "%Y-%m-%d") - start_date).days  # end date (included) of the 4th week
    w['w4_begin'] = w['w4_end'] - 7     # day before the start of the 4th week
    w['w3_end'] = w['w4_begin']         # end date (included) of the 3rd week
    w['w3_begin'] = w['w3_end'] - 7     # day before the start of the 3rd week
    w['w2_end'] = w['w3_begin']         # end date (included) of the 2nd week
    w['w2_begin'] = w['w2_end'] - 7     # day before the start of the 2nd week
    w['w1_end'] = w['w2_begin']         # end date (included) of the 1st week
    w['w1_begin'] = w['w1_end'] - 7     # day before the start of the 1st week
    return w


def compute_diff_from_date(date):
    """
    Compute diff from the start_date from date
    Args:
        date: String representing the date to be considered. Takes format YYYY-mm-dd

    Returns: Difference from the start date

    """
    diff = (datetime.strptime(date, "%Y-%m-%d") - start_date).days
    return diff


def compute_date_from_diff(diff):
    """
    Compute date value from diff from the start_date
    Args:
        diff: Difference from the start date

    Returns: A string representing the date in format YYYY-mm-dd

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
        return scipy.stats.chi2_contingency(observed=[freq1, freq2])[1]
    except:
        return -1


def correct_pvalues(statistics):
    """
    Given a list of statistics including the values for the p-values, it corrects the p-values fot multiple tests
    Args:
        statistics: Dictionary including the p-values to be corrected

    Returns:    Statistics dictionary including the corrected p-values

    """
    uncorrected_p_vals = []
    for s in statistics:
        uncorrected_p_vals.extend([s['p_value_with_mut'], s['p_value_without_mut'], s['p_value_comp']])
    # Filter out cases where p-value is unknown (-1) or equal to 1.0 (avoid library exceptions)
    uncorrected_valid_p_vals = list(filter(lambda p_val: abs(p_val) != 1, uncorrected_p_vals))

    if len(uncorrected_valid_p_vals) > 0:
        corrected_p_vals = sm.stats.multipletests(pvals=uncorrected_valid_p_vals)[1]

        # Update statistics by replacing p-values
        idx = 0
        for s in statistics:
            if abs(uncorrected_p_vals[idx]) != 1:
                s['p_value_with_mut'] = corrected_p_vals[idx]
                idx += 1

            if abs(uncorrected_p_vals[idx]) != 1:
                s['p_value_without_mut'] = corrected_p_vals[idx]
                idx += 1

            if abs(uncorrected_p_vals[idx]) != 1:
                s['p_value_comp'] = corrected_p_vals[idx]
                idx += 1

    return statistics


def produce_statistics(week_sequence_counts, mutation_data):
    """
    Process the statistics values by properly formatting them into a list of dicts
    Args:
        week_sequence_counts:   Week sequences data
        mutation_data:          Mutation data

    Returns:    A list of the following form
                [
                    {
                        'item_key': row identifier obtained as protein_mut
                        'protein': name of the protein, example='NSP4'
                        'mut': name of the mutation, example='A146V'
                        'slope': slope computed through linear interpolation of the diffusion (percentage)
                        'f1': mutation diffusion in percentage during week 1
                        'f2': mutation diffusion in percentage during week 2
                        'f3': mutation diffusion in percentage during week 3
                        'f4': mutation diffusion in percentage during week 4
                        'w1': absolute number of sequences affected by the mutation during week 1
                        'w2': absolute number of sequences affected by the mutation during week 2
                        'w3': absolute number of sequences affected by the mutation during week 3
                        'w4': absolute number of sequences affected by the mutation during week 4
                        'p_value_with_mut': shows if the population «with mutation» is growing differently
                                            compared to everything (corrected for multiple tests)
                        'p_value_without_mut':  shows if the population «without mutation» is growing differently
                                                compared to everything (corrected for multiple tests)
                        'p_value_comp': shows if the population «with mutation» is growing differently
                                        compared to the population «without mutation» (corrected for multiple tests)
                    },...
                ]

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
            'item_key': mut,
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
    if len(statistics) > 0:
        statistics = correct_pvalues(statistics)

    return statistics
