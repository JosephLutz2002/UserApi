from flask import Flask, request,send_from_directory
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, create_refresh_token, get_jwt_identity
from flask_jwt_extended.exceptions import JWTDecodeError
from werkzeug.utils import secure_filename
from datetime import timedelta
import os
import uuid
from flask_cors import CORS
from insert import insert_user,get_user,validate_unique_user,add_module,add_Assingment,add_test,update_Assignment,update_Test,getAllModuleForUser,deleteUserModule,getAllAssignments,getAllTests,getMark,deleteAssig,deleteT
app = Flask(__name__)
CORS(app)
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
@app.route('/api/account/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if not username or not password:
        return {'message': 'Authentication failed'}, 401
    login = get_user(username,password)
    if len(login) == 0:
        return {'message':'Username or password incorrect'},400
    print(type(login))
    access_token = create_access_token(identity=login[0][0])
    refresh_token = create_refresh_token(identity=login[0][0])
    refresh_tokens[username] = refresh_token
    return {'access_token': access_token, 'refresh_token': refresh_token,'userid':login[0][0],'username':login[0][1],'password':login[0][2],'email':login[0][3]}, 200

@app.route('/api/account/createUser',methods=['POST'])
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

@app.route('/api/modules/addModule', methods=['POST'])
@jwt_required()
def addModule():
    module_name = request.json.get('module',None)
    module_year = request.json.get('year',None)
    module_code = request.json.get('code',None)
    user_id = get_jwt_identity()
    module_id = str(uuid.uuid4())
    add_module(module_id,module_name,module_year,module_code,user_id)
    return {"id":module_id}

@app.route('/api/modules/addAssignment',methods=['POST'])
@jwt_required()
def addAssignment():
    name = request.json.get('name',None)
    desc = request.json.get('desc',None)
    date = request.json.get('date',None)
    userid = get_jwt_identity()
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
    return {"id":Assignment_id}

@app.route('/api/modules/addTest',methods=['POST'])
@jwt_required()
def addTest():
    name = request.json.get('name',None)
    date = request.json.get('date',None)
    user_id = get_jwt_identity()
    module_id = request.json.get('moduleid',None)
    weighting = request.json.get('weighting',None)
    test_id = str(uuid.uuid4())
    add_test(name,date,test_id,module_id,user_id,weighting)
    return{"id":test_id}

@app.route('/api/modules/updateAssignment',methods=['POST'])
@jwt_required()
def updateAssignment():
    name = request.json.get('name',None)
    assign_id = request.json.get('assignid',None)
    module_id = request.json.get('moduleid',None)
    user_id = get_jwt_identity()
    mark = request.json.get("mark",None)
    update_Assignment(assign_id,module_id,user_id,mark,name)
    mark = getMark(user_id,module_id)
    return {"mark":mark}

@app.route('/api/modules/updateTest',methods=['POST'])
@jwt_required()
def updateTest():
    name = request.json.get('name',None)
    test_id = request.json.get('testid',None)
    module_id = request.json.get('module',None)
    user_id = get_jwt_identity()
    mark = request.json.get('mark',None)
    update_Test(mark,name,test_id,user_id,module_id)
    mark = getMark(user_id,module_id)
    return {"mark":mark}

@app.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh_token():
    current_user = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user)
    return {'access_token': new_access_token}, 200


@app.route('/api/modules/getModules',methods=['GET'])
@jwt_required()
def getNotes():
    id = get_jwt_identity()
    modules = getAllModuleForUser(id)
    return {"Modules":modules}

@app.route('/api/modules/deleteModule',methods=['POST'])
@jwt_required()
def deleteModule():
    moduleId = request.json.get('moduleid')
    userid = get_jwt_identity()
    print(moduleId)
    print(userid)
    deleteUserModule(moduleId,userid)
    return {'delete':"success"}


@app.route('/api/modules/getAssignments',methods=['GET'])
@jwt_required()
def getAssignments():
    module_id = request.args.get('module_id')
    user_id = get_jwt_identity()
    assignments = getAllAssignments(module_id,user_id)
    print(assignments)
    return {'assignments':assignments}

@app.route('/api/modules/getTests',methods=['GET'])
@jwt_required()
def getTests():
    module_id = request.args.get('module_id')
    user_id = get_jwt_identity()
    tests = getAllTests(module_id,user_id)
    print(tests)
    return {'tests':tests}    


@app.route('/api/modules/average',methods=['GET'])
@jwt_required()
def getUserMark():
    userid=get_jwt_identity()
    module_id = request.args.get('module_id')
    mark = getMark(userid,module_id)
    print(mark)
    return {'average':mark}
    
    
@app.route('/api/modules/deleteAssignment',methods=['POST'])
@jwt_required()
def deleteAssignment():
    assign_id = request.json.get('assignid')
    module_id = request.json.get('moduleid')
    user_id = get_jwt_identity()
    deleteAssig(user_id,assign_id,module_id)
    mark = getMark(user_id,module_id)
    return {"mark":mark}

@app.route('/api/modules/deleteTest',methods=['POST'])
@jwt_required()
def deleteTest():
    test_id = request.json.get('testid')
    module_id = request.json.get('moduleid')
    user_id = get_jwt_identity()
    deleteT(user_id,module_id,test_id)
    mark = getMark(user_id,module_id)
    return {"mark":mark}  

UPLOAD_FOLDER = 'upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/upload', methods=['POST'])
@jwt_required()
def upload_file():
    current_user = get_jwt_identity()
    print(current_user)
    if 'file' not in request.files:
        return {'error': 'No file part'}
    print(request.files)
    file = request.files['file']
    print('file is ', file)
    if file.filename == '':
        return {'error': 'No selected file'}

    if file:
        filename = secure_filename(current_user+'.png')
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return {'message': 'File uploaded successfully'}

@app.route('/download')
@jwt_required()
def download_file():
    current_user = get_jwt_identity()

    if current_user:
        file_path = os.path.join(UPLOAD_FOLDER, current_user+'.png')
        if os.path.exists(file_path):
            return send_from_directory(UPLOAD_FOLDER, current_user+'.png')        
        else:
            return "File not found", 404
    else:
        return "Missing 'filename' query parameter", 400
  
if __name__ == '__main__':
    app.run(debug=True)
