from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import PrimaryKeyConstraint, create_engine
import psycopg2

app = Flask(__name__)

ENV = 'dev'
if ENV == 'dev':
    address = 'postgresql://postgres:postgres@localhost/'
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = address
else:
    address = 'postgres://swtsxkwlolegyh:ce7118b4964bf64170dba2e2aab740e2305ec8b69e572bf9d2d0f54381088bb4@ec2-54-159-138-67.compute-1.amazonaws.com:5432/d8uu6s9ng0kauk'
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = address
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
engine = create_engine(address)
connection = engine.raw_connection()
cursor = connection.cursor()

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
        self.continent_exp = continent_exp

class Reports(db.Model):
    __tablename__ = 'reports'
    report_id = db.Column(db.Integer, primary_key=True)
    geoID = db.Column(db.String(200))
    day = db.Column(db.Integer)
    month = db.Column(db.Integer)
    year = db.Column(db.Integer)
    cases = db.Column(db.Integer)
    deaths = db.Column(db.Integer)

    def __init__(self, cat, popdata, ctc, continent_exp):
        self.report_id = report_id
        self.geoID = geoID
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
    dateRep = db.Column(db.String(200))
    cat = db.Column(db.String(200), db.ForeignKey('countries.cat'))
    report_id = db.Column(db.Integer, db.ForeignKey('reports.report_id'))

    def __init__(self, cat, popdata, ctc, continent_exp):
        self.dateRep = dateRep
        self.cat = cat
        self.report_id = report_id

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/country/<name>', methods=['GET'])
def get_country(name):
    if request.method == 'GET':
        country = request.form['country']
    if country == '':
        return render_template('index.html', message='Please eneter required fields')
    return render_template('countries.html')

if __name__ == '__main__':
    app.run()
