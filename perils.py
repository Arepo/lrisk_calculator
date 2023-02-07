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
  return parameterised_transition_probability(k, p, 'survival')

@cache
def preindustrial_given_perils(k, p):
  return parameterised_transition_probability(k, p, 'preindustrial')

@cache
def industrial_given_perils(k, p):
  return parameterised_transition_probability(k, p, 'industrial')

@cache
def multiplanetary_given_perils(k, p):
  return parameterised_transition_probability(k, p, 'multiplanetary')

@cache
def extinction_given_perils(k, p):
  return parameterised_transition_probability(k, p, 'extinction')

@cache
def interstellar_given_perils(k, p):
  return parameterised_transition_probability(k, p, 'interstellar')

def parameterised_transition_probability(k, p, target_state):
  # To allow for some inside view about the first time we reboot, we could
  # have an explicit condition here:
  # if k == 1:
  #   do_something_different

  @cache
  def x_stretch(k, target_state):
    return PARAMS[target_state]['base_x_stretch'] * PARAMS[target_state]['stretch_per_reboot'] ** (k + 1)

  @cache
  def y_stretch(target_state):
    """Max probability per year of this transition"""
    return PARAMS[target_state]['y_stretch']

  @cache
  def x_translation(target_state):
    """How many progress years into the time of perils does this possibility rise meaningfully above
    0"""
    return PARAMS[target_state]['x_translation']

  @cache
  def sharpness(target_state):
    return PARAMS[target_state]['sharpness']

  @cache
  def background_risk(target_state):
    return (PARAMS[target_state]['base_background_risk']
            * PARAMS[target_state]['per_reboot_background_risk_multiplier'] ** (k + 1))

  return background_risk(target_state) + sigmoid_curved_risk(
                                                             x=p,
                                                             x_stretch=x_stretch(k, target_state),
                                                             y_stretch=y_stretch(target_state),
                                                             x_translation=x_translation(target_state),
                                                             sharpness=sharpness(target_state))

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


# The functions below single out AI for special treatment, and will not be used in the MVP (and may
# become redundant afterwards).

# def _ai_x_translation():
#     return PARAMS['extinction']['agi_development']['x_translation']

# def annual_ai_first_development_probability(p):
#   def gamma_shape():
#     return PARAMS['extinction']['agi_development']['shape']

#   def gamma_scale():
#     return PARAMS['extinction']['agi_development']['scale']

#   return gamma.pdf(p, gamma_shape(), loc=_ai_x_translation(), scale=gamma_scale())
