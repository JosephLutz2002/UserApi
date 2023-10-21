from flask import Flask, request
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, create_refresh_token, get_jwt_identity
from flask_jwt_extended.exceptions import JWTDecodeError
from datetime import timedelta
import os
import uuid
from insert import insert_user,get_user,validate_unique_user
app = Flask(__name__)

# Change these to your own secret keys
app.config['JWT_SECRET_KEY'] = os.environ.get('ACCESS')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=30)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)

jwt = JWTManager(app)

# Sample user data (replace with your user management system)
users = {
   "Joseph":123 
}
refresh_tokens = {}

# Endpoint for user authentication and token generation
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    print(request.json)
    if username not in users or users[username] != password:
        return {'message': 'Authentication failed'}, 401
    access_token = create_access_token(identity=username)
    refresh_token = create_refresh_token(identity=username)
    refresh_tokens[username] = refresh_token
    user_data = get_user(username,password)
    print(user_data)
    return {'access_token': access_token, 'refresh_token': refresh_token}, 200

@app.route('/createUser',methods=['POST'])
def createAccount():
    username = request.json.get('username',None)
    password = request.json.get('password',None)
    email = request.json.get('email',None)
    if not validate_unique_user(username):
        return {'message': 'Username not unique'},401
    
    if not username or not password:
        return {'message': 'Authentication failed'}, 401
    users[username]=password
    user_id = str(uuid.uuid4())
    user_data = {
    "userid": user_id,
    "user": username,
    "pass": password,
    "email": email
    }
    insert_user(user_data)
    return {"Success": True}

@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()  # Retrieve the identity from the JWT
    print(current_user)
    return {'message': f'Hello, {current_user}! This is a protected resource.'}, 200


if __name__ == '__main__':
    app.run(debug=True)
