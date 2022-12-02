"""

    APIs to retrieve locations data
    Endpoints:
    └── getLocations: endpoint to get the locations

"""

import sqlite3
import time

from flask import request
from flask_restplus import Namespace, Resource

from .utils.path_manager import db_path

api = Namespace('locations', description='locations')

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


def get_location_data(location):
    """
    Fetch all the data of a given location
    """
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    query = '''
                SELECT  LO.location AS reg_name, LO.location_id AS reg_id, 
                        COU.location AS cou_name, COU.location_id AS cou_id,
                        CON.location AS cont_name, CON.location_id AS cont_id
                FROM locations AS LO
                JOIN regions AS RE ON LO.location_id=RE.region_id
                JOIN locations AS COU ON COU.location_id=RE.country_id
                JOIN countries AS CC ON CC.country_id=RE.country_id
                JOIN locations AS CON ON CON.location_id=CC.continent_id
                WHERE LO.location_id=:loc
                UNION
                SELECT  null AS reg_name, null AS reg_id, 
                        LO.location AS cou_name, LO.location_id AS cou_id,
                        CON.location AS cont_name, CON.location_id AS cont_id
                FROM locations AS LO
                JOIN countries AS CO ON LO.location_id=CO.country_id
                JOIN locations AS CON ON CON.location_id=CO.continent_id
                WHERE LO.location_id=:loc
                UNION
                SELECT  null AS reg_name, null AS reg_id, 
                        null AS cou_name, null AS cou_id,
                        LO.location AS cont_name, LO.location_id AS cont_id
                FROM locations AS LO JOIN continents AS CO ON LO.location_id=CO.continent_id
                WHERE LO.location_id=:loc
            '''
    data = cur.execute(query, {'loc': location}).fetchone()

    con.close()
    return {
        'region': {'id': data[1], 'text': data[0]} if data[0] is not None else None,
        'country': {'id': data[3], 'text': data[2]} if data[2] is not None else None,
        'continent': {'id': data[5], 'text': data[4]}}


def get_locations(string):
    """
    Fetch all the locations starting with a given string
    """
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    locations = []
    params = {
        'first_w': string + '%',  # e.g., "Eu" will match "Europe"
        'middle_w': '% ' + string + '%'  # e.g., "Kin" will match "United Kingdom"
    }

    # Fetch continents
    query = f'''    SELECT LO.location AS cont_name, LO.location_id AS cont_id
                    FROM locations AS LO JOIN continents AS CO ON LO.location_id=CO.continent_id
                    WHERE (upper(LO.location) LIKE upper(:first_w)) OR (upper(LO.location) LIKE upper(:middle_w));'''
    locations.extend([
        {'value': {'id': x[1], 'text': x[0]},
         'type': 'continent',
         'country': None,
         'continent': None
         } for x in cur.execute(query, params).fetchall()])

    # Fetch countries
    query = f'''    SELECT  LO.location AS cou_name, LO.location_id AS cou_id, 
                            CON.location AS cont_name, CON.location_id AS cont_id
                    FROM locations AS LO
                    JOIN countries AS CO ON LO.location_id=CO.country_id
                    JOIN locations AS CON ON CON.location_id=CO.continent_id
                    WHERE (upper(LO.location) LIKE upper(:first_w)) OR (upper(LO.location) LIKE upper(:middle_w)) 
                    OR (upper(CON.location) LIKE upper(:first_w)) OR (upper(CON.location) LIKE upper(:middle_w));'''
    locations.extend([
        {'value': {'id': x[1], 'text': x[0]},
         'type': 'country',
         'country': None,
         'continent': {'id': x[3], 'text': x[2]}
         } for x in cur.execute(query, params).fetchall()])

    # Fetch regions
    query = f'''    SELECT  LO.location AS reg_name, LO.location_id AS reg_id, 
                            COU.location AS cou_name, COU.location_id AS cou_id,
                            CON.location AS cont_name, CON.location_id AS cont_id
                    FROM locations AS LO
                    JOIN regions AS RE ON LO.location_id=RE.region_id
                    JOIN locations AS COU ON COU.location_id=RE.country_id
                    JOIN countries AS CC ON CC.country_id=RE.country_id
                    JOIN locations AS CON ON CON.location_id=CC.continent_id
                    WHERE (upper(LO.location) LIKE upper(:first_w)) OR (upper(LO.location) LIKE upper(:middle_w)) 
                    OR (upper(COU.location) LIKE upper(:first_w)) OR (upper(COU.location) LIKE upper(:middle_w)) 
                    OR (upper(CON.location) LIKE upper(:first_w)) OR (upper(CON.location) LIKE upper(:middle_w));'''
    locations.extend([
        {'value': {'id': x[1], 'text': x[0]},
         'type': 'region',
         'country': {'id': x[3], 'text': x[2]},
         'continent': {'id': x[5], 'text': x[4]}
         } for x in cur.execute(query, params).fetchall()])

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
        exec_start = time.time()

        args = request.args
        args.to_dict()
        locations = get_locations(args.get('string'))

        print(f'\t[GET] /getLocations: processed in {time.time() - exec_start:.5f} seconds.')

        return locations
