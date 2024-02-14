from flask import Flask, jsonify, request, abort, render_template, url_for, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
client =  MongoClient('localhost', 27017)
# client =  MongoClient('mongo', 27017)

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
        password = request.form['password']
        usertype = request.form['usertype']
        users.insert_one({'username':username, 'password':password , 'usertype':usertype})
        return redirect(url_for('index'))
    all_users = users.find()
    return render_template('index.html', users = all_users)

@app.route('/forgot_password', methods=['POST' , 'GET'])
def forgot_password():
    if request.method == 'POST':
        username = request.form['username']
        user = users.find_one({"username": username})
        if user:
            #If user is found, redirect to the reset password page
            return redirect(url_for('reset_password', username=username))
        else:
            #If user is not found alert user that user does not exist
            return render_template('forgot_password.html', message='User name was not found')
    return render_template('forgot_password.html')

@app.route('/reset_password/<username>', methods=['GET', 'POST'])
def reset_password(username):
    if request.method == 'POST':
        new_password = request.form['new_password']
        #updating old password from username to new password
        users.update_one({"username": username}, {"$set": {"password": new_password}})
        #Redirecting to sign in page
        return redirect(url_for('index'))
    return render_template('reset_password.html', username=username)

#Deleting user from mongoDb via _id
@app.post("/<id>/delete/")
def delete(id):
    #Delete user by getting mongo object id
    users.delete_one({"_id":ObjectId(id)})
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int("5003"),debug = True)