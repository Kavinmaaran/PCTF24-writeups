from flask import Flask, request, jsonify, render_template,redirect,url_for,make_response,session
import requests,time,os,secrets,uuid, validators,jwt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from urllib.parse import unquote
from  werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import urlpath
from functools import wraps

app = Flask(__name__)
app.config['SESSION_COOKIE_HTTPONLY'] = False
app.config['JWT_SECRET_KEY'] = os.environ['JWT_SECRET_KEY']
app.config['SECRET_KEY'] = os.environ['FLASK_SECRET_KEY']
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://{}:{}@{}/{}'.format(
    os.getenv('DB_USER', 'flask'),
    os.getenv('DB_PASSWORD', ''),
    os.getenv('DB_HOST', 'mysql'),
    os.getenv('DB_NAME', 'flask')
)
db = SQLAlchemy(app)
readonlyuser  = create_engine('mysql://{}:{}@{}/{}'.format(
    os.getenv('ROMYSQL_USER', 'flask'),
    os.getenv('ROMYSQL_PASSWORD', ''),
    os.getenv('DB_HOST', 'mysql'),
    os.getenv('DB_NAME', 'flask')
))
rosession  = Session(readonlyuser)

class messages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(100), nullable=False)
    storedname = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    public_id = db.Column(db.String(50), unique = True)
    name = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(255))

class notAdminUser(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    public_id = db.Column(db.String(50), unique = True)
    name = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(255))

