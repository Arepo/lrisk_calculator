from flask import Flask, request, render_template
import pdb

import calculators.simple_calc.simple_calc as sc
from calculators.website.forms.simple_calc import SimpleCalcForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'seekrit' # TODO Any reason to care about this in the absence of a
# database except that Flask/WTForms seem to require it?

@app.route('/', methods=['GET', 'POST'])
def simple_calc_page():
  form = SimpleCalcForm()
  calc = None
  if form.validate_on_submit():
    calc = sc.SimpleCalc(request.form)
  return render_template('simple_calc_page.html', form=form, calc=calc)

# def create_app(config_filename):
#     app = Flask(__name__)
#     app.config.from_pyfile(config_filename)
#     return app
