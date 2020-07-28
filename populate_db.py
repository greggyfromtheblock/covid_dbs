import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_sqlalchemy import SQLAlchemy

engine = create_engine('postgresql://postgres:postgres@localhost:5432/covid_staging')
con = engine.connect()
print(engine.table_names())

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
    countrydf.columns = ['cat', 'popdata', 'ctc', 'continent_exp']
    return countrydf

def readReported():
   print('Reading csv...')
   df = pd.read_csv('data/covid19.csv')
   reporteddf = df[['countriesAndTerritories', 'dateRep']]
   reporteddf.columns = ['cat', 'dateRep']
   return reporteddf

def readReports():
    print('Reading csv...')
    df = pd.read_csv('data/covid19.csv')
    reportsdf = df[['geoId', 'day', 'month', 'year',
                'cases', 'deaths']]
    reportsdf.columns = ['geoID', 'day', 'month', 'year', 'cases', 'deaths']
    return reportsdf

countrydf = readCountries()
countrydf.to_sql('countries', con, if_exists = 'append', index=False)

reportsdf = readReports()
reportsdf.to_sql('reports', con, if_exists = 'append', index=False)

print('success biatch')

con.close
