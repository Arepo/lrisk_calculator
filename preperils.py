from functools import cache
import yaml
import pdb

with open('params.yml', 'r') as stream:
  PARAMS = yaml.safe_load(stream)['preperils']

class InvalidTransitionProbabilities(Exception):
  """Raised when transition probabilities from a state don't sum to 1"""
  pass

## Transition probabilities from survival state

@cache
def extinction_given_survival(k):
  base_estimate = PARAMS['survival']['base_estimate']
  expected_number_of_previous_survivals = (k - 1) * PARAMS['survival']['survival_given_regression']
  probability_multiplier_per_previous_survival = PARAMS['survival']['per_survival_multiplier']
  return (base_estimate *
          probability_multiplier_per_previous_survival ** expected_number_of_previous_survivals)

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
  """I expect this to decrease slightly with the value of k, given civilisations in the state have
  evidently survived to reach perils. Depleted resources will be a slight issue. There are various
  different suggested values in the comments below. The output of this function"""

  expected_time_in_years = PARAMS['preindustrial']['expected_time_in_years']

  extinction_probability_per_year = 1 / PARAMS['preindustrial']['extinction_probability_per_year_denominator']

  base_total_extinction_probability = 1 - ((1 - extinction_probability_per_year) ** expected_time_in_years)

  expected_number_of_previous_preindustrials = (k - 1) * PARAMS['preindustrial']['preindustrial_given_regression']

  multiplier_per_previous_preindustrial = PARAMS['preindustrial']['per_preindustrial_multiplier']

  return (base_total_extinction_probability *
          multiplier_per_previous_preindustrial ** expected_number_of_previous_preindustrials)

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
  """I expect this to have a complex relationship with k. Initially I think it decreases with k as
  resources are preferentially used up so each civilisation has to do more with less, but after some
  number of retries it should probably increase, as we gain evidence of our capacity to deal with
  those scarcer resources. There might also be dramatic differences in difficulty based exactly on what
  has been used up or left behind by previous civilisations, so we might want a branching function.
  Below I've used a branching function for the pessimistic case, but otherwise defaulted to the simple
  approach of assuming exponential decline
  """

  I_PARAMS = PARAMS['industrial']

  # For extinction probability per year, we can start with the base rates given in the previous
  # calculation, and then multiply them by some factor based on whether we think industry would make
  # humans more or less resilient.
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
  stretch_per_reboot = I_PARAMS['optimistic']['stretch_per_reboot']
  expected_time_in_years = I_PARAMS['optimistic']['base_expected_time_in_years'] * stretch_per_reboot ** k

  return 1 - (
    (1 - base_annual_extinction_probability * annual_extinction_probability_multiplier)
    ** expected_time_in_years)

@cache
def perils_given_industrial(k, k1):
  if k != k1:
    # We can't transition to different civilisations from a preperils state
    return 0
  return 1 - extinction_given_industrial(k)

# if not extinction_given_industrial() + perils_given_industrial() == 1:
#   raise InvalidTransitionProbabilities("Transition probabilities from industrial must == 1")
