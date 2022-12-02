import pdb
import math
# This script prints out a series of probabilities for transition becoming interstellar based on
# estimates of the transition probabilities of various(values are currently hardcoded placeholders)
# states, as in a Markov chain. The states are extinction, survival, preindustrial, industrial, time
# of perils, multiplanetary, and interstellar.
#
# A full description/explanation of the model is in the section titled The Cyclical Model in this
# post:
# https://forum.effectivealtruism.org/posts/YnBwoNNqe6knBJH8p/modelling-civilisation-after-a-catastrophe#The_cyclical_model


# Transition probabilities



class InvalidTransitionProbabilities(Exception):
  """Raised when transition probabilities from a state don't sum to 1"""
  pass

## Transition probabilities from survival state

def extinction_given_survival(k):
  """I expect this to decrease slightly with the value of k, given civilisations in the state have
  evidently survived to reach perils."""
  base_estimate = 0.0003 # I've just lifted this from one of Rodriguez's most pessimistic scenarios
  # in this post: https://forum.effectivealtruism.org/posts/GsjmufaebreiaivF7/what-is-the-likelihood-that-civilizational-collapse-would
  # I don't think the first two scenarios really describe a state of 'survival' for much the reasons
  # she describes. It could be much higher, given model uncertainty or its sensitivity to
  # lower numbers of surviving humans or much lower if we define the survival state more broadly
  probability_multiplier_per_previous_survival = 0.4 # This is just intuition. There's probably a
                                                     # more formal way of deriving such a multiplier
  expected_number_of_previous_survivals = (k - 1) * 0.01 # Again, just intuition of what proportion
                                                         # of milestone regressions took us back to
                                                         # a survival state.
  return (base_estimate *
          probability_multiplier_per_previous_survival ** expected_number_of_previous_survivals)

def preindustrial_given_survival(k):
  return 1 - extinction_given_survival(k)

if not extinction_given_survival() + preindustrial_given_survival() == 1:
  raise InvalidTransitionProbabilities("Transition probabilities from survival must == 1")


## Transition probabilities from preindustrial state

