from flask import Flask,render_template
import os
app = Flask(__name__)

key = os.environ['JWT_SECRET_KEY']

@app.route('/', methods=['GET','POST'])
def home():
    return render_template('index.html')

@app.route('/notices', methods=['GET','POST'])
def notices():
    return render_template('notices.html', flask_secret=key )

@app.route('/view', methods=['GET','POST'])
def view():
    return render_template('notices.html')

@app.route('/submit', methods=['GET','POST'])
def predictinitial():
    return render_template('submit.html',message='')

@app.route('/signupform', methods=['GET','POST'])
def signupform():
    return render_template('signup.html')

@app.route('/userpanel', methods=['GET','POST'])
def userpanel():
    return render_template('userpanel.html')

@app.route('/userloginform', methods=['GET','POST'])
def userloginform():
    return render_template('userlogin.html')

if __name__ == "__main__":
    app.run(port=5001, debug=True)