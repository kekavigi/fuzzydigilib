from flask import Flask, render_template, request
from pickle import load

######################

app = Flask(__name__)

with open('d.pickle', 'rb') as handle:
    DICTI = load(handle)
    
LENDICTI = len(DICTI)

def transform(row):
    res = set()
    for col in row:
        res.update(col.lower().split())
    return res

def found(word, textset):
    l = len(word)
    for text in textset:
        if len(text)>=l and text[:l]==word:
            return True
    return False

def founds(words, text):
    textset = transform(text)
    for word in words.lower().split():
        if not found(word, textset):
            return False
    return True

######################

@app.route('/', methods = ['GET', 'POST'])
def search():
    if request.method == 'GET':
        return render_template('home.html')

    if request.method == 'POST':
        words = request.form['searchbar']
        result = [DICTI[i] for i, text in zip(range(LENDICTI), DICTI)
                if founds(words, text)]

        return render_template('home.html',
                            in_search_mode = True,
                            query = words,
                            data = result,
                            datasize = len(result))

if __name__ == '__main__':
   app.run()
