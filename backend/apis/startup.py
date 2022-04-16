"""

    Startup setup
    Database creation, data extraction from .tsv file and database population

"""

from __future__ import print_function

import sqlite3
import time

from flask_restplus import Namespace

from .parsers.GisaidParser import GisaidParser
from .parsers.NextstrainParser import NextstrainParser
from .utils.cmd_parser import get_cmd_arguments

api = Namespace('startup', description='startup')
db_name = 'varianthunter.db'
args = get_cmd_arguments()


def startup():
    """
    Performs the startup setup: database creation, data extraction and database population

    """
    exec_start = time.time()
    print("> Starting initial setup ...")
    curr_step, tot_steps = 1, 4

    with open(args.file_path) as f:
        con = sqlite3.connect(db_name)
        con.execute("pragma journal_mode=off;")
        con.execute("pragma locking_mode=EXCLUSIVE;")
        con.execute("pragma synchronous=OFF;")
        cur = con.cursor()

        # Check if tables already exists
        cur.execute(" SELECT count(name) FROM sqlite_master WHERE type='table'")
        if cur.fetchone()[0] > 1:
            print('   INFO: Database already exists ', end='')
            if args.reload:
                # Clear current database
                print('[database overwrite started]...')
                con.execute("pragma writable_schema=1;")
                cur.execute("DELETE FROM sqlite_master WHERE type in ('table', 'index', 'trigger')")
                con.execute("pragma writable_schema=0;")
                con.commit()
                con.execute("vacuum")

            else:
                # Start the app directly
                print('[database overwrite skipped]\n')
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

        run_query('''   CREATE TABLE aa_substitutions
                        (sequence_id int, protein_id int, mut text)''')

        run_query('''   CREATE TABLE aggr_aa_substitutions
                        (date int, lineage_id int, location_id int, protein_id int, mut text, count int)''')

        run_query('''   CREATE TABLE lineages
                        (lineage_id int primary key , lineage text)''')

        run_query('''   CREATE TABLE lineages_characteristics
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

        if args.file_type != 'nextstrain':
            print(" [GISAID parser] ...")
            parser = GisaidParser(con, f)
        else:
            print(" [NEXTSTRAIN parser] ...")
            parser = NextstrainParser(con, f)
        parser.set_date_range(args.beginning_date, args.end_date)
        parser.parse(args.filtered_countries)
        del parser

        print(f'\t\tdone in {time.time() - step_start:.5f} seconds.')
        step_start = time.time()

        ###############################################################
        # Aggregate data
        curr_step += 1
        print(f"\t STEP {curr_step}/{tot_steps}: Data aggregation...", end="")

        run_query('''   INSERT INTO aggr_aa_substitutions 
                            SELECT date, lineage_id, continent_id AS location_id, protein_id, mut, count(*) AS count 
                            FROM sequences SQ JOIN aa_substitutions SB ON SQ.sequence_id=SB.sequence_id
                            GROUP BY date, lineage_id, continent_id, protein_id, mut;''')

        run_query('''   INSERT INTO aggr_aa_substitutions 
                            SELECT date, lineage_id, country_id AS location_id, protein_id, mut, count(*) AS count 
                            FROM sequences SQ JOIN aa_substitutions SB ON SQ.sequence_id=SB.sequence_id
                            GROUP BY date, lineage_id, country_id, protein_id, mut;''')

        run_query('''   INSERT INTO aggr_aa_substitutions 
                            SELECT date, lineage_id, region_id AS location_id, protein_id, mut, count(*) AS count 
                            FROM sequences SQ JOIN aa_substitutions SB ON SQ.sequence_id=SB.sequence_id
                            GROUP BY date, lineage_id, region_id, protein_id, mut;''')

        run_query('''   DROP TABLE aa_substitutions;''')

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

        run_query('''   DROP TABLE sequences;''')

        print(f'done in {time.time() - step_start:.5f} seconds.')
        step_start = time.time()

        ###############################################################
        # Create indexes
        curr_step += 1
        print(f"\t STEP {curr_step}/{tot_steps}: Data indexing...", end="")

        run_query('''   CREATE INDEX aggr_aa_substitutions_idx1
                        ON  aggr_aa_substitutions(location_id, date, lineage_id)''')

        run_query('''   CREATE INDEX aggr_aa_substitutions_idx2 
                        ON  aggr_aa_substitutions(date, lineage_id)''')

        run_query('''   CREATE INDEX aggr_sequences_idx1
                        ON  aggr_sequences(date, lineage_id)''')

        run_query('''   CREATE INDEX aggr_sequences_idx2
                                ON  aggr_sequences(location_id, lineage_id)''')
        con.close()
        print(f'done in {time.time() - step_start:.5f} seconds.')

    print(f'>> Setup overall time: {time.time() - exec_start:.5f} seconds.\n')


startup()
