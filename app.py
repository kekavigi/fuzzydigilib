#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from flask import Flask, render_template, request

# untuk koneksi ke MongoDB

from flask_pymongo import PyMongo

# :)

app = Flask(__name__, instance_relative_config=True)
app.config['MONGO_URI'] = os.environ['MONGO_URI']
infobox = PyMongo(app).cx.digilib.infobox


# daftar rute

@app.route('/about')
def about():
    return render_template('about.html', title='Tentang situs')


@app.route('/advanced')
def advanced():
    return render_template('advanced.html', title='Pencarian lanjut')


@app.route('/')
@app.route('/index', methods=['GET'])
def index():
    if request.method == 'GET':
        return render_template('index.html', title='UwU*')


@app.route('/results', methods=['GET', 'POST'])
def results():
    if request.method == 'GET':
        return render_template('results.html', title='Hasil...',
                               total='', query='', response=[])
    if request.method == 'POST':
        if 'query' not in request.form:
            not_found(None)
        query = request.form['query']
        result = infobox.find({'$text': {'$search': query}},
                              {'score': {'$meta': 'textScore'
                              }}).sort('score', -1).limit(200)
        response = []
        for info in result:
            response.append({
                'id': info['id'],
                'judul': info['title'] or '',
                'oleh': info['oleh'] or '',
                'kontributor': info['kontributor'] or '',
                'tanggal': info['tanggal'] or '',
                'abstrak': info['abstrak'] or '',
                })
        return render_template('results.html', title='Hasil...',
                               total=len(response), query=query,
                               response=response)


@app.route('/<int:idnum>')
def get_infobox(idnum):
    try:
        info = [_ for _ in infobox.find({'id': idnum})][0]
    except IndexError:
        return not_found(None)
    response = {
        'id': info['id'],
        'judul': info['title'] or '',
        'oleh': info['oleh'] or '',
        'kontributor': info['kontributor'] or '',
        'koleksi': info['koleksi'] or '',
        'fakultas': info['fakultas'] or '',
        'penerbit': info['penerbit'] or '',
        'subjek': info['subjek'] or '',
        'kunci': info['keyword'] or '',
        'sumber': info['sumber'] or '',
        'tanggal': info['tanggal'] or '',
        'abstrak': info['abstrak'] or '',
        'pdf': info['pdf'],
        }

    return render_template('item.html', title=info['title'],
                           response=response)


@app.errorhandler(404)
def not_found(error):
    return (render_template('404.html'), 404)

@app.errorhandler(405)
def error405(error):
    return (render_template('405.html'), 405)

@app.errorhandler(500)
def error500(error):
    return (render_template('500.html'), 500)
