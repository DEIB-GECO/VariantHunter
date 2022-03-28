from __future__ import print_function
import sqlite3
import sys
import time
from flask_restplus import Namespace

# Fetch the parameters: file path, selected countries and type (either gisaid or nextstrain)
from .parsers.GisaidParser import GisaidParser
from .parsers.NextstrainParser import NextstrainParser

file_path = sys.argv[1]
selected_countries = set([x.lower() for x in sys.argv[2].strip().split(',') if x])
if len(selected_countries)==1 and 'all' in selected_countries:
    selected_countries.clear()
file_type = sys.argv[3].lower().strip() if len(sys.argv) > 3 else 'gisaid'

api = Namespace('create_database', description='create_database')
db_name = 'varianthunter.db'


def create_database():
    """
    Creates and populates the database with the dataset passed as parameter

    """
    exec_start = time.time()
    print("> Starting database setup ...")

    with open(file_path) as f:
        con = sqlite3.connect(db_name)
        con.execute("pragma journal_mode=off;")
        con.execute("pragma locking_mode=EXCLUSIVE;")
        con.execute("pragma synchronous=OFF;")
        cur = con.cursor()

        # Check if tables already exist to skip database creation
        cur.execute(" SELECT count(name) FROM sqlite_master WHERE type='table' ")
        if cur.fetchone()[0] > 0:
            print('\t SKIPPED: database already exists.')
            return

        def run_query(query):
            cur.execute(query)
            con.commit()

        ###############################################################
        # Create all the tables
        print("\t STEP 1/4: Table creation...", end="")

        run_query('''   CREATE TABLE muts 
                        (date integer, lineage text, mut text, continent text, country text, region text )''')

        run_query('''   CREATE TABLE mutsg 
                        (date integer, lineage text, mut text, location text, count integer)''')

        run_query('''   CREATE TABLE timeloclin 
                        (date integer, continent text, country text, region text, lineage text)''')

        run_query('''   CREATE TABLE timelocling 
                        (date integer, location text, lineage text, count integer)''')

        run_query('''   CREATE TABLE continent_table 
                        (continent text)''')

        run_query('''   CREATE TABLE country_table 
                        (country text, continent text)''')

        run_query('''   CREATE TABLE region_table 
                        (region text, country text)''')

        run_query('''   CREATE TABLE lineage_table 
                        (lineage text)''')

        print(f'done in {time.time() - exec_start:.5f} seconds.')
        exec_start = time.time()

        ###############################################################
        # Parse the files and load the data into the tables
        print("\t STEP 2/4: Data extraction...", end="")

        if file_type == 'gisaid':
            print(" GISAID parsing...")
            parser = GisaidParser(con=con, f=f)
        else:
            print(" NEXTSTRAIN parsing...")
            parser = NextstrainParser(con, f)
        parser.parse(selected_countries)

        print(f'\t\tdone in {time.time() - exec_start:.5f} seconds.')
        exec_start = time.time()

        ###############################################################
        # Aggregate data
        print("\t STEP 3/4: Data aggregation...", end="")

        run_query('''   INSERT INTO mutsg 
                        SELECT date, lineage, mut, continent AS location, count(*) AS count 
                        FROM muts 
                        GROUP BY date, lineage, mut, continent;''')

        run_query('''   INSERT INTO mutsg 
                        SELECT date, lineage, mut, country AS location, count(*) AS count 
                        FROM muts 
                        GROUP BY date, lineage, mut, country;''')

        run_query('''   INSERT INTO mutsg 
                        SELECT date, lineage, mut, region AS location, count(*) AS count 
                        FROM muts 
                        GROUP BY date, lineage, mut, region;''')

        run_query('''   DROP TABLE muts;''')

        run_query('''   INSERT INTO timelocling 
                        SELECT date, continent AS location, lineage, count(*) AS count 
                        FROM timeloclin 
                        GROUP BY date, continent, lineage;''')

        run_query('''   INSERT INTO timelocling 
                        SELECT date, country AS location, lineage, count(*) AS count 
                        FROM timeloclin 
                        GROUP BY date, country, lineage;''')

        run_query('''   INSERT INTO timelocling 
                        SELECT date, region AS location, lineage, count(*) AS count 
                        FROM timeloclin 
                        GROUP BY date, region, lineage;''')

        run_query('''   INSERT INTO continent_table 
                        SELECT DISTINCT continent 
                        FROM timeloclin;''')

        run_query('''   INSERT INTO country_table 
                        SELECT DISTINCT country, continent 
                        FROM timeloclin;''')

        run_query('''   INSERT INTO region_table 
                        SELECT DISTINCT region, country
                        FROM timeloclin;''')

        run_query('''   INSERT INTO lineage_table 
                        SELECT DISTINCT lineage 
                        FROM timeloclin;''')

        run_query('''   DROP TABLE timeloclin;''')

        print(f'done in {time.time() - exec_start:.5f} seconds.')
        exec_start = time.time()

        ###############################################################
        # Create indexes
        print("\t STEP 3/3: Data indexing...", end="")

        run_query('''   CREATE INDEX mutsg_idx1 
                        ON  mutsg(location, date, lineage)''')

        run_query('''   CREATE INDEX mutsg_idx2 
                        ON  mutsg(date, lineage)''')

        run_query('''   CREATE INDEX timelocling_idx 
                        ON  timelocling(date, lineage)''')

        con.close()
        print(f'done in {time.time() - exec_start:.5f} seconds.')


create_database()
