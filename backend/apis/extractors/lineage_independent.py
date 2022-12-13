"""

    DATA EXTRACTORS AND ANALYZER FOR LINEAGE INDEPENDENT APIs
    These methods provide access points to the database for lineage independent analyses

"""

import sqlite3

from ..utils.path_manager import db_path


def extract_week_seq_counts(location, w, prot=None, mut=None):
    """
    Extract weekly sequence counts for the given location and weeks.
    If prot_mut is defined, then consider only sequences containing that mutation
    Args:
        location:   Identifier of the location to be considered
        w:          Dictionary describing the weeks to be considered
        prot:       If set, the counts consider only the sequences with a given protein
        mut:        If set, the counts consider only the sequences with a given mutation

    Returns:    Array containing for each of the 4 weeks, the total number of sequences
                matching the input parameters.
                [tot_week1, tot_week2, tot_week3, tot_week4]

    """
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    def extract_week_count(start, stop):
        if prot is not None and mut is not None:
            # Count the seq collected daily for a given week and location having a given prot_mut
            query = ''' SELECT sum(count)
                        FROM  aggr_aa_substitutions SB
                            JOIN proteins PR ON SB.protein_id = PR.protein_id
                        WHERE date > :start AND date <= :stop AND location_id = :loc_id
                            AND mut=:mut AND protein=:prot 
                        GROUP BY date, SB.location_id;'''
        else:
            # Count the seq collected daily for a given week and location
            query = ''' SELECT sum(count)
                        FROM  aggr_sequences SQ
                        WHERE date > :start AND date <= :stop AND location_id = :loc_id
                        GROUP BY date, SQ.location_id;'''
        params = {'start': start, 'stop': stop, 'loc_id': location, 'prot': prot, 'mut': mut}
        return sum([x[0] for x in cur.execute(query, params).fetchall()])  # sum daily counts within the week

    tot_seq_w4 = extract_week_count(w['w4_begin'], w['w4_end'])
    tot_seq_w3 = extract_week_count(w['w3_begin'], w['w3_end'])
    tot_seq_w2 = extract_week_count(w['w2_begin'], w['w2_end'])
    tot_seq_w1 = extract_week_count(w['w1_begin'], w['w1_end'])
    con.close()
    return [tot_seq_w1, tot_seq_w2, tot_seq_w3, tot_seq_w4]


def extract_mutation_data(location, w, min_sequences=0):
    """
    Extract weekly mutation data for the given location and weeks
    Args:
        location:       Identifier of the location to be considered
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
                        WHERE date > :start AND date <= :stop AND location_id = :loc_id
                        GROUP BY SB.protein_id, mut
                        {having_clause if is_target else ""};'''
        params = {'start': start, 'stop': stop, 'loc_id': location, 'min_seq': min_sequences}
        return {p + '_' + m: c for p, m, c in cur.execute(query, params).fetchall()}

    muts_w4 = extract_week_mutation(w['w4_begin'], w['w4_end'], is_target=True)  # extract muts having tot>min_seq
    muts_w3 = extract_week_mutation(w['w3_begin'], w['w3_end'])  # extract all muts
    muts_w2 = extract_week_mutation(w['w2_begin'], w['w2_end'])  # extract all muts
    muts_w1 = extract_week_mutation(w['w1_begin'], w['w1_end'])  # extract all muts
    con.close()
    return [muts_w1, muts_w2, muts_w3, muts_w4]


def extract_lineages_data(location, prot, mut, w):
    """
    Extract lineages data for the given location, prot_mut and weeks
    Args:
        location:   Identifier of the location to be considered
        prot:       String representing the protein to be considered
        mut:        String representing the mutation to be considered
        w:          Dictionary describing the weeks to be considered

    Returns:    List of dictionaries representing the lineages
                [
                    {
                        'name': lineage name
                        'f1': mutation diffusion in percentage during week 1 for the lineage
                        'f2': mutation diffusion in percentage during week 2 for the lineage
                        'f3': mutation diffusion in percentage during week 3 for the lineage
                        'f4': mutation diffusion in percentage during week 4 for the lineage
                        'w1': absolute number of sequences affected by the mutation during week 1 for the lineage
                        'w2': absolute number of sequences affected by the mutation during week 2 for the lineage
                        'w3': absolute number of sequences affected by the mutation during week 3 for the lineage
                    },...
                ]

    """
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    # Extract week seq counts for the mutation
    week_sequence_counts = extract_week_seq_counts(location, w, prot, mut)
    tot_seq_w1, tot_seq_w2, tot_seq_w3, tot_seq_w4 = week_sequence_counts

    def extract_all_lineages(start, stop):
        # Extract the lineages for the considered period, location, prot and mut
        query = f'''    SELECT DISTINCT SB.lineage_id, lineage
                        FROM aggr_aa_substitutions SB
                            JOIN lineages LN ON SB.lineage_id = LN.lineage_id
                            JOIN proteins PR ON SB.protein_id = PR.protein_id
                        WHERE date > :start AND date <= :stop AND location_id = :loc_id
                            AND mut=:mut AND protein=:prot
                        ORDER BY lineage;'''
        params = {'start': start, 'stop': stop, 'loc_id': location, 'prot': prot, 'mut': mut}
        return {k: v for k, v in cur.execute(query, params).fetchall()}

    def extract_week_info(lin_id, start, stop):
        # Extract the daily total number of mutations detected in the period and location associated
        # with the given lineage and mutation
        query = f'''    SELECT sum(count) 
                        FROM aggr_aa_substitutions SB
                            JOIN proteins PR ON SB.protein_id = PR.protein_id
                        WHERE date > :start AND date <= :stop AND location_id = :loc_id
                            AND lineage_id = :lin_id AND mut=:mut AND protein=:prot
                        GROUP BY date, SB.location_id, SB.protein_id, mut, lineage_id;'''
        params = {'start': start, 'stop': stop, 'loc_id': location, 'prot': prot, 'mut': mut, 'lin_id': lin_id}
        return sum([x[0] for x in cur.execute(query, params).fetchall()])  # sum daily counts within the week

    lineages = extract_all_lineages(w['w1_begin'], w['w4_end'])  # extract all the lineages in the period and location
    lineages_data = []

    # Iterate over the lineages
    for lineage_id, lineage_name in lineages.items():
        # Extracts the counts of the sequences, associated with the lineage, having the mutation, in the 4 weeks
        lin_w4 = extract_week_info(lineage_id, w['w4_begin'], w['w4_end'])
        lin_w3 = extract_week_info(lineage_id, w['w3_begin'], w['w3_end'])
        lin_w2 = extract_week_info(lineage_id, w['w2_begin'], w['w2_end'])
        lin_w1 = extract_week_info(lineage_id, w['w1_begin'], w['w1_end'])

        # Store the data in the final structure
        lineages_data.append({
            'name': lineage_name,
            # Frequencies
            'f1': (lin_w1 / tot_seq_w1) * 100 if tot_seq_w1 > 0 else 0,
            'f2': (lin_w2 / tot_seq_w2) * 100 if tot_seq_w2 > 0 else 0,
            'f3': (lin_w3 / tot_seq_w3) * 100 if tot_seq_w3 > 0 else 0,
            'f4': (lin_w4 / tot_seq_w4) * 100 if tot_seq_w4 > 0 else 0,
            # Absolute values
            'w1': lin_w1,
            'w2': lin_w2,
            'w3': lin_w3,
            'w4': lin_w4
        })

    con.close()
    return lineages_data
