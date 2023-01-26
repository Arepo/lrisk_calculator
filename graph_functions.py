from functools import cache
import math
import pdb

# TODO simplify these functions if possible

@cache
def sigmoid_curved_risk(x:int, x_stretch:float, y_stretch:float, x_translation: float, sharpness: float=2) -> float:
  """A stretched sigmoid is the simplest intuitive trajectory I can think of to describe most risks in
  a time of perils, and some in a multiplanetary state. Risks of all exits, good or bad, start at ~0
  and asymptote to some value V, such that 0 < V < 1.

  x_stretch determines how extended the sigmoid curve will be from some base, eg due to decreased
  resources slowing tech progress down. Higher = a more drawn out curve.

  y_stretch determines max probability per year of this transition - a value of 0.5 would mean it
  asymptotes towards 0.5.

  x_translation determines (pre-x_stretch adjustment) how many progress years after entering the
  time of perils technologies that enable this outcome are to start getting produced - ie when the
  risk starts climbing above 0.

  sharpness affects the gradient near the 'edges' of the S (the points where it noticeably climbs/
  levels off).

  Then the questions the parameters let us answer are 'how high does annual risk asymptote to?'
  (y_stretch), and 'when does it start meaningfully climbing' (x_translation) and 'how fast does it
  climb from that point?' (x_stretch)

  In general for my default estimates, I'm using the current time of perils, dated from 1945, as a
  template for k = 0

  An example version of the graph is at https://www.desmos.com/calculator/7zriffon47

  I owe this interpretation of an S-curve to Nick Krempel.

  TODO: look into failure rate functions as an alternative approach
  TODO: look into simpler scipy implementations"""

  modified_x_value = 1 / x_stretch * (x - x_translation)

  if x - x_translation == 0 or modified_x_value < 0:
    return 0 # Theoretically this makes it discontinuous, but the value should be so small it's
    # indistinguishable from 0 for practical purposes

  return y_stretch /  (1 + modified_x_value ** -sharpness * math.e ** -(modified_x_value))

@cache
def exponentially_decaying_risk(x, starting_value, decay_rate, min_value=0, x_translation=0):
  """The simplest way I can think of to intuit the various risks given multiple interplanetary
  settlements is as an exponential decay based on the number of planets.

  Another intuitive option would be something like 1/(x ** <some_value>), which would eventually
  decrease the probability of the risks more slowly, but could decrease it faster early on
  if we thought eg proving the concept would substantially improve our prospects.

  k is available as a parameter if people think it's important, but I'm treating it as irrelevant
  once we've reached this stage.

  You can play with the generic formula at https://www.desmos.com/calculator/vbvu6a1yyo

  x_translation defaults to 2, since this is mostly used for muultiplanetary
  functions in which we define 2 as the min number of planets in the state

  Note that min_value is a translation on the y-axis. So if you set starting_value as 0.4 and
  min_value as 0.1, your actual starting_value will be 0.5

  TODO: look into simpler scipy implementations"""
  return starting_value * (1 - decay_rate) ** (x - x_translation) + min_value






