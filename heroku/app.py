from flask import Flask, render_template, request
from pickle import load
from rapidfuzz.fuzz import token_set_ratio as T

######################

app = Flask(__name__)

with open('dt.pickle', 'rb') as handle:
    DICTI, TOTAL = load(handle)
LENDICTI = len(DICTI)

######################

@app.route('/', methods = ['GET', 'POST'])
def search():
    if request.method == 'GET':
        return render_template('home.html')
    if request.method == 'POST':
        words = request.form['searchbar']
        result = [DICTI[i] for i, text in zip(range(LENDICTI), TOTAL)
                if T(text, words)==100]

        return render_template('home.html',
                            in_search_mode = True,
                            query = words,
                            data = result,
                            datasize = len(result))

if __name__ == '__main__':
   app.run()
