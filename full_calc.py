import pdb

from pydtmc import MarkovChain

import constant
import multiplanetary
import perils
import preperils


def intra_perils_markov_chain(k):
  extinction_probililities =     [1,0,0,0,0,0] + [0] * constant.MAX_PROGRESS_YEARS
  survival_probabilities =       [0,1,0,0,0,0] + [0] * constant.MAX_PROGRESS_YEARS
  preindustrial_probabilities =  [0,0,1,0,0,0] + [0] * constant.MAX_PROGRESS_YEARS
  industrial_probabilities =     [0,0,0,1,0,0] + [0] * constant.MAX_PROGRESS_YEARS
  multiplanetary_probabilities = [0,0,0,0,1,0] + [0] * constant.MAX_PROGRESS_YEARS
  interstellar_probabilities =   [0,0,0,0,0,1] + [0] * constant.MAX_PROGRESS_YEARS
  year_range = range(0, constant.MAX_PROGRESS_YEARS)

  exit_probabilities = {p:[perils.extinction_given_perils(k, p),
                        perils.survival_given_perils(k, p),
                        perils.preindustrial_given_perils(k, p),
                        perils.industrial_given_perils(k, p),
                        perils.multiplanetary_given_perils(k, p),
                        perils.interstellar_given_perils(k, p)] for p in year_range}

  intra_transition_probabilities = {p:[perils.transition_to_year_n_given_perils(k, p, n) for n in year_range]
                                    for p in year_range}

  year_p_probabilities = [exit_probabilities[p] + intra_transition_probabilities[p] for p in year_range]

  probability_matrix = year_p_probabilities + [extinction_probililities,
                                               survival_probabilities,
                                               preindustrial_probabilities,
                                               industrial_probabilities,
                                               multiplanetary_probabilities,
                                               interstellar_probabilities]

  pdb.set_trace()

  return MarkovChain(probability_matrix, list(year_range)
                                         + ['Extinction',
                                           'Survival',
                                           'Preindustrial',
                                           'Industrial',
                                           'Perils',
                                           'Interstellar'])

def intra_multiplanetary_markov_chain(k):
  extinction_probililities =     [0] * (constant.MAX_PLANETS - 1) + [1,0,0,0,0,0]
  survival_probabilities =       [0] * (constant.MAX_PLANETS - 1) + [0,1,0,0,0,0]
  preindustrial_probabilities =  [0] * (constant.MAX_PLANETS - 1) + [0,0,1,0,0,0]
  industrial_probabilities =     [0] * (constant.MAX_PLANETS - 1) + [0,0,0,1,0,0]
  perils_probabilities =         [0] * (constant.MAX_PLANETS - 1) + [0,0,0,0,1,0]
  interstellar_probabilities =   [0] * (constant.MAX_PLANETS - 1) + [0,0,0,0,0,1]
  planet_range = range(2, constant.MAX_PLANETS + 1) # Python range excludes max value

  intra_transition_probabilities = {q:[multiplanetary.transition_to_n_planets_given_multiplanetary(k, q, n) for n in planet_range]
                                    for q in planet_range}
  exit_probabilities = {q:[multiplanetary.extinction_given_multiplanetary(k,q),
                        multiplanetary.survival_given_multiplanetary(k,q),
                        multiplanetary.preindustrial_given_multiplanetary(k,q),
                        multiplanetary.industrial_given_multiplanetary(k,q),
                        multiplanetary.perils_given_multiplanetary(k,q),
                        multiplanetary.interstellar_given_multiplanetary(k,q)] for q in planet_range}

  qth_planet_probabilities = [intra_transition_probabilities[q] + exit_probabilities[q] for q in planet_range]

  qth_planet_list = {q:qth_planet_probabilities[q - 2] for q in planet_range}
  # Useful for figuring out the row corresponding to q planets, not used in code

  probability_matrix = qth_planet_probabilities + [extinction_probililities,
                                                   survival_probabilities,
                                                   preindustrial_probabilities,
                                                   industrial_probabilities,
                                                   perils_probabilities,
                                                   interstellar_probabilities]

  numbers = [f"{num}" for num in planet_range]
  return MarkovChain(probability_matrix, list(numbers)
                                         + ['Extinction',
                                           'Survival',
                                           'Preindustrial',
                                           'Industrial',
                                           'Perils',
                                           'Interstellar'])

intra_perils_markov_chain(1)

########

# def extinction_transition_probabilities(k=0):
#   return [1, 0, 0, 0, 0, 0, 0]

# def survival_transition_probabilities(k):
#   return [extinction_given_survival(k),
#           0,
#           preindustrial_given_survival(k),
#           0,
#           0,
#           0,
#           0]

# def preindustrial_transition_probabilities(k):
#   return [extinction_given_preindustrial(k),
#           0,
#           0,
#           industrial_given_preindustrial(k),
#           0,
#           0,
#           0]

# def industrial_transition_probabilities(k):
#   return [extinction_given_industrial(k),
#           0,
#           0,
#           0,
#           perils_given_industrial(k),
#           0,
#           0]

# def perils_transition_probabilities(k):
#   return [extinction_given_perils(k),
#           survival_given_perils(k),
#           preindustrial_given_perils(k),
#           industrial_given_perils(k),
#           0,
#           multiplanetary_given_perils(k),
#           interstellar_given_perils(k)]

# def multiplanetary_transition_probabilities(k):
#   return [extinction_given_multiplanetary(k),
#           survival_given_multiplanetary(k),
#           preindustrial_given_multiplanetary(k),
#           industrial_given_multiplanetary(k),
#           perils_given_multiplanetary(k),
#           0,
#           interstellar_given_multiplanetary(k)]

# def interstellar_transition_probabilities(k=0):
#   return [0, 0, 0, 0, 0, 0, 1]

# Planets transition matrix
# [extinction_given_multiplanetary(k, q) for q in range(2, constant.MAX_PLANETS)]
# [survival_given_multiplanetary(k, q) for q in range(2, constant.MAX_PLANETS)]
# [preindustrial_given_multiplanetary(k, q) for q in range (2, constant.MAX_PLANETS)]
# [industrial_given_multiplanetary(k, q) for q in range(2, constant.MAX_PLANETS)]
# [perils_given_multiplanetary(k, q) for q in range(2, constant.MAX_PLANETS)]
# [0 for q in range(2, constant.MAX_PLANETS)]
# # [transition_to_n_planets_given_multiplanetary(k, q, n)]
# [industrial_given_multiplanetary(k, q) for q in range(2, constant.MAX_PLANETS)]


