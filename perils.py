import pdb
import math
import constant
from graph_functions import sigmoid_curved_risk

## Transition probabilities from time of perils state

def extinction_given_perils(k):
  """Sum of total extinction exit probability over all values of p given k"""
  pass

def extinction_given_perils(k, p):
  def x_stretch(k):
    """How much longer/less long would it take a typical reboot than in the previous one to develop
     modern weaponry given considerations of headwinds from eg resource depletion, environmental
     damage, and tailwinds from knowledge left over from previous civilisations"""
    return 1.5 ** k

  def y_stretch(k, p):
    """ I treat this as diminishing with k, since the more chances we've had to
    develop technology that might make us extinct, the less likely we should think it that that
    technology will actually do so"""

    # Desmos formula (not functioning)
    # x^{3}\cdot\max\left(1-x,0\ +\left(c+e^{-x^{2}}\right)\max\left(\min\left(x,1\right),0\right)\right)
    # To translate right by n units, add that for x < n, value = 0
    pass

  def x_translation():
    pass

  def gradient_factor(k):
    pass

  return sigmoid_curved_risk(x_stretch(), y_stretch(), gradient_factor())

def survival_given_perils(k):
  """Sum of total survival exit probability over all values of p given k"""
  pass

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
  """
  def x_stretch(k):
    base_value = 80 # Puts us slightly above 1/2way to max risk in the present day, technology-wise
    stretch_per_reboot = 1.5 # Intuition, no substantive reasoning
    return base_value * stretch_per_reboot ** (k + 1)

  def y_stretch():
    """Max probability per year of this transition."""
    return 0.0000005 # Seems like substantially the lowest probability perils exit, requiring
    # a pinhead balance

  def x_translation():
    """When does this risk start rising above 0, pre x-stretch?"""
    return 15

  def gradient_factor():
    return 1.1 # Intuition, no substantive reasoning

  return sigmoid_curved_risk(p, x_stretch(k), y_stretch(), x_translation(), gradient_factor())

def preindustrial_given_perils(k):
  """Sum of total preindustrial exit probability over all values of p given k"""
  pass

def preindustrial_given_perils(k, p):
  """I'm treating nukes as being substantially the most likely tech to cause this outcome, since
  they destroy far more resources than a pandemic would, making rebuilding much harder. So I expect
  the risk to more or less max out relatively early, as nuclear aresenals peak."""
  def x_stretch(k):
    base_value = 20 # Puts us more or less at max risk of this already, technology-wise
    stretch_per_reboot = 1.5 # Intuition, no substantive reasoning
    return base_value * stretch_per_reboot ** (k + 1)

  def y_stretch():
    """Max probability per year of this transition"""
    return 0.0002 # Roughly based on Ord's estimate of a 5% chance of full scale nuclear war in the
    # next century, given at
    # https://80000hours.org/podcast/episodes/toby-ord-the-precipice-existential-risk-future-humanity/#transcript
    # And assuming a roughly 40% chance of this outcome in that scenario

  def x_translation():
    return 10 # About the time the arsenal reached multiple thousands

  def gradient_factor():
    return 1.3 # Intuition, no substantive reasoning, except that it should be higher early than
    # going to survival

  return sigmoid_curved_risk(x_stretch(), y_stretch(), gradient_factor())

def industrial_given_perils(k):
  """Sum of total industrial exit probability over all values of p given k"""
  pass

def industrial_given_perils(k, p):
  """I treat this as possible through any weapons tech, meaning it has the slowest incline but
  reaches the highest peak of the bad exits, and is generally higher per year than the others"""

  def x_stretch(k, p):
    base_value = 65 # Puts us approx 3/4 of the way to max annual risk, technology-wise
    stretch_per_reboot = 1.5 # Intuition, no substantive reasoning
    return base_value * stretch_per_reboot ** (k + 1)

  def y_stretch(k, p):
    """Max probability per year of this transition"""
    return 0.0012

  def x_translation():
    return 8 # Around the time the US would have reached 1000 nuclear warheads

  def gradient_factor(k, p):
    return 1.3

  return sigmoid_curved_risk(x_stretch(), y_stretch(), gradient_factor())

def regression_to_perils_year_n_given_perils(k:int, p:int, n=None):
  """The simplest intuitive way I can think of to deal with this is to assume the probability of
  regressing decreases exponentially with the number of years we regressing, eg for p = 3, given that
  there has been some intra-perils regression we might say the probability of that regression is 1/15,
  2/15, 4/15, and 8/15 respectively for 'regressions' to p = 0, 1, 2, and 3.

  More generally, we woud say that, given some intra-perils regression, the probability of a
  regression to exactly progress-year n is a weighting_for_progress_year_n = <some weighting_decay_rate>**n,
  divided by the sum of weighting_for_progress_year_n for all valid values of n.

  I don't think this is a very convincing algorithm. Based on global GDP, we've arguably regressed
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
  def intra_perils_regression(k, p):
    return 0.026 # Should be a function - but for now this is a placeholder based on it roughly
                 # happening twice in 77 years on these graphs
                 # https://data.worldbank.org/indicator/NY.GDP.MKTP.KD.ZG
                 # https://ourworldindata.org/grapher/world-gdp-over-the-last-two-millennia?time=1940..2015
                 # See also UK GDP, for which reliable data goes back farther but is unsurprisingly
                 # more uneven: https://ourworldindata.org/grapher/total-gdp-in-the-uk-since-1270

  if not n:
    # Allows us to check total probability sums to 1
    return intra_perils_regression(k, p)
  elif n:
    return intra_perils_regression(k, p) * weighting_for_progress_year_n / arithmetic_sum_of_weightings

    total_probability_of_loss = intra_perils_regression(k, p) # How likely is it in total
    # we regress any number of progress years between 0 and p inclusive?
    weighting_decay_rate = 1.4 # Higher gives higher probability that given such a loss we'll lose a
    # smaller number of progress years: 2 would mean regressing to year n is 2x
    # as likely as regressing to year n-1. I chose the current value fairly arbitrarily, by
    # looking at this graph - https://data.worldbank.org/indicator/NY.GDP.MKTP.KD.ZG, treating
    # 1975, and 1982 as a regression of 0 years, 2009 as a regression of 1, and 2020 as a
    # regression of 2, and looking for a probability outcome slightly below that (to account for
    # eg survivor bias, and selection effects from starting to count immediately *after* WWII).
    weighting_for_progress_year_n = weighting_decay_rate ** n # How likely is it, that given some loss,
    # that loss took us to exactly progress year n?
    geometric_sum_of_weightings = (1 - weighting_decay_rate ** p) / (1 - weighting_decay_rate)
    # Thus weighting_for_progress_year_n / geometric_sum_of_weightings is a proportion; you can play with
    # the values at https://www.desmos.com/calculator/1pcgidwr3f

    return total_probability_of_loss * weighting_for_progress_year_n / geometric_sum_of_weightings

    # Linear version:
    # arithmetic_sequence_sum = p + 1 + (p**2 + p)/2
    # return (n + 1) / arithmetic_sequence_sum
    # Desmos version:
    # https://www.desmos.com/calculator/xtlzmxvikn

