from flask import Flask, jsonify, request, abort, render_template, url_for, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
client =  MongoClient('localhost', 27017)

#mongodb database
db = client.flask_database
#todos collection
users = db.users

log_the_user_in = "Test"

#Adding user to mongoDb
@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        usertype = request.form['usertype']
        users.insert_one({'username':username, 'usertype':usertype})
        return redirect(url_for('index'))
    all_users = users.find()
    return render_template('index.html', users = all_users)

#Deleting user from mongoDb via _id
@app.post("/<id>/delete/")
def delete(id):
    users.delete_one({"_id":ObjectId(id)})
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int("5003"),debug = True)