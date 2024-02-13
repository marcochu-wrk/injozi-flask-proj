from flask import Flask, jsonify, request, abort
from markupsafe import escape
app = Flask(__name__)
log_the_user_in = "Test"


books = [
    {"id": 1, "title":"Book 1", "author": "Author 1"},
    {"id": 2, "title":"Book 2", "author": "Author 2"},
    {"id": 3, "title":"Book 3", "author": "Author 3"}
]

valid_login = [
    {"id": 1, "username":"User_1", "password": "1"},
    {"id": 2, "username":"User_2", "password": "2"},
    {"id": 3, "username":"User_3", "password": "3"}
]



@app.route('/login', methods=['POST','GET'])
def login():
    error = None
    if request.method == 'POST':
        if valid_login(request.form['username'],
                       request.form['password']):
            return log_the_user_in(request.form['username'])
            

@app.route('/books', methods=['GET'])
def get_books():
    return jsonify(books)

@app.route('/books/<int:book_id>',methods=['GET'])
def get_book(book_id):
    for book in books:
        if book['id']==book_id:
            return jsonify(book)
        
    return jsonify({'error':'Book not found'}), 404

@app.route('/books', methods=['POST'])
def create_book():
    if not request.json:
        abort(400, description="Request must be JSON")
    
    # Assuming the JSON request contains 'title' and 'author'
    new_book = {
        'id': len(books) + 1,
        'title': request.json.get('title'),
        'author': request.json.get('author')
    }
    books.append(new_book)
    return jsonify(new_book), 201

if __name__ == '__main__':
    app.run(debug = True)