import pdb

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
  pass

def extinction_given_survival():
  return 0.1

def preindustrial_given_survival():
  return 0.9

if not extinction_given_survival() + preindustrial_given_survival() == 1:
  raise InvalidTransitionProbabilities("Transition probabilities from survival must == 1")



def extinction_given_preindustrial():
  return 0.1

def industrial_given_preindustrial():
  return 0.9

if not extinction_given_preindustrial() + industrial_given_preindustrial() == 1:
  raise InvalidTransitionProbabilities("Transition probabilities from preindustrial must == 1")



def extinction_given_industrial():
  return 0.1

def perils_given_industrial():
  return 0.9

if not extinction_given_industrial() + perils_given_industrial() == 1:
  raise InvalidTransitionProbabilities("Transition probabilities from industrial must == 1")



def extinction_given_perils():
  return 0.1

def survival_given_perils():
  return 0.1

def preindustrial_given_perils():
  return 0.1

def industrial_given_perils():
  return 0.1

def multiplanetary_given_perils():
  return 0.5

def interstellar_given_perils():
  return 0.1

if not extinction_given_perils() + survival_given_perils() + preindustrial_given_perils() + industrial_given_perils() + multiplanetary_given_perils() + interstellar_given_perils() == 1:
  raise InvalidTransitionProbabilities("Transition probabilities from perils must == 1")



def extinction_given_multiplanetary():
  return 0.1

def survival_given_multiplanetary():
  return 0.1

def preindustrial_given_multiplanetary():
  return 0.1

def industrial_given_multiplanetary():
  return 0.1

def perils_given_multiplanetary():
  return 0.1

def interstellar_given_multiplanetary():
  return 0.5

if not extinction_given_multiplanetary() + survival_given_multiplanetary() + preindustrial_given_multiplanetary() + industrial_given_multiplanetary() + perils_given_multiplanetary() + interstellar_given_multiplanetary() == 1:
  raise InvalidTransitionProbabilities("Transition probabilities from multiplanetary must == 1")


# Shortcuts for the probability of direct-path transitions

probability_of_industrial_to_perils_directly = perils_given_industrial()
probability_of_preindustrial_to_perils_directly = industrial_given_preindustrial() * probability_of_industrial_to_perils_directly
probability_of_survival_to_perils_directly = preindustrial_given_survival() * probability_of_preindustrial_to_perils_directly


# Calculated absorbtion probabilities from the different starting states (see working in calculations.md)

probability_of_interstellar_from_extinction = 0
probability_of_interstellar_from_interstellar = 1
probability_of_interstellar_from_perils = (interstellar_given_perils() + multiplanetary_given_perils() * interstellar_given_multiplanetary()) / (
                                           1 - (survival_given_perils() * probability_of_survival_to_perils_directly
                                                + preindustrial_given_perils() * probability_of_preindustrial_to_perils_directly
                                                + industrial_given_perils() * probability_of_preindustrial_to_perils_directly
                                                + multiplanetary_given_perils() * (survival_given_multiplanetary() * probability_of_survival_to_perils_directly
                                                                                   + preindustrial_given_multiplanetary() * probability_of_preindustrial_to_perils_directly
                                                                                   + industrial_given_multiplanetary() * probability_of_industrial_to_perils_directly
                                                                                   + perils_given_multiplanetary())))
probability_of_interstellar_from_survival = probability_of_survival_to_perils_directly * probability_of_interstellar_from_perils
probability_of_interstellar_from_industrial = probability_of_industrial_to_perils_directly * probability_of_interstellar_from_perils
probability_of_interstellar_from_preindustrial = probability_of_preindustrial_to_perils_directly * probability_of_interstellar_from_perils
probability_of_interstellar_from_multiplanetary = (survival_given_multiplanetary() * probability_of_interstellar_from_survival
                                                   + preindustrial_given_multiplanetary() * probability_of_interstellar_from_preindustrial
                                                   + industrial_given_multiplanetary() * probability_of_interstellar_from_industrial
                                                   + perils_given_multiplanetary() * probability_of_interstellar_from_perils
                                                   + interstellar_given_multiplanetary())


print(f"""
Probability of becoming interstellar from extinction = {probability_of_interstellar_from_extinction}
Probability of becoming interstellar from survival = {probability_of_interstellar_from_survival}
Probability of becoming interstellar from preindustrial = {probability_of_interstellar_from_preindustrial}
Probability of becoming interstellar from industrial = {probability_of_interstellar_from_industrial}
Probability of becoming interstellar from perils = {probability_of_interstellar_from_perils}
Probability of becoming interstellar from multiplanetary = {probability_of_interstellar_from_multiplanetary}
Probability of becoming interstellar from interstellar = {probability_of_interstellar_from_interstellar}

Differences in probability from perils...
... for survival = {probability_of_interstellar_from_perils - probability_of_interstellar_from_survival}
... for preindustrial = {probability_of_interstellar_from_perils - probability_of_interstellar_from_preindustrial}
... for industrial = {probability_of_interstellar_from_perils - probability_of_interstellar_from_industrial}
""")


