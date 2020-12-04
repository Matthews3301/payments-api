from __main__ import app, db
import traceback
from accounts import accounts

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
