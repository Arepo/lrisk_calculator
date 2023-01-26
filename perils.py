from functools import cache
import math
from scipy.stats import gamma
import pdb

import yaml


import runtime_constants as constant
from graph_functions import sigmoid_curved_risk, exponentially_decaying_risk


## Transition probabilities from time of perils state

with open('params.yml', 'r') as stream:
  PARAMS = yaml.safe_load(stream)['perils']

@cache
def survival_given_perils(k, p):
  """In principle the y_stretch (max probability per year) of this would probably decrease with
  higher values of k, since they provide some evidence that we're less likely to end in states that
  are more likely to make us extinct. In practice, both the initial probability of ending in survival
  and the probability of extinction from there seem small enough that I'm treating it as a constant.

  Based on this source, nuclear weapon stockpiles started hitting the thousands after about 10
  years https://en.wikipedia.org/wiki/Historical_nuclear_weapons_stockpiles_and_nuclear_tests_by_country
  though only for the US - though until the Soviet Union had comparable numbers peaking in 1986, the
  risk of extremely bad outcomes was probably low. It might have kept growing under someone other
  than Gorbachev, and arguably has continued to grow even given declining nuclear arsenals, given the
  increase in biotech and environmental damage.

  Setting this to be 0 seems pretty reasonable.

  Editable graph with these values: https://www.desmos.com/calculator/sghhv9sadb
  """

  def x_stretch(k):
    return PARAMS['survival']['base_x_stretch'] * PARAMS['stretch_per_reboot'] ** (k + 1)

  def y_stretch():
    """Max probability per year of this transition."""
    return PARAMS['survival']['y_stretch']

  def x_translation():
    """When does this risk start rising above 0, pre x-stretch?"""
    return PARAMS['survival']['x_translation']

  def sharpness():
    return PARAMS['survival']['sharpness'] # Intuition, no substantive reasoning

  return sigmoid_curved_risk(
    x=p,
    x_stretch=x_stretch(k),
    y_stretch=y_stretch(),
    x_translation=x_translation(),
    sharpness=sharpness())

@cache
def preindustrial_given_perils(k, p):
  """I'm treating nukes as being substantially the most likely tech to cause this outcome, since
  they destroy far more resources than a pandemic would, making rebuilding much harder. So I expect
  the risk to more or less max out relatively early, as nuclear aresenals peak."""

  def x_stretch(k):
    return PARAMS['preindustrial']['base_x_stretch'] * PARAMS['stretch_per_reboot'] ** (k + 1)

  def y_stretch():
    """Max probability per year of this transition"""
    return PARAMS['preindustrial']['y_stretch']

  def x_translation():
    return PARAMS['preindustrial']['x_translation'] # About the time the world's nuclear arsenal took to reach multiple thousands

  def sharpness():
    return PARAMS['preindustrial']['sharpness']

  return sigmoid_curved_risk(
    x=p,
    x_stretch=x_stretch(k),
    y_stretch=y_stretch(),
    x_translation=x_translation(),
    sharpness=sharpness())

@cache
def industrial_given_perils(k, p):
  """I treat this as possible through any weapons tech, meaning it has the slowest incline but
  reaches the highest peak of the bad exits, and is generally higher per year than the others"""

  def x_stretch(k):
    return PARAMS['industrial']['base_x_stretch'] * PARAMS['stretch_per_reboot'] ** (k + 1)

  def y_stretch():
    """Max probability per year of this transition. TODO: no way this should be lower than extinction"""
    return PARAMS['industrial']['y_stretch']

  def x_translation():
    return PARAMS['industrial']['x_translation']

  def sharpness():
    return PARAMS['industrial']['sharpness']

  return sigmoid_curved_risk(
    x=p,
    x_stretch=x_stretch(k),
    y_stretch=y_stretch(),
    x_translation=x_translation(),
    sharpness=sharpness())

