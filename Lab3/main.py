from flask import Flask, request, jsonify, g
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, unset_jwt_cookies
from flask_cors import CORS  # Add this line to enable CORS
# import subprocess

# bash_command = "python -m http.server"
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['JWT_SECRET_KEY'] = 'jwt_secret_key'  # Change this to a secure key in production
app.config['PAGE_SIZE'] = 5  # Set the number of items per page
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@app.before_request
def before_request():
    if request.endpoint != 'create_tables':
        create_tables()

def create_tables():
    db.create_all()

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = User(username=data['username'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'})

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and bcrypt.check_password_hash(user.password, data['password']):
        access_token = create_access_token(identity=user.id)
        return jsonify({'message': 'Login successful', 'access_token': access_token})
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    resp = jsonify({'message': 'Logout successful'})
    unset_jwt_cookies(resp)
    return resp

@app.route('/books', methods=['GET'])
@jwt_required()  # This decorator enforces authentication
def get_books():
    page = request.args.get('page', 1, type=int)
    per_page = app.config['PAGE_SIZE']
    books = Book.query.paginate(page=page, per_page=per_page, error_out=False)
    book_list = [{'id': book.id, 'title': book.title, 'author': book.author} for book in books.items]
    return jsonify({'books': book_list, 'total_pages': books.pages, 'current_page': page})

@app.route('/books/<int:book_id>', methods=['GET'])
@jwt_required()  # This decorator enforces authentication
def get_book(book_id):
    book = Book.query.get_or_404(book_id)
    return jsonify({'id': book.id, 'title': book.title, 'author': book.author})

@app.route('/books', methods=['POST'])
@jwt_required()  # This decorator enforces authentication
def add_book():
    data = request.get_json()
    new_book = Book(title=data['title'], author=data['author'], user_id=get_jwt_identity())
    db.session.add(new_book)
    db.session.commit()
    return jsonify({'message': 'Book added successfully'})

@app.route('/add_books', methods=['POST'])
@jwt_required()  # This decorator enforces authentication
def add_books():
    data = request.get_json()
    user_id = get_jwt_identity()
    new_books = [Book(title=book['title'], author=book['author'], user_id=user_id) for book in data['books']]
    db.session.add_all(new_books)
    db.session.commit()
    return jsonify({'message': 'Books added successfully'})

@app.route('/books/<int:book_id>', methods=['DELETE'])
@jwt_required()  # This decorator enforces authentication
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    if book.user_id != get_jwt_identity():
        return jsonify({'message': 'Unauthorized to delete this book'}), 403

    db.session.delete(book)
    db.session.commit()
    return jsonify({'message': 'Book deleted successfully'})

if __name__ == '__main__':
    # result = subprocess.run(bash_command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    # output = result.stdout
    # error = result.stderr
    # print("Output:", output)
    # print("Error:", error)
    app.run(port=8080)
