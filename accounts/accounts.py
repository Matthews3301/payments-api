# A class to represent an Account with an id and integer balance
class Account:

  # Member properties:
  #   id:      Integer id
  #   balance: Integer balance
  #   locked: Boolean locked

  # Note that these property names match the column names
  def __init__(self, id, balance, locked):
    self.id = id
    self.balance = balance
    self.locked = locked

# Gets a single account with the given id from the database, or None if it does not exist.
def getAccount(db, id):
  # Open a database connection
  with db.cursor() as cur:
    # Fetch the row.  %(id)s is filled in with 'id' from the parameters dictionary.
    cur.execute('SELECT * FROM accounts WHERE id = %(id)s', { 'id': id })
    # See if we got any rows back
    if cur.rowcount == 0:
      # We didn't, so return None
      return None

    # We did, so build an Account from it.  Note that we can pass the row directly into the
    # Account constructor because the column names match with the constructor arguments, so
    # the splat (**row) maps the named properties in the row dictionary to the named kwargs
    # in the Account constructor.
    row = cur.fetchone()
    return Account(**row)

# Changes the balance of the account
def updateBalance(db, id, new_amount):
  with db.cursor() as cur:
    cur.execute('''UPDATE accounts
                   SET balance = %(new_amount)s
                   WHERE id = %(id)s;''', { 'id': id, 'new_amount': new_amount })
    return True
