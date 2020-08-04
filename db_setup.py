from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

ENV = 'DEV'

if ENV == 'DEV':
    engine = create_engine('postgresql://postgres:postgres@localhost:5432/covid_staging')
else:
    engine = create_engine('postgres://wzeldjxjbxkkjk:615dffd940139b8c47cb0d0abbe40addda41b6d09b998e3a0253a67e34997c46@ec2-34-225-162-157.compute-1.amazonaws.com:5432/dc3rluetv2c0e8')

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    import models
    Base.metadata.create_all(bind=engine)
