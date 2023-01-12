import pdb
import math
import constant
from functools import cache
from graph_functions import sigmoid_curved_risk, exponentially_decaying_risk

## Transition probabilities from time of perils state

@cache
def extinction_given_perils(k, p):
  def x_stretch(k):
    base_x_stretch = 83 # To set the initial shape of the graph to something plausibly consistent
    # with our current perceived risk

    # How much longer/less long would it take a typical reboot than in the previous one to develop
    # modern weaponry given considerations of headwinds from eg resource depletion, environmental
    # damage, and tailwinds from knowledge left over from previous civilisations
    reboot_multiplier = 1.5 ** k
    return base_x_stretch * reboot_multiplier

  def y_stretch(k):
    """ I treat this as diminishing with k, since the more chances we've had to
    develop technology that might make us extinct, the less likely we should think it that that
    technology will actually do so"""

    max_annual_risk = 0.04 # Based on the highest estimate for the present day
    # on the existential risks database: https://docs.google.com/spreadsheets/d/1W10B6NJjicD8O0STPiT3tNV3oFnT8YsfjmtYR8RO_RI/edit#gid=0
    min_risk = 0.004 # Intuition, on it seeming unlikely to decrease more than 10-fold
    decay_rate = 0.4 # Intuition
    return exponentially_decaying_risk(max_annual_risk, k, decay_rate, min_risk, x_translation=0)

  def x_translation():
    # TODO I can probably subtract the lowest x_translation value from all the others to save some
    # runtime, since nothing interesting happens until we hit it
    return 15

  def gradient_factor():
    return 2.5 # Intuition, no substantive reasoning

  # Graph with these values for k=0 at https://www.desmos.com/calculator/mbwoy2muin
  return sigmoid_curved_risk(p, x_stretch(k), y_stretch(k), x_translation() ,gradient_factor())

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
    base_value = 80 # Puts us slightly above 1/2way to max risk in the present day, technology-wise
    stretch_per_reboot = 1.5 # Intuition, no substantive reasoning
    return base_value * stretch_per_reboot ** (k + 1)

  def y_stretch():
    """Max probability per year of this transition."""
    return 0.000_005 # Seems like substantially the lowest probability perils exit, requiring
    # a pinhead balance of maybe 99.99% killed, but not immediate extinction

  def x_translation():
    """When does this risk start rising above 0, pre x-stretch?"""
    return 15

  def gradient_factor():
    return 1.1 # Intuition, no substantive reasoning

  return sigmoid_curved_risk(p, x_stretch(k), y_stretch(), x_translation(), gradient_factor())

@cache
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
    return 0.00045 # Ord's estimate of a 0.05 chance of full scale nuclear war in the next century, given at
    # https://80000hours.org/podcast/episodes/toby-ord-the-precipice-existential-risk-future-humanity/#transcript
    # implies a ~0.0005 average chance per year. I assume it reaches double that at peak, and that
    # such a war would move us to preindustrial with 0.3 probability. Then I add half as much again for
    # the combined chance of getting here via any other catastrophe

  def x_translation():
    return 10 # About the time the world's nuclear arsenal took to reach multiple thousands

  def gradient_factor():
    return 1.3 # Intuition, no substantive reasoning, except that it should be higher early than
    # going to survival

  return sigmoid_curved_risk(p, x_stretch(k), y_stretch(), x_translation(), gradient_factor())

