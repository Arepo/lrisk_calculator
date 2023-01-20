from functools import cache
import math
import pdb

# TODO simplify these functions if possible

@cache
def sigmoid_curved_risk(x:int, x_stretch:float, y_stretch:float, x_translation: float, gradient_factor: float=2) -> float:
  """A stretched sigmoid the simplest intuitive trajectory I can think of to describe most risks in
  a time of perils, and some in a multiplanetary state. Risks of all exits, good or bad, start at 0
  and asymptote to some value V, such that 0 < V < 1, and such that the sum of V for all possible
  exits is <= 1, with p as the x-axis, and annual probability of the event in question as the y-axis.

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

  https://www.desmos.com/calculator/eb29bnsssr

  TODO: look into failure rate functions as an alternative approach
  TODO: look into simpler scipy implementations"""

  min_value = 1 / x_stretch * (x - x_translation)

  if x - x_translation == 0 or min_value < 0:
    return 0 # Hack to prevent a DivisionbyZero error or accidentally introducing complex numbers

  return y_stretch /  (1 + (min_value) ** -gradient_factor * math.e ** -(1 / x_stretch * (x - x_translation)))

@cache
def exponentially_decaying_risk(starting_value, x, decay_rate=0.5, min_value=0, x_translation=0):
  """The simplest way I can think of to intuit the various risks given multiple interplanetary
  settlements is as an exponential decay based on the number of planets.

  Another intuitive option would be something like 1/(x ** <some_value>), which would eventually
  decrease the probability of the risks more slowly, but could decrease it faster early on
  if we thought eg proving the concept would substantially improve our prospects.

  k is available as a parameter if people think it's important, but I'm treating it as irrelevant
  once we've reached this stage.

  You can play with the formula and values at https://www.desmos.com/calculator/bcu1qfp8wu

  x_translation defaults to 2, since this is mostly used for muultiplanetary
  functions in which we define 2 as the min number of planets in the state

  Note that min_value is a translation on the y-axis. So if you set starting_value as 0.4 and
  min_value as 0.1, your actual starting_value will be 0.5

  TODO: look into simpler scipy implementations"""
  return starting_value  * (1 - decay_rate) ** (x - x_translation) + min_value

@cache
def power_law_risk(x, y_stretch, decay_rate, x_translation=0):
  if x - x_translation < 1:
    return 0
  else:
    return y_stretch * (x - x_translation) ** -(decay_rate)