def extinction_given_preindustrial(k):
  """I expect this to decrease slightly with the value of k, given civilisations in the state have
  evidently survived to reach perils. Depleted resources will be a slight issue. There are various
  different suggested values in the comments below. The output of this function"""

  # Uncomment a value below to taste of expected time in years. The estimates of expected time to
  # recover come from Luisa Rodriguez's post,
  # https://forum.effectivealtruism.org/posts/Nc9fCzjBKYDaDJGiX/what-is-the-likelihood-that-civilizational-collapse-would-1
  # She now claims that she has updated towards 'technological stagnation', for which 'The biggest
  # reason is probably the risk of extreme, long-lasting climate change. It seems possible that
  # anthropogenic climate change could cause global warming extreme enough that agriculture would
  # become much more difficult than it was for early agriculturalists. Temperatures wouldn’t return to
  # current levels for hundreds of thousands of years, so if the warmer temperatures were much less
  # conducive to recovering agriculture and downstream technological developments, humanity might be
  # stagnant for millennia.' Unfortunately she doesn't further quantify this shift in estimates, but
  # hers is still the most comprehensive piece I know on the subject. So the first values are based
  # on her initial estimates (not they're in the order they appear in the post, not ascending):

  # 'If we think recovery time is limited by...'
  # 'Agricultural rev. and industrialization take as long as they did the first time'
  # expected_time_in_years = 300_000

  # 'Agricultural civilization returns quickly, industrial revolution takes as long as it did the
  # first time'
  # expected_time_in_years = 500 # Lower end of her range in this scenario
  # expected_time_in_years = 30_000 # Upper end of her range in this scenario

  # 'Inside view — If we assume that existing physical and human capital would accelerate the speed
  # of re-industrialization relative to the base rate'

  # 'Best case guess - Assumes the British industrial revolution happened about when we’d have expected'
  # expected_time_in_years = 100 # Lower end of her range in this scenario
  # expected_time_in_years = 3700 # Upper end of her range in this scenario

  # 'Pessimistic case guess - Assumes we got very lucky with the British industrial revolution'
  # expected_time_in_years = 1000 # Lower end of her range in this scenario
  # expected_time_in_years = 33_000 # Upper end of her range in this scenario

  # To account for her remarks about technological stagnation, I just naively add 10000 years to
  # above each of the:
  # expected_time_in_years = 10_100
  # expected_time_in_years = 10_500
  # expected_time_in_years = 11_000
  expected_time_in_years = 13_700
  # expected_time_in_years = 40_000
  # expected_time_in_years = 43_000
  # expected_time_in_years = 310_000

  # The below estimates of annual extinction rate come from this paper:
  # https://www.nature.com/articles/s41598-019-47540-7 - quotes from the same. Uncomment to taste.
  # Note that for narrative reasons they're in the order they appeared in that article, not ascending
  # extinction_probability_per_year = 1/14_000
  # 'Assuming a 200 thousand year (kyr) survival time, we can be exceptionally confident that rates
  # do not exceed 6.9 * 10^−5. This corresponds to an annual extinction probability below roughly 1 in 14,000.'

  # extinction_probability_per_year = 1/22_800
  # 'Extinction can be represented by the exponential distribution with constant extinction rate μ...
  # Using the fossil dated to 315ka as a starting point for humanity gives an upper bound
  # of μ < 4.4 * 10^−5, corresponding to an annual extinction probability below 1 in 22,800'

  # extinction_probability_per_year = 1/140_000
  # 'Using the emergence of Homo as our starting point pushes the initial bound back a full order of
  # magnitude, resulting in an annual extinction probability below 1 in 140,000.'

  extinction_probability_per_year = 1/87_000
  # 'We can also relax the one in million relative likelihood constraint and derive less conservative
  # upper bounds. An alternative bound would be rates with relative likelihood below 10−1 (1 in 10)
  # when compared to the baseline rate of 10−8. If we assume humanity has lasted 200kyr, we
  # obtain a bound of μ < 1.2 * 10^−5, corresponding to an annual extinction probability below 1 in 87,000.'

  # extinction_probability_per_year = 1/870_000
  # 'Using the 2Myr origin of Homo strengthens the bound by an order of magnitude in a
  # similar way and produces annual extinction probabilities below 1 in 870,000.''

  base_total_extinction_probability = 1 - ((1 - extinction_probability_per_year) ** expected_time_in_years)
  raise BaseException("there's a lot of negations I need to check in this function")

  multiplier_per_previous_preindustrial = 0.4 # Naively this seems like it should be
                                              # the same as in the
                                              # extinction_given_survival() function

  expected_number_of_previous_preindustrials = (k - 1) * 0.4
  # Thoughts behind above variable: I assume biopandemics would leave us enough technology to retain
  # industry; malevolent AI would most likely either wipe us out or be controlled by bad acting humans,
  # who would want to leave us with at least industrial technology; nuclear arsenals could eventually
  # destroy industry, but wouldn't be big enough for the first few years of a time of perils; some
  # kind of multiple catastrophe could also cause this

  return ((1 - base_total_extinction_probability) *
          multiplier_per_previous_preindustrial ** expected_number_of_previous_preindustrials)

def industrial_given_preindustrial(k):
  return 1 - extinction_given_preindustrial(k)

if not extinction_given_preindustrial() + industrial_given_preindustrial() == 1:
  raise InvalidTransitionProbabilities("Transition probabilities from preindustrial must == 1")


## Transition probabilities from industrial state

