import pdb

from pydtmc import MarkovChain

import constant
import preperils_transition_probabilities
import perils_transition_probabilities
from multiplanetary_transition_probabilities import (extinction_given_multiplanetary,
                                                    survival_given_multiplanetary,
                                                    preindustrial_given_multiplanetary,
                                                    industrial_given_multiplanetary,
                                                    perils_given_multiplanetary,
                                                    interstellar_given_multiplanetary,
                                                    transition_to_n_planets_given_multiplanetary)


# def intra_perils_markov_chain(k):
#   extinction_probililities =     [1,0,0,0,0,0] + [0] * constant.MAX_PROGRESS_YEARS
#   survival_probabilities =       [0,1,0,0,0,0] + [0] * constant.MAX_PROGRESS_YEARS
#   preindustrial_probabilities =  [0,0,1,0,0,0] + [0] * constant.MAX_PROGRESS_YEARS
#   industrial_probabilities =     [0,0,0,1,0,0] + [0] * constant.MAX_PROGRESS_YEARS
#   multiplanetary_probabilities = [0,0,0,0,1,0] + [0] * constant.MAX_PROGRESS_YEARS
#   interstellar_probabilities =   [0,0,0,0,0,1] + [0] * constant.MAX_PROGRESS_YEARS
#   year_range = range(0, constant.MAX_PROGRESS_YEARS)

#   exit_probabilities = {p:[extinction_given_perils(k, p),
#                         survival_given_perils(k, p),
#                         preindustrial_given_perils(k, p),
#                         industrial_given_perils(k, p),
#                         perils_given_perils(k, p),
#                         interstellar_given_perils(k, p)] for p in year_range}

#   intra_transition_probabilities = {p:[transition_to_year_n_given_perils(k, p, n) for n in year_range]
#                                     for p in year_range}

#   year_p_probabilities = [exit_probabilities[p] + intra_transition_probabilities[p] for p in year_range]

#   probability_matrix = [extinction_probililities,
#           survival_probabilities,
#           preindustrial_probabilities,
#           industrial_probabilities,
#           perils_probabilities,
#           interstellar_probabilities] + year_p_probabilities

#   return MarkovChain(probability_matrix,
#                      ['Extinction',
#                      'Survival',
#                      'Preindustrial',
#                      'Industrial',
#                      'Perils',
#                      'Interstellar'] + list(year_range))

def intra_multiplanetary_markov_chain(k):
  extinction_probililities =     [1,0,0,0,0,0] + [0] * (constant.MAX_PLANETS - 1)
  survival_probabilities =       [0,1,0,0,0,0] + [0] * (constant.MAX_PLANETS - 1)
  preindustrial_probabilities =  [0,0,1,0,0,0] + [0] * (constant.MAX_PLANETS - 1)
  industrial_probabilities =     [0,0,0,1,0,0] + [0] * (constant.MAX_PLANETS - 1)
  perils_probabilities =         [0,0,0,0,1,0] + [0] * (constant.MAX_PLANETS - 1)
  interstellar_probabilities =   [0,0,0,0,0,1] + [0] * (constant.MAX_PLANETS - 1)
  planet_range = range(2, constant.MAX_PLANETS)

  exit_probabilities = {q:[extinction_given_multiplanetary(k,q),
                        survival_given_multiplanetary(k,q),
                        preindustrial_given_multiplanetary(k,q),
                        industrial_given_multiplanetary(k,q),
                        perils_given_multiplanetary(k,q),
                        interstellar_given_multiplanetary(k,q)] for q in planet_range}

  intra_transition_probabilities = {q:[transition_to_n_planets_given_multiplanetary(k, q, n) for n in planet_range]
                                    for q in planet_range}

  q_planet_probabilities = [exit_probabilities[q] + intra_transition_probabilities[q] for q in planet_range]

  probability_matrix = [extinction_probililities,
          survival_probabilities,
          preindustrial_probabilities,
          industrial_probabilities,
          perils_probabilities,
          interstellar_probabilities] + q_planet_probabilities

  pdb.set_trace()
  return MarkovChain(probability_matrix,
                     ['Extinction',
                     'Survival',
                     'Preindustrial',
                     'Industrial',
                     'Perils',
                     'Interstellar'] + list(planet_range))

intra_multiplanetary_markov_chain(1)

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


