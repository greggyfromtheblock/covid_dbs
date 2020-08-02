from flask import Flask, render_template, request
from sqlalchemy import UniqueConstraint, PrimaryKeyConstraint, create_engine, ForeignKey
from sqlalchemy.orm import relationship
import psycopg2
from flask_sqlalchemy import SQLAlchemy
from send_mail import send_mail

app = Flask(__name__)

ENV = 'prod'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/covid_staging'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://wzeldjxjbxkkjk:615dffd940139b8c47cb0d0abbe40addda41b6d09b998e3a0253a67e34997c46@ec2-34-225-162-157.compute-1.amazonaws.com:5432/dc3rluetv2c0e8'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Countries(db.Model):
    __tablename__ = 'countries'
    cat = db.Column(db.String(200), primary_key=True)
    popdata = db.Column(db.String(200))
    ctc = db.Column(db.String(200))
    continent_exp = db.Column(db.String(200))
    def __init__(self, cat, popdata, ctc, continent_exp, geo_id):
        self.cat = cat
        self.popdata = popdata
        self.ctc = ctc
        self.continent_exp = continent_exP

class Reports(db.Model):
    __tablename__ = 'reports'
    report_id = db.Column(db.Integer, primary_key=True)
    geo_id = db.Column(db.String(200), ForeignKey('countries.geo_id'))
    day = db.Column(db.Integer)
    month = db.Column(db.Integer)
    year = db.Column(db.Integer)
    cases = db.Column(db.Integer)
    deaths = db.Column(db.Integer)

    def __init__(self, cat, popdata, ctc, continent_exp):
        self.report_id = report_id
        self.geo_id = geo_id
        self.day = day
        self.month = month
        self.year = year
        self.cases = cases
        self.deaths = deaths

class Reported(db.Model):
    __tablename__ = 'reported'
    __table_args__ = (
        PrimaryKeyConstraint('cat', 'report_id'),
    )
    report_id = db.Column(db.Integer, db.ForeignKey('reports.report_id'))
    dateRep = db.Column(db.String(200))
    cat = db.Column(db.String(200), db.ForeignKey('countries.cat'))

    def __init__(self, cat, popdata, ctc, continent_exp):
        self.report_id = report_id
        self.dateRep = dateRep
        self.cat = cat

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
