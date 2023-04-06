from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

@app.route('/')
def hello(name=None):
  return render_template('simple_calc.html', name=name)

@app.post("/")
def stuff():
  return "<p>g'bye, World!</p>"
