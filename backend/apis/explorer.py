"""

    DATASET EXPLORATION APIS @ /explorer
    These APIs provide dataset exploration capabilities.
    They allow the extraction of information about the quantity of sequences,
    the distribution of sequences over lineages, and other metadata of the dataset

"""

import time

from flask import request
from flask_restplus import Namespace, Resource

from .extractors.explorer import extract_seq_num, extract_lineage_characterization, extract_dataset_info, \
    extract_lineage_breakdown, extract_mutation_history, extract_characterized_lineages
from .utils.utils import compute_diff_from_date

api = Namespace(name='Dataset exploration', path='/explorer')


# ######################################################################################
# #############################   [GET] /getSequenceInfo   #############################
# ######################################################################################


@api.route('/getSequenceInfo')
class FieldList(Resource):
    @api.doc()
    def get(self):
        """
        API to obtain information regarding the number of sequences collected
        for a given location and possibly a specific lineage.

        Query params:
        - location (int):   Location identifier
        - lineage (string): Lineage name

        Success response (code 200):
            List of dictionaries representing the sequences.
            [
                {
                    'date':         number of days since the reference date
                    'seq_count':    number of sequences collected in the day for the specified parameters
                }, ...
            ]

        Error responses
        # code 423: Resource unavailable: dataset update in progress
        # code 500: Generic server error

        """
        exec_start = time.time()
        args = request.args
        location = args.get('location')
        lineage = args.get('lineage')

        info = extract_seq_num(location, lineage)
        print(f'\t[GET] /getSequenceInfo: processed in {time.time() - exec_start:.5f} seconds.')
        return info


# #######################################################################################
# ###########################   [GET] /getLineagesBreakdown   ###########################
# #######################################################################################


@api.route('/getLineagesBreakdown')
class FieldList(Resource):
    @api.doc()
    def get(self):
        """
        API to obtain information regarding the distribution over lineage of
        the sequences of a given location for a specified time interval.

        Query params:
        - location (int):   Location identifier
        - begin (string):   Start date of the period to be considered. Takes format YYYY-mm-dd.
        - end (string):     End date of the period to be considered. Takes format YYYY-mm-dd.

        Success response (code 200):
            The response object is a hashmap with lineage names as the key and an object as
            the value. That object is a hashmap that has the days (defined as the number
            of days since the reference date) as the key and the number of sequences assigned
            to that lineage collected on that day as the value.
            For each day, only lineages that affected at least 10% of the collected sequences
            on that date are considered; the others are counted under 'Others'.
            Example: {'BA.5':{'876':1, '878':3}, ... ,'Others':{'873':14, '874':3}}

        Error responses
        # code 423: Resource unavailable: dataset update in progress
        # code 500: Generic server error

        """
        exec_start = time.time()
        args = request.args
        location = args.get('location')
        period = {
            'begin': compute_diff_from_date(args.get('begin')) + 1,
            'end': compute_diff_from_date(args.get('end')),
        }

        info = extract_lineage_breakdown(location, period)
        print(f'\t[GET] /getLineagesBreakdown: processed in {time.time() - exec_start:.5f} seconds.')
        return info


# #######################################################################################
# ##############################   [GET] /getDatasetInfo   ##############################
# #######################################################################################


@api.route('/getDatasetInfo')
class FieldList(Resource):
    @api.doc()
    def get(self):
        """
        API to obtain information regarding the dataset in use

        Query params:
        - string (string):  Name of location. Possibly partial for autocompletion.

        Success response (code 200):
            {
                'last_update': date of the most recent sequence in the database. Takes format YYYY-mm-dd.
                'file_type': provider of the dataset. Either 'gisaid' or 'nextstrain'
                'filtered_countries': list of countries the dataset has been restricted to, 'all' otherwise
                'begin_date': start date of the time period the dataset was restricted to, 'beginning' otherwise
                'end_date': end date of the time period the dataset was restricted to, 'end' otherwise
                'parsed_on': date on which the dataset was uploaded to VariantHunter. Takes format YYYY-mm-dd
                'version': running backend version of VariantHunter
            }

        Error responses
        # code 423: Resource unavailable: dataset update in progress
        # code 500: Generic server error

        """
        exec_start = time.time()

        data = extract_dataset_info()
        print(f'\t[GET] /getDatasetInfo: processed in {time.time() - exec_start:.5f} seconds.')
        return data


# #######################################################################################
# ######################   [GET] /getLineagesCharacteristics   ##########################
# #######################################################################################


@api.route('/getLineagesCharacteristics')
class FieldList(Resource):
    @api.doc()
    def get(self):
        """
        API to obtain the list of characterizing mutations for a given list of lineages.
        A mutation is defined as characterizing if it affects at least 50% of the lineage sequences.

        Query params:
        - lineages (list):  List of lineages names

        Success response (code 200):
            List of characterizing mutation for the lineages

        Error responses
        # code 423: Resource unavailable: dataset update in progress
        # code 500: Generic server error

        """
        exec_start = time.time()
        args = request.args
        lineages = args.getlist('lineages')

        characterization = extract_lineage_characterization(lineages)
        print(f"\t[GET] /getLineagesCharacteristics: processed in {time.time() - exec_start:.5f} seconds.")
        return characterization


# ######################################################################################
# #############################   [GET] /getSequenceInfo   #############################
# ######################################################################################


@api.route('/getMutationHistory')
class FieldList(Resource):
    @api.doc()
    def get(self):
        """
        API to obtain information regarding a given mutation

        Query params:
        - protein (string): Protein name
        - mut (string):     Mutation name

        Success response (code 200):
            {
                'characterized_lineages':   list of all lineages that have been characterized by the
                                            given mutation (such that at least 50 percent of the lineage
                                            sequences have the mutation)
                'history':  hashmap in which: keys are names of lineages in which the mutation was found;
                            values are objects of the form {abs, percentage} representing the number of
                            sequences in absolute value and percentage.
                            Example: {'BA.2':{'abs':12, 'percentage':53.4},...}

        Error responses
        # code 423: Resource unavailable: dataset update in progress
        # code 500: Generic server error

        """

        exec_start = time.time()
        args = request.args
        protein = args.get('protein')
        mut = args.get('mut')

        mutation_history = extract_mutation_history(prot=protein, mut=mut)
        characterized_lineages = extract_characterized_lineages(prot=protein, mut=mut)

        print(f'\t[GET] /getMutationHistory: processed in {time.time() - exec_start:.5f} seconds.')
        return {'history': mutation_history, 'characterized_lineages': characterized_lineages}
