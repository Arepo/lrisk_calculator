import pdb
from functools import cache

from pydtmc import MarkovChain

import constant
import multiplanetary
import perils
import preperils

# See https://dbader.org/blog/python-memoization for a primer on caching

class IntraPerilsMCWrapper():
  def __init__(self, k):
    self.k = k
    extinction_row =     [0] * constant.MAX_PROGRESS_YEARS + [1,0,0,0,0,0]
    survival_row =       [0] * constant.MAX_PROGRESS_YEARS + [0,1,0,0,0,0]
    preindustrial_row =  [0] * constant.MAX_PROGRESS_YEARS + [0,0,1,0,0,0]
    industrial_row =     [0] * constant.MAX_PROGRESS_YEARS + [0,0,0,1,0,0]
    multiplanetary_row = [0] * constant.MAX_PROGRESS_YEARS + [0,0,0,0,1,0]
    interstellar_row =   [0] * constant.MAX_PROGRESS_YEARS + [0,0,0,0,0,1]
    year_range = range(0, constant.MAX_PROGRESS_YEARS)

    intra_transition_probabilities = {p:[perils.transition_to_year_n_given_perils(k, p, n) for n in year_range]
                                      for p in year_range}

    # k = 1
    # p = 101
    # arr = [perils.transition_to_year_n_given_perils(1, 101, n) for n in year_range]


    exit_probabilities = {p:[perils.extinction_given_perils(k, p),
                          perils.survival_given_perils(k, p),
                          perils.preindustrial_given_perils(k, p),
                          perils.industrial_given_perils(k, p),
                          perils.multiplanetary_given_perils(k, p),
                          perils.interstellar_given_perils(k, p)] for p in year_range}

    year_p_rows = [intra_transition_probabilities[p] + exit_probabilities[p] for p in year_range]

    probability_matrix = year_p_rows + [extinction_row,
                                        survival_row,
                                        preindustrial_row,
                                        industrial_row,
                                        multiplanetary_row,
                                        interstellar_row]

    numbers = [f"{num}" for num in year_range]
    # pdb.set_trace()
    self.mc = MarkovChain(probability_matrix, list(numbers)
                                              + ['Extinction',
                                                'Survival',
                                                'Preindustrial',
                                                'Industrial',
                                                'Perils',
                                                'Interstellar'])

  def extinction_given_perils(self):
    return self.mc.absorption_probabilities()[some_value][some_other_value]

  def survival_given_perils(self, k1):
    if self.k + 1 == k1:
      return self.mc.absorption_probabilities()[some_value][some_other_value]
    else:
      return 0

  def preindustrial_given_perils(self, k1):
    if self.k + 1 == k1:
      return self.mc.absorption_probabilities()[some_value][some_other_value]
    else:
      return 0

  def industrial_given_perils(self, k1):
    if self.k + 1 == k1:
      return self.mc.absorption_probabilities()[some_value][some_other_value]
    else:
      return 0

  def multiplanetary_given_perils(self, k1):
    if self.k == k1:
      return self.mc.absorption_probabilities()[some_value][some_other_value]
    else:
      return 0

  def interstellar_given_perils(self):
    return self.mc.absorption_probabilities()[some_value][some_other_value]



@cache
def intra_multiplanetary_markov_chain():
  extinction_row =     [0] * (constant.MAX_PLANETS - 1) + [1,0,0,0,0,0]
  survival_row =       [0] * (constant.MAX_PLANETS - 1) + [0,1,0,0,0,0]
  preindustrial_row =  [0] * (constant.MAX_PLANETS - 1) + [0,0,1,0,0,0]
  industrial_row =     [0] * (constant.MAX_PLANETS - 1) + [0,0,0,1,0,0]
  perils_row =         [0] * (constant.MAX_PLANETS - 1) + [0,0,0,0,1,0]
  interstellar_row =   [0] * (constant.MAX_PLANETS - 1) + [0,0,0,0,0,1]
  planet_range = range(2, constant.MAX_PLANETS + 1) # Python range excludes max value

  intra_transition_probabilities = {q:[multiplanetary.transition_to_n_planets_given_multiplanetary(q, n) for n in planet_range]
                                    for q in planet_range}
  exit_probabilities = {q:[multiplanetary.extinction_given_multiplanetary(q),
                           multiplanetary.survival_given_multiplanetary(q),
                           multiplanetary.preindustrial_given_multiplanetary(q),
                           multiplanetary.industrial_given_multiplanetary(q),
                           multiplanetary.perils_given_multiplanetary(q),
                           multiplanetary.interstellar_given_multiplanetary(q)] for q in planet_range}

  qth_planet_rows = [intra_transition_probabilities[q] + exit_probabilities[q] for q in planet_range]

  qth_planet_list = {q:qth_planet_rows[q - 2] for q in planet_range}
  # Useful for figuring out the row corresponding to q planets, not used in code

  probability_matrix = qth_planet_rows + [extinction_row,
                                          survival_row,
                                          preindustrial_row,
                                          industrial_row,
                                          perils_row,
                                          interstellar_row]

  numbers = [f"{num}" for num in planet_range]
  return MarkovChain(probability_matrix, list(numbers)
                                         + ['Extinction',
                                           'Survival',
                                           'Preindustrial',
                                           'Industrial',
                                           'Perils',
                                           'Interstellar'])



