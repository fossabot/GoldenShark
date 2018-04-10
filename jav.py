import json
import os
import subprocess

from flask import Flask, jsonify, request, send_from_directory
from scrapinghub import ScrapinghubClient

app = Flask(__name__, static_url_path='')


@app.route("/")
def index():
    return app.send_static_file('index.html')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/thzdetails/<int:page_id>', methods=['GET'])
def getdetail(page_id):
    if request.method == 'GET':
        with open(r'/home/GoldenShark/codelist/' + str(page_id + 100) + r'.json', 'r') as thzfile:
            return corsresponse(json.load(thzfile))


@app.route('/totalpages', methods=['GET'])
def gettotalpages():
    if request.method == 'GET':
        return corsresponse(len(os.listdir(r'/home/GoldenShark/codelist/')))


@app.route('/updatecode', methods=['POST'])
def performupdatecode():
    if request.method == 'POST':
        output = subprocess.check_output(
            ['git', '-C', r'/home/GoldenShark', 'pull', '-v'])
        return output


@app.route('/codelist', methods=['GET'])
def fetchcodelist():
    if request.method == 'GET':
        subprocess.Popen(['python3', r'/home/GoldenShark/codelist.py'])
        return 'update run fetch code list'


def corsresponse(origres):
    corsres = jsonify(origres)
    corsres.headers['Access-Control-Allow-Origin'] = '*'
    corsres.headers['Access-Control-Allow-Methods'] = 'GET, POST'
    corsres.headers['Access-Control-Allow-Headers'] = 'x-requested-with, content-type'
    return corsres
