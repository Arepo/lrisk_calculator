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

def sigmoid_curved_risk(x:int, x_stretch:float, y_stretch:float, x_translation: float, gradient_factor: float=2) -> float:
  """A stretched sigmoid the simplest intuitive trajectory I can think of to describe most risks in
  a time of perils. Risks of all exits, good or bad, start at 0 and asymptote to some value V, such
  that 0 < V < 1, and such that the sum of V for all possible exits is <= 1, with p as the
  x-axis, and annual probability of the event in question as the y-axis.

  p is a 'progress year' - a year of real time at a certain level of technology, such that the time
  of perils starts at p = 0, and we generally advance by one unit per year, but can regress by 0 up
  to p years within the time of perils given 'minor' disasters.

  x_stretch determines how extended the sigmoid curve will be from some base, eg due to decreased
  resources slowing tech progress down. Higher = a more drawn out curve.

  gradient_factor is related to x_stretch, but determines how quick relative to the the main incline
  risks accelerate and eventually level off - a value looks more like a log-curve than an
  s-curve.

  y_stretch determines max probability per year of this transition - a value of 0.5 would mean it
  asymptotes towards 0.5.

  x_translation determines (pre-x_stretch adjustment) how many progress years after entering the
  time of perils technologies that enable this outcome are to start getting produced - ie when the
  risk starts climbing above 0.

  Then the questions the parameters let us answer are 'how high does annual risk asymptote to?'
  (y_stretch), and 'when does it start climbing' (x_translation, x_stretch) and 'how fast does it
  climb from that point?' (x_stretch, gradient_factor)

  In general for my default estimates, I'm using the current time of perils as a template for
  k = 0

  https://www.desmos.com/calculator/egndiwnukv

  TODO: look into failure rate functions as an alternative approach"""

  return y_stretch /  (1 + (1/x_stretch * x - x_translation) ** -gradient_factor
                             * math.e ** -(1/x_stretch * (x - x_translation)))


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

  def

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

  return return sigmoid_curved_risk(x_stretch(), y_stretch(), gradient_factor())

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

def _non_continuation_given_perils(k, p)
  return (extinction_given_perils(k, p)
          + survival_given_perils(k, p)
          + preindustrial_given_perils(k, p)
          + industrial_given_perils(k, p)
          + regression_to_perils_year_n_given_perils(k, p)
          + multiplanetary_given_perils(k, p)
          + interstellar_given_perils(k, p))

progress_year_cap = 1_000_000 # To make perils a finite subchain

def perils_stasis_given_perils(k, p):
  """The probability that we transition to the same progress year."""
  if p >= progress_year_cap:
    return 1 - _non_continuation_given_perils
  else:
    return (1 - _non_continuation_given_perils) * 1/30 # Using the same source as in regressions,
    # this is based on 'flattish' years appearing roughly this often for the last 60 years in World
    # Bank data
    # https://data.worldbank.org/indicator/NY.GDP.MKTP.KD.ZG
    # https://ourworldindata.org/grapher/world-gdp-over-the-last-two-millennia?time=1940..2015

def perils_progression_given_perils(k, p):
  if p >= progress_year_cap:
    return 0
  else:
    return _non_continuation_given_perils - perils_stasis_given_perils(k, p)


if not 1 == (extinction_given_perils(k, p)
             + survival_given_perils(k, p)
             + preindustrial_given_perils(k, p)
             + industrial_given_perils(k, p)
             + regression_to_perils_year_n_given_perils(k, p)
             + multiplanetary_given_perils(k, p)
             + interstellar_given_perils(k, p)
             + perils_continuation_given_perils(k, p)):
  raise InvalidTransitionProbabilities("Transition probabilities from perils must == 1")


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

  def any_intra_multiplanetary_regression(k, q):
    return exponentially_decaying_risk(two_planet_risk(), q, k, decay_rate())

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

if not 1 == (extinction_given_multiplanetary(k)
             + survival_given_multiplanetary(k)
             + preindustrial_given_multiplanetary(k)
             + industrial_given_multiplanetary(k)
             + perils_given_multiplanetary(k)
             + interstellar_given_multiplanetary(k)):
  raise InvalidTransitionProbabilities("Transition probabilities from multiplanetary must == 1")


# Planets transition matrix
[extinction_given_multiplanetary(k, q) for q in range(2, constant.MAX_PLANETS)]
[survival_given_multiplanetary(k, q) for q in range(2, constant.MAX_PLANETS)]
[preindustrial_given_multiplanetary(k, q) for q in range (2, constant.MAX_PLANETS)]
[industrial_given_multiplanetary(k, q) for q in range(2, constant.MAX_PLANETS)]
[perils_given_multiplanetary(k, q) for q in range(2, constant.MAX_PLANETS)]
[0 for q in range(2, constant.MAX_PLANETS)]
# [transition_to_n_planets_given_multiplanetary(k, q, n)]
[industrial_given_multiplanetary(k, q) for q in range(2, constant.MAX_PLANETS)]


