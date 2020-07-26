ifrom flask import Flask, render_template, reqiest
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


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['REQUEST'])
def request():
    if request.method == 'REQUEST':
        # put request queries here
        return render_template('country.html')




if __name__ == '__main__':
    app.run()
