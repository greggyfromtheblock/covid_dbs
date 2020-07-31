from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:!0307Postgresql!@localhost/postgres_db'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:!0307Postgresql!@localhost/postgres_db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Country(db.Model):
    __tablename__ = 'country'
    countriesandterritories = db.Column(db.Text(), primary_key = True)
    popdata2018 = db.Column(db.Integer)
    countryterritorycode = db.Column(db.Text())
    continentexp = db.Column(db.Text())

    def __init__(self, countriesandterritories, popdata2018, countryterritorycode, continentexp):
        self.countriesandterritories = countriesqndterritories
        self.popdata2018 = popdata2018
        self.countryterritorycode = countryterritorycode
        self.continentexp = continentexp

class Report(db.Model):
    __tablename__ = 'report'
    id = db.Column(db.Integer, primary_key = True)
    geoid = db.Column(db.Text())
    day = db.Column(db.Integer)
    month = db.Column(db.Integer)
    year = db.Column(db.Integer)
    cases = db.Column(db.Integer)
    deaths = db.Column(db.Integer)

    def __init__(self, id, geoid, day, month, year, cases, deaths):
        self.id = id
        self.geoid = geoid
        self.day = day
        self.month = month
        self.year = year
        self.cases = cases
        self.deaths = deaths

class Reported(db.Model):
    __tablename__ = 'reported'
    countriesandterritories = db.Column(db.Text())
    report_id = db.Column(db.Integer, primary_key = True)
    daterep = db.Column(db.Text())

    def __init__(self, countriesandterritories, report_id, daterep):
        self.countriesandterritories = countriesandterritories
        self.report_id = report_id
        self.daterep = daterep

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        tables = request.form['tables']
        if tables == '':
            return render_template('index.html', message='Please select a table.')
        if tables == 'Full Country Table':
            test = Country.query.all()
            return render_template('country.html', test=test)
        if tables == 'Full Report Table':
            test2 = Report.query.all()
            return render_template('report.html', test2=test2)
        if tables == 'Full Reported Table':
            test3 = Reported.query.all()
            return render_template('reported.html', test3=test3)
        if tables == 'Germany': 
            labels = db.engine.execute("SELECT report.day,report.month,report.year,report.deaths FROM country,report,reported WHERE country.countriesandterritories=reported.countriesandterritories AND reported.report_id=report.id AND country.countriesandterritories='Germany' AND report.year = 2020")
            values = db.engine.execute("SELECT report.day,report.month,report.year,report.cases FROM country,report,reported WHERE country.countriesandterritories=reported.countriesandterritories AND reported.report_id=report.id AND country.countriesandterritories='Germany' AND report.year = 2020")
            return render_template('germany.html', labels=labels, values=values)

if __name__ == '__main__':
    app.run()
