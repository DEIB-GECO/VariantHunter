"""

    DATA EXTRACTORS AND ANALYZER FOR LOCATIONS APIs
    These methods provide access points to the database for locations data

"""

import sqlite3

from ..utils.path_manager import db_path


def extract_location_id(location_name):
    """
    Given the name of a location, extract the identifier
    Args:
        location_name:  Location name specified using continent[/country[/region]] notation

    Returns:    Integer identifier for the location or None if not found

    """
    locs = location_name.split('/')
    locs_len = len(locs)

    con = sqlite3.connect(db_path)
    cur = con.cursor()

    if locs_len == 1:
        # Is a continent
        query = ''' SELECT CO.continent_id
                    FROM continents AS CO
                        JOIN locations AS CO_LO ON CO.continent_id=CO_LO.location_id
                    WHERE CO_LO.location=?;'''
    elif locs_len == 2:
        # Is a country
        query = ''' SELECT COU.country_id
                    FROM continents AS CO
                        JOIN locations AS CO_LO ON CO.continent_id=CO_LO.location_id
                        JOIN countries COU ON CO.continent_id = COU.continent_id
                        JOIN locations AS COU_LO ON COU.country_id=COU_LO.location_id
                    WHERE CO_LO.location=? AND COU_LO.location=?;'''
    else:
        # Is a region
        query = ''' SELECT RE.region_id
                    FROM continents AS CO
                        JOIN locations AS CO_LO ON CO.continent_id=CO_LO.location_id
                        JOIN countries COU ON CO.continent_id = COU.continent_id
                        JOIN locations AS COU_LO ON COU.country_id=COU_LO.location_id
                        JOIN regions RE ON RE.country_id = COU.country_id
                        JOIN locations AS RE_LO ON RE.region_id=RE_LO.location_id
                    WHERE CO_LO.location=? AND COU_LO.location=? AND RE_LO.location=?;'''
    location_id = cur.execute(query, locs).fetchone()

    con.close()
    return location_id[0] if location_id is not None else None


def extract_location_data(location):
    """
    Extract all the data of a given location
    Args:
        location:   Identifier of the location to be considered

    Returns:    A dictionary as follows
                {
                    'continent': { 'id': identifier,'text': continent name}
                    'country': null if the location is a continent, otherwise { 'id': identifier,'text': country name}
                    'region': null if the location is not a region, otherwise { 'id': identifier,'text': region name}
                }
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


def extract_locations(string):
    """
    Extract all the locations starting with or related to a given string
    Args:
        string:   String representing the name of a location. Possibly partially written.

    Returns:    List of dictionaries representing possible locations.
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
    """
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    locations = []
    params = {
        'first_w': string + '%',  # e.g., "Eu" will match "Europe"
        'middle_w': '% ' + string + '%'  # e.g., "Kin" will match "United Kingdom"
    }

    # Fetch continents starting with/containing string
    query = ''' SELECT LO.location AS cont_name, LO.location_id AS cont_id
                FROM locations AS LO JOIN continents AS CO ON LO.location_id=CO.continent_id
                WHERE (upper(LO.location) LIKE upper(:first_w)) OR (upper(LO.location) LIKE upper(:middle_w));'''
    locations.extend([
        {'value': {'id': x[1], 'text': x[0]},
         'type': 'continent',
         'country': None,
         'continent': None
         } for x in cur.execute(query, params).fetchall()])

    # Fetch countries starting with/containing string or having continent starting with/containing string
    query = ''' SELECT  LO.location AS cou_name, LO.location_id AS cou_id, 
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

    # Fetch regions starting with/containing string or having continent or country starting with/containing string
    query = ''' SELECT  LO.location AS reg_name, LO.location_id AS reg_id, 
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