def multiplanetary_given_perils(k):
  pass

def multiplanetary_given_perils(k, p):
  """The default stretch/gradient values here are hacked so as to make it vaguely plausible (~10%)
  that at the annual probability predicted for 2050, Elon Musk's target, we would develop a colony within 10 years.
  Meanwhile I also tried to get them looking massively above/below Metaculus's prediction for 2100
  (https://www.metaculus.com/questions/1432/will-humans-have-a-sustainable-off-world-presence-by-2100/)
  on the probabilities for 2050 and 2100 respectively."""
  def x_stretch(k):
    base_value = 400
    stretch_per_reboot = 1.5 # Intuition, no substantive reasoning
    return base_value * stretch_per_reboot ** (k + 1)

  def y_stretch():
    """Max probability per year of this transition"""
    return 0.07 # Meaning a high tech civilisation could create a new settlement about once every 15
                # years, given enough space to expand into

  def x_translation():
    return 55 # Around 10 years after the time earliest estimates for a Mars base seemed to be when
              # the Apollo program was running

  def gradient_factor():
    return 0.8

def interstellar_given_perils(k):
  def interstellar_given_perils(k, p):
    return (1 - extinction_given_perils(k, p))

def _non_continuation_given_perils(k, p):
  return (extinction_given_perils(k, p)
          + survival_given_perils(k, p)
          + preindustrial_given_perils(k, p)
          + industrial_given_perils(k, p)
          + regression_to_perils_year_n_given_perils(k, p)
          + multiplanetary_given_perils(k, p)
          + interstellar_given_perils(k, p))

def perils_stasis_given_perils(k, p):
  """The probability that we transition to the same progress year."""
  if p >= constant.MAX_PROGRESS_YEARS:
    return 1 - _non_continuation_given_perils
  else:
    return (1 - _non_continuation_given_perils) * 1/30 # Using the same source as in regressions,
    # this is based on 'flattish' years appearing roughly this often for the last 60 years in World
    # Bank data
    # https://data.worldbank.org/indicator/NY.GDP.MKTP.KD.ZG
    # https://ourworldindata.org/grapher/world-gdp-over-the-last-two-millennia?time=1940..2015

def perils_progression_given_perils(k, p):
  if p >= constant.MAX_PROGRESS_YEARS:
    return 0
  else:
    return _non_continuation_given_perils - perils_stasis_given_perils(k, p)


# TODO - consider reintroducing this checksum
# if not 1 == (extinction_given_perils(k, p)
#              + survival_given_perils(k, p)
#              + preindustrial_given_perils(k, p)
#              + industrial_given_perils(k, p)
#              + regression_to_perils_year_n_given_perils(k, p)
#              + multiplanetary_given_perils(k, p)
#              + interstellar_given_perils(k, p)
#              + perils_continuation_given_perils(k, p)):
#   raise InvalidTransitionProbabilities("Transition probabilities from perils must == 1")
