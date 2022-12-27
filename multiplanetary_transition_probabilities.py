import pdb
import math
import constant


# This script prints out a series of probabilities for transition becoming interstellar based on
# estimates of the transition probabilities of various(values are currently hardcoded placeholders)
# states, as in a Markov chain. The states are extinction, survival, preindustrial, industrial, time
# of perils, multiplanetary, and interstellar.
#
# A full description/explanation of the model is in the section titled The Cyclical Model in this
# post:
# https://forum.effectivealtruism.org/posts/YnBwoNNqe6knBJH8p/modelling-civilisation-after-a-catastrophe#The_cyclical_model

## Transition probabilities from multiplanetary state

def exponentially_decaying_risk(two_planet_risk, q, k, decay_rate=0.5, min_risk=0):
  """The simplest way I can think of to intuit the various risks given multiple interplanetary
  settlements is as an exponential decay based on the number of planets.

  Another intuitive option would be something like 1/(x ** <some_value>), which would eventually
  decrease the probability of the risks more slowly, but could decrease it faster early on
  if we thought eg proving the concept would substantially improve our prospects.

  k is available as a parameter if people think it's important, but I'm treating it as irrelevant
  once we've reached this stage.

  You can play with the formula and values at https://www.desmos.com/calculator/bcu1qfp8wu

  Note that min_risk is a translation on the y-axis. So if you set two_planet_risk as 0.4 and
  min_risk as 0.1, your actual two_planet_risk will be 0.5
  """
  return two_planet_risk  * (1 - decay_rate) ** (q - 2) + min_risk


def extinction_given_multiplanetary(k):
  """Sum of total extinction exit probability over all values of q given k"""



def extinction_given_multiplanetary(k, q):
  def single_planet_risk():
    return 0.2

  def decay_rate():
    """Should be a value between 0 and 1. Lower treats the per-planet risk reduction as lower. This
    values is just a wild guess, though see the note on the equivalent decay_rate for the
    perils_given_multiplanetary function for an ordering"""
    return 0.55

  def min_risk():
    """For the very long run, if this doesn't tend to become almost 0, longtermism isn't possible"""
    return 0

  return exponentially_decaying_risk(single_planet_risk(), q, k, decay_rate(), min_risk())

def survival_given_multiplanetary(k):
  """Sum of total survival exit probability over all values of q given k. I treat this as 0 on the
  grounds that it seems such a precise amount of damage that it's not worth the computation/complexity
  costs"""
  return 0

def preindustrial_given_multiplanetary(k):
  """Sum of total preindustrial exit probability over all values of q given k. Again, while this seems
  more plausible than going directly to a survival state, it seems unlikely enough to treat as 0"""
  return 0

def industrial_given_multiplanetary(k):
  """Sum of total industrial exit probability over all values of q given k. Again, while this looks
  somewhat more plausible, it still seems so much less likely than an event which either wipes out
  humanity or leaves the reaminder with some advanced technology as to be treatable as 0"""
  return 0

def perils_given_multiplanetary(k):
  """Sum of total perils exit probability over all values of q given k"""
  pass

def any_intra_multiplanetary_regression(k, q):
    return exponentially_decaying_risk(two_planet_risk(), q, k, decay_rate())

