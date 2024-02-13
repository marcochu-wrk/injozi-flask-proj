from flask import Flask, jsonify, request, abort, render_template, url_for, redirect
from pymongo import MongoClient
from markupsafe import escape
app = Flask(__name__)
client =  MongoClient('localhost', 27017)

#mongodb database
db = client.flask_database
#todos collection
todos = db.todos


log_the_user_in = "Test"


@app.route("/", methods=['POST', 'GET'])
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int("3000"),debug = True)