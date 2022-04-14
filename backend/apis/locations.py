"""

    APIs to retrieve locations data
    Endpoints:
    ├── getContinents: endpoint to get all the continents
    ├── getCountries: endpoint to get all the countries of given a continent
    └── getRegions: endpoint to get all the regions of given a country

"""

from __future__ import print_function

import sqlite3

from flask_restplus import Namespace, Resource

api = Namespace('locations', description='locations')
db_name = 'varianthunter.db'

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


def get_continents():
    """
    Fetch all the continents form the database
    @return:    An array of continents
    """
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    query = ''' SELECT location 
                FROM continents JOIN locations ON location_id = continent_id
                WHERE location is not null;'''
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
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    query = f'''    SELECT CTR.location 
                    FROM countries 
                        JOIN locations CTR ON CTR.location_id = country_id
                        JOIN locations CNT ON CNT.location_id = continent_id
                    WHERE CTR.location is not null AND CNT.location = '{continent}';'''
    countries = [x[0] for x in cur.execute(query).fetchall()]
    con.close()
    return countries


def get_regions(country):
    """
    Fetch all the regions of a specified country form the database
    @param country: The country to be considered
    @return:        An array of regions
    """
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    query = f'''    SELECT REG.location 
                    FROM regions 
                        JOIN locations REG ON REG.location_id = region_id
                        JOIN locations CTR ON CTR.location_id = country_id
                    WHERE REG.location is not null AND CTR.location = '{country}';'''
    regions = [x[0] for x in cur.execute(query).fetchall()]
    con.close()
    return regions


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
