from flask import Flask
app = Flask(__name__)
from flask import request

import chatbot as cb
cb.init()

@app.route('/')
def hello():
    return "Hello World!"



@app.route('/chatbot/', methods=["POST"])
def chat():
    query = request.form['query']
  #  print(query)
    resp= cb.getChatResponse(query)
  #  print(resp)
    return str(resp)



if __name__ == '__main__':
    app.run()
