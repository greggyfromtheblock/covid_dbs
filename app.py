from flask import Flask, render_template, request, redirect, flash
from sqlalchemy import UniqueConstraint, PrimaryKeyConstraint, create_engine, ForeignKey, Sequence
from sqlalchemy.orm import relationship
import psycopg2
from flask_sqlalchemy import SQLAlchemy
from send_mail import send_mail
from wtforms import Form, StringField, SelectField
from db_setup import  init_db, db_session
from flask_table import Table, Col

app = Flask(__name__)

ENV = 'prod'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/covid_staging'
    app.secret_key = 'gresziu'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://wzeldjxjbxkkjk:615dffd940139b8c47cb0d0abbe40addda41b6d09b998e3a0253a67e34997c46@ec2-34-225-162-157.compute-1.amazonaws.com:5432/dc3rluetv2c0e8'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class MainForm(Form):
    countries = [('Germany', 'Germany'),
                   ('USA', 'USA'),
                   ('Afghanistan', 'Afghanistan')]
    select = SelectField('Country', choices=countries)
    search = StringField('')

class Countries(db.Model):
    __tablename__ = 'countries'
    cat = db.Column(db.String(200), primary_key=True)
    popdata = db.Column(db.String(200))
    ctc = db.Column(db.String(200))
    continent_exp = db.Column(db.String(200))
    def __init__(self, cat, popdata, ctc, continent_exp):
        self.cat = cat
        self.popdata = popdata
        self.ctc = ctc
        self.continent_exp = continent_exP

class Reports(db.Model):
    __tablename__ = 'reports'
    report_id = db.Column(db.Integer, primary_key=True)
    # cat = db.Column(db.String(200))
    geo_id = db.Column(db.String(200))
    day = db.Column(db.Integer)
    month = db.Column(db.Integer)
    year = db.Column(db.Integer)
    cases = db.Column(db.Integer)
    deaths = db.Column(db.Integer)

    def __init__(self, report_id, cat, geo_id, day, month, year, cases, deaths):
        self.report_id = report_id
        self.cat = cat
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
    report_id = db.Column(db.Integer, db.Sequence('reported_seq'), db.ForeignKey('reports.report_id'))
    dateRep = db.Column(db.String(200))
    cat = db.Column(db.String(200), db.ForeignKey('countries.cat'))

    def __init__(self, report_id, dateRep, cat):
        self.report_id = report_id
        self.dateRep = dateRep
        self.cat = cat

class Results(Table):
  cat = Col('Countries and Territories')
  popdata = Col('Population Data 2018')
  ctc = Col('Country Territory Code')
  continent_exp = Col('Continent')

class CasesAndDeaths(Table):
    dateRep = Col('Date')
    cases = Col('Cases')
    deaths = Col('Deaths')


@app.route('/', methods=['GET', 'POST'])
def index():
    search = MainForm(request.form)
    if request.method == 'POST':
        return search_results(search)
    return render_template('index.html', form=search)

@app.route('/results/<search>')
def search_results(search):
    results = []
    search_string = search.data['search']
    countries_query = db_session.query(Countries).filter(Countries.cat == search_string)
    cd_query = db_session.query(Reports).with_entities(Reported.dateRep, Reports.cases, Reports.deaths).filter(Reported.cat == search_string)
    cd = cd_query.all()
    results = countries_query.all()

    # if search.data['search'] == '':
    #     qry = db_session.query(Countries)
    #     results = qry.all()

    if not results:
        flash('No results found!')
        return redirect('/')
    else:
        # display results
        table = Results(results)
        cd_table = Results(cd)
        table.border = True
        return render_template('results.html', table=cd)

if __name__ == '__main__':
    app.run()
