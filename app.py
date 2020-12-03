#!/usr/bin/env python3

import traceback

import flask
import psycopg2
import psycopg2.extras

from accounts import accounts
from transactions import transactions
from configs import configs

# Load the configuration
config = configs.parseConfig()

# Start up the database connection, by default returning dictionaries with property names from queries
db = psycopg2.connect(**config['database'], cursor_factory=psycopg2.extras.RealDictCursor)
# Run the session in autocommit (ie, non-transactional) mode by default.  Do not change this setting.
db.set_session(autocommit=True)

# Build a basic Flask app
app = flask.Flask(__name__)

# TODO: Consider pulling some logic out of this big file.

# Basic ping endpoint
@app.route('/ping')
def ping():
  return {
    'message': 'pong'
  }

# Single account endpoint
@app.route('/accounts/<int:id>')
def getAccount(id):
  # Try to fetch the Account object from the database
  account = None
  try:
    # Do the fetch
    account = accounts.getAccount(db, id)
  except Exception:
    # Something went wrong, so log it and return a 500
    traceback.print_exc()
    return { 'message': 'Unknown error' }, 500

  # Couldn't find the Account
  if account is None:
    return { 'message': 'Unable to find that account' }, 404

  # Found the Account, so return it.  __dict__ gives us the default serialization of all properties.
  return { 'data': account.__dict__ }

# Account transactions endpoint
@app.route('/transactions/<int:id>')
def getAccountTransactions(id):
  transactions_list = []
  try:
    transactions_list = transactions.getTransactions(db, id)
  except Exception:
    traceback.print_exc()
    return { 'message': 'Unknown error' }, 500

  transactions_list_dicts = []
  for transaction in transactions_list:
    transactions_list_dicts.append(transaction.__dict__)
  return { 'data': transactions_list_dicts }

# Create transaction endpoint
@app.route('/transact', methods = ['POST'])
def transact():
  id_from = flask.request.get_json().get('id_from')
  id_to = flask.request.get_json().get('id_to')
  amount = flask.request.get_json().get('amount')

  if not id_from or not id_to or not amount:
    return {'message': 'Incomplete data'}, 400

  def getAccountData(id):
    account = None
    try:
      account = accounts.getAccount(db, id)
    except Exception:
      traceback.print_exc()
      return {'message': 'Unknown error'}, 500
    return account

  account_from = getAccountData(id_from)
  account_to = getAccountData(id_to)

  # Check if the accounts exist
  if not account_from or not account_to:
    return {'message': 'Account doesn\'t exist'}, 400

  # Check if id_from account has enough funds
  if account_from.balance < amount:
    return {'message': 'Not enough balance in the account'}, 400

  new_transaction = None
  try:
    new_transaction = transactions.newTransaction(db, id_from, id_to, amount)
    accounts.updateBalance(db, account_from.id, account_from.balance - amount)
    accounts.updateBalance(db, account_to.id, account_to.balance + amount)
  except Exception:
    traceback.print_exc()
    return { 'message': 'Unknown error' }, 500

  return { 'data': new_transaction.__dict__ }

# Start the app listening.
if __name__ == '__main__':
  app.run(port=config['server']['port'])
