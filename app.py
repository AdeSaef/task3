from flask import Flask, request, render_template, url_for, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
import requests
from datetime import datetime
from os.path import join, dirname
import os
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME =  os.environ.get("DB_NAME")
app = Flask(__name__)

cxn_str='mongodb+srv://ade:adesaef@cluster0.lqterof.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'
client= MongoClient(cxn_str)

db=client.ade

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/detail/<keyword>')
def detail(keyword):
    api_key='2c20153b-293a-41ba-92c2-77ad2d0e4407'
    url = f'https://www.dictionaryapi.com/api/v3/references/collegiate/json/{keyword}?key={api_key}'
    response = requests.get(url)
    definitions = response.json()
    status=request.args.get('status_give', 'new')
    return render_template(
        'detail.html',
        word=keyword,
        definitions=definitions,
        status=status
    )

@app.route('/api/save_word', methods=['POST'])
def save_word():
    json_data = request.get_json()
    word = json_data.get('word_give')
    definitions = json_data.get('definitions_give')
    doc = {
        'word': word,
        'definitions': definitions,
        'date' : datetime.now().strftime('%Y-%m-%d'),
    }
    db.words.insert_one(doc)
    return jsonify({
        'result': 'success',
        'msg': f'the word, {word}, was saved!!!',
    })

@app.route('/api/delete_word', methods=['POST'])
def delete_word():
    word = request.form.get('word_give')
    db.words.delete_one({'word': word})
    return jsonify({
        'result': 'success',
        'msg': f'the word {word} was deleted'
    })
# @app.route('/practice')
# def practice():
#     return render_template('practice.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)