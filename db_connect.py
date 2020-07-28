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
        conn = psycopg2.connect(host="localhost", database="postgres", user="mytestuser", password="qwerty")

        # create a cursor
        cur = conn.cursor()

       
        # create tables
        cur.execute("""CREATE TABLE COUNTRY(
                countriesAndTerritories     TEXT    PRIMARY KEY     NOT NULL,
                popData2018                 INT                             ,
                countryTerritoryCode        TEXT                            ,
                continentExp                TEXT                            );
                """)
        
        # insert info from files
        with open('Country.csv') as csvfile:
            country_data = csv.reader(csvfile)
            next(country_data, None)
            for row in country_data:
                cur.execute('INSERT INTO COUNTRY(countriesAndTerritories, popData2018, countryTerritoryCode, continentExp)' 'VALUES(%s, %s, %s, %s)', row)
              
        # give the info for check
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
