from flask import Flask, render_template, request,make_response



app = Flask(__name__)

        
@app.route("/", methods = ['GET','POST'])
def homepage():
    content = request.form.get('content')
    resp = make_response(render_template('test.html',contents=content))
    return resp

if __name__ == "__main__":
    app.run(port=8001,debug=False)
