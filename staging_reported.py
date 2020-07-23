#!/usr/bin/env python
# coding: utf-8

# In[1]:


import psycopg2
import pandas as pd
from staging_createdb import connect


# In[3]:


def readReported():
   print('Reading csv...')
   df = pd.read_csv('data/covid19.csv')
   reporteddf = df[['countriesAndTerritories', 'dateRep']]
   return reporteddf

def insertReported(conn, reporteddf):
   cur = conn.cursor()
   print("Adding report data...")
   i = 0
   for index, reported in reporteddf.iterrows():
       cur.execute('INSERT INTO "staging_reported"                   VALUES(%s, %s, DEFAULT);',                   (reported['countriesAndTerritories'],                    reported['dateRep']))
       i += 1
   cur.close()
   conn.commit()
   print(i, "Reported data added to the table")

def main():
   conn = None
   
   try:
       conn = connect()
       reporteddf = readReported()
       insertReported(conn, reporteddf)
       print('Success binches')
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

