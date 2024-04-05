from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)

# Configure the database connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/login'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
CORS(app, origins=['http://localhost:3001'])

# Define a model for the user registration data
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    lines = db.Column(db.Text, nullable=False)

# Route to handle form submission for registration
@app.route("/register", methods=['POST','GET'])
def register():
    if request.method == 'POST':
        try:
            # Retrieve data from the form
            username = request.json['username']
            password = request.json['password']
            email = request.json['email']
            lines = request.json['lines']

            new_user = User(username=username, password=password, email=email, lines=lines)

            db.session.add(new_user)
            db.session.commit()

            return jsonify({
                "message": "User registered successfully",
                "user": {
                    "id": new_user.id,
                    "username": new_user.username,
                    "password": new_user.password,
                    "email": new_user.email,
                    "lines": new_user.lines
                }
            })
        except Exception as e:
            # If an error occurs, rollback the session and return an error message
            db.session.rollback()
            return jsonify({"error": str(e)})
    else:
        try:
            # Fetch all user records from the database
            all_users = User.query.all()

            # Prepare user data for JSON serialization
            user_data = []
            for user in all_users:
                user_data.append({
                    "id": user.id,
                    "username": user.username,
                    "password": user.password,  # Note: This is sensitive information, consider removing it
                    "email": user.email,
                    "lines": user.lines
                    # Add more fields as needed
                })

            # Return JSON response with all user data
            return jsonify({"users": user_data})
        except Exception as e:
            # Error handling for database query
            return jsonify({"error": str(e)})


@app.route("/authenticate", methods=['GET'])
def authenticate_user():
    # Retrieve username and password from the request parameters
    username = request.args.get('username')
    password = request.args.get('password')

    # Perform authentication logic by querying the database
    user = User.query.filter_by(username=username, password=password).first()

    if user:
        return jsonify({"success": True}),200
    else:
        return jsonify({"success": False}),401


if __name__ == '__main__':
    app.run(debug=True ,host='192.168.5.34',port=8089)