@cache
def transition_to_year_n_given_perils(k:int, p:int, n=None):
  possible_regressions = p + 1

  if possible_regressions == constant.MAX_PROGRESS_YEARS:
    # We're at the maximum allowable number of progress years, so lose the 'regression' of  staying
    # on the spot (which becomes our remainder)
    possible_regressions -= 1

  if n > (possible_regressions):
    # We only allow progress to increment by up to one.
    return 0

  def any_intra_perils_regression():
    """How likely is it in total we regress any number of progress years between 0 and p inclusive?"""
    return PARAMS['progress_year_n']['any_regression']

  def remainder_outcome(k, p):
    return 1 - (extinction_given_perils(k, p)
                + survival_given_perils(k, p)
                + preindustrial_given_perils(k, p)
                + industrial_given_perils(k, p)
                + any_intra_perils_regression()
                + multiplanetary_given_perils(k, p)
                + interstellar_given_perils(k, p))

  if n == possible_regressions:
    # Our catchall is either progressing one progress year or staying on the spot if we're at max
    return remainder_outcome(k, p)

  if possible_regressions - n > constant.MAX_PROGRESS_YEAR_REGRESSION_STEPS:
    # We round to 0 when numbers get small enough,
    # so we don't have to deal with fractions like ~a^10000/2a^10000 in the geometric sequence below
    return 0

  # If we get this far, we're setting up to calculate the division of the total probability of
  # any_intra_perils_regression() into the specific probability of a regression to year n
  if possible_regressions > constant.MAX_PROGRESS_YEAR_REGRESSION_STEPS:
    # Reduce large numbers to the minimum, eg regression from progress-year 1000 from progress-year
    # 950 with max_distance 100 becomes regression from PY 100 to PY 50. This way we ensure proportions still sum to 0.
    max_regressed_states = constant.MAX_PROGRESS_YEAR_REGRESSION_STEPS
    target_year = n - (possible_regressions - constant.MAX_PROGRESS_YEAR_REGRESSION_STEPS)
  else:
    max_regressed_states = possible_regressions
    target_year = n

  geometric_base = PARAMS['progress_year_n']['geometric_base']

  geometric_sum_of_weightings = ( (1 - geometric_base ** max_regressed_states)
                                  / (1 - geometric_base))

  numerator_for_progress_year_n = geometric_base ** target_year # How likely is it, that given some loss,
  # that loss took us to exactly progress year n?

  # Linear version:
  # arithmetic_sequence_sum = p + 1 + (p**2 + p)/2
  # return (n + 1) / arithmetic_sequence_sum
  # Desmos version:
  # https://www.desmos.com/calculator/xtlzmxvikn

  # Thus numerator_for_progress_year_n / geometric_sum_of_weightings is a proportion; you can play with
  # the values at https://www.desmos.com/calculator/1pcgidwr3f
  return any_intra_perils_regression() * numerator_for_progress_year_n / geometric_sum_of_weightings

@cache
def multiplanetary_given_perils(k, p):
  def x_stretch(k):
    return PARAMS['multiplanetary']['base_x_stretch'] * PARAMS['stretch_per_reboot'] ** (k + 1)

  def y_stretch():
    """Max probability per year of this transition"""
    return PARAMS['multiplanetary']['y_stretch']

  def x_translation():
    """How many progress years into the time of perils does this possibility rise meaningfully above
    0"""
    return PARAMS['multiplanetary']['x_translation']

  def sharpness():
    return PARAMS['multiplanetary']['sharpness']

  return sigmoid_curved_risk(
    x=p,
    x_stretch=x_stretch(k),
    y_stretch=y_stretch(),
    x_translation=x_translation(),
    sharpness=sharpness())

def _ai_x_translation():
    return PARAMS['extinction']['agi_development']['x_translation']

def annual_ai_first_development_probability(p):
  def gamma_shape():
    return PARAMS['extinction']['agi_development']['shape']

  def gamma_scale():
    return PARAMS['extinction']['agi_development']['scale']

  return gamma.pdf(p, gamma_shape(), loc=_ai_x_translation(), scale=gamma_scale())

@cache
def extinction_given_perils(k, p):
  X_PARAMS = PARAMS['extinction']

  def sigmoid_x_stretch(k):
    return X_PARAMS['non_ai_causes']['base_x_stretch'] * PARAMS['stretch_per_reboot'] ** (k + 1)

  def sigmoid_y_stretch(k):
    return X_PARAMS['non_ai_causes']['y_stretch']

  def sigmoid_x_translation():
    return X_PARAMS['non_ai_causes']['x_translation']

  def sigmoid_sharpness():
    return X_PARAMS['non_ai_causes']['sharpness']

  non_ai_extinction_risk_by_year = sigmoid_curved_risk(
    x=p,
    x_stretch=sigmoid_x_stretch(k),
    y_stretch=sigmoid_y_stretch(k),
    x_translation=sigmoid_x_translation(),
    sharpness=sigmoid_sharpness())

  def ai_extinction_multiplier_decay_rate():
    return X_PARAMS['agi_threat']['threat_decay_rate']

  def ai_extinction_multiplier_current_threat():
    return X_PARAMS['agi_threat']['max_threat']

  # TODO consider an x-stretch for extinction_multiplier_for_year_p (It's not obvious whether we should have one,
  # since this might be as much a social problem as a technological one. But without one, it might
  # end up looking more likely that we become interstellar given non-extinction catastrophes - though
  # this might not be wrong). This will stop being a relevant concern if we add post-AI time of perils
  # as a separate class of states

  ai_extinction_multiplier_for_year_p = exponentially_decaying_risk(
    x=p,
    starting_value=ai_extinction_multiplier_current_threat(),
    decay_rate=ai_extinction_multiplier_decay_rate(),
    x_translation=_ai_x_translation())

  # Graph with these values for k=0 at https://www.desmos.com/calculator/mbwoy2muin
  return annual_ai_first_development_probability(p) * ai_extinction_multiplier_for_year_p + non_ai_extinction_risk_by_year

@cache
def interstellar_given_perils(k, p):
  def value_lock_in_given_ai():
    return PARAMS['interstellar']['value_lock_in_given_ai']

  return annual_ai_first_development_probability(p) * value_lock_in_given_ai()

