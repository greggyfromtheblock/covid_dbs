#!/usr/bin/env python
# coding: utf-8

# In[1]:


import psycopg2
import csv
import json
from staging_createdb import connect
import pandas as pd


# In[2]:


def readCountries():
    print('Reading csv...')
    df = pd.read_csv('data/covid19.csv')
    # print(df['countriesAndTerritories'])
    countries = pd.unique(df['countriesAndTerritories'])
    fvi = []
    for country in countries:
        fvi.append(df[df.countriesAndTerritories==country].first_valid_index())
    countrydf = df.loc[fvi,['countriesAndTerritories', 'popData2018', 
                'countryterritoryCode', 'continentExp']]
    return countrydf

def insertCountries(conn, countrydf):
    cur = conn.cursor()
    print("Adding country data...")
    i = 0
    for index, country in countrydf.iterrows():
        cur.execute('INSERT INTO "staging_country"                    VALUES(%s, %s, %s, %s);',                    (country['countriesAndTerritories'],                     country['popData2018'],                     country['countryterritoryCode'],                     country['continentExp']))
        i += 1
    cur.close()
    conn.commit()
    print(i, "Countries added to the table")

def main():
    conn = None
    
    try:
        conn = connect()
        countrylist = readCountries()
        insertCountries(conn, countrylist)
        print('success binches')
    except(Exception, psycopg2.Error) as error:
        if(conn):
            print('Failed to insert')
        print(error)
    finally:
        if conn is not None:
            conn.close
            print('Closing connection')

if __name__ == '__main__':
    main()

