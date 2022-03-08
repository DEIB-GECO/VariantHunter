from __future__ import print_function

import datetime as dtime
import sqlite3
import sys
import time

import tqdm
from flask_restplus import Namespace

input_file_name = sys.argv[1]
select_country = set([x.lower() for x in sys.argv[2].strip().split(',') if x])
db_name = 'varianthunter.db'
api = Namespace('create_database', description='create_database')

startex = time.time()
print("Starting database creation...")


with open(input_file_name) as f:
    startdate = dtime.datetime.strptime("2020-01-01", "%Y-%m-%d")

    con = sqlite3.connect(db_name)
    # con.execute("begin exclusive")
    con.execute("pragma journal_mode=off;")
    con.execute("pragma locking_mode=EXCLUSIVE;")
    con.execute("pragma synchronous=OFF;")
    cur = con.cursor()

    # Create table
    cur.execute(
        '''CREATE TABLE muts (date integer, lineage text, mut text, continent text, country text, region text )''')

    con.commit()

    cur.execute('''CREATE TABLE mutsg (date integer, lineage text, mut text, location text, count integer)''')

    con.commit()

    cur.execute('''CREATE TABLE timeloclin (date integer, continent text, country text, region text, lineage text)''')
    con.commit()

    cur.execute('''CREATE TABLE timelocling (date integer, location text, lineage text, count integer)''')
    con.commit()

    cur.execute('''CREATE TABLE continent_table (continent text)''')
    con.commit()

    cur.execute('''CREATE TABLE country_table (country text, continent text)''')
    con.commit()

    cur.execute('''CREATE TABLE region_table (region text, country text)''')
    con.commit()

    cur.execute('''CREATE TABLE lineage_table (lineage text)''')
    con.commit()

    print("Table creation completed...")

    header = f.readline()
    i = 0
    batch = []
    batch_timeloclin = []
    for line in tqdm.tqdm(f):
        s = line.split("\t")

        locs = s[4].split('/')
        country = locs[1].strip()
        if len(select_country) != 0:
            if country.lower() not in select_country:
                continue
        continent = locs[0].strip()
        if len(locs) < 3:
            region = None
        else:
            region = locs[2].strip()

        try:
            n = float(s[20])
        except:
            n = 0.

        l = int(s[6])

        lin = s[11]

        try:
            date = (dtime.datetime.strptime(s[3], "%Y-%m-%d") - startdate).days
        except:
            continue

        if (29000 < l < 30000) and (n < 0.05):
            batch_timeloclin.append((date, continent, country, region, lin))
            for aa in s[14][1:-1].split(","):
                batch.append((date, lin, aa, continent, country, region))

        if len(batch) > 50000:
            con.executemany("insert into muts(date,lineage,mut,continent, country, region) values (?,?,?,?,?,?)", batch)
            con.commit()
            del batch
            batch = []

        if len(batch_timeloclin) > 50000:
            con.executemany("insert into timeloclin(date,continent,country,region,lineage) values (?,?,?,?,?)",
                            batch_timeloclin)
            con.commit()
            del batch_timeloclin
            batch_timeloclin = []

        del line

    con.executemany("insert into muts(date,lineage,mut,continent, country, region)  values (?,?,?,?,?,?)", batch)
    con.commit()
    del batch
    con.executemany("insert into timeloclin(date,continent,country,region,lineage) values (?,?,?,?,?)",
                    batch_timeloclin)
    con.commit()
    del batch_timeloclin
    con.commit()
    cur.execute(
        "insert into mutsg select date, lineage, mut, continent as location, count(*) as count from muts group by date,lineage,mut,continent")
    con.commit()
    cur.execute('''insert into mutsg select date, lineage, mut, country as location, count(*) as count 
                       from muts 
                       group by date,lineage,mut,country''')
    con.commit()
    cur.execute('''insert into mutsg select date, lineage, mut, region as location, count(*) as count 
                       from muts 
                       group by date,lineage,mut,region''')
    con.commit()
    cur.execute("DROP TABLE muts;")
    con.commit()
    cur.execute('''insert into timelocling select date, continent as location, lineage, count(*) as count 
                       from timeloclin group by date, continent, lineage''')
    con.commit()
    cur.execute('''insert into timelocling select date, country as location, lineage, count(*) as count 
                       from timeloclin group by date, country, lineage''')
    con.commit()
    cur.execute('''insert into timelocling select date, region as location, lineage, count(*) as count 
                       from timeloclin group by date, region, lineage''')
    con.commit()

    cur.execute('''insert into continent_table select distinct continent 
                       from timeloclin''')
    con.commit()

    cur.execute('''insert into country_table select distinct country, continent 
                       from timeloclin''')
    con.commit()

    cur.execute('''insert into region_table select distinct region, country
                       from timeloclin''')
    con.commit()

    cur.execute('''insert into lineage_table select distinct lineage 
                       from timeloclin''')
    con.commit()

    cur.execute("DROP TABLE timeloclin;")
    con.commit()

    cur.execute("CREATE INDEX mutsg_idx1 ON  mutsg(location, date, lineage);")
    con.commit()

    cur.execute("CREATE INDEX mutsg_idx2 ON  mutsg(date, lineage);")
    con.commit()

    cur.execute("CREATE INDEX timelocling1 ON  timelocling(date, lineage);")
    con.commit()

    cur.execute("CREATE INDEX timelocling2 ON  timelocling(date, lineage);")
    con.commit()


    con.close()

print(f'Database creation completed in {time.time() - startex} seconds')