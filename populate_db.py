import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_sqlalchemy import SQLAlchemy

ENV = 'PROD'

if ENV == 'DEV':
    engine = create_engine('postgresql://postgres:postgres@localhost:5432/covid_staging')
else:
    engine = create_engine('postgres://wzeldjxjbxkkjk:615dffd940139b8c47cb0d0abbe40addda41b6d09b998e3a0253a67e34997c46@ec2-34-225-162-157.compute-1.amazonaws.com:5432/dc3rluetv2c0e8')

con = engine.connect()

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
   serial = [x for x in range(1, 11182)]
   reporteddf.insert(0, 'report_id', serial)
   reporteddf.columns = ['report_id', 'cat', 'dateRep']
   return reporteddf

def readReports():
    print('Reading csv...')
    df = pd.read_csv('data/covid19.csv')
    reportsdf = df[['geoId', 'countriesAndTerritories', 'day', 'month', 'year',
                'cases', 'deaths']]
    reportsdf.columns = ['geo_id', 'cat', 'day', 'month', 'year', 'cases', 'deaths']
    return reportsdf

countrydf = readCountries()
countrydf.to_sql('countries', con, if_exists = 'append', index=False)
print(countrydf)

reportsdf = readReports()
reportsdf.to_sql('reports', con, if_exists = 'append', index=False)
print(reportsdf)

reporteddf = readReported()
reporteddf.to_sql('reported', con, if_exists = 'append', index=False)
print(reporteddf)

print('success biatch')

con.close
