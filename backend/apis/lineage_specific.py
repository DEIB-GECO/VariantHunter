"""

    LINEAGE SPECIFIC ANALYSIS APIS @ /lineage_specific
    These APIs provide lineage-specific analysis.

"""

import time

from flask import request
from flask_restplus import Namespace, Resource

from .extractors.explorer import extract_lineage_characterization, extract_dataset_info
from .extractors.lineage_specific import get_all_lineages, get_lineages_from_loc, get_lineages_from_loc_date, \
    extract_week_seq_counts, extract_mutation_data, parse_lineages
from .extractors.locations import extract_location_data, extract_location_id
from .utils.utils import compute_weeks_from_date, produce_statistics

api = Namespace(name='Lineage specific analysis', path='/lineage_specific')


# ############################################################################################
# ##################################   [GET] /getLineages   ##################################
# ############################################################################################


@api.route('/getLineages')
class FieldList(Resource):
    @api.doc()
    def get(self):
        """
        API to get list of possible lineages. Possibly filtered by location and week.

        Query params:
        - location (int):   Location identifier. Possibly not specified.
        - date (string):    End date (included) of the week to be considered. Takes format YYYY-mm-dd.
                            Possibly not specified, unless location is specified.

        Success response (code 200):
            Object containing lineages info
            {
                possible_lineages: ['BA.1','BA.2',...]  List of lineage names
                availability:   dictionary describing the availability in the specified period and location,
                                None if at least one between location or date is None.
                                { 'lineage_name': int_num_sequence }
            }

        Error responses
        # code 423: Resource unavailable: dataset update in progress
        # code 500: Generic server error

        """
        exec_start = time.time()
        args = request.args
        location = args.get('location')
        date = args.get('date')

        if (location is None and date is None) or (location == '' and date == ''):
            lineages_data = {'possible_lineages': get_all_lineages()}
        elif date is None:
            lineages_data = {'possible_lineages': get_lineages_from_loc(location)}
        else:
            lineages_data = get_lineages_from_loc_date(location, date)

        print(f'\t[GET] /getLineages: processed in {time.time() - exec_start:.5f} seconds.')
        return lineages_data


# #############################################################################################
# #################################   [GET] /getStatistics   ##################################
# #############################################################################################


@api.route('/getStatistics')
class FieldList(Resource):
    @api.doc()
    def get(self):
        """
        API to perform a lineage-specific analysis. Given a location, a 4-week period,
        and a lineage, it extracts the mutations present in the last week of the period
        and analyzes their trend over the 4 weeks.

        Query params:
        - location (int):           Location identifier
        - locationName (string):    Location name specified using continent[/country[/region]] notation
                                    (used in alternative to location, when the id is not known)
        - date (string):            End date of the 4-weeks period to be considered. Takes format YYYY-mm-dd
        - lineages (list):          List of lineage names to be considered (both specific and in star-notation)

        Success response (code 200):
            Dictionary containing the statistics
            {
                'characterizing_muts':  List of mutations characterizing the selected lineage if only one lineage is selected.
                                        (i.e.,mutations affecting at least 50% of the lineage sequences). [] otherwise.
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
                    'lineage': {
                        'items': list of well-defined selected lineages,
                        'groups': list of selected lineages in star notation,
                        'groups_items': list of well-defined lineages associated with those in 'groups'
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
        if location is None:
            location_name = args.get('locationName')
            location = extract_location_id(location_name)
        lineages = args.getlist('lineages')
        date = args.get('date')

        w = compute_weeks_from_date(date)

        # parse lineages data
        items, groups, lineages = parse_lineages(location, w['w4_end'], lineages)

        week_sequence_counts = extract_week_seq_counts(location, lineages, w)

        min_sequences = int(week_sequence_counts[-1] * 0.005 + 1)
        mutation_data = extract_mutation_data(location, lineages, w, min_sequences)

        statistics = produce_statistics(week_sequence_counts, mutation_data)
        # Compute char muts only if one lineage has been selected, otherwise disable feature.
        characterizing_muts = extract_lineage_characterization(lineages) if len(lineages) == 1 else []

        metadata = {
            'date': date,
            'location': extract_location_data(location),
            'lineage': {'items': items, 'groups': groups},
            'dataset_info': extract_dataset_info()
        }

        print(f'\t[GET] /getStatistics: processed in {time.time() - exec_start:.5f} seconds.')
        return {'rows': statistics,
                'tot_seq': week_sequence_counts,
                'characterizing_muts': characterizing_muts,
                'metadata': metadata}
