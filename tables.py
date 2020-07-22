import psycopg2
from psycopg2 import Error

try:
    connection = psycopg2.connect(user = "postgres",
                                  password = "!0307Postgresql!",
                                  host = "127.0.0.1",
                                  port = "5432",
                                  database = "postgres_db")

    cursor = connection.cursor()
    
    create_table_query = '''CREATE TABLE COUNTRY (
                    countriesAndTerritories     TEXT PRIMARY KEY    NOT NULL,
                    popData2018                 INT                         ,
                    countryterritoryCode        TEXT                        ,
                    continentExp                TEXT                        );
                    CREATE TABLE REPORT(
                    ID                          INT PRIMARY KEY     NOT NULL,
                    geoID                       TEXT                NOT NULL,
                    day                         INT                 NOT NULL,
                    month                       INT                 NOT NULL,
                    year                        INT                 NOT NULL,
                    cases                       INT                 NOT NULL,
                    deaths                      INT                 NOT NULL);
                    CREATE TABLE REPORTED(
                    countriesAndTerritories     TEXT                NOT NULL,
                    Report_ID                   INT PRIMARY KEY     NOT NULL,
                    dateRep                     TEXT                NOT NULL);'''

    create_table_values = ''' COPY country   FROM '/home/mitsukiakina/project/country.csv'   DELIMITER ',' CSV HEADER;
                            COPY report    FROM '/home/mitsukiakina/project/report.csv'    DELIMITER ',' CSV HEADER;
                            COPY reported  FROM '/home/mitsukiakina/project/reported.csv'  DELIMITER ',' CSV HEADER;'''
    
    cursor.execute(create_table_query)
    cursor.execute(create_table_values)
    connection.commit()
    print("Table created successfully in PostgreSQL ")

except (Exception, psycopg2.DatabaseError) as error :
    print ("Error while creating PostgreSQL table", error)
finally:
    #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed") 