from __future__ import print_function

from datetime import datetime
from flask_restplus import Namespace
from pymongo import MongoClient

import os
import sys
import timeit

import json

import re

# download geo_group dictionary
import urllib.request

from sys import argv
import argparse

file_path = argv[1]
location_db = argv[2]
date_db = argv[3]
print("file name: ", file_path, location_db, date_db)

api = Namespace('create_database', description='create_database')

url = 'https://raw.githubusercontent.com/DEIB-GECO/virusurf_downloader/master/geo_groups.py'
urllib.request.urlretrieve(url, 'geo_groups.py')

# definitions for location split

prov_in_parentheses = re.compile(r'.*\((.+)\).*')

# pattern to split mutation
PATTERN = re.compile("([a-zA-Z0-9]+)_([a-zA-Z]+)([\d]+)([a-zA-Z]+)")
FULL_DATE_PATTERN = re.compile("^(\d\d\d\d)-(\d\d?)-(\d\d?)$")
MONTH_DATE_PATTERN = re.compile("^\d\d\d\d-\d\d$")
YEAR_DATE_PATTERN = re.compile("^\d\d\d\d?$")

geo_groups = {
    'angola': 'Africa',
    'burkina faso': 'Africa',
    'burundi': 'Africa',
    'benin': 'Africa',
    'botswana': 'Africa',
    'democratic republic of congo': 'Africa',
    'democratic republic of the congo': 'Africa',
    'republic of the congo': 'Africa',
    'zaire': 'Africa',
    'central african republic': 'Africa',
    'congo': 'Africa',
    'cote d\'ivoire': 'Africa',
    'cameroon': 'Africa',
    'cape verde': 'Africa',
    'djibouti': 'Africa',
    'algeria': 'Africa',
    'egypt': 'Africa',
    'western sahara': 'Africa',
    'eritrea': 'Africa',
    'ethiopia': 'Africa',
    'gabon': 'Africa',
    'ghana': 'Africa',
    'gambia': 'Africa',
    'guinea': 'Africa',
    'equatorial guinea': 'Africa',
    'guinea-bissau': 'Africa',
    'kenya': 'Africa',
    'comoros': 'Africa',
    'liberia': 'Africa',
    'lesotho': 'Africa',
    'libyan arab jamahiriya': 'Africa',
    'morocco': 'Africa',
    'madagascar': 'Africa',
    'mali': 'Africa',
    'mauritania': 'Africa',
    'mauritius': 'Africa',
    'malawi': 'Africa',
    'mozambique': 'Africa',
    'namibia': 'Africa',
    'niger': 'Africa',
    'nigeria': 'Africa',
'reunion': 'Africa',
    'rwanda': 'Africa',
    'seychelles': 'Africa',
    'sudan': 'Africa',
    'south sudan': 'Africa',
    'st. helena': 'Africa',
    'sierra leone': 'Africa',
    'senegal': 'Africa',
    'somalia': 'Africa',
    'sao tome and principe': 'Africa',
    'swaziland': 'Africa',
    'chad': 'Africa',
    'togo': 'Africa',
    'tunisia': 'Africa',
    'tanzania, united republic of': 'Africa',
    'tanzania': 'Africa',
    'uganda': 'Africa',
    'mayotte': 'Africa',
    'south africa': 'Africa',
    'zambia': 'Africa',
    'zimbabwe': 'Africa',
    'antarctica': 'Antartica',
    'bouvet island': 'Antartica',
    'south georgia and the south sandwich islands': 'Antartica',
    'heard and mc donald islands': 'Antartica',
    'french southern territories': 'Antartica',
    'united arab emirates': 'Asia',
    'afghanistan': 'Asia',
    # 'armenia': 'Asia',
    # 'azerbaijan': 'Asia',
    'bangladesh': 'Asia',
    'bahrain': 'Asia',
    'borneo': 'Asia',
    'brunei darussalam': 'Asia',
    'brunei': 'Asia',
    'bhutan': 'Asia',
    'cocos (keeling) islands': 'Asia',
    'china': 'Asia',
    'christmas island': 'Asia',
    # 'cyprus': 'Asia',
# 'georgia': 'Asia',
    'east timor': 'Asia',
    'timor-leste': 'Asia',
    'hong kong': 'Asia',
    'indonesia': 'Asia',
    'israel': 'Asia',
    'india': 'Asia',
    'british indian ocean territory': 'Asia',
    'iraq': 'Asia',
    'iran (islamic republic of)': 'Asia',
    'iran': 'Asia',
    'jordan': 'Asia',
    'japan': 'Asia',
    'kyrgyzstan': 'Asia',
    'cambodia': 'Asia',
    'north korea': 'Asia',
    'south korea': 'Asia',
    'korea, republic of': 'Asia',
    'kuwait': 'Asia',
    # 'kazakhstan': 'Asia',
    'lao people\'s democratic republic': 'Asia',
    'laos': 'Asia',
    'lebanon': 'Asia',
    'sri lanka': 'Asia',
    'myanmar': 'Asia',
    'mongolia': 'Asia',
    'macau': 'Asia',
    'maldives': 'Asia',
    'malaysia': 'Asia',
    'nepal': 'Asia',
    'oman': 'Asia',
    'philippines': 'Asia',
    'pakistan': 'Asia',
    'qatar': 'Asia',
    # 'russian federation': 'Asia',
    'saudi arabia': 'Asia',
    'singapore': 'Asia',
    'syrian arab republic': 'Asia',
    'thailand': 'Asia',
    'tajikistan': 'Asia',
    'turkmenistan': 'Asia',
# 'turkey': 'Asia',
    'taiwan': 'Asia',
    'uzbekistan': 'Asia',
    'viet nam': 'Asia',
    'west bank': 'Asia',
    'yemen': 'Asia',
    'andorra': 'Europe',
    'albania': 'Europe',
    'armenia': 'Europe, Asia',  # It's a transcontinental country
    'austria': 'Europe',
    'azerbaijan': 'Europe, Asia',  # It's a transcontinental country
    'bosnia and herzegovina': 'Europe',
    'belgium': 'Europe',
    'bulgaria': 'Europe',
    'belarus': 'Europe',
    'switzerland': 'Europe',
    'cyprus': 'Europe, Asia',  # It's a transcontinental country
    'czech republic': 'Europe',
    'germany': 'Europe',
    'denmark': 'Europe',
    'estonia': 'Europe',
    'spain': 'Europe',
    'finland': 'Europe',
    'faroe islands': 'Europe',
    'france': 'Europe',
    'united kingdom': 'Europe',
    'georgia': 'Europe, Asia',  # It's a transcontinental country
    'gibraltar': 'Europe',
    'greece': 'Europe',
    'croatia': 'Europe',
    'hungary': 'Europe',
    'ireland': 'Europe',
    'iceland': 'Europe',
    'italy': 'Europe',
    'kazakhstan': 'Europe, Asia',  # It's a transcontinental country
    'liechtenstein': 'Europe',
    'lithuania': 'Europe',
    'luxembourg': 'Europe',
    'latvia': 'Europe',
    'monaco': 'Europe',
    'moldova, republic of': 'Europe',
'macedonia': 'Europe',
    'malta': 'Europe',
    'netherlands': 'Europe',
    'norway': 'Europe',
    'poland': 'Europe',
    'portugal': 'Europe',
    'romania': 'Europe',
    'russian federation': 'Europe, Asia',  # It's a transcontinental country
    'russia': 'Europe, Asia',
    'serbia': 'Europe',
    'republic of serbia': 'Europe',
    'sweden': 'Europe',
    'slovenia': 'Europe',
    'svalbard and jan mayen islands': 'Europe',
    'slovak republic': 'Europe',
    'san marino': 'Europe',
    'turkey': 'Europe, Asia',  # It's a transcontinental country
    'ukraine': 'Europe',
    'vatican city state (holy see)': 'Europe',
    'antigua and barbuda': 'North America',
    'anguilla': 'North America',
    'netherlands antilles': 'North America',
    'aruba': 'North America',
    'barbados': 'North America',
    'bermuda': 'North America',
    'bahamas': 'North America',
    'belize': 'North America',
    'canada': 'North America',
    'costa rica': 'North America',
    'cuba': 'North America',
    'dominica': 'North America',
    'dominican republic': 'North America',
    'grenada': 'North America',
    'greenland': 'North America',
    'guadeloupe': 'North America',
    'guatemala': 'North America',
    'honduras': 'North America',
    'haiti': 'North America',
    'jamaica': 'North America',
    'saint kitts and nevis': 'North America',
'grenada': 'North America',
    'greenland': 'North America',
    'guadeloupe': 'North America',
    'guatemala': 'North America',
    'honduras': 'North America',
    'haiti': 'North America',
    'jamaica': 'North America',
    'saint kitts and nevis': 'North America',
    'saint-barthelemy': 'North America',
    'saint barthelemy': 'North America',
    'cayman islands': 'North America',
    'saint lucia': 'North America',
    'martinique': 'North America',
    'montserrat': 'North America',
    'mexico': 'North America',
    'nicaragua': 'North America',
    'panama': 'North America',
    'st. pierre and miquelon': 'North America',
    'puerto rico': 'North America',
    'el salvador': 'North America',
    'turks and caicos islands': 'North America',
    'trinidad and tobago': 'North America',
    'united states minor outlying islands': 'North America, Oceania',  # It's a transcontinental country
    'united states': 'North America',
    'usa': 'North America',
    'saint vincent and the grenadines': 'North America',
    'virgin islands (british)': 'North America',
    'virgin islands (u.s.)': 'North America',
    'british virgin islands': 'North America',
    'virgin islands': 'North America',
    'american samoa': 'Oceania',
    'australia': 'Oceania',
    'cook islands': 'Oceania',
    'fiji': 'Oceania',
    'micronesia, federated states of': 'Oceania',
    'micronesia': 'Oceania',
    'guam': 'Oceania',
'kiribati': 'Oceania',
    'marshall islands': 'Oceania',
    'northern mariana islands': 'Oceania',
    'new caledonia': 'Oceania',
    'norfolk island': 'Oceania',
    'nauru': 'Oceania',
    'niue': 'Oceania',
    'new zealand': 'Oceania',
    'french polynesia': 'Oceania',
    'papua new guinea': 'Oceania',
    'pitcairn': 'Oceania',
    'palau': 'Oceania',
    'solomon islands': 'Oceania',
    'tokelau': 'Oceania',
    'tonga': 'Oceania',
    'tuvalu': 'Oceania',
    # 'united states minor outlying islands': 'Oceania',
    'vanuatu': 'Oceania',
    'wallis and futuna islands': 'Oceania',
    'wallis and futuna': 'Oceania',
    'samoa': 'Oceania',
    'argentina': 'South America',
    'bolivia': 'South America',
    'brazil': 'South America',
    'chile': 'South America',
    'colombia': 'South America',
    'ecuador': 'South America',
    'falkland islands (malvinas)': 'South America',
    'french guiana': 'South America',
    'guyana': 'South America',
    'peru': 'South America',
    'paraguay': 'South America',
    'suriname': 'South America',
    'uruguay': 'South America',
    'venezuela': 'South America',
}


