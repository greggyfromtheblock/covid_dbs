from flask import Flask, render_template, request, redirect, flash
from sqlalchemy import UniqueConstraint, PrimaryKeyConstraint, create_engine, ForeignKey, Sequence
from sqlalchemy.orm import relationship
import psycopg2
from flask_sqlalchemy import SQLAlchemy
from send_mail import send_mail
from wtforms import Form, StringField, SelectField
from db_setup import  init_db, db_session
from flask_table import Table, Col
from sqlalchemy import text
from bokeh.models import ColumnDataSource, Grid, LinearAxis, Plot, VBar
import pandas as pd
from bokeh.plotting import figure, output_file, show, save, ColumnDataSource
from bokeh.embed import components

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
    cat = db.Column(db.String(200))
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
    month = Col('Month')
    day = Col('Day')
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
    cd_query = db_session.query(Reports).with_entities(Reports.month, Reports.day, Reports.cases, Reports.deaths).filter(Reports.cat == search_string)
    cd = cd_query.all()
    cd.reverse()
    results = countries_query.all()


    if not results:
        flash('No results found!')
        return redirect('/')
    else:

        # display results
        info_table = Results(results)
        cd_table = CasesAndDeaths(cd)
        cd_table.border = True
        info_table.border = True
        df = pd.DataFrame(cd, columns=['month', 'day', 'cases', 'deaths'])
        source = ColumnDataSource(df)

        # Car list
        day = df ['day']
        cases = df['cases']
        length = len(df)
        print(length)
        date_list = source.data['day'].tolist()
        cases_list = source.data['cases'].tolist()
        deaths_list = source.data['deaths'].tolist()

        print(date_list)

        p = figure(
            plot_width=800,
            plot_height=600,
            title='COVID data for {search}'.format(search=search_string),
            x_axis_label='Date',
            tools="pan,box_select,zoom_in,zoom_out,save,reset"
        )

        glyph = VBar(x='day', top='cases', bottom=0, width=0.5, fill_color="#b3de69")
        p.add_glyph(source, glyph)
        script, div = components(p)
        return render_template('results.html', table=info_table, div=div, script=script)


if __name__ == '__main__':
    app.run()
