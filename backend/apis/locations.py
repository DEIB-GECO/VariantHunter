"""

    LOCATIONS MANAGER APIS @ /locations
    These APIs provide access to geographic data from locations
    whose sequencing data are analyzable by Variant Hunter

"""

import time

from flask import request
from flask_restplus import Namespace, Resource

from .extractors.locations import extract_locations

api = Namespace(name='Locations manager', path='/locations')


# #####################################################################################
# ##############################   [GET] /getLocations   ##############################
# #####################################################################################

@api.route('/getLocations')
class FieldList(Resource):
    @api.doc()
    def get(self):
        """
        API to get list of geographic areas (regions, countries, or continents) associated
        with a given text string.

        Query params:
        - string (string):  Name of location. Possibly partial for autocompletion.

        Success response (code 200):
            List of dictionaries representing possible locations.
            [
                {  'value': {
                        'id': integer location identifier,
                        'text': string representing the location name
                    },
                    'type': either 'region', 'country' or 'continent'
                    'continent': null if type=='continent', otherwise {
                        'id': integer identifier for the continent of the location,
                        'text': string representing the continent name of the location
                    }
                    'country': null if type!=='region', otherwise {
                        'id': integer identifier for the country of the location,
                        'text': string representing the country name of the location
                    }
                }, ...
            ]

        Error responses
        # code 423: Resource unavailable: dataset update in progress
        # code 500: Generic server error

        """
        exec_start = time.time()
        args = request.args
        args.to_dict()

        locations = extract_locations(args.get('string'))
        print(f'\t[GET] /getLocations: processed in {time.time() - exec_start:.5f} seconds.')
        return locations
