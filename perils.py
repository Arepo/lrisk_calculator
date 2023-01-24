from functools import cache
import math
import pdb

import yaml
from scipy.stats import gamma

import runtime_constants as constant
from graph_functions import sigmoid_curved_risk, power_law_risk, exponentially_decaying_risk


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

  return sigmoid_curved_risk(p, x_stretch(k), y_stretch(), x_translation(), sharpness())

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

  return sigmoid_curved_risk(p, x_stretch(k), y_stretch(), x_translation(), sharpness())

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

  return sigmoid_curved_risk(p, x_stretch(k), y_stretch(), x_translation(), sharpness())

@cache
def transition_to_year_n_given_perils(k:int, p:int, n=None):
  """The simplest intuitive way I can think of to deal with this is to assume the probability of
  regressing decreases exponentially with the number of years we regressing, eg for p = 3, given that
  there has been some intra-perils regression we might say the probability of that regression is 1/15,
  2/15, 4/15, and 8/15 respectively for 'regressions' to p = 0, 1, 2, and 3.

  More generally, we woud say that, given some intra-perils regression, the probability of a
  regression to exactly progress-year n is a weighting_for_progress_year_n = <some weighting_decay_rate>**n,
  divided by the sum of weighting_for_progress_year_n for all valid values of n.

  I'm not sure this is a very convincing algorithm. Based on global GDP, we've arguably regressed
  in about 4 calendar years since 1961, when the world bank started tracking global data and perhaps
  5 times in the 20th century based on UK data between about 0 and 2 progress years each time, and about . For comparatively tiny
  values of weighting_decay_rate (ie barely above 1), being limited to such small regressions looks
  incredibly unlikely. For higher values of weighting_decay_rate, it puts the total probability of
  regressing more than a few years at a far lower value than the probability of a milestone
  regression - a regression to an earlier technological state - which seems wrong.

  A simple alternative that errs way too much in the other direction would be a linear decrease given by
  an arithmetic progression. This seems like a much worse fit for the data, but I include that
  version, commented out below, as a way of getting an upper bound on the significance of regressions
  within the time of perils."""

  # ... this function really sucks.

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

  geometric_base = PARAMS['progress_year_n']['geometric_base'] # Higher gives higher probability that given such a loss we'll lose a
  # smaller number of progress years: 2 would mean regressing to year n is 2x
  # as likely as regressing to year n-1. I chose the current value fairly arbitrarily, by
  # looking at this graph - https://data.worldbank.org/indicator/NY.GDP.MKTP.KD.ZG, treating
  # 1975, and 1982 as a regression of 0 years, 2009 as a regression of 1, and 2020 as a
  # regression of 2, and looking for a probability outcome slightly below that (to account for
  # eg survivor bias, and selection effects from starting to count immediately *after* WWII).

  geometric_sum_of_weightings = ( (1 - geometric_base ** max_regressed_states)
                                  / (1 - geometric_base))

  numerator_for_progress_year_n = geometric_base ** target_year # How likely is it, that given some loss,
  # that loss took us to exactly progress year n?

  # Thus numerator_for_progress_year_n / geometric_sum_of_weightings is a proportion; you can play with
  # the values at https://www.desmos.com/calculator/1pcgidwr3f
  return any_intra_perils_regression() * numerator_for_progress_year_n / geometric_sum_of_weightings

    # Linear version:
    # arithmetic_sequence_sum = p + 1 + (p**2 + p)/2
    # return (n + 1) / arithmetic_sequence_sum
    # Desmos version:
    # https://www.desmos.com/calculator/xtlzmxvikn

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

  return sigmoid_curved_risk(p, x_stretch(k), y_stretch(), x_translation(), sharpness())

def _ai_x_translation():
    return PARAMS['extinction']['agi_development']['x_translation']

def annual_ai_development_probability(p):
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
    base_max_annual_risk = X_PARAMS['non_ai_causes']['y_stretch']['max']
    min_annual_risk = X_PARAMS['non_ai_causes']['y_stretch']['min']
    decay_rate = X_PARAMS['non_ai_causes']['y_stretch']['decay_rate']
    return exponentially_decaying_risk(
      x=k,
      starting_value=base_max_annual_risk,
      decay_rate=decay_rate,
      min_value=min_annual_risk)

  def sigmoid_x_translation():
    return X_PARAMS['non_ai_causes']['x_translation']

  def sigmoid_sharpness():
    return X_PARAMS['non_ai_causes']['sharpness']

  non_ai_extinction_risk_by_year = sigmoid_curved_risk(p, sigmoid_x_stretch(k), sigmoid_y_stretch(k), sigmoid_x_translation(), sigmoid_sharpness())

  # Using a power law distribution to estimate probability of AI eventually wiping us out conditional
  # on it on it being created in year p.
  # Play with these numbers at https://www.desmos.com/calculator/znklhoherj
  def ai_extinction_multiplier_decay_rate():
    return X_PARAMS['agi_threat']['threat_decay_rate']

  def ai_extinction_multiplier_y_stretch():
    """Determines the max probability that, given AI is developed in some year, it will wipe us out"""
    return X_PARAMS['agi_threat']['max_threat']

  # TODO consider an x-stretch for extinction multiplier (It's not obvious whether we should have one,
  # since this might be as much a social problem as a technological one. But without one, it might
  # end up looking more likely that we become interstellar given non-extinction catastrophes - though
  # this might not be wrong)



  ai_extinction_multiplier_by_year = power_law_risk(
    p, ai_extinction_multiplier_y_stretch(), ai_extinction_multiplier_decay_rate(), _ai_x_translation())

  # Graph with these values for k=0 at https://www.desmos.com/calculator/mbwoy2muin
  return annual_ai_development_probability(p) * ai_extinction_multiplier_by_year + non_ai_extinction_risk_by_year

@cache
def interstellar_given_perils(k, p):
  def value_lock_in_given_ai():
    return PARAMS['interstellar']['value_lock_in_given_ai']

  return annual_ai_development_probability(p) * value_lock_in_given_ai()

@cache
def _non_continuation_given_perils(k, p):
  return (extinction_given_perils(k, p)
          + survival_given_perils(k, p)
          + preindustrial_given_perils(k, p)
          + industrial_given_perils(k, p)
          + transition_to_year_n_given_perils(k, p)
          + multiplanetary_given_perils(k, p)
          + interstellar_given_perils(k, p))

# @cache
# def perils_stasis_given_perils(k, p):
#   """The probability that we transition to the same progress year."""
#   if p >= constant.MAX_PROGRESS_YEARS:
#     return 1 - _non_continuation_given_perils
#   else:
#     return (1 - _non_continuation_given_perils) * 1/30 # Using the same source as in regressions,
#     # this is based on 'flattish' years appearing roughly this often for the last 60 years in World
#     # Bank data
#     # https://data.worldbank.org/indicator/NY.GDP.MKTP.KD.ZG
#     # https://ourworldindata.org/grapher/world-gdp-over-the-last-two-millennia?time=1940..2015

# @cache
# def perils_progression_given_perils(k, p):
#   if p >= constant.MAX_PROGRESS_YEARS:
#     return 0
#   else:
#     return _non_continuation_given_perils - perils_stasis_given_perils(k, p)