def extinction_given_industrial(k):
  """I expect this to have a complex relationship with k. Initially I think it decreases with k as
  resources are preferentially used up so each civilisation has to do more with less, but after some
  number of retries it should probably increase, as we gain evidence of our capacity to deal with
  those scarcer resources. There might also be dramatic differences in difficulty based exactly on what
  has been used up or left behind by previous civilisations, so we might want a branching function.
  Below I've used a branching function for the pessimistic case, but otherwise defaulted to the simple
  approach of assuming exponential decline
  """

  # For extinction probability per year, we can start with the base rates given in the previous
  # calculation, and then multiply them by some factor based on whether we think industry would make
  # humans more or less resilient.
  # base_annual_extinction_probability = 1/14_000
  # base_annual_extinction_probability = 1/22_800
  # base_annual_extinction_probability = 1/140_000
  base_annual_extinction_probability = 1/87_000
  # base_annual_extinction_probability = 1/870_000

  annual_extinction_probability_multiplier = 0.7 # Intuition based on the reasoning below:
  # This paper estimates that British grain output approxmately doubled between ~1760-1850, and had
  # approximately doubled over the 300 years before that:
  # https://www.researchgate.net/publication/228043115_Yields_Per_Acre_in_English_Agriculture_1250-1860_Evidence_from_Labour_Inputs
  # So if we assume losses of food are uncorrelated with each other, and the majority of the world
  # would go through a similar transition at once, that would suggest a lower bound on this multiplier
  # of ~0.25. Obviously the rest of the world was slower, though - going by these estimates of historical
  # *wheat* yield, the US took til about the 1930s to start catching up:
  # https://www.researchgate.net/figure/Wheat-Yields-1800-2004_fig1_263620307
  # https://www.agry.purdue.edu/ext/corn/news/timeless/yieldtrends.html
  # Declining resources might slow down the spread of agricultural improvements, though. Also,
  # surplus food production might not matter much for extreme events such as a supervolcano that blocked out
  # the sky for many years - although it might incentivise surplus food preservation. I suspect
  # such events constitute the majority of pre-modern extinction risk.

  # For expected time in years, we have to make some strong assumptions.

  # Pessimistic scenario
  # In this scenario, I assume all knowledge of previous civilisations' technology is either lost or
  # made useless by different resource constraints. Thus I imagine the original ~145 years for this
  # transition is stretched substantially by the decline in resource availability - most strongly so
  # from the initial lack of fossil fuels in reboot 1 and from phosphorus in subsequent reboots, then
  # somewhat more gently as rare earths etc are gradually left in unusable states.

  per_reboot_difficulty_modifier = 1.5 # How much longer/less long would it take a typical reboot than in the
  # previous one to develop modern technology given resource-depletion considerations

  if k == 1:
    expected_time_in_years = 1450
    # I mostly arbitrarily assume ten times the duration for rebooting with no oil, much less
    # coal that's more expensive to mine, and maybe 10% of the energy of our current civilisation
    # embodied in landfill:
    # https://scitechdaily.com/scientists-estimate-that-the-embodied-energy-of-waste-plastics-equates-to-12-of-u-s-industrial-energy-use/
    # Dartnell envisions what the process might look like here:
    # https://aeon.co/essays/could-we-reboot-a-modern-civilisation-without-fossil-fuels
    # He gives no probability estimates, but uses phrases like 'For a society to stand any chance of
    # industrialising under such conditions' and 'an industrial revolution without coal would be, at
    # a minimum, very difficult', suggesting he might think it's unlikely to *ever* happen.
  elif k == 2:
    expected_time_in_years = 2900
    # I imagine this disproportionately stretched again by the complete absence of coal and other easily
    # depletable resources. In particular easily phosphorus accessible rock phosphorus would be gone
    # (see discussion between John Halstead and David Denkenberger here):
    # https://forum.effectivealtruism.org/posts/rtoGkzQkAhymErh2Q/are-we-going-to-run-out-of-phosphorous
  else:
    expected_time_in_years = 2900 * per_reboot_difficulty_modifier ** (k - 2)

  # Optimistic scenario
  # In this scenario I assume the absence of fossil fuels/other resources is much less punitive
  # especially early on and enough knowledge from previous civilisations is mostly retained to actually
  # speed up this transition the first couple of times
  per_reboot_difficulty_modifier = 1.2
  expected_time_in_years = 100 * per_reboot_difficulty_modifier ** k

  return 1 - ((1 - base_annual_extinction_probability * annual_extinction_probability_multiplier) ** expected_time_in_years)

def perils_given_industrial(k):
  return 1 - extinction_given_industrial(k)

if not extinction_given_industrial() + perils_given_industrial() == 1:
  raise InvalidTransitionProbabilities("Transition probabilities from industrial must == 1")


## Transition probabilities from time of perils state

def sigmoid_curved_risk(x_stretch:float, y_stretch:float, gradient_factor:float) -> float:
  """The simplest intuitive trajectory I can think of to describe risks in a time of perils. Risks of
  all exits, good or bad, start at 0 and asymptote to some value(V) 0 < V <= 1

  Then the questions the parameters let us answer are 'how high do they asymptote to?' (y_stretch),
  and 'when do they start climbing and how fast do they climb?' (both a combination of x_stretch
  and gradient_factor). You can play with these values on Desmos:
  https://www.desmos.com/calculator, by pasting in
  \frac{1}{c\left(1+\left[bx+d\right]^{-a}e^{-\left[bx+d\right]}\right)}"""
  return 1 / y_stretch * (1 + (x_stretch * progress_year) ** -gradient_factor
                               * math.e ** -(x_stretch * progress_year))

def extinction_given_perils(k):
  """Sum of total extinction exit probability over all values of p given k"""
  pass

