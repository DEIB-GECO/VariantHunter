from __future__ import print_function

import sqlite3
import sys
import time

from flask_restplus import Namespace

from .parsers.GisaidParser import GisaidParser
from .parsers.NextstrainParser import NextstrainParser

# Fetch the parameters: file path, selected countries and type (either gisaid or nextstrain)
file_path = sys.argv[1]
selected_countries = set([x.lower() for x in sys.argv[2].strip().split(',') if x])
if len(selected_countries) == 1 and 'all' in selected_countries:
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
    curr_step, tot_steps = 1, 4

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
        print(f"\t STEP {curr_step}/{tot_steps}: Tables creation...", end="")

        run_query('''   CREATE TABLE sequences
                        (sequence_id int, date int, lineage_id int, continent_id int, country_id int, region_id int )''')

        run_query('''   CREATE TABLE aggr_sequences
                        (date int, lineage_id int, location_id int, count int )''')

        run_query('''   CREATE TABLE substitutions
                        (sequence_id int, protein_id int, mut text)''')

        run_query('''   CREATE TABLE aggr_substitutions
                        (date int, lineage_id int, location_id int, protein_id int, mut text, count int)''')

        run_query('''   CREATE TABLE lineages
                        (lineage_id int primary key , lineage text)''')

        run_query('''   CREATE TABLE lineages_characterization
                        (lineage_id int , protein_id int, mut text)''')

        run_query('''   CREATE TABLE locations
                        (location_id int primary key , location text)''')

        run_query('''   CREATE TABLE continents 
                        (continent_id int)''')

        run_query('''   CREATE TABLE countries
                        (country_id int, continent_id int)''')

        run_query('''   CREATE TABLE regions
                        (region_id int, country_id int)''')

        run_query('''   CREATE TABLE proteins
                        (protein_id int primary key , protein text)''')

        print(f'done in {time.time() - exec_start:.5f} seconds.')
        step_start = time.time()

        ###############################################################
        # Parse the file and load the data into the tables
        curr_step += 1
        print(f"\t STEP {curr_step}/{tot_steps}: Data extraction ", end="")

        if file_type != 'nextstrain':
            print(" [GISAID parser] ...")
            parser = GisaidParser(con, f)
        else:
            print(" [NEXTSTRAIN parser] ...")
            parser = NextstrainParser(con, f)
        parser.parse(selected_countries)
        del parser

        print(f'\t\tdone in {time.time() - step_start:.5f} seconds.')
        step_start = time.time()

        ###############################################################
        # Aggregate data
        curr_step += 1
        print(f"\t STEP {curr_step}/{tot_steps}: Data aggregation...", end="")

        run_query('''   INSERT INTO aggr_substitutions 
                            SELECT date, lineage_id, continent_id AS location_id, protein_id, mut, count(*) AS count 
                            FROM sequences SQ JOIN substitutions SB ON SQ.sequence_id=SB.sequence_id
                            GROUP BY date, lineage_id, continent_id, protein_id, mut;''')

        run_query('''   INSERT INTO aggr_substitutions 
                            SELECT date, lineage_id, country_id AS location_id, protein_id, mut, count(*) AS count 
                            FROM sequences SQ JOIN substitutions SB ON SQ.sequence_id=SB.sequence_id
                            GROUP BY date, lineage_id, country_id, protein_id, mut;''')

        run_query('''   INSERT INTO aggr_substitutions 
                            SELECT date, lineage_id, region_id AS location_id, protein_id, mut, count(*) AS count 
                            FROM sequences SQ JOIN substitutions SB ON SQ.sequence_id=SB.sequence_id
                            GROUP BY date, lineage_id, region_id, protein_id, mut;''')

        #run_query('''   DROP TABLE substitutions;''')

        run_query('''   INSERT INTO aggr_sequences 
                            SELECT date, lineage_id, continent_id AS location_id, count(*) AS count 
                            FROM sequences 
                            GROUP BY date, lineage_id, continent_id;''')

        run_query('''   INSERT INTO aggr_sequences 
                            SELECT date, lineage_id, country_id AS location_id, count(*) AS count 
                            FROM sequences 
                            GROUP BY date, lineage_id, country_id;''')

        run_query('''   INSERT INTO aggr_sequences 
                            SELECT date, lineage_id, region_id AS location_id, count(*) AS count 
                            FROM sequences 
                            GROUP BY date, lineage_id, region_id;''')

        #run_query('''   DROP TABLE sequences;''')

        print(f'done in {time.time() - step_start:.5f} seconds.')
        step_start = time.time()

        ###############################################################
        # Create indexes
        curr_step += 1
        print(f"\t STEP {curr_step}/{tot_steps}: Data indexing...", end="")

        run_query('''   CREATE INDEX aggr_substitutions_idx1
                        ON  aggr_substitutions(location_id, date, lineage_id)''')

        run_query('''   CREATE INDEX aggr_substitutions_idx2 
                        ON  aggr_substitutions(date, lineage_id)''')

        run_query('''   CREATE INDEX aggr_sequences_idx1
                        ON  aggr_sequences(date, lineage_id)''')

        run_query('''   CREATE INDEX aggr_sequences_idx2
                                ON  aggr_sequences(location_id, lineage_id)''')
        con.close()
        print(f'done in {time.time() - step_start:.5f} seconds.')

    print(f'> Setup overall time: {time.time() - exec_start:.5f} seconds.')

create_database()
