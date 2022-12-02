"""

    Startup setup
    Database creation, data extraction from .tsv file and database population

"""

from __future__ import print_function

import os
from datetime import datetime
from shutil import rmtree
from sqlite3 import connect
from threading import Thread
from time import time

from flask_restplus import Namespace

from .parsers.GisaidParser import GisaidParser
from .parsers.NextstrainParser import NextstrainParser
from .utils.arg_manager import get_cmd_arguments
from .utils.db_manager import connection_preset, clear_db
from .utils.path_manager import db_paths as paths

api = Namespace('startup', description='startup')
args = get_cmd_arguments()
version = "2.0.0"  # Keep consistent wrt package.json file


def on_done():
    # clean temporary files
    rmtree(paths.temp_tree, ignore_errors=True)
    port = os.getenv('PORT', 5000)
    print(
        "\n\n\033[01m\033[32m> * STARTUP COMPLETED:\033[0m\033[32m The application is now accessible from your browser at http://localhost:"
        + str(port) + " (PRESS CTRL+C to stop)\033[0m\n")


def startup():
    """
    Performs the startup setup: database creation, data extraction and database population

    """

    def run_query(query, params=None):
        cur.execute(query) if params is None else cur.execute(query, params)
        con.commit()

    def print_parsing_info(prepend="", params_only=False):
        info_q = f'''   SELECT file_type, filtered_countries, beginning_date, end_date, parse_date, version
                        FROM  info;'''
        info = cur.execute(info_q).fetchone()
        print(f'''\t{prepend} File type: {info[0]},''' +
              f'''\n\t{prepend} Filtered countries: {info[1] if len(info[1]) > 0 else "all"},''' +
              f'''\n\t{prepend} Begin date: {info[2]},\n\t{prepend} End date: {info[3]},''')
        if not params_only:
            print(f'''\t{prepend} Parsed on: {info[4]}, using app version: {info[5]}\n''')

    exec_start = time()
    print("\033[01m\033[33m> Starting initial setup ... \033[0m")
    curr_step, tot_steps = 1, 4

    con = connect(paths.db_path)
    connection_preset(con)
    cur = con.cursor()

    # Check if tables already exists
    cur.execute(" SELECT count(name) FROM sqlite_master WHERE type='table'")
    if cur.fetchone()[0] > 1:
        print('   \033[34mINFO: Database already exists ', end='')
        if args.regenerate:
            # Clear current database
            print('[database overwrite started]... \033[0m')
            clear_db(db_con=con, db_cur=cur)

        else:
            # Start the app directly
            print('[loading existing one]\033[0m')
            print_parsing_info()
            con.close()
            on_done()
            return

    with open(args.file_path) as f:
        clear_db(db_name=paths.temp_db1_path)
        clear_db(db_name=paths.temp_db2_path)
        cur.execute(f''' ATTACH DATABASE '{paths.temp_db1_path}' AS temp_table1; ''')
        cur.execute(f''' ATTACH DATABASE '{paths.temp_db2_path}' AS temp_table2;''')
        connection_preset(con)

        ###############################################################
        # Create all the tables
        print(f"\t STEP {curr_step}/{tot_steps}: Tables creation ... ", end="")

        run_query('''   CREATE TABLE temp_table1.sequences
                        (sequence_id int, date int, lineage_id int, continent_id int, country_id int, region_id int )''')

        run_query('''   CREATE TABLE aggr_sequences
                        (date int, lineage_id int, location_id int, count int )''')

        run_query('''   CREATE TABLE temp_table2.aa_substitutions
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

        run_query('''   CREATE TABLE info
                        (file_type text, filtered_countries text, beginning_date text, end_date text, parse_date text, version text)''')

        params = vars(args)
        params['filtered_countries'] = '; '.join(params['filtered_countries'])
        params['version'] = version
        run_query('''   INSERT INTO info VALUES 
                        (:file_type,:filtered_countries,:beginning_date, :end_date, DATE('now'), :version);''', params)

        print(f'done in {time() - exec_start:.5f} seconds.')
        step_start = time()

        ###############################################################
        # Parse the file and load the data into the tables
        curr_step += 1
        print(f"\t STEP {curr_step}/{tot_steps}: Data extraction ...")
        print_parsing_info(prepend='\t   *', params_only=True)
        if args.file_type != 'nextstrain':
            parser = GisaidParser(con, f)
        else:
            parser = NextstrainParser(con, f)
        parser.set_date_range(args.beginning_date, args.end_date)
        parser.parse(args.filtered_countries)
        del parser

        print(f'\t\tdone in {time() - step_start:.5f} seconds.')
        step_start = time()

        ###############################################################
        # Aggregate data
        curr_step += 1
        print(f"\t STEP {curr_step}/{tot_steps}: Data aggregation ... ")

        print("\t\tProcessing aa substitutions by continent ...")
        run_query('''   INSERT INTO aggr_aa_substitutions 
                            SELECT date, lineage_id, continent_id AS location_id, protein_id, mut, count(*) AS count 
                            FROM temp_table1.sequences SQ JOIN temp_table2.aa_substitutions SB ON SQ.sequence_id=SB.sequence_id
                            WHERE continent_id IS NOT NULL AND mut IS NOT NULL
                            GROUP BY date, lineage_id, continent_id, protein_id, mut;''')

        print("\t\tProcessing aa substitutions by country ...")
        run_query('''   INSERT INTO aggr_aa_substitutions 
                            SELECT date, lineage_id, country_id AS location_id, protein_id, mut, count(*) AS count 
                            FROM temp_table1.sequences SQ JOIN temp_table2.aa_substitutions SB ON SQ.sequence_id=SB.sequence_id
                            WHERE country_id IS NOT NULL AND mut IS NOT NULL
                            GROUP BY date, lineage_id, country_id, protein_id, mut;''')

        print("\t\tProcessing aa substitutions by region ...")
        run_query('''   INSERT INTO aggr_aa_substitutions 
                            SELECT date, lineage_id, region_id AS location_id, protein_id, mut, count(*) AS count 
                            FROM temp_table1.sequences SQ JOIN temp_table2.aa_substitutions SB ON SQ.sequence_id=SB.sequence_id
                            WHERE region_id IS NOT NULL AND mut IS NOT NULL
                            GROUP BY date, lineage_id, region_id, protein_id, mut;''')

        run_query('''   DETACH DATABASE 'temp_table2';''')
        clear_db(db_name=paths.temp_db2_path)

        print("\t\tProcessing sequences by continent ...")
        run_query('''   INSERT INTO aggr_sequences 
                            SELECT date, lineage_id, continent_id AS location_id, count(*) AS count 
                            FROM temp_table1.sequences 
                            WHERE continent_id IS NOT NULL 
                            GROUP BY date, lineage_id, continent_id;''')

        print("\t\tProcessing sequences by country ...")
        run_query('''   INSERT INTO aggr_sequences 
                            SELECT date, lineage_id, country_id AS location_id, count(*) AS count 
                            FROM temp_table1.sequences 
                            WHERE country_id IS NOT NULL 
                            GROUP BY date, lineage_id, country_id;''')

        print("\t\tProcessing sequences by region ...")
        run_query('''   INSERT INTO aggr_sequences 
                            SELECT date, lineage_id, region_id AS location_id, count(*) AS count 
                            FROM temp_table1.sequences 
                            WHERE region_id IS NOT NULL 
                            GROUP BY date, lineage_id, region_id;''')

        run_query('''   DETACH DATABASE 'temp_table1';''')
        clear_db(db_name=paths.temp_db1_path)

        print(f'\t\tdone in {time() - step_start:.5f} seconds.')
        step_start = time()

        ###############################################################
        # Create indexes
        curr_step += 1
        print(f"\t STEP {curr_step}/{tot_steps}: Data indexing ... ")

        run_query('''   CREATE INDEX aggr_aa_substitutions_idx1
                        ON  aggr_aa_substitutions(location_id, date, lineage_id)''')

        run_query('''   CREATE INDEX aggr_aa_substitutions_idx2 
                        ON  aggr_aa_substitutions(date, lineage_id)''')

        run_query('''   CREATE INDEX aggr_sequences_idx1
                        ON  aggr_sequences(date, lineage_id)''')

        run_query('''   CREATE INDEX aggr_sequences_idx2
                                ON  aggr_sequences(location_id, lineage_id)''')
        con.close()
        print(f'\t\tdone in {time() - step_start:.5f} seconds.')

    print(f'\t>> Setup overall time: {time() - exec_start:.5f} seconds.\n')

    on_done()


print("...\n...\tServer started on " + str(datetime.now()))
print("...\tVersion " + version + "\n...")
print("\n\n\033[01m⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯    V A R I A N T    H U N T E R    ⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\033[0m\n")

# create a thread
thread = Thread(target=startup)
thread.start()
