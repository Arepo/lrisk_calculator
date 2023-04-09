from flask import Flask
from flask import render_template
from flask import request
import pdb

import calculators.simple_calc.simple_calc as sc
from forms.simple_calc import SimpleCalcForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'seekrit' # TODO Any reason to care about this in the absence of a
# database except that Flask/WTForms seem to require it?


@app.route('/', methods=['GET', 'POST'])
def simple_calc():
  form = SimpleCalcForm()
  success = ""
  if form.validate_on_submit():
    pdb.set_trace()
    success = sc.extinction_given_industrial()
  return render_template('simple_calc.html', form=form, success=success)

# @app.post("/")
# def stuff():
#   return "<p>g'bye, World!</p>"