@cache
def industrial_given_perils(k, p):
  """I treat this as possible through any weapons tech, meaning it has the slowest incline but
  reaches the highest peak of the bad exits, and is generally higher per year than the others"""

  def x_stretch(k):
    base_value = 65 # Puts us approx 3/4 of the way to max annual risk, technology-wise
    stretch_per_reboot = 1.5 # Intuition, no substantive reasoning
    return base_value * stretch_per_reboot ** (k + 1)

  def y_stretch():
    """Max probability per year of this transition. TODO: no way this should be lower than extinction"""
    return 0.0015 # I assume a 0.1 total chance of a catastrophe that would wipe out billions in the
    # next century, giving a ~0.001 average chance per year. I assume it reaches triple that at peak.
    # and that such an event would move us to preindustrial with 0.5 probability.

  def x_translation():
    return 8 # Around the time the US would have reached 1000 nuclear warheads

  def gradient_factor():
    return 1.3

  return sigmoid_curved_risk(p, x_stretch(k), y_stretch(), x_translation(), gradient_factor())

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

  def any_intra_perils_regression():
    return 0.026 # Might be a function of k and/or p - but for now this is a placeholder based on it
                 # roughly happening twice in 77 years on these graphs
                 # https://data.worldbank.org/indicator/NY.GDP.MKTP.KD.ZG
                 # https://ourworldindata.org/grapher/world-gdp-over-the-last-two-millennia?time=1940..2015
                 # See also UK GDP, for which reliable data goes back farther but is unsurprisingly
                 # more uneven: https://ourworldindata.org/grapher/total-gdp-in-the-uk-since-1270

  def remainder_outcome(k, p):
    return 1 - (extinction_given_perils(k, p)
                + survival_given_perils(k, p)
                + preindustrial_given_perils(k, p)
                + industrial_given_perils(k, p)
                + any_intra_perils_regression()
                + multiplanetary_given_perils(k, p)
                + interstellar_given_perils(k, p))

  at_max_year = p == constant.MAX_PROGRESS_YEARS - 1 # The case where we've said we can't increment
  # progress years any further

  if (n == p + 1 and not at_max_year) or n == p and at_max_year:
    # Our catchall is either progressing one progress year or staying on the spot if we're at max
    return remainder_outcome(k, p)
  elif n > (p + 1):
    # We only allow progress to increment by up to one.
    return 0
  elif p - n + 1 > constant.MAX_PROGRESS_YEAR_REGRESSION_STEPS:
    # We round to 0 when numbers get small enough,
    # so we don't have to deal with fractions like ~10^10000/2*10^10000 in the geometric sequence below
    return 0

  # If we get this far, we're setting up to calculate the division of the total probability of
  # any_intra_perils_regression() into the specific probability of a regression to year n

  if p >= constant.MAX_PROGRESS_YEAR_REGRESSION_STEPS and at_max_year:
    # Reduce large numbers to the minimum, eg regression from progress-year 1000 from progress-year
    # 950 becomes regression from PY 50 to PY 0. This way we ensure proportions still sum to 0.
    # In the specific case of being in the last allowed progress year, we have one fewer years to that
    # point to distribute our total probability between (since staying on the spot becomes our
    # remainder, rather than our smallest 'regression')
    target_year = n - p + constant.MAX_PROGRESS_YEAR_REGRESSION_STEPS + 1
    max_regressed_states = constant.MAX_PROGRESS_YEAR_REGRESSION_STEPS - 1
  elif p >= constant.MAX_PROGRESS_YEAR_REGRESSION_STEPS:
    # Reduce large numbers to the minimum, eg regression from progress-year 1000 from progress-year
    # 950 with max_distance 100 becomes regression from PY 100 to PY 50. This way we ensure proportions still sum to 0.
    target_year = n - p + constant.MAX_PROGRESS_YEAR_REGRESSION_STEPS + 1
    max_regressed_states = constant.MAX_PROGRESS_YEAR_REGRESSION_STEPS
  elif at_max_year:
    target_year = n
    max_regressed_states = p
  else:
    target_year = n
    max_regressed_states = p + 1

   # How likely is it in total
  # we regress any number of progress years between 0 and p inclusive?

  weighting_decay_rate = 1.4 # Higher gives higher probability that given such a loss we'll lose a
  # smaller number of progress years: 2 would mean regressing to year n is 2x
  # as likely as regressing to year n-1. I chose the current value fairly arbitrarily, by
  # looking at this graph - https://data.worldbank.org/indicator/NY.GDP.MKTP.KD.ZG, treating
  # 1975, and 1982 as a regression of 0 years, 2009 as a regression of 1, and 2020 as a
  # regression of 2, and looking for a probability outcome slightly below that (to account for
  # eg survivor bias, and selection effects from starting to count immediately *after* WWII).

  geometric_sum_of_weightings = ( (1 - weighting_decay_rate ** max_regressed_states)
                                  / (1 - weighting_decay_rate))

  numerator_for_progress_year_n = weighting_decay_rate ** target_year # How likely is it, that given some loss,
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

  return sigmoid_curved_risk(p, x_stretch(k), y_stretch(), x_translation(), gradient_factor())

@cache
def interstellar_given_perils(k, p):
  """Graph with these values at https://www.desmos.com/calculator/kcrmqyqow5"""
  def x_stretch(k):
    base_value = 100 # The base value and x-stretch here are values which, given y_stretch and x_translation, eyeball to
    # giving a total probability by 2100 vaguely consistent with the ~60% estimate on Metaculus:
    # https://www.metaculus.com/questions/1432/will-humans-have-a-sustainable-off-world-presence-by-2100/
    # and which don't accelerate much before 2050
    stretch_per_reboot = 1.5 # Intuition, no substantive reasoning
    return base_value * stretch_per_reboot ** (k + 1)

  def y_stretch():
    """Max probability per year of this transition"""
    return 0.07 # I assume that a high tech civilisation with access to a nearby planet could
    # colonise it within about 15 years

  def x_translation():
    return 80 # Robert Zubrin seems to have been the first person to make a practical proposal to settle
    # Mars, and that was around 1990, and somewhat similar to SpaceX's plan. In his most optimistic
    # vision, the program would have taken maybe
    # a few years to get going, but have been slower to accelerate than Musk's idea, which Musk thought
    # in about 2020 was doable by about 2050. So if Zubrin's plan had been followed enthusiastically,
    # it might in the absolute best case have got there about 25 years earlier.

  def gradient_factor():
    return 3.3

  return sigmoid_curved_risk(p, x_stretch(k), y_stretch(), x_translation(), gradient_factor())

@cache
def _non_continuation_given_perils(k, p):
  return (extinction_given_perils(k, p)
          + survival_given_perils(k, p)
          + preindustrial_given_perils(k, p)
          + industrial_given_perils(k, p)
          + transition_to_year_n_given_perils(k, p)
          + multiplanetary_given_perils(k, p)
          + interstellar_given_perils(k, p))

@cache
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

@cache
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
#              + transition_to_year_n_given_perils(k, p)
#              + multiplanetary_given_perils(k, p)
#              + interstellar_given_perils(k, p)
#              + perils_continuation_given_perils(k, p)):
#   raise InvalidTransitionProbabilities("Transition probabilities from perils must == 1")
