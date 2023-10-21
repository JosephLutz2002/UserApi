from flask import Flask, request
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, create_refresh_token, get_jwt_identity
from flask_jwt_extended.exceptions import JWTDecodeError
from datetime import timedelta
import os
import uuid
from insert import insert_user,get_user,validate_unique_user,add_module,add_Assingment,add_test,update_Assignment,update_Test
app = Flask(__name__)

# Change these to your own secret keys
app.config['JWT_SECRET_KEY'] = os.environ.get('ACCESS')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=10)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)

jwt = JWTManager(app)

# Sample user data (replace with your user management system)
users = {
   "Joseph":123,
   "user1":"password1"
}
refresh_tokens = {}

# Endpoint for user authentication and token generation
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if not username or not password:
        return {'message': 'Authentication failed'}, 401
    login = get_user(username,password)
    if len(login) == 0:
        return {'message':'Username or password incorrect'}
    print(type(login))
    access_token = create_access_token(identity=login[0][0])
    refresh_token = create_refresh_token(identity=login[0][0])
    refresh_tokens[username] = refresh_token
    return {'access_token': access_token, 'refresh_token': refresh_token,'userid':login[0][0],'username':login[0][1],'password':login[0][2],'email':login[0][3]}, 200

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

@app.route('/addModule', methods=['POST'])
def addModule():
    module_name = request.json.get('module',None)
    module_year = request.json.get('year',None)
    module_code = request.json.get('code',None)
    user_id = request.json.get('userid',None)
    module_id = str(uuid.uuid4())
    add_module(module_id,module_name,module_year,module_code,user_id)
    return {"Message":"Success"}

@app.route('/addAssignment',methods=['POST'])
def addAssignment():
    name = request.json.get('name',None)
    desc = request.json.get('desc',None)
    date = request.json.get('date',None)
    userid = request.json.get('id',None)
    module_id = request.json.get("module")
    weighting = request.json.get('weighting',None)
    Assignment_id = str(uuid.uuid4())
    print(name)
    print(desc)
    print(date)
    print(userid)
    print(module_id)
    print(weighting)
    add_Assingment(name,desc,date,userid,Assignment_id,module_id,weighting)
    return {"Message":"Success"}

@app.route('/addTest',methods=['POST'])
def addTest():
    name = request.json.get('name',None)
    date = request.json.get('date',None)
    user_id = request.json.get('userid',None)
    module_id = request.json.get('moduleid',None)
    weighting = request.json.get('weighting',None)
    test_id = str(uuid.uuid4())
    add_test(name,date,test_id,module_id,user_id,weighting)
    return{"Message":"Success"}

@app.route('/updateAssignment',methods=['POST'])
def updateAssignment():
    name = request.json.get('name',None)
    assign_id = request.json.get('assignid',None)
    module_id = request.json.get('moduleid',None)
    user_id = request.json.get('userid',None)
    mark = request.json.get("mark",None)
    print(name)
    print(assign_id)
    print(module_id)
    print(user_id)
    print(mark)
    update_Assignment(assign_id,module_id,user_id,mark,name)
    return{"Message":"Success"}

@app.route('/updateTest',methods=['POST'])
def updateTest():
    name = request.json.get('name',None)
    test_id = request.json.get('testid',None)
    module_id = request.json.get('module',None)
    user_id = request.json.get('user',None)
    mark = request.json.get('mark',None)
    update_Test(mark,name,test_id,user_id,module_id)
    return {"Message":"Success"}

@app.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh_token():
    current_user = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user)
    return {'access_token': new_access_token}, 200

if __name__ == '__main__':
    app.run(debug=True)
