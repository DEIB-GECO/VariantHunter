"""

    APIs to retrieve locations data
    Endpoints:
    ├── getContinents: endpoint to get all the continents
    ├── getCountries: endpoint to get all the countries of given a continent
    ├── getRegions: endpoint to get all the regions of given a country
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


def get_continents():
    """
    Fetch all the continents form the database
    @return:    An array of continents
    """
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    query = ''' SELECT location 
                FROM continents JOIN locations ON location_id = continent_id
                WHERE location is not null
                ORDER BY location;'''
    continents = [x[0] for x in cur.execute(query).fetchall()]
    con.close()
    return continents


all_continents = get_continents()  # At server startup, fetch all the continents


def get_countries(continent):
    """
    Fetch all the countries of a specified continent form the database
    @param continent:   The continent to be considered
    @return:            An array of countries
    """
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    query = f'''    SELECT CTR.location 
                    FROM countries 
                        JOIN locations CTR ON CTR.location_id = country_id
                        JOIN locations CNT ON CNT.location_id = continent_id
                    WHERE CTR.location is not null AND CNT.location = '{continent}'
                    ORDER BY CTR.location;'''
    countries = [x[0] for x in cur.execute(query).fetchall()]
    con.close()
    return countries


def get_regions(country):
    """
    Fetch all the regions of a specified country form the database
    @param country: The country to be considered
    @return:        An array of regions
    """
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    query = f'''    SELECT REG.location 
                    FROM regions 
                        JOIN locations REG ON REG.location_id = region_id
                        JOIN locations CTR ON CTR.location_id = country_id
                    WHERE REG.location is not null AND CTR.location = '{country}'
                    ORDER BY REG.location;'''
    regions = [x[0] for x in cur.execute(query).fetchall()]
    con.close()
    return regions


def get_locations(o_string):
    """
    Fetch all the locations starting with a given string
    """
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    locations = []
    params = {
        'first_w': o_string + '%',  # e.g., "Eu" will match "Europe"
        'middle_w': '% ' + o_string + '%'   # e.g., "Kin" will match "United Kingdom"
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


@api.route('/getContinents')
class FieldList(Resource):
    @api.doc('get_continents')
    def get(self):
        """
        Endpoint to get all the continents
        @return:    An array of continents
        """
        return all_continents


@api.route('/getCountries')
class FieldList(Resource):
    @api.doc('get_countries')
    def post(self):
        """
        Endpoint to get all the countries of given a continent
        @return:    An array of countries
        """
        countries = get_countries(api.payload['continent'])
        return countries


@api.route('/getRegions')
class FieldList(Resource):
    @api.doc('get_regions')
    def post(self):
        """
        Endpoint to get all the regions of given a country
        @return:    An array of regions
        """
        regions = get_regions(api.payload['country'])
        return regions


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
