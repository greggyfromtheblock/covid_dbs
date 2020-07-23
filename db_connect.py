#!/usr/bin/python
# -*- coding: utf-8 -*-
import psycopg2
import csv

def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(host="localhost", database="postgres", user="mytestuser", password="imt-mc-450")

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        # print('PostgreSQL database version:')
        # cur.execute('SELECT version()')

        # display the PostgreSQL database server version
        # db_version = cur.fetchone()
        # print(db_version)
        
        # create a table with the user account data
        cur.execute("""CREATE TABLE COUNTRY(
                countriesAndTerritories     TEXT    PRIMARY KEY     NOT NULL,
                popData2018                 INT                             ,
                countryTerritoryCode        TEXT                            ,
                continentExp                TEXT                            );
                """)
        
        # insert info for 2 users
        with open('Country.csv') as csvfile:
            country_data = csv.reader(csvfile)
            next(country_data, None)
            for row in country_data:
                for i in row:
                    if i == '':
                        print (row.index(i))

                        #row.index(i) = 0              
                cur.execute('INSERT INTO COUNTRY(countriesAndTerritories, popData2018, countryTerritoryCode, continentExp)' 'VALUES(%s, %s, %s, %s)', row)
              
        # give the list of usernames from the account table
        cur.execute("""SELECT * FROM COUNTRY;""")
        query_results = cur.fetchall()
        print(query_results)
        
        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


def main():
    connect()

if __name__ == '__main__':
    main()
