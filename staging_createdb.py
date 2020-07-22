import psycopg2
from dbs_config import config

def connect():
    conn = None
    # get config
    params_ = config()
    # connect with the config from the .ini file
    conn = psycopg2.connect(**params_)
    conn.autocommit = True
    return conn

def createDB(conn):
    cur = conn.cursor()
    conn.autocommit = True
    # make fake table for country
    cur.execute("""
    DROP TABLE IF EXISTS staging_country CASCADE;
    CREATE UNLOGGED TABLE staging_country (
        countriesAndTerritories text PRIMARY KEY NOT NULL,
        popData2018 text,
        countryterritoryCode text,
        continentExp text
    );""")
    # make fake table for report
    cur.execute("""
    DROP TABLE IF EXISTS staging_report CASCADE;
    CREATE UNLOGGED TABLE staging_report (
        report_id serial primary key NOT NULL,
        geoID text NOT NULL,
        day int NOT NULL,
        month int NOT NULL,
        year int NOT NULL,
        cases int NOT NULL,
        deaths int NOT NULL
    );""")
    cur.execute("""
    DROP TABLE IF EXISTS staging_reported;
    CREATE UNLOGGED TABLE staging_reported (
        countriesAndTerritories text references staging_country (countriesAndTerritories),
        report_id serial references staging_report (report_id) NOT NULL,
        dateRep text NOT NULL,
        PRIMARY KEY (report_id, countriesAndTerritories)
    );""")
    conn.commit
    return conn

def main():
    conn = None
    
    try:
        conn = connect()
        conn = createDB(conn)
    except (Exception, psycopg2.DatabaseError) as error:
        print("WRONG")
        print(error)
    finally:
        if conn is not None:
            conn.close

if __name__ == '__main__':
    main()
    print('I put the succ in success')
