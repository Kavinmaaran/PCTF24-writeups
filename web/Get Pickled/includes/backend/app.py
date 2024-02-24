from flask_cors import CORS
from flask import Flask, request
from config import SECRET_KEY,FRONTEND_URL
from pathlib import Path
import pickle
import hmac
import hashlib
import base64
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

CORS(app, resources={r"/*":{"origins":[FRONTEND_URL]}})
shared_key = "donttrustpickles"

users = open("secrets.txt").readlines()
@app.route('/form',methods=['POST'])
def index():
    try:
        name=request.form["name"]
        key = int(request.form["key"])
        Name = re.sub(r'[^a-zA-Z0-9\s]', '', name)
        if('&'in name):
            Name=re.sub(re.escape('&'),"",name)
        if('*'in Name):
            Name=re.sub(re.escape('*'),"",Name)
        if('@'in Name):
            Name=re.sub(re.escape('@'),"",Name)
        if('#'in Name):
            Name=re.sub(re.escape('#'),"",Name)
        if('%'in Name):
            Name=re.sub(re.escape('%'),"",Name)
        if('/'in Name):
            Name=re.sub(re.escape('/'),"",Name)
        if('.'in Name):
            Name=re.sub(re.escape('.'),"",Name)
        if('$'in Name):
            Name=re.sub(re.escape('$'),"",Name)
        if('^'in Name):
            Name=re.sub(re.escape('^'),"",Name)
        if('('in Name):
            Name=re.sub(re.escape('('),"",Name)
        if('>'in Name):
            Name=re.sub(re.escape('>'),"",Name)
        if('<'in Name):
            Name=re.sub(re.escape('<'),"",Name)
        results=[]
        for line in users:
            results += re.findall(r"^(?:Country\s)" + name+r"(?:\sCapital\s.*)",line, flags=key)
            results = [x.strip() for x in results if x or len(x)>1]
        return results
    except re.error as e:
        return str(e)


@app.route('/theroutewhichmustnotbenamed', methods=['POST'])
def theRouteWhichMustNotBeNamed():
    try: 
        data = base64.urlsafe_b64decode(request.data)
        recvd_digest, pickled_data = data.split(b' ',1)
        new_digest = hmac.new(shared_key.encode(), pickled_data, hashlib.sha1).hexdigest().encode()
        if recvd_digest != new_digest:
            return 'Integrity Check Failed, I think I have secured my server or have I?', 400
        else:
            unpickled_data = pickle.loads(pickled_data)
            return 'Data received successfully', 200

    except Exception as e:
        print(f"Error: {str(e)}")
        return 'Internal Server Error', 500


# for running in dev
if __name__ == '__main__':
    app.run(debug=True,port=5000)
