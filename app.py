from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import PrimaryKeyConstraint, create_engine
import psycopg2
from staging_createdb import createDB

app = Flask(__name__)

ENV = 'dev'
if ENV == 'dev':
    address = 'postgresql://postgres:postgres@localhost/'
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = address
    db = SQLAlchemy(app)
else:
    address = 'postgres://swtsxkwlolegyh:ce7118b4964bf64170dba2e2aab740e2305ec8b69e572bf9d2d0f54381088bb4@ec2-54-159-138-67.compute-1.amazonaws.com:5432/d8uu6s9ng0kauk'
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = address
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

conn_string = address
conn = psycopg2.connect(conn_string)
print('success')

@app.route('/')
def index():
    return render_template('index.html')

# @app.route('/country/<name>', methods=['GET'])
# def get_country(name):
#     if request.method == 'GET':
#         country = request.form['country']
#     if country == '':
#         return render_template('index.html', message='Please eneter required fields')
#     return render_template('countries.html')

if __name__ == '__main__':
    app.run()