def getTF(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'tokenno1' not in request.cookies:
            is_admin = 'a'
        else:
            token = request.cookies.get('tokenno1')
  
        try:
            data = jwt.decode(token, app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
            is_admin = data['is_admin']
        except:
            is_admin = 'a'
        return  f(is_admin,*args, **kwargs)
    return decorated



def admin_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'tokenno1' in request.cookies:
            token = request.cookies.get('tokenno1')
        if not token:
            return redirect(url_for('adminlogin'))
  
        try:
            data = jwt.decode(token, app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
            current_user = User.query\
                .filter_by(public_id = data['public_id'])\
                .first()
            is_admin = data['is_admin']
            if is_admin != True:
                return redirect(url_for('adminlogin'))
        except:
            return redirect(url_for('adminlogin'))
        return  f(current_user,is_admin, *args, **kwargs)
  
    return decorated

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'tokenno1' in request.cookies:
            token = request.cookies.get('tokenno1')
        if not token:
            return redirect(url_for('userloginform'))
  
        try:
            data = jwt.decode(token, app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
            current_user = notAdminUser.query\
                .filter_by(public_id = data['public_id'])\
                .first()
            is_admin = data['is_admin']
            if is_admin != False:
                return redirect(url_for('userloginform'))
        except:
            return render_template('userloginform')
        return  f(current_user,is_admin,*args, **kwargs)
  
    return decorated

@app.route('/userlogin', methods =['POST'])
def userlogin():
    auth = request.get_json()
  
    if not auth or not auth['password']:
        return make_response(
            'Could not verify',
            401,
            {'WWW-Authenticate' : 'Basic realm ="Login required !!"'}
        )
  
    user = notAdminUser.query\
        .filter_by(name = auth['username'])\
        .first()
  
    if not user:
        return make_response(
            'Could not verify',
            401
        )
  
    if check_password_hash(user.password, auth['password']):
        token = jwt.encode({
            'public_id': user.public_id,
            'exp' : datetime.utcnow() + timedelta(days= 1),
            'is_admin' : False
        }, app.config['JWT_SECRET_KEY'])
        resp = make_response(jsonify({'token' : token}), 201)
        resp.set_cookie('tokenno1',token)
        session['port'] = 5001
        return resp
    return make_response(
        'Could not verify',
        403,
        {'WWW-Authenticate' : 'Basic realm ="Wrong Password !!"'}
    )


@app.route('/signup', methods =['POST'])
def signup():
    data = request.get_json()
    username= data['username']
    password = data['password']

    if username is None or password is None:
        return make_response('Error invalid params',400) 
  
    user = notAdminUser.query\
        .filter_by(name = username)\
        .first()
    if not user:
        user = notAdminUser(
            public_id = str(uuid.uuid4()),
            name = username,
            password = generate_password_hash(password)
        )
        db.session.add(user)
        db.session.commit()
  
        return make_response('Successfully registered.', 201)
    else:
        return make_response('User already exists. Please Log in.', 202)

@app.route('/userloginform', methods=['GET'])
@getTF
def userloginform(isadmin):
    if isadmin == True:
        return redirect(url_for('adminview'))
    if isadmin == False:
        return redirect(url_for('userpanel'))
    return render_template('userlogin.html')

@app.route('/notices', methods=['GET'])
@getTF
def notices(isadmin):
    if isadmin == True:
        return redirect(url_for('adminview'))
    if isadmin == False:
        return redirect(url_for('userpanel'))
    return render_template('notices.html')

@app.route('/signupform', methods=['GET'])
@getTF
def signupform(isadmin):
    if isadmin == True:
        return redirect(url_for('adminview'))
    if isadmin == False:
        return redirect(url_for('userpanel'))
    return render_template('signup.html')

@app.route('/userpanel', methods=['GET'])
@token_required
def userpanel(currentuser,is_admin):
    if is_admin == True:
        return redirect(url_for('adminview'))
    return render_template('userpanel.html')

@app.route('/login', methods =['POST'])
def login():
    auth = request.get_json()
  
    if not auth or not auth['password']:
        return make_response(
            'Could not verify',
            401,
            {'WWW-Authenticate' : 'Basic realm ="Login required !!"'}
        )
  
    user = User.query\
        .filter_by(name = auth['username'])\
        .first()
  
    if not user:
        return make_response(
            'Could not verify',
            401
        )
  
    if check_password_hash(user.password, auth['password']):
        token = jwt.encode({
            'public_id': user.public_id,
            'exp' : datetime.utcnow() + timedelta(days = 1),
            'is_admin': True
        }, app.config['JWT_SECRET_KEY'])
        resp = make_response(jsonify({'token' : token}), 201)
        resp.set_cookie('tokenno1',token)
        return resp
    return make_response(
        'Could not verify',
        403,
        {'WWW-Authenticate' : 'Basic realm ="Wrong Password !!"'}
    )

@app.route('/', methods=['GET'])
@getTF
def home(isadmin):
    if isadmin == True:
        return redirect(url_for('adminview'))
    if isadmin == False:
        return redirect(url_for('userpanel'))
    return render_template('index.html')

@app.route('/submit', methods=['GET'])
@token_required
def predictinitial(current_user,is_admin):
    if is_admin == True:
        return redirect(url_for('adminview'))
    return render_template('submit.html',message='')

@app.route('/submitnew', methods=['POST'])
@token_required
def predict(current_user,is_admin):
    if is_admin == True:
        return redirect(url_for('adminview'))
    user = current_user.public_id
    requestdata = request.get_json()
    if not requestdata:
        return make_response(jsonify({'message':'Status: Fill data'}),200)
    url = requestdata['message_text']
    text_content=''
    validation = validators.url(url)
    if validation:
        try:
            url_request = requests.get(url)
            text_content = url_request.text
        except requests.exceptions.Timeout:
            return make_response(jsonify({'message':'Status: Time Out'}),200)
        except requests.exceptions.TooManyRedirects:
            return make_response(jsonify({'message':'Status: Invalid Url'}),200)
        except requests.exceptions.ConnectionError:
            return make_response(jsonify({'message':'Status: Invalid Url'}),200)
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)
    else:
        return make_response(jsonify({'message':'Status: Invalid Url'}),200)
    message_content = (text_content[:100] + '..') if len(text_content) > 100 else text_content

    view_date = requestdata['view_date']
    try:
        res = bool(datetime.strptime(view_date, "%Y-%m-%d"))
    except ValueError:
        return make_response(jsonify({'message': 'Invalid Date'}),200)
    name = secrets.token_hex(16)
    
    if view_date is None or len(view_date)==0:
        return make_response(jsonify({'message': 'No Date'}),200)

    if view_date is not None and datetime.strptime(view_date,'%Y-%m-%d').date()<datetime.today().date():
        return make_response(jsonify({'message': 'Status: Date too Early'}),200)

    if message_content is not None and len(message_content)!=0:
        with open(os.path.join('/application/webserver/',"files/{0}.txt".format(name)), "w") as fo:
            fo.write(message_content)
        record = messages(user=user,storedname=name,date=view_date)
        db.session.add(record)
        db.session.commit()
    else:
        return make_response(jsonify({'message': 'Status: Invalid Inputs'}),200)
    return make_response(jsonify({'message': 'Status: Success'}),200)

@app.route('/view', methods=['GET'])
@token_required
def show_initial(currentuser,is_admin):
    if is_admin == True:
        return redirect(url_for('adminview'))
    results = [{'id':'Click Button'},]
    return render_template('view.html',content='No Id selected',ids=results)
    
@app.route('/viewnew', methods=['POST'])
@token_required
def show(current_user,is_admin):
    if is_admin == True:
        return redirect(url_for('adminview'))
    user = current_user.public_id
    today = time.strftime("%Y-%m-%d")
    requestdata = request.get_json()
    message_tosearch = requestdata['message_tosearch']
    if message_tosearch is None or message_tosearch == '':
        results = messages.query.with_entities(messages.id).filter(messages.date <= today,messages.user != 'admin',messages.user == user).all()
        results = [tuple(row) for row in results]
        if len(results) == 0:
            results = [('No id since the time mentioned has\'t arrived',)]
        return make_response(jsonify({'content': 'Message:No Id selected','ids':results}),200)
    else:
        stored_name = messages.query.with_entities(messages.storedname).filter(messages.id == message_tosearch,messages.date <= today, messages.user !='admin', messages.user == user).one_or_none()
        if stored_name is None:
            return make_response(jsonify({'content': 'Message: That id isn\'t available','ids':[('',)]}),200)
        stored_name = stored_name[0]
        with open(os.path.join('/application/webserver/',"files/{0}.txt".format(stored_name)), "r") as fo:
                lines = fo.readlines()
        content = 'Message: '+''.join(lines)
        return make_response(jsonify({'content': content,'ids':[('',)]}),200)
    
@app.route('/userlogout', methods=['POST'])
@token_required
def userlogout(currentuser,isadmin):
    if isadmin == True:
        return redirect(url_for('adminview'))
    res = make_response("Logout",200)
    res.delete_cookie('tokenno1')
    return res

@app.route('/adminlogout', methods=['POST'])
@admin_token_required
def adminlogout(currentuser,isadmin):
    if isadmin == False:
        return redirect(url_for('userpanel'))
    res = make_response("Logout",200)
    res.delete_cookie('tokenno1')
    return res

@app.route('/adminlogin', methods=['GET'])
@getTF
def adminlogin(isadmin):
    if isadmin == True:
        return redirect(url_for('adminview'))
    if isadmin == False:
        return redirect(url_for('userpanel'))
    return render_template('login.html')

@app.route('/admincheck', methods=['POST'])
def admincheck():
    try:
        return make_response('ok',200)
    except:
        return make_response('bad',400)

@app.route('/adminview', methods=['GET'])
@admin_token_required
def adminview(currentuser,isadmin):
    if isadmin == False:
        return redirect(url_for('userpanel'))
    results = [{'id':'Click Button'},]
    return render_template('admin_view.html',content='No Id selected',ids=results)

@app.route('/adminviewnew/<string:groupby>', methods=['POST'])
@admin_token_required
def adminshow(current_user,isadmin,groupby):
    if isadmin == False:
        return redirect(url_for('userpanel'))
    today = time.strftime("%Y-%m-%d")
    stuff = request.get_json()
    blacklist = "qwertyuioplkjhgfdsazxcvbnm,./'[]=-!@#$^&*()\\|~`_+<>?:\""
    final = ''
    if groupby != 'user':
        final = urlpath.URL(unquote(groupby)).name
        for i in blacklist:
            if i in groupby.lower():
                final = 'user'
                break
        if groupby == None:
            final = 'user'
    message_tosearch = stuff['message_tosearch']
    if message_tosearch is None or message_tosearch == '':
        results = messages.query.with_entities(messages.id).filter(messages.date <= today,messages.user == 'admin').all()
        results = [tuple(row) for row in results]
        if len(results) == 0:
            results = [('No id since the time mentioned has\'t arrived',)]
        return make_response(jsonify({'content': 'Message:','ids':results}),200)
    else:
        try:
            stored_name = rosession.query(messages).filter(messages.user == 'admin',messages.date <= today,messages.id == message_tosearch).group_by(final).one_or_none()
            if stored_name is None:
                return make_response(jsonify({'content': 'Message: That id isn\'t available','ids':[('',)]}),200)
            stored_name = stored_name.storedname
            with open(os.path.join('/application/webserver/',"files/{0}.txt".format(stored_name)), "r") as fo:
                    lines = fo.readlines()
            content = 'Message: '+''.join(lines)
            return make_response(jsonify({'content': content,'ids':[('',)]}),200)
        except Exception as e:
            return make_response(jsonify({'content': f'Message: Invalid parameters:{e}','ids':[('',)]}),400)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)