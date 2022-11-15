"""

    APIs to retrieve locations data
    Endpoints:
    └── getLocations: endpoint to get the locations

"""

import sqlite3
from flask import request
import time
from .utils.path_manager import db_path
from flask_restplus import Namespace, Resource

api = Namespace('locations', description='locations')

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


def get_locations(string):
    """
    Fetch all the locations starting with a given string
    """
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    locations = []
    params = {
        'first_w': string + '%',  # e.g., "Eu" will match "Europe"
        'middle_w': '% ' + string + '%'   # e.g., "Kin" will match "United Kingdom"
    }

    # Fetch continents
    query = f'''    SELECT LO.location
                    FROM locations AS LO JOIN continents AS CO ON LO.location_id=CO.continent_id
                    WHERE (upper(LO.location) LIKE upper(:first_w)) OR (upper(LO.location) LIKE upper(:middle_w));'''
    locations.extend([{'value': x[0], 'type': 'continent', 'country': None, 'continent': None} for x in
                      cur.execute(query, params).fetchall()])

    # Fetch countries
    query = f'''    SELECT LO.location, CON.location
                    FROM locations AS LO
                    JOIN countries AS CO ON LO.location_id=CO.country_id
                    JOIN locations AS CON ON CON.location_id=CO.continent_id
                    WHERE (upper(LO.location) LIKE upper(:first_w)) OR (upper(LO.location) LIKE upper(:middle_w)) 
                    OR (upper(CON.location) LIKE upper(:first_w)) OR (upper(CON.location) LIKE upper(:middle_w));'''
    locations.extend([{'value': x[0], 'type': 'country', 'country': None, 'continent': x[1]} for x in
                      cur.execute(query, params).fetchall()])

    # Fetch regions
    query = f'''    SELECT LO.location, COU.location, CON.location
                    FROM locations AS LO
                    JOIN regions AS RE ON LO.location_id=RE.region_id
                    JOIN locations AS COU ON COU.location_id=RE.country_id
                    JOIN countries AS CC ON CC.country_id=RE.country_id
                    JOIN locations AS CON ON CON.location_id=CC.continent_id
                    WHERE (upper(LO.location) LIKE upper(:first_w)) OR (upper(LO.location) LIKE upper(:middle_w)) 
                    OR (upper(COU.location) LIKE upper(:first_w)) OR (upper(COU.location) LIKE upper(:middle_w)) 
                    OR (upper(CON.location) LIKE upper(:first_w)) OR (upper(CON.location) LIKE upper(:middle_w));'''
    locations.extend([{'value': x[0], 'type': 'region', 'country': x[1], 'continent': x[2]} for x in
                      cur.execute(query, params).fetchall()])

    con.close()
    return locations


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""                             ENDPOINTS                               """""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

@api.route('/getLocations')
class FieldList(Resource):
    @api.doc('get_locations')
    def get(self):
        """
        Endpoint to get all the locations matching a given string
        @return:    An array of regions
        """
        print("\t /getLocations processing...", end="")
        exec_start = time.time()

        args = request.args
        args.to_dict()
        locations = get_locations(args.get('string'))

        print(f'done in {time.time() - exec_start:.5f} seconds.')
        return locations
