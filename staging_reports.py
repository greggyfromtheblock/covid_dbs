#!/usr/bin/env python
# coding: utf-8

# In[1]:


import psycopg2
import pandas as pd
from staging_createdb import connect


# In[2]:


def readReports():
    print('Reading csv...')
    df = pd.read_csv('data/covid19.csv')
    reportdf = df[['geoId', 'day', 'month', 'year',
                'cases', 'deaths']]
    return reportdf

def insertReports(conn, countrydf):
    cur = conn.cursor()
    print("Adding report data...")
    i = 0
    for index, country in countrydf.iterrows():
        cur.execute('INSERT INTO "staging_report"                    VALUES(DEFAULT, %s, %s, %s, %s, %s, %s);',                    (country['geoId'],                     country['day'],                     country['month'],                     country['year'],                     country['cases'],                     country['deaths']))
        i += 1
    cur.close()
    conn.commit()
    print(i, "Reports added to the table")

def main():
    conn = None
    
    try:
        conn = connect()
        reportlist = readReports()
        insertReports(conn, reportlist)
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

