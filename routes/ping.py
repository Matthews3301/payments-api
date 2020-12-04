from __main__ import app

# Basic ping endpoint
@app.route('/ping')
def ping():
  return {
    'message': 'pong'
  }