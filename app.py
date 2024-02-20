from flask import Flask, jsonify, request, render_template, url_for, redirect, flash, session
import jwt
from datetime import datetime, timedelta
from functools import wraps
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

#JWT secret key
app.config['SECRET_KEY'] = 'b0c28c7c1c7a4b4f959abda78d11971e'

#Local db connection string
client =  MongoClient('localhost', 27017)

#Docker db connection string
# client =  MongoClient('mongo', 27017)

#mongodb database
db = client.flask_database
#todos collection
users = db.users

def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        #Extract token from the Authorization header
        auth_header = request.headers.get('Authorization')
        token = None
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(" ")[1]
        
        if not token:
            return jsonify({'Alert': 'Token is missing'}), 403
        
        try:
            payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            request.user_role = payload.get('role')
        except jwt.ExpiredSignatureError:
            return jsonify({'Alert': 'Token has expired'}), 401  #Token is expired
        except jwt.InvalidTokenError:
            return jsonify({'Alert': 'Invalid token'}), 403  #Token is invalid
            
        return func(*args, **kwargs)
    return decorated

#Home
@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        user_role = session.get('role')
    if user_role in ['admin', 'super']:
        user_collection = users.find()
        users_list = list(user_collection)
        return render_template('home.html', users=users_list, role=user_role)
    else:
        return render_template('home.html', role=user_role)

#Public
@app.route('/public')
def public():
    return 'For Public'

#Authenticated
@app.route('/auth')
@token_required
def auth():
    return jsonify({'role': request.user_role})

#Checking if user exists in db and creating a session
@app.route('/login', methods=['POST','GET'])
def login():
    username = request.form['username']
    password = request.form['password']

    user = users.find_one({"username":username, "password":password})
    if user:
        user_role = user.get('role','USER')
        session['logged_in'] = True
        session['role'] = user_role
        token = jwt.encode({
            'user':request.form['username'],
            'role': user_role,
            'exp': datetime.utcnow() + timedelta(seconds=120)
        },
            app.config['SECRET_KEY'])
        return jsonify({'token':token})
    else:

        if session.get('logged_in'):
            return redirect(url_for('home'))
        
        flash('Your username or password does not match', 'danger')
        return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))  # Use the name of the function


#Adding user to mongoDb
@app.route("/signup", methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']

        existing_user = users.find_one({'username': username})
        if existing_user:
            return "Username already exists.", 400

        users.insert_one({'username': username, 'password': password, 'role': role})
        return redirect(url_for('home'))

    return render_template('signup.html')

#Route to forgot password
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

#Rest password if username exists
@app.route('/reset_password/<username>', methods=['GET', 'POST'])
def reset_password(username):
    if request.method == 'POST':
        new_password = request.form['new_password']
        #updating old password from username to new password
        users.update_one({"username": username}, {"$set": {"password": new_password}})
        #Redirecting to sign in page
        return redirect(url_for('login'))
    return render_template('reset_password.html', username=username)

#Editing user profile based on _id
@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):
    if request.method == 'POST':
        new_username = request.form['username']
        new_password = request.form['password']
        users.update_one({"_id": ObjectId(id)}, {"$set": {"username": new_username, "password": new_password}})
        return redirect(url_for('home'))
    else:
        user = users.find_one({"_id": ObjectId(id)})
        if user:
            return render_template('edit_user.html', user=user)
        else:
            return 'User not found', 404

#Deleting user from mongoDb via _id
@app.post("/<id>/delete/")
def delete(id):
    #Delete user by getting mongo object id
    users.delete_one({"_id":ObjectId(id)})
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int("5003"),debug = True)