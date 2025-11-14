from flask import Flask

app = Flask (__name__)

@app.route('/')
def hello():
    return 'Hola mundos'
@app.route('/yop.html')
def hola():
    return