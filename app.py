from flask import Flask, render_template, reqiest
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

ENV = 'dev'
if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/'

else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

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


@app.route('/submit', methods=['GET'])
def request():
    if request.method == 'REQUEST':
        # put request queries here
        return render_template('country.html')


if __name__ == '__main__':
    app.run()