prov_in_parentheses = re.compile(r'.*\((.+)\).*')


def strip_or_none(string_or_none):
    if string_or_none is not None:
        return string_or_none.strip()
    else:
        return None


# taken from https://raw.githubusercontent.com/DEIB-GECO/virusurf_downloader/master/data_sources/gisaid_sars_cov_2/sample.py
def province__region__country__geo_group(covv_location):
    province, region, country, geo_group = None, None, None, None
    try:
        split_locations = [x.strip() for x in covv_location.split('/')]
        geo_group = split_locations[0]
        country = split_locations[1]
        region = split_locations[2]
        province = split_locations[3]
    except KeyError:
        pass
    except IndexError:
        pass
    #  assign geo group based on the country but use the provided geo_group as fallback value
    geo_group = strip_or_none(geo_group)
    if country:
        country = country.strip()
        geo_group = geo_groups.get(country.lower(), geo_group)
    else:
        country = None

    # clean-up region
    if region:
        region = region.strip()
        if region.endswith('r.'):
            region = region.replace('r.', '')
    else:
        region = None

    # clean-up province
    if province:
        province_has_parentheses = prov_in_parentheses.match(province)
        # if it has parentheses, take what's inside
        if province_has_parentheses:
            province = province_has_parentheses.group(1).strip()
        else:
            # take left part of string if comma is present
            province = province.split(',')[0]
            # replace _ with spaces
            # remove trailing/leading spaces
            province = province.replace('_', ' ').strip().lower()
            province = province.replace('co.', 'county')
        province = province.capitalize()

    return province, region, country, geo_group


