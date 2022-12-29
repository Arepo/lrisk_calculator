import math

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

  https://www.desmos.com/calculator/egndiwnukv

  TODO: look into failure rate functions as an alternative approach"""

  return y_stretch /  (1 + (1/x_stretch * x - x_translation) ** -gradient_factor
                             * math.e ** -(1/x_stretch * (x - x_translation)))
