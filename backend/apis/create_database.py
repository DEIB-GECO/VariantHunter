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
    curr_step, tot_steps = 1, 5

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
        print(f"\t STEP {curr_step}/{tot_steps}: Table creation...", end="")

        run_query('''   CREATE TABLE muts 
                        (date integer, lineage text, mut text, continent text, country text, region text )''')

        run_query('''   CREATE TABLE mutsg 
                        (date integer, lineage text, mut text, location text, count integer)''')

        run_query('''   CREATE TABLE timeloclin 
                        (date integer, continent text, country text, region text, lineage text)''')

        run_query('''   CREATE TABLE timelocling 
                        (date integer, location text, lineage text, count integer)''')

        run_query('''   CREATE TABLE continents 
                        (continent text)''')

        run_query('''   CREATE TABLE countries
                        (country text, continent text)''')

        run_query('''   CREATE TABLE regions 
                        (region text, country text)''')

        run_query('''   CREATE TABLE lineages_characterization 
                        (lineage text, mut text)''')

        print(f'done in {time.time() - exec_start:.5f} seconds.')
        exec_start = time.time()

        ###############################################################
        # Parse the files and load the data into the tables
        curr_step += 1
        print(f"\t STEP {curr_step}/{tot_steps}: Data extraction...", end="")

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
        curr_step += 1
        print(f"\t STEP {curr_step}/{tot_steps}: Data indexing...", end="")

        run_query('''   CREATE INDEX muts_idx
                        ON  muts(date, lineage, mut)''')

        print(f'done in {time.time() - exec_start:.5f} seconds.')
        exec_start = time.time()

        ###############################################################
        # Aggregate data
        curr_step += 1
        print(f"\t STEP {curr_step}/{tot_steps}: Data aggregation...", end="")

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

        run_query('''   CREATE VIEW temp.lin_mut_counts AS
                                SELECT lineage, mut, count(*) AS count
                                FROM muts
                                GROUP BY lineage,mut;''')

        run_query('''   CREATE VIEW temp.lin_counts AS
                            SELECT lineage, count(*) as count
                            FROM timeloclin
                            GROUP BY lineage;''')

        run_query('''   INSERT INTO lineages_characterization
                        SELECT lineage, mut
                        FROM lin_mut_counts AS T1
                        WHERE T1.count >= (
                            SELECT count*0.5
                            FROM lin_counts
                            WHERE lineage=T1.lineage
                            );''')

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

        run_query('''   INSERT INTO continents 
                        SELECT DISTINCT continent 
                        FROM timeloclin;''')

        run_query('''   INSERT INTO countries 
                        SELECT DISTINCT country, continent 
                        FROM timeloclin;''')

        run_query('''   INSERT INTO regions
                        SELECT DISTINCT region, country
                        FROM timeloclin;''')

        run_query('''   DROP TABLE timeloclin;''')

        print(f'done in {time.time() - exec_start:.5f} seconds.')
        exec_start = time.time()

        ###############################################################
        # Create indexes
        curr_step += 1
        print(f"\t STEP {curr_step}/{tot_steps}: Data indexing...", end="")

        run_query('''   CREATE INDEX mutsg_idx1 
                        ON  mutsg(location, date, lineage)''')

        run_query('''   CREATE INDEX mutsg_idx2 
                        ON  mutsg(date, lineage)''')

        run_query('''   CREATE INDEX timelocling_idx 
                        ON  timelocling(date, lineage)''')

        con.close()
        print(f'done in {time.time() - exec_start:.5f} seconds.')


create_database()
