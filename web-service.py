from flask import Flask
app = Flask(__name__)
from flask import request

import chatbot as cb
cb.init()

@app.route('/')
def hello():
    cb.init2()
    cb.newReq()
    return "Hello World!"



@app.route('/chatbot/', methods=["POST"])
def chat():
    query = request.form['query']
    resp= cb.request2(query)
    return str(resp)



if __name__ == '__main__':
    app.run(host="0.0.0.0",port=80)