def transition_to_n_planets_given_multiplanetary(k, q, n):
  """Should be a value between 0 and 1. Lower treats events that could cause regression to a
  1-planet civilisation in a perils state as having their probability less reduced by having
  multiple settlements.

  On the inside view it seems like the decay rate could be either a) higher than for extinction,
  since late-development AI seems like the main extinction risk at this stage, and that might be as
  able to destroy multiple settlements as it is one, or b) lower than for extinction, since AI risk
  seems like it would peak early and then rapidly decline if it doesn't kill us almost immediately.

  On the outside view, it seems like it should be slightly lower, since a multiplanetary
  civilisation provides less evidence against the probability of regressing to perils than it does
  against the probability of going extinct.

  So on balance I err towards making it slightly lower.
  """

  def two_planet_risk():
    return 0.2 # Intuition, no substantive reasoning

  def decay_rate():
    return 0.4 # Intuition, no substantive reasoning

  def min_risk():
    """Across a Kardashev II civilisation the probability of losing at least one settlement
    seems like it should remain significant, though given that for the foreseeable future
    scope for expansion increases cubicly (when you include rocky bodies, and assume after a point
    even relatively small settlements will have the technology to self-sustain), I would expect it
    to tend to a low rate relative to the probability of adding a settlement"""
    return 0.01

  if not n:
    # Allows us to check total probability sums to 1
    return any_intra_multiplanetary_regression(k, q)
  elif n == q:
    return 0
  elif n == q+1:
    return some_leftover_value_TODO()
  else:
    # The commented return value describes the linear decrease described above
    # Uncomment the next two lines if you think this is a more reasonable treatment
    # return any_intra_multiplanetary_regression(k, q) * ((n + 1)
    #                                               / (1 + (q ** 2)/2 + 3 * q / 2))

    # The commented out return values is the exponential decrease described above.
    total_probability_of_loss = any_intra_multiplanetary_regression(k, q) # How likely is it in total
    # we lose any number of planets between 1 and (q - 1) inclusive?
    weighting_decay_rate = 1.4 # Higher gives higher probability that given such a loss we'll lose a
    # smaller number of planets
    weighting_for_n_planets = weighting_decay_rate ** n # How likely is it, that given some loss,
    # that loss took us to exactly n planets?
    geometric_sum_of_weightings = ((1 - weighting_decay_rate ** (q - 1)) / (1 - weighting_decay_rate)
                                   - weighting_decay_rate) # We subtract the zeroth term from the series,
                                                           # since we're considering separately the
                                                           # possibility of losing all planets under
                                                           # 'extinction'
    # Thus weighting_for_n_planets / geometric_sum_of_weightings is a proportion; you can play with
    # the values at https://www.desmos.com/calculator/ku0p2iahq3

    return total_probability_of_loss * weighting_for_n_planets / geometric_sum_of_weightings

def regression_given_multiplanetary(k, q):
  return (extinction_given_multiplanetary(k, q)
          + survival_given_multiplanetary(k, q)
          + preindustrial_given_multiplanetary(k, q)
          + industrial_given_multiplanetary(k, q)
          + any_intra_multiplanetary_regression(k, q)
          + interstellar_given_multiplanetary(k, q))

def intraplanetary_regression_matrix(k):
  return [[transition_to_n_planets_given_multiplanetary(k, q, n) for n in range(2, q-1)]
           for q in range(2, constant.MAX_PLANETS)]

def perils_given_multiplanetary(k, q):
  """Ideally this would have a more specific notion of where in a time of perils you expect to end
  up given this transition, but since that could get complicated fast, I'm treating it as going to
  perils year 0 for now.

  Since perils is basically defined as 'modern+ technology but with only 1 planet', we can just use
  the existing formula for this.

  TODO if going to a fixed perils year, make it a later one."""
  return transition_to_n_planets_given_multiplanetary(k, q, 1)

def interstellar_given_multiplanetary(k, q):
  """Max value should get pretty close to 1, since at a certain number of planets the tech is all
  necessarily availabile and you've run out of extra planets to spread to.

  TODO need to specify behaviour for max value."""

  def x_stretch():
    return 0.2

  def y_stretch():
    return 1
    raise Exception('TODO - if this asymptotes too fast, we might get invalid total probabilities')

  def x_translation():
    return 2

  def gradient_factor():
    return 1

  return sigmoid_curved_risk(q, x_stretch(), y_stretch(), x_translation(), gradient_factor())

# TODO - consider reintroducing this checksum
# if not 1 == (extinction_given_multiplanetary(k)
#              + survival_given_multiplanetary(k)
#              + preindustrial_given_multiplanetary(k)
#              + industrial_given_multiplanetary(k)
#              + perils_given_multiplanetary(k)
#              + interstellar_given_multiplanetary(k)):
#   raise InvalidTransitionProbabilities("Transition probabilities from multiplanetary must == 1")
