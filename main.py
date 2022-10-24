import psycopg2
import requests
from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

db = psycopg2.connect(dbname='dbpython', user='postgres', password='212552', host='localhost')
cur = db.cursor()


@app.route('/index')
def index():
    return render_template("index.html")


@app.route('/nft', methods=['POST', 'GET'])
def nft():
    output = request.form.to_dict()
    adress = output["adress"]
    headers = {

        "accept": "application/json",
        "X-API-Key": "SWnpmagdLrYt67aFhsaBRRzoubD59cdQkydkZLeljvVREBpWGmpLktfRLZXcvudp"

    }
    url = 'https://solana-gateway.moralis.io/nft/mainnet/' + adress + '/metadata'

    cur.execute("SELECT * FROM address WHERE addres = %s", (adress,))
    ans = cur.fetchall()
    response = requests.get(url, headers=headers)
    print(ans)
    if ans != []:
        print('from db')
        return render_template("result.html", result=response.text)
    else:
        cur.execute("INSERT INTO address (addres, info) VALUES (%s, %s)", (adress, response.text))
        db.commit()
        print('to db')
        return render_template("result.html", result=response.text)


if __name__ == '__main__':
    app.run(debug=True)
    '''4Jb9EzcUd6k1gC7GSH2iu6H7UcL2ez3NgvAF8n6a1QDs
'''