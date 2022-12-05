"""

    LINEAGE INDEPENDENT ANALYSIS APIS @ /lineage_independent
    These APIs provide lineage-independent analysis.

"""

import time

from flask import request
from flask_restplus import Namespace, Resource

from .explorer import extract_dataset_info
from .extractors.lineage_independent import extract_week_seq_counts, extract_mutation_data, extract_lineages_data
from .extractors.locations import extract_location_data
from .utils.utils import compute_weeks_from_date, produce_statistics

api = Namespace(name='Lineage independent analysis',path='/lineage_independent')

# ##############################################################################################
# ##################################   [GET] /getStatistics   ##################################
# ##############################################################################################


@api.route('/getStatistics')
class FieldList(Resource):
    @api.doc()
    def get(self):
        """
        API to perform a lineage-independent analysis. Given a location and a 4-week period,
        it extracts the mutations present in the last week of the period and analyzes their trend
        over the 4 weeks.

        Query params:
        - location (int):   Location identifier
        - date (string):    End date of the 4-weeks period to be considered. Takes format YYYY-mm-dd

        Success response (code 200):
           Dictionary containing the statistics
           {
                'metadata': {
                    'dataset_info': {
                        'last_update': date of the most recent sequence in the database. Takes format YYYY-mm-dd.
                        'file_type': provider of the dataset. Either 'gisaid' or 'nextstrain'
                        'filtered_countries': list of countries the dataset has been restricted to, 'all' otherwise
                        'begin_date': start date of the time period the dataset was restricted to, 'beginning' otherwise
                        'end_date': end date of the time period the dataset was restricted to, 'end' otherwise
                        'parsed_on': date on which the dataset was uploaded to VariantHunter. Takes format YYYY-mm-dd
                        'version': running backend version of VariantHunter
                    },
                    'date': end date of the 4-weeks period to be considered. Takes format YYYY-mm-dd
                    'location': {
                        'continent':
                            { 'id': identifier,'text': continent name}
                        'country': null if the location is a continent, otherwise
                            { 'id': identifier,'text': country name}
                        'region': null if the location is not a region, otherwise
                            { 'id': identifier,'text': region name}
                    },
                },
                'rows': [
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
                ],
                'tot_seq':  List reporting for each of the 4 weeks the total number of sequences
                            collected for that period and location (if defined).
                            [ tot_seq_week1,tot_seq_week2,tot_seq_week3,tot_seq_week4]
           }

        Error responses
        # code 423: Resource unavailable: dataset update in progress
        # code 500: Generic server error

        """
        exec_start = time.time()
        args = request.args
        location = args.get('location')
        date = args.get('date')

        w = compute_weeks_from_date(date)

        week_sequence_counts = extract_week_seq_counts(location, w)

        min_sequences = int(week_sequence_counts[-1] * 0.005 + 1)  # 0.5% of seq in the last week
        mutation_data = extract_mutation_data(location, w, min_sequences)

        statistics = produce_statistics(week_sequence_counts, mutation_data)

        metadata = {
            'date': date,
            'location': extract_location_data(location),
            'dataset_info': extract_dataset_info()
        }

        print(f'\t[GET] /getStatistics: processed in {time.time() - exec_start:.5f} seconds.')
        return {'rows': statistics,
                'tot_seq': week_sequence_counts,
                'metadata': metadata}


# ################################################################################################
# ###############################   [GET] /getLineagesStatistics   ###############################
# ################################################################################################


@api.route('/getLineagesStatistics')
class FieldList(Resource):
    @api.doc()
    def get(self):
        """
        API to obtain the decomposition over lineages of the sequences of a given mutation,
        location and period.

        Query params:
        - location (int):   Location identifier
        - date (string):    End date of the 4-weeks period to be considered. Takes format YYYY-mm-dd
        - protein (string): Protein name
        - mut (string):     Mutation name

        Success response (code 200):
            List of dictionaries representing the lineages
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

        Error responses
        # code 423: Resource unavailable: dataset update in progress
        # code 500: Generic server error

        """
        exec_start = time.time()
        args = request.args
        location = args.get('location')
        date = args.get('date')
        prot = args.get('prot')
        mut = args.get('mut')

        w = compute_weeks_from_date(date)
        lineage_data = extract_lineages_data(location, prot, mut, w)

        print(f'\t[GET] /getLineagesStatistics: processed in {time.time() - exec_start:.5f} seconds.')
        return lineage_data
