import pdb
from flask_wtf import FlaskForm
from wtforms import DecimalField
from wtforms.validators import InputRequired, NumberRange

class SimpleCalcForm(FlaskForm):
  extinction_given_survival = DecimalField('Extinction Given Survival', validators=[InputRequired(), NumberRange(min=0, max=1)], default=0)
  extinction_given_preindustrial = DecimalField('Extinction Given Preindustrial', validators=[InputRequired(), NumberRange(min=0, max=1)], default=0)
  extinction_given_industrial = DecimalField('Extinction Given Industrial', validators=[InputRequired(), NumberRange(min=0, max=1)], default=0)

  extinction_given_perils = DecimalField('Extinction Given Perils', validators=[InputRequired(), NumberRange(min=0, max=1)], default=0)
  survival_given_perils = DecimalField('Survival Given Perils', validators=[InputRequired(), NumberRange(min=0, max=1)], default=0)
  preindustrial_given_perils = DecimalField('Preindustrial Given Perils', validators=[InputRequired(), NumberRange(min=0, max=1)], default=0)
  industrial_given_perils = DecimalField('Industrial Given Perils', validators=[InputRequired(), NumberRange(min=0, max=1)], default=0)
  interstellar_given_perils = DecimalField('Interstellar Given Perils', validators=[InputRequired(), NumberRange(min=0, max=1)], default=0)

  extinction_given_multiplanetary = DecimalField('Extinction Given Multiplanetary', validators=[InputRequired(), NumberRange(min=0, max=1)], default=0)
  survival_given_multiplanetary = DecimalField('Survival Given Multiplanetary', validators=[InputRequired(), NumberRange(min=0, max=1)], default=0)
  preindustrial_given_multiplanetary = DecimalField('Preindustrial Given Multiplanetary', validators=[InputRequired(), NumberRange(min=0, max=1)], default=0)
  industrial_given_multiplanetary = DecimalField('Industrial Given Multiplanetary', validators=[InputRequired(), NumberRange(min=0, max=1)], default=0)
  perils_given_multiplanetary = DecimalField('Perils Given Multiplanetary', validators=[InputRequired(), NumberRange(min=0, max=1)], default=0)

  def validate(self, extra_validators=None):
    initial_validation = super(SimpleCalcForm, self).validate(extra_validators)
    # pdb.set_trace()
    if not initial_validation:
      return False

    valid = True
    if (self.extinction_given_perils.data + self.survival_given_perils.data
        + self.preindustrial_given_perils.data + self.industrial_given_perils.data
        + self.interstellar_given_perils.data > 1):
      self.extinction_given_perils.errors.append('Perils transition probabilities must sum to <= 1')
      valid = False

    if (self.extinction_given_multiplanetary.data + self.survival_given_multiplanetary.data
        + self.preindustrial_given_multiplanetary.data + self.industrial_given_multiplanetary.data
        + self.perils_given_multiplanetary.data > 1):
      self.extinction_given_multiplanetary.errors.append('Multiplanetary transition probabilities must sum to <= 1')
      valid = False

    return valid


