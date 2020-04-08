from flask import Flask
from flask_restful import Api
from flask_talisman import Talisman
from flask_cors import CORS
from db import db
import os

from resources.issue import Issue

app = Flask(__name__)
Talisman(app)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///issue-tracker')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)

db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

api.add_resource(Issue, '/api/issues/<project_name>')

if __name__ == '__main__':
    app.run(debug=True)