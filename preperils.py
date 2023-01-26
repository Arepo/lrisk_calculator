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

#  TODO - decide whether to reintroduce these checksums
#  if not extinction_given_survival(k) + preindustrial_given_survival(k) == 1:
#   raise InvalidTransitionProbabilities("Transition probabilities from survival must == 1")

## Transition probabilities from preindustrial state

@cache
def extinction_given_preindustrial(k):
  expected_time_in_years = PARAMS['preindustrial']['expected_time_in_years']

  extinction_probability_per_year = 1 / PARAMS['preindustrial']['extinction_probability_per_year_denominator']

  return 1 - ((1 - extinction_probability_per_year) ** expected_time_in_years)

@cache
def industrial_given_preindustrial(k, k1):
  if k != k1:
    # We can't transition to different civilisations from a preperils state
    return 0
  else:
    return 1 - extinction_given_preindustrial(k)

# if not extinction_given_preindustrial() + industrial_given_preindustrial() == 1:
#   raise InvalidTransitionProbabilities("Transition probabilities from preindustrial must == 1")


## Transition probabilities from industrial state

@cache
def extinction_given_industrial(k):
  I_PARAMS = PARAMS['industrial']

  base_annual_extinction_probability = 1/I_PARAMS['base_annual_extinction_probability_denominator']

  annual_extinction_probability_multiplier = I_PARAMS['annual_extinction_probability_multiplier']

  # Pessimistic scenario
  stretch_per_reboot = I_PARAMS['pessimistic']['stretch_per_reboot']

  if k == 1:
    expected_time_in_years = I_PARAMS['pessimistic']['first_reboot_expected_time_in_years']
  elif k == 2:
    expected_time_in_years = I_PARAMS['pessimistic']['second_reboot_expected_time_in_years']
  else:
    expected_time_in_years = I_PARAMS['pessimistic']['second_reboot_expected_time_in_years'] * stretch_per_reboot ** (k - 2)

  # Optimistic scenario
  # In this scenario I assume the absence of fossil fuels/other resources is much less punitive
  # especially early on and enough knowledge from previous civilisations is mostly retained to actually
  # speed up this transition the first couple of times
  # stretch_per_reboot = I_PARAMS['optimistic']['stretch_per_reboot']
  # expected_time_in_years = I_PARAMS['optimistic']['base_expected_time_in_years'] * stretch_per_reboot ** k

  return (1 - (1 - base_annual_extinction_probability * annual_extinction_probability_multiplier)
              ** expected_time_in_years)

@cache
def perils_given_industrial(k, k1):
  if k != k1:
    # We can't transition to different civilisations from a preperils state
    return 0
  return 1 - extinction_given_industrial(k)

