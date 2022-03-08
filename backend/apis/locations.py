"""
    API to retrieve locations data

    Endpoints:
    ├── getContinents
    ├── getCountries
    └── getRegions
"""

from __future__ import print_function
import sqlite3
from flask_restplus import Namespace, Resource

api = Namespace('locations', description='locations')
sqlite_db_name = 'varianthunter.db'


def get_continents():
    """
    Fetch all the continents form the database
    @return:    An array of continents
    """
    con = sqlite3.connect(sqlite_db_name)
    cur = con.cursor()
    query = "select continent from continent_table where continent is not null;"
    continents = [x[0] for x in cur.execute(query).fetchall()]
    con.close()
    return continents


def get_countries(continent):
    """
    Fetch all the countries of a specified continent form the database
    @param continent:   The continent to be considered
    @return:            An array of countries
    """
    con = sqlite3.connect(sqlite_db_name)
    cur = con.cursor()
    query = f'''select country from country_table where country is not null and continent='{continent}';'''
    countries = [x[0] for x in cur.execute(query).fetchall()]
    con.close()
    return countries


def get_regions(country):
    """
    Fetch all the regions of a specified country form the database
    @param country: The country to be considered
    @return:        An array of regions
    """
    con = sqlite3.connect(sqlite_db_name)
    cur = con.cursor()
    query = f'''select region from region_table where region is not null and country='{country}';'''
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
        Endpoint to get the continents
        @return:    An array of continents
        """
        continents = get_continents()
        return continents


@api.route('/getCountries')
class FieldList(Resource):
    @api.doc('get_countries')
    def post(self):
        """
        Endpoint to get the countries given a continent
        @return:    An array of countries
        """
        countries = get_countries(api.payload['continent'])
        return countries


@api.route('/getRegions')
class FieldList(Resource):
    @api.doc('get_regions')
    def post(self):
        """
        Endpoint to get the regions given a country
        @return:    An array of regions
        """
        regions = get_regions(api.payload['country'])
        return regions
