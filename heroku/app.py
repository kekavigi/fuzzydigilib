import pymongo
import os

from flask import Flask, render_template, request
from pickle import load

######################

app = Flask(__name__)

url = os.environ.get('MONGODB_URI', None)
client = pymongo.MongoClient(url)
katalog = client.digilib.katalog

######################

@app.route('/', methods = ['GET', 'POST'])
def search():
    if request.method == 'GET':
        return render_template('home.html')

    if request.method == 'POST':
        words = request.form['searchbar']
        
        # cari exact match di database
        cursor = katalog.find({'$text': { '$search': '\"{}\"'.format(words) }},
                              {'_id':0, 'id':0})
        
        # simplify format to list of dict
        result = [x for x in cursor]
        
        # render it on screen
        return render_template('home.html',
                            in_search_mode = True,
                            query = words,
                            result = result,
                            datasize = len(result))

if __name__ == '__main__':
   app.run()