def correct_country(country):
    if country:
        return country.title() \
            .replace('And', 'and') \
            .replace('The', 'the') \
            .replace('Of', 'of') \
            .replace("D'Ivoire", "d'Ivoire") \
            .replace('Usa', 'USA')
    else:
        return None


def insert_single_line(line):
    d = json.loads(line)
    d['_id'] = d['covv_accession_id']

    # split location
    province, region, country, geo_group = province__region__country__geo_group(d['covv_location'])
    country = correct_country(country)
    location = {'geo_group': geo_group, 'country': country, 'region': region, 'province': province}
    d['location'] = location
    # print(location)

    muts = d['covsurver_prot_mutations']
    if muts:
        if muts.startswith("(") and muts.endswith(")"):
            muts = muts[1:-1]
        #                 print(muts)
        else:
            print("==========> ERROR covsurver_prot_mutations doesn't contains ():", line, file=sys.stderr,
                  flush=True)
            pass

    #  mutation list
    new_muts = []
    if muts:
        for mut in muts.split(","):
            #                     print(mut)
            m = PATTERN.fullmatch(mut)
            #                     print(m)
            if m:
                protein, orig, loc, alt = m.groups()
                orig = orig.replace('stop', '*')
                alt = alt.replace('stop', '*')

                loc = int(loc)
                if orig == 'ins':
                    orig = '-' * len(alt)
                    t = 'INS'
                elif alt == 'del':
                    alt = '-'
                    t = 'DEL'
                else:
                    t = 'SUB'

                l = len(alt)

                #                         new_mut = {'pr': protein, 'org': orig, 'loc':loc, 'alt':alt}
                new_mut = {'pro': protein, 'org': orig,
                           'loc': loc, 'alt': alt,
                           'typ': t, 'len': l}
                new_muts.append(new_mut)
            else:
                #                         ADD BETTER ERROR
                print('==========> ERROR IN A MUTATION:', mut, 'ACESSIONID:', d['_id'], file=sys.stderr,
                      flush=True)
    #                         print('INPUT LINE OF THE PROBLEM:', line, file=sys.stderr)
    #                         assert(False)
    #                         pass

    d['muts'] = new_muts
    #             d['mutations'] = new_muts

    #           DATES
    covv_subm_date = d['covv_subm_date']
    m = FULL_DATE_PATTERN.fullmatch(covv_subm_date)
    if m:
        year, month, day = (int(x) for x in m.groups())
        # d['subm_date'] = {"$date": f"{year:04d}-{month:02d}-{day:02d}T00:00:00Z"}
        d['subm_date'] = datetime.strptime(f"{year:04d}-{month:02d}-{day:02d}", '%Y-%m-%d')
    else:
        d['subm_date'] = None
        print('==========> ERROR IN covv_subm_date:', covv_subm_date, 'ACESSIONID:', d['_id'], file=sys.stderr)

    covv_collection_date = d['covv_collection_date']
    m = FULL_DATE_PATTERN.fullmatch(covv_collection_date)
    if m:
        year, month, day = (int(x) for x in m.groups())
        # d['collection_date'] = {"$date": f"{year:04d}-{month:02d}-{day:02d}T00:00:00Z"}
        d['collection_date'] = datetime.strptime(f"{year:04d}-{month:02d}-{day:02d}", '%Y-%m-%d')
        d['c_coll_date_prec'] = 2
    elif MONTH_DATE_PATTERN.fullmatch(covv_collection_date):
        d['collection_date'] = None
        d['c_coll_date_prec'] = 1
    elif YEAR_DATE_PATTERN.fullmatch(covv_collection_date):
        d['collection_date'] = None
        d['c_coll_date_prec'] = 0
    else:
        d['collection_date'] = None
        d['c_coll_date_prec'] = -1
        print('==========> ERROR IN covv_collection_date:', covv_collection_date, 'ACESSIONID:', d['_id'],
              file=sys.stderr)

    #             pangolin_lineages_version
    pangolin_lineages_version = d['pangolin_lineages_version']
    m = FULL_DATE_PATTERN.fullmatch(pangolin_lineages_version)
    if m:
        year, month, day = (int(x) for x in m.groups())
        # d['pangolin_version'] = {"$date": f"{year:04d}-{month:02d}-{day:02d}T00:00:00Z"}
        d['pangolin_version'] = datetime.strptime(f"{year:04d}-{month:02d}-{day:02d}", '%Y-%m-%d')
    else:
        print('==========> ERROR IN pangolin_lineages_version:', pangolin_lineages_version, 'ACESSIONID:',
              d['_id'], file=sys.stderr)
        d['pangolin_version'] = None

    out = d
    return out


