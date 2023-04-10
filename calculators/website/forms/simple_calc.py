import pdb
from flask_wtf import FlaskForm
from wtforms import DecimalField
from wtforms.validators import InputRequired, NumberRange

class SimpleCalcForm(FlaskForm):
  extinction_given_pre_equilibrium = DecimalField('Extinction given Pre-equilibrium', validators=[InputRequired(), NumberRange(min=0, max=1)], default=0)
  extinction_given_preindustrial = DecimalField('Extinction given Preindustrial', validators=[InputRequired(), NumberRange(min=0, max=1)], default=0)
  extinction_given_industrial = DecimalField('Extinction given Industrial', validators=[InputRequired(), NumberRange(min=0, max=1)], default=0)

  extinction_given_present_perils = DecimalField('Extinction given Perils', validators=[InputRequired(), NumberRange(min=0, max=1)], default=0)
  pre_equilibrium_given_present_perils = DecimalField('Pre-equilibrium given Perils', validators=[InputRequired(), NumberRange(min=0, max=1)], default=0)
  preindustrial_given_present_perils = DecimalField('Preindustrial given Perils', validators=[InputRequired(), NumberRange(min=0, max=1)], default=0)
  industrial_given_present_perils = DecimalField('Industrial given Perils', validators=[InputRequired(), NumberRange(min=0, max=1)], default=0)
  interstellar_given_present_perils = DecimalField('Interstellar given Perils', validators=[InputRequired(), NumberRange(min=0, max=1)], default=0)

  extinction_given_future_perils = DecimalField('Extinction given Perils', validators=[InputRequired(), NumberRange(min=0, max=1)], default=0)
  pre_equilibrium_given_future_perils = DecimalField('Pre-equilibrium given Perils', validators=[InputRequired(), NumberRange(min=0, max=1)], default=0)
  preindustrial_given_future_perils = DecimalField('Preindustrial given Perils', validators=[InputRequired(), NumberRange(min=0, max=1)], default=0)
  industrial_given_future_perils = DecimalField('Industrial given Perils', validators=[InputRequired(), NumberRange(min=0, max=1)], default=0)
  interstellar_given_future_perils = DecimalField('Interstellar given Perils', validators=[InputRequired(), NumberRange(min=0, max=1)], default=0)

  extinction_given_multiplanetary = DecimalField('Extinction given Multiplanetary', validators=[InputRequired(), NumberRange(min=0, max=1)], default=0)
  pre_equilibrium_given_multiplanetary = DecimalField('Pre-quilibrium given Multiplanetary', validators=[InputRequired(), NumberRange(min=0, max=1)], default=0)
  preindustrial_given_multiplanetary = DecimalField('Preindustrial given Multiplanetary', validators=[InputRequired(), NumberRange(min=0, max=1)], default=0)
  industrial_given_multiplanetary = DecimalField('Industrial given Multiplanetary', validators=[InputRequired(), NumberRange(min=0, max=1)], default=0)
  future_perils_given_multiplanetary = DecimalField('Perils given Multiplanetary', validators=[InputRequired(), NumberRange(min=0, max=1)], default=0)

  def validate(self, extra_validators=None):
    initial_validation = super(SimpleCalcForm, self).validate(extra_validators)
    if not initial_validation:
      return False

    valid = True
    if (self.extinction_given_present_perils.data + self.pre_equilibrium_given_present_perils.data
        + self.preindustrial_given_present_perils.data + self.industrial_given_present_perils.data
        + self.interstellar_given_present_perils.data > 1):
      self.extinction_given_present_perils.errors.append('Transition probabilities from our current time of perils must sum to <= 1')
      valid = False

    if (self.extinction_given_future_perils.data + self.pre_equilibrium_given_future_perils.data
        + self.preindustrial_given_future_perils.data + self.industrial_given_future_perils.data
        + self.interstellar_given_future_perils.data > 1):
      self.extinction_given_future_perils.errors.append('Transition probabilities from future times of perils must sum to <= 1')
      valid = False

    if (self.extinction_given_multiplanetary.data + self.pre_equilibrium_given_multiplanetary.data
        + self.preindustrial_given_multiplanetary.data + self.industrial_given_multiplanetary.data
        + self.perils_given_multiplanetary.data > 1):
      self.extinction_given_multiplanetary.errors.append('Transition probabilities from a multiplanetary state must sum to <= 1')
      valid = False

    return valid


