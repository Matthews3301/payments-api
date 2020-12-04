#!/usr/bin/env python3

import flask
import psycopg2
import psycopg2.extras

from configs import configs

# Load the configuration
config = configs.parseConfig()

# Start up the database connection, by default returning dictionaries with property names from queries
db = psycopg2.connect(**config['database'], cursor_factory=psycopg2.extras.RealDictCursor)
# Run the session in autocommit (ie, non-transactional) mode by default.  Do not change this setting.
db.set_session(autocommit=True)

# Build a basic Flask app
app = flask.Flask(__name__)

from routes import ping
from routes import accounts
from routes import transactions

# Start the app listening.
if __name__ == '__main__':
  app.run(port=config['server']['port'])