def insert_in_database():

    myclient = MongoClient(host='test_mongodb',
                           port=27017,
                           username='root',
                           password='pass',
                           authSource="admin")
    mydb = myclient["viruclust_db"]
    mydb.db_meta.drop()
    mycol = mydb["db_meta"]

    mydict = {
        "_id": 'viruclust_db_0',
        "collection_name": "viruclust_db_0",
        "date": datetime.today()
    }

    mycol.insert_one(mydict)

    mydb.viruclust_db_0.drop()
    mycol2 = mydb["viruclust_db_0"]

    filename = 'export.json'

    f = open(f"{filename}", 'r')

    try:
        # i = 0
        for line in f:
            # i = i + 1
            # print("INSERT: ", i)
            s1 = json.dumps(line)
            d = json.loads(s1)
            mydict2 = insert_single_line(d)
            mycol2.insert_one(mydict2)
        end = timeit.default_timer()
        print("TIMER ", end - start)

        resp = mycol2.create_index(
            [
                ("c_coll_date_prec", 1),
                ("collection_date", 1)
            ]
        )

        resp = mycol2.create_index(
            [
                ("collection_date", 1),
            ]
        )

        resp = mycol2.create_index(
            [
                ("c_coll_date_prec", 1),
            ]
        )

        resp = mycol2.create_index(
            [
                ("covv_lineage", 1),
            ]
        )

        resp = mycol2.create_index(
            [
                ("location.geo_group", 1),
            ]
        )

        resp = mycol2.create_index(
            [
                ("location.country", 1),
            ]
        )

        resp = mycol2.create_index(
            [
                ("location.province", 1),
            ]
        )

        resp = mycol2.create_index(
            [
                ("location.region", 1),
            ]
        )

        resp = mycol2.create_index(
            [
                ("muts.pro", 1),
            ]
        )

        resp = mycol2.create_index(
            [
                ("muts.org", 1),
            ]
        )

        resp = mycol2.create_index(
            [
                ("muts.loc", 1),
            ]
        )

        resp = mycol2.create_index(
            [
                ("muts.alt", 1),
            ]
        )

    except BrokenPipeError:
        devnull = os.open(os.devnull, os.O_WRONLY)
        os.dup2(devnull, sys.stdout.fileno())
        pass
    finally:
        sys.stdout.flush()
        sys.stderr.flush()
        f.close()


def insert_single_line_tsv(line):
    d = line
    d['_id'] = d['Accession ID']

    d['covv_accession_id'] = d['Accession ID']
    d['covv_lineage'] = d['Pango lineage']

    province, region, country, geo_group = province__region__country__geo_group(d['Location'])
    country = correct_country(country)
    location = {'geo_group': geo_group, 'country': country, 'region': region, 'province': province}
    d['location'] = location

    muts = d['AA Substitutions']
    d['covsurver_prot_mutations'] = d['AA Substitutions']
    if muts:
        if muts.startswith("(") and muts.endswith(")"):
            muts = muts[1:-1]
        else:
            print("==========> ERROR AA Substitutions doesn't contains ():", line, file=sys.stderr,
                  flush=True)
            pass

    #  mutation list
    new_muts = []
    if muts:
        for mut in muts.split(","):
            m = PATTERN.fullmatch(mut)
            if m:
                protein, orig, loc, alt = m.groups()
                orig = orig.replace('stop', '*')
                alt = alt.replace('stop', '*')

                loc = int(loc)
                if orig == 'ins':
                    orig = '-' * len(alt)
                    t = 'INS'
                elif alt == 'del':
                    alt = '-'
                    t = 'DEL'
                else:
                    t = 'SUB'

                l = len(alt)

                new_mut = {'pro': protein, 'org': orig,
                           'loc': loc, 'alt': alt,
                           'typ': t, 'len': l}
                new_muts.append(new_mut)
            else:
                #                         ADD BETTER ERROR
                print('==========> ERROR IN A MUTATION:', mut, 'ACESSIONID:', d['_id'], file=sys.stderr,
                      flush=True)

    d['muts'] = new_muts
    covv_subm_date = d['Submission date']
    m = FULL_DATE_PATTERN.fullmatch(covv_subm_date)
    if m:
        year, month, day = (int(x) for x in m.groups())
        d['subm_date'] = datetime.strptime(f"{year:04d}-{month:02d}-{day:02d}", '%Y-%m-%d')
    else:
        d['subm_date'] = None
        print('==========> ERROR IN covv_subm_date:', covv_subm_date, 'ACESSIONID:', d['_id'], file=sys.stderr)

    covv_collection_date = d['Collection date']
    m = FULL_DATE_PATTERN.fullmatch(covv_collection_date)
    if m:
        year, month, day = (int(x) for x in m.groups())
        d['collection_date'] = datetime.strptime(f"{year:04d}-{month:02d}-{day:02d}", '%Y-%m-%d')
        d['c_coll_date_prec'] = 2
    elif MONTH_DATE_PATTERN.fullmatch(covv_collection_date):
        d['collection_date'] = None
        d['c_coll_date_prec'] = 1
    elif YEAR_DATE_PATTERN.fullmatch(covv_collection_date):
        d['collection_date'] = None
        d['c_coll_date_prec'] = 0
    else:
        d['collection_date'] = None
        d['c_coll_date_prec'] = -1
        print('==========> ERROR IN covv_collection_date:', covv_collection_date, 'ACESSIONID:', d['_id'],
              file=sys.stderr)

    #             pangolin_lineages_version
    pangolin_lineages_version = d['Pangolin version']
    m = FULL_DATE_PATTERN.fullmatch(pangolin_lineages_version)
    if m:
        year, month, day = (int(x) for x in m.groups())
        d['pangolin_version'] = datetime.strptime(f"{year:04d}-{month:02d}-{day:02d}", '%Y-%m-%d')
    else:
        print('==========> ERROR IN pangolin_lineages_version:', pangolin_lineages_version, 'ACESSIONID:',
              d['_id'], file=sys.stderr)
        d['pangolin_version'] = None

    out = d
    return out


