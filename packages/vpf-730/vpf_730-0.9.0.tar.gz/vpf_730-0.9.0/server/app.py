from flask import Flask
from flask import request
from flask import redirect
from flask import url_for
from random import randint

app = Flask(__name__)

@app.route('/api/vpf-730/data', methods=['GET', 'POST'])
def data():
    print(request.json)
    return {'code': 200}


@app.route('/api/vpf-730/status')
def status():
    return {'latest_date': 1671229620 }

if __name__ == '__main__':
    app.run(debug=True)
