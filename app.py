from flask import Flask,request,render_template
from main import test
app = Flask(__name__)


@app.route("/")
def hello_world():
    return render_template('query.html')

@app.route('/submit',methods=["POST"])
def gfg():
    test(query=request.form.get("query"))
    return 0
    # your code
    # return a response
    
    






if __name__ == '__main__':
   app.run()