def extinction_given_perils(k, p):
  def x_stretch(k):
    """How much longer/less long would it take a typical reboot than in the previous one to develop
     modern technology given resource-depletion considerations"""
    return 1.5 ** k

  def y_stretch(k):
    """This determines max probability per year of this transition - a value of 0.5 would mean it asymptotes towards 0.5. I treat this is a constant,
    since theoretically accessible technologies won't change across reboots."""
    return pass

  def x_translation():
    return pass

  def gradient_factor(k):
    return pass

  return sigmoid_curved_risk(x_stretch(), y_stretch(), gradient_factor())

def survival_given_perils(k):
  """Sum of total survival exit probability over all values of p given k"""
  pass

def survival_given_perils(k, p):
  def x_stretch(k, p):
    return pass

  def y_stretch(k, p):
    """This determines max probability per year of this transition. I treat this is a constant,
    since theoretically accessible technologies won't change across reboots."""
    return pass

  def x_translation(k, p):
    return pass

  def gradient_factor(k, p):
    return pass

  return sigmoid_curved_risk(x_stretch(), y_stretch(), gradient_factor())

def preindustrial_given_perils(k):
  """Sum of total preindustrial exit probability over all values of p given k"""
  pass

def preindustrial_given_perils(k, p):
  def x_stretch(k, p):
    return pass

  def y_stretch(k, p):
    """This determines max probability per year of this transition. I treat this is a constant,
    since theoretically accessible technologies won't change across reboots."""
    return pass

  def x_translation(k, p):
    return pass

  def gradient_factor(k, p):
    return pass

  return sigmoid_curved_risk(x_stretch(), y_stretch(), gradient_factor())

def industrial_given_perils(k):
  """Sum of total industrial exit probability over all values of p given k"""
  pass

def industrial_given_perils(k, p):
  """Probability of regressing to industrial state in the pth progress year after k reboots.
  I assume this function has no x-translation, since the point where this risk starts rising is
  defined as the start of the time of perils"""

  def x_stretch(k, p):
    return pass

  def y_stretch(k, p):
    """This determines max probability per year of this transition. I treat this is a constant,
    since theoretically accessible technologies, which I assume determine max risk, won't change
    across reboots."""
    return 500

  def gradient_factor(k, p):
    return pass

  return return sigmoid_curved_risk(x_stretch(), y_stretch(), gradient_factor())

def perils_regression_to_year_n_given_perils(k, p, n=None):
  """I see two intutive and relatively simple ways of treating this. In both ways we assume some
  total probability of regressing within perils given k & p, and that regressions divide up this
  probability, becoming less likely the larger they are. Then either:
  1) assume the probability of regressing a year decreases linearly with the number of years we
  consider regressing, eg for p = 4, we might have probabilities of 5/15, 4/15, 3/15, 2/15, or 1/15 for
  regressing 0, 1, 2, 3, or 4 years respectively.
  2) assume the probability of regressing decreases exponentially with the number of years we consider
  regressing, eg for p = 4 we might have probabilities of """
  def perils_regression_given_perils(k, p):
    return 0.052 # Should be a function - but for now this is a placeholder based on it roughly
                 # happening 4 times in 77 years on these graphs
                 # https://data.worldbank.org/indicator/NY.GDP.MKTP.KD.ZG
                 # https://ourworldindata.org/grapher/world-gdp-over-the-last-two-millennia?time=1940..2015
  if not n:
    # So can can check total probability sums to 1
    return perils_regression_given_perils(k, p)
  else:
    # The commented return value describes the linear decrease described above
    # Uncomment the next two lines if you think this is a more reasonable treatment
    # return perils_regression_given_perils(k, p) * ((n + 1)
    #                                               / (1 + (p ** 2)/2 + 3 * p / 2))

    # The commented out return values is the exponential decrease described above.
    r = 1.4 # A constant determining the rate of decrease: 2 would mean regressing to year n is 2x
          # as likely as regressing to year n-1. I chose the current value fairly arbitrarily, by
          # looking at this graph - https://data.worldbank.org/indicator/NY.GDP.MKTP.KD.ZG, treating
          # 1975, and 1982 as a regression of 0 years, 2009 as a regression of 1, and 2020 as a
          # regression of 2, and looking for a gave probability slightly below that (to account for
          # eg survivor bias, and selection effects from starting to count immediately *after* WWII).
    return perils_regression_given_perils(k, p) * (r ** n / ((1 - r ** p) / (1 - r))) # These latter two lines are the
                                                              # geometric sum of all the
                                                              # numerators for p progress years,
                                                              # so that the sum of all the
                                                              # numerators over the denominator
                                                              # is 1

