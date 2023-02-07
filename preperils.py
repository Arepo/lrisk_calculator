from functools import cache
import yaml
import pdb

with open('params.yml', 'r') as stream:
  PARAMS = yaml.safe_load(stream)['preperils']

## Transition probabilities from survival state
@cache
def extinction_given_survival(k):
  return PARAMS['survival']['base_estimate']

@cache
def preindustrial_given_survival(k, k1):
  if k != k1:
    # We can't transition to different civilisations from a preperils state
    return 0
  else:
    return 1 - extinction_given_survival(k)

## Transition probabilities from preindustrial state
@cache
def extinction_given_preindustrial(k):
  base_expected_time_in_years = PARAMS['preindustrial']['base_expected_time_in_years']

  stretch_per_reboot = PARAMS['preindustrial']['stretch_per_reboot']

  expected_time_in_years = base_expected_time_in_years * stretch_per_reboot ** k

  extinction_probability_per_year = 1 / PARAMS['preindustrial']['extinction_probability_per_year_denominator']

  return 1 - ((1 - extinction_probability_per_year) ** expected_time_in_years)

@cache
def industrial_given_preindustrial(k, k1):
  if k != k1:
    # We can't transition to different civilisations from a preperils state
    return 0
  else:
    return 1 - extinction_given_preindustrial(k)

## Transition probabilities from industrial state
@cache
def extinction_given_industrial(k):
  # To allow for some inside view about the first time we reboot, we could
  # have an explicit condition here:
  # if k == 1:
  #   do_something_different

  I_PARAMS = PARAMS['industrial']

  base_annual_extinction_probability = 1/I_PARAMS['base_annual_extinction_probability_denominator']

  annual_extinction_probability_multiplier = I_PARAMS['annual_extinction_probability_multiplier']

  stretch_per_reboot = I_PARAMS['stretch_per_reboot']

  expected_time_in_years = I_PARAMS['base_expected_time_in_years'] * stretch_per_reboot ** (k - 1)

  return (1 - (1 - base_annual_extinction_probability * annual_extinction_probability_multiplier)
              ** expected_time_in_years)

@cache
def perils_given_industrial(k, k1):
  if k != k1:
    # We can't transition to different civilisations from a preperils state
    return 0
  return 1 - extinction_given_industrial(k)

