from __main__ import app, db, flask
import traceback
from transactions import transactions
from accounts import accounts

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
'''
Example POST data:
{
    "id_from": 2,
    "id_to": 1,
    "amount": 100
}
'''
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
      return None
    return account

  account_from = getAccountData(id_from)
  account_to = getAccountData(id_to)

  # Check if the accounts exist
  if not account_from or not account_to:
    return {'message': 'Account doesn\'t exist'}, 400

  # Check if account is not locked
  if account_from.locked:
    return {'message': 'Processing another transaction for this account - please try again'}, 400

  # Check if id_from account has enough funds
  if account_from.balance < amount:
    return {'message': 'Not enough balance in the account'}, 400

  def manageAccountLock(lock):
    with db.cursor() as cur:
      cur.execute('''UPDATE accounts SET locked = %(lock)s WHERE id = %(id)s;''',
                  {'id': id_from, 'lock': 'TRUE' if lock else 'FALSE'})

  # Lock "from" account until the transaction is done - to prevent double spend
  manageAccountLock(True)

  new_transaction = None
  try:
    new_transaction = transactions.newTransaction(db, id_from, id_to, amount)
    accounts.updateBalance(db, account_from.id, account_from.balance - amount)
    accounts.updateBalance(db, account_to.id, account_to.balance + amount)
  except Exception:
    traceback.print_exc()
    # Unlock "from" account
    manageAccountLock(False)
    return { 'message': 'Unknown error' }, 500

  # Unlock "from" account
  manageAccountLock(False)

  return { 'data': new_transaction.__dict__ }