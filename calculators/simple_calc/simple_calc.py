from functools import cache
import pdb
from pydtmc import MarkovChain


# This script prints out a series of probabilities for transition becoming interstellar based on
# estimates of the transition probabilities of various(values are currently hardcoded placeholders)
# states, as in a Markov chain. The states are extinction, survival, preindustrial, industrial, time
# of perils, multiplanetary, and interstellar.
#
# A full description/explanation of the model is in the section titled The Cyclical Model in this
# post:
# https://forum.effectivealtruism.org/posts/YnBwoNNqe6knBJH8p/modelling-civilisation-after-a-catastrophe#The_cyclical_model
#
# These values are all placeholders. Add your own, and see what happens.

# TODO Might want this model to still have two ToP-states - the current one, and all future ones

# Transition probabilities

# From survival

# if False:
#   raise InvalidTransitionProbabilities("Transition probabilities from multiplanetary must == 1")

def extinction_given_survival():
  return 0

def preindustrial_given_survival():
  return 1 - extinction_given_survival()

# From preindustrial

def extinction_given_preindustrial():
  return 0

def industrial_given_preindustrial():
  return 1 - extinction_given_preindustrial()


# From industrial

def extinction_given_industrial():
  return 1/2

def perils_given_industrial():
  return 1 - extinction_given_industrial()

# From perils

def extinction_given_perils():
  return 1/6

def survival_given_perils():
  return 2/6

def preindustrial_given_perils():
  return 0

def industrial_given_perils():
  return 0

def multiplanetary_given_perils():
  return 2/6

def interstellar_given_perils():
  return 1 - (extinction_given_perils()
              + survival_given_perils()
              + preindustrial_given_perils()
              + industrial_given_perils()
              + multiplanetary_given_perils())

# From mutiplanetary

def extinction_given_multiplanetary():
  return 1/6

def survival_given_multiplanetary():
  return 1/6

def preindustrial_given_multiplanetary():
  return 0

def industrial_given_multiplanetary():
  return 0

def perils_given_multiplanetary():
  return 1/6

def interstellar_given_multiplanetary():
  return 1 - (extinction_given_multiplanetary()
              + survival_given_multiplanetary()
              + preindustrial_given_multiplanetary()
              + industrial_given_multiplanetary()
              + perils_given_multiplanetary())

@cache
def markov_chain():
  extinction_transition_probabilities =     [1, 0, 0, 0, 0, 0, 0]
  survival_transition_probabilities =       [extinction_given_survival(),
                                             0,
                                             preindustrial_given_survival(),
                                             0,
                                             0,
                                             0,
                                             0]
  preindustrial_transition_probabilities =  [extinction_given_preindustrial(),
                                             0,
                                             0,
                                             industrial_given_preindustrial(),
                                             0,
                                             0,
                                             0]
  industrial_transition_probabilities =     [extinction_given_industrial(),
                                             0,
                                             0,
                                             0,
                                             perils_given_industrial(),
                                             0,
                                             0]
  perils_transition_probabilties =          [extinction_given_perils(),
                                             survival_given_perils(),
                                             preindustrial_given_perils(),
                                             industrial_given_perils(),
                                             0,
                                             multiplanetary_given_perils(),
                                             interstellar_given_perils()]
  multiplanetary_transition_probabilities = [extinction_given_multiplanetary(),
                                             survival_given_multiplanetary(),
                                             preindustrial_given_multiplanetary(),
                                             industrial_given_multiplanetary(),
                                             perils_given_multiplanetary(),
                                             0,
                                             interstellar_given_multiplanetary()]
  interstellar_transition_probabilities =   [0, 0, 0, 0, 0, 0, 1]

  transition_probability_matrix = [extinction_transition_probabilities,
                                   survival_transition_probabilities,
                                   preindustrial_transition_probabilities,
                                   industrial_transition_probabilities,
                                   perils_transition_probabilties,
                                   multiplanetary_transition_probabilities,
                                   interstellar_transition_probabilities]

  # mini = [[0.2, 0.7, 0.0, 0.1], [0.0, 0.6, 0.3, 0.1], [0.0, 0.0, 1.0, 0.0], [0.5, 0.0, 0.5, 0.0]]
  # mc = MarkovChain(mini, ['A', 'B', 'C', 'D'])

  return MarkovChain(transition_probability_matrix, ['Extinction',
                                                   'Survival',
                                                   'Preindustrial',
                                                   'Industrial',
                                                   'Perils',
                                                   'Multiplanetary',
                                                   'Interstellar'])

  # Shortcuts for the probability of direct-path transitions

def probability_of_preindustrial_to_perils_directly():
  return industrial_given_preindustrial() * perils_given_industrial()

def probability_of_survival_to_perils_directly():
  return preindustrial_given_survival() * probability_of_preindustrial_to_perils_directly()

def net_interstellar_from_survival():
  return markov_chain().absorption_probabilities()[1][0]

def net_interstellar_from_preindustrial():
  return markov_chain().absorption_probabilities()[1][1]

def net_interstellar_from_industrial():
  return markov_chain().absorption_probabilities()[1][2]

def net_interstellar_from_perils():
  return markov_chain().absorption_probabilities()[1][3]

def net_interstellar_from_multiplanetary():
  return markov_chain().absorption_probabilities()[1][4]

def total_probability_of_non_extinction_milestone_regression_from_perils():
  return survival_given_perils() + preindustrial_given_perils() + industrial_given_perils()

def weighted_net_interstellar_from_unspecified_regress():
  return ((net_interstellar_from_survival() * survival_given_perils())
           + (net_interstellar_from_preindustrial() * preindustrial_given_perils())
           + (net_interstellar_from_industrial() * industrial_given_perils())
              / total_probability_of_non_extinction_milestone_regression_from_perils())


# print(f"""On your assumptions...
# Probability of becoming interstellar from survival = {net_interstellar_from_survival()}
# Probability of becoming interstellar from preindustrial = {net_interstellar_from_preindustrial()}
# Probability of becoming interstellar from industrial = {net_interstellar_from_industrial()}
# Probability of becoming interstellar from perils = {net_interstellar_from_perils()}
# Probability of becoming interstellar from multiplanetary = {net_interstellar_from_multiplanetary()}

# *****

# Therefore, if we assume that becoming interstellar is the only concern...
# a castatrophe that put us into a survival state would reduce our chance of becoming interstellar by {(net_interstellar_from_perils() - net_interstellar_from_survival()) / net_interstellar_from_perils() * 100}%
# a castatrophe that put us into a preindustrial state would reduce our chance of becoming interstellar by {(net_interstellar_from_perils() - net_interstellar_from_preindustrial()) / net_interstellar_from_perils() * 100}%
# a castatrophe that put us into an industrial state would reduce our chance of becoming interstellar by {(net_interstellar_from_perils() - net_interstellar_from_industrial()) / net_interstellar_from_perils() * 100}%
# and if we reached a multiplanetary state, it would increase our chance of becoming interstellar by {(net_interstellar_from_multiplanetary() - net_interstellar_from_perils()) / net_interstellar_from_perils() * 100}%
# """)

