def insert_in_database_tsv():
    myclient = MongoClient(host='test_mongodb',
                           port=27017,
                           username='root',
                           password='pass',
                           authSource="admin")
    mydb = myclient["viruclust_db"]
    mydb.db_meta.drop()
    mycol = mydb["db_meta"]

    mydict = {
        "_id": 'viruclust_db_0',
        "collection_name": "viruclust_db_0",
        "date": datetime.today()
    }

    mycol.insert_one(mydict)

    real_file_path = '/backend/app/database/' + file_path

    f = open(f"{real_file_path}", 'r')

    a = f.readline()
    titles = [t.strip() for t in a.split('\t')]

    mydb.viruclust_db_0.drop()
    mycol2 = mydb["viruclust_db_0"]

    len_file = sum(1 for line in open(f"{real_file_path}", 'r'))
    kk = 0
    last_perc = 0
    for line in f:
        kk = kk + 1
        num_file_perc = (kk / len_file) * 100
        int_num_file_perc = int(num_file_perc)
        if (int_num_file_perc % 5) == 0 and int_num_file_perc != last_perc:
            print("database --> ", int_num_file_perc, " % ")
            last_perc = int_num_file_perc

        d = {}
        for t, f in zip(titles, line.split('\t')):
            d[t] = f.strip()
        date_db_translated = datetime.strptime(date_db, '%Y-%m-%d')
        date_precision = d['Collection date'].count('-')
        if date_precision == 0:
            date_single_line_db = datetime.strptime(d['Collection date'], '%Y')
        elif date_precision == 1:
            date_single_line_db = datetime.strptime(d['Collection date'], '%Y-%m')
        else:
            date_single_line_db = datetime.strptime(d['Collection date'], '%Y-%m-%d')
        if (location_db.lower() in d['Location'].lower() or location_db.lower() == 'world') \
                and date_single_line_db >= date_db_translated:
            mydict2 = insert_single_line_tsv(d)
            mycol2.insert_one(mydict2)
    end = timeit.default_timer()
    print("DATABASE UPDATE ENDED (TIMER: ", end - start, ' )')

    resp = mycol2.create_index(
        [
            ("c_coll_date_prec", 1),
            ("collection_date", 1)
        ]
    )

    resp = mycol2.create_index(
        [
            ("collection_date", 1),
        ]
    )

    resp = mycol2.create_index(
        [
            ("c_coll_date_prec", 1),
        ]
    )

    resp = mycol2.create_index(
        [
            ("covv_lineage", 1),
        ]
    )

    resp = mycol2.create_index(
        [
            ("location.geo_group", 1),
        ]
    )

    resp = mycol2.create_index(
        [
            ("location.country", 1),
        ]
    )

    resp = mycol2.create_index(
        [
            ("location.province", 1),
        ]
    )

    resp = mycol2.create_index(
        [
            ("location.region", 1),
        ]
    )

    resp = mycol2.create_index(
        [
            ("muts.pro", 1),
        ]
    )

    resp = mycol2.create_index(
        [
            ("muts.org", 1),
        ]
    )

    resp = mycol2.create_index(
        [
            ("muts.loc", 1),
        ]
    )

    resp = mycol2.create_index(
        [
            ("muts.alt", 1),
        ]
    )


start = timeit.default_timer()
# insert_in_database()
insert_in_database_tsv()

# from os import listdir
# from os.path import isfile, join
# onlyfiles = [f for f in listdir('/backend/app/database') if isfile(join('/backend/app/database', f))]
# print("FILES: ", onlyfiles)

# f = open(f"/backend/app/database.json", 'r')