def multiplanetary_given_perils(k):
  """Sum of total multiplanetary exit probability over all values of p given k"""
  pass

def multiplanetary_given_perils(k, p):
  def x_stretch(k, p):
    return pass

  def y_stretch(k, p):
    return pass

  def x_translation(k, p):
    return pass

  def gradient_factor(k, p):
    return pass
  return 0.5

def interstellar_given_perils(k):
  def interstellar_given_perils(k, p):
    return (1 - extinction_given_perils(k, p))

if not 1 == (extinction_given_perils(k, p)
             + survival_given_perils(k, p)
             + preindustrial_given_perils(k, p)
             + industrial_given_perils(k, p)
             + perils_regression_to_year_n_given_perils(k, p)
             + multiplanetary_given_perils(k, p)
             + interstellar_given_perils(k, p)):
  raise InvalidTransitionProbabilities("Transition probabilities from perils must == 1")


## Transition probabilities from multiplanetary state

def fractional_risk(single_planet_risk, q, correlation_adjustment):
  """The simplest way I can think of to intuit the risk given multiple interplanetary settlements is
  as a fraction of some initially specified risk, with some adjustment to account for the fact that
  the risk of losing settlements is somewhat correlated
  """
  return single_planet_risk / q ** correlation_adjustment

def extinction_given_multiplanetary(k):
  """Sum of total extinction exit probability over all values of q given k"""
  pass

def extinction_given_multiplanetary(k, q):
  def single_planet_risk(k):
    return 0.1

   def correlation_adjustment(k):
    """Should be a value between 0 and 1. Lower treats events that could cause a 1-planet
    civilisation to go extinct as less likely to be reduced by having multiple settlements"""
    return 0.9

  return fractional_risk(single_planet_risk(), q, correlation_adjustment())

def survival_given_multiplanetary(k):
  """Sum of total survival exit probability over all values of q given k"""
  pass

def survival_given_multiplanetary(k, q):
  def single_planet_risk(k):
    return 0.1

   def correlation_adjustment(k):
    """Should be a value between 0 and 1. Lower treats events that could cause regression to a
    1-planet civilisation in a survival state as having their probability less reduced by having
    multiple settlements"""
    return 0.9

  return fractional_risk(single_planet_risk(), q, correlation_adjustment())

def preindustrial_given_multiplanetary(k):
  """Sum of total preindustrial exit probability over all values of q given k"""
  pass

def preindustrial_given_multiplanetary(k, q):
  def single_planet_risk(k):
    return 0.1

   def correlation_adjustment(k):
    """Should be a value between 0 and 1. Lower treats events that could cause regression to a
    1-planet civilisation in a preindustrial state as having their probability less reduced by having
    multiple settlements"""
    return 0.9

  return fractional_risk(single_planet_risk(), q, correlation_adjustment())

def industrial_given_multiplanetary(k):
  """Sum of total industrial exit probability over all values of q given k"""
  pass

def industrial_given_multiplanetary(k, q):
  def single_planet_risk(k):
    return 0.1

   def correlation_adjustment(k):
    """Should be a value between 0 and 1. Lower treats events that could cause regression to a
    1-planet civilisation in an industrial state as having their probability less reduced by having
    multiple settlements"""
    return 0.9

  return fractional_risk(single_planet_risk(), q, correlation_adjustment())

def perils_given_multiplanetary(k):
  """Sum of total perils exit probability over all values of q given k"""
  pass

def perils_given_multiplanetary(k, q):
  def single_planet_risk(k):
    return 0.1

   def correlation_adjustment(k):
    """Should be a value between 0 and 1. Lower treats events that could cause regression to a
    1-planet civilisation in a perils state as having their probability less reduced by having
    multiple settlements"""
    return 0.9

  return fractional_risk(single_planet_risk(), q, correlation_adjustment())

def interstellar_given_multiplanetary(k):
  return (1 - extinction_given_multiplanetary(k)
            - survival_given_multiplanetary(k)
            - preindustrial_given_multiplanetary(k)
            - industrial_given_multiplanetary(k)
            - perils_given_multiplanetary(k))

if not 1 == (extinction_given_multiplanetary(k)
             + survival_given_multiplanetary(k)
             + preindustrial_given_multiplanetary(k)
             + industrial_given_multiplanetary(k)
             + perils_given_multiplanetary(k)
             + interstellar_given_multiplanetary(k)):
  raise InvalidTransitionProbabilities("Transition probabilities from multiplanetary must == 1")


