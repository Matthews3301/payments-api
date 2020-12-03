# A class to represent a Transaction
class Transaction:

  def __init__(self, id, id_from, id_to, amount, datetime):
    self.id = id
    self.id_from = id_from
    self.id_to = id_to
    self.amount = amount
    self.datetime = datetime

def getTransactions(db, id):
  with db.cursor() as cur:
    cur.execute('SELECT * FROM transactions WHERE id_from = %(id)s OR id_to = %(id)s ORDER BY datetime DESC', { 'id': id })
    if cur.rowcount == 0:
      return []

    rows = cur.fetchall()
    transactions = []
    for row in rows:
      transactions.append(Transaction(**row))
    return transactions

def newTransaction(db, id_from, id_to, amount):
  with db.cursor() as cur:
    # Create new transaction record
    cur.execute('''INSERT INTO transactions (id, id_from, id_to, amount, datetime)
                   VALUES (DEFAULT, %(id_from)s, %(id_to)s, %(amount)s, NOW())
                   RETURNING *''',
                { 'id_from': id_from, 'id_to': id_to, 'amount': amount })
    new_transaction = cur.fetchone()

    return Transaction(**new_transaction)
