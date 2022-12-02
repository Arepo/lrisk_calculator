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


# Transition probabilities

class InvalidTransitionProbabilities(Exception):
  pass

extinction_given_survival = 0.1
preindustrial_given_survival = 0.9

if not extinction_given_survival + preindustrial_given_survival == 1:
  raise InvalidTransitionProbabilities("Transition probabilities from survival must == 1")


extinction_given_preindustrial = 0.1
industrial_given_preindustrial = 0.9

if not extinction_given_preindustrial + industrial_given_preindustrial == 1:
  raise InvalidTransitionProbabilities("Transition probabilities from preindustrial must == 1")


extinction_given_industrial = 0.1
perils_given_industrial = 0.9

if not extinction_given_industrial + perils_given_industrial == 1:
  raise InvalidTransitionProbabilities("Transition probabilities from industrial must == 1")


extinction_given_perils = 0.1
survival_given_perils = 0.1
preindustrial_given_perils = 0.1
industrial_given_perils = 0.1
multiplanetary_given_perils = 0.5
interstellar_given_perils = 0.1

if not (extinction_given_perils
        + survival_given_perils
        + preindustrial_given_perils
        + industrial_given_perils
        + multiplanetary_given_perils
        + interstellar_given_perils
        == 1):
  raise InvalidTransitionProbabilities("Transition probabilities from perils must == 1")


extinction_given_multiplanetary = 0.1
survival_given_multiplanetary = 0.1
preindustrial_given_multiplanetary = 0.1
industrial_given_multiplanetary = 0.1
perils_given_multiplanetary = 0.1
interstellar_given_multiplanetary = 0.5

if not (extinction_given_multiplanetary
        + survival_given_multiplanetary
        + preindustrial_given_multiplanetary
        + industrial_given_multiplanetary
        + perils_given_multiplanetary
        + interstellar_given_multiplanetary
        == 1):
  raise InvalidTransitionProbabilities("Transition probabilities from multiplanetary must == 1")


extinction_transition_probabilities =     [1, 0, 0, 0, 0, 0, 0]
survival_transition_probabilities =       [extinction_given_survival,
                                           0,
                                           preindustrial_given_survival,
                                           0,
                                           0,
                                           0,
                                           0]
preindustrial_transition_probabilities =  [extinction_given_preindustrial,
                                           0,
                                           0,
                                           industrial_given_preindustrial,
                                           0,
                                           0,
                                           0]
industrial_transition_probabilities =     [extinction_given_industrial,
                                           0,
                                           0,
                                           0,
                                           perils_given_industrial,
                                           0,
                                           0]
perils_transition_probabilties =          [extinction_given_perils,
                                           survival_given_perils,
                                           preindustrial_given_perils,
                                           industrial_given_perils,
                                           0,
                                           multiplanetary_given_perils,
                                           interstellar_given_perils]
multiplanetary_transition_probabilities = [extinction_given_multiplanetary,
                                           survival_given_multiplanetary,
                                           preindustrial_given_multiplanetary,
                                           industrial_given_multiplanetary,
                                           perils_given_multiplanetary,
                                           0,
                                           interstellar_given_multiplanetary]
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

# pdb.set_trace()
mc = MarkovChain(transition_probability_matrix, ['Extinction',
                                                 'Survival',
                                                 'Preindustrial',
                                                 'Industrial',
                                                 'Perils',
                                                 'Multiplanetary',
                                                 'Interstellar'])

# pdb.set_trace()
# Shortcuts for the probability of direct-path transitions

probability_of_industrial_to_perils_directly = perils_given_industrial
probability_of_preindustrial_to_perils_directly = industrial_given_preindustrial * probability_of_industrial_to_perils_directly
probability_of_survival_to_perils_directly = preindustrial_given_survival * probability_of_preindustrial_to_perils_directly


# Calculated absorbtion probabilities from the different starting states (see working in calculations.md)

# probability_of_interstellar_from_extinction = 0
# probability_of_interstellar_from_interstellar = 1
# probability_of_interstellar_from_perils = (interstellar_given_perils + multiplanetary_given_perils * interstellar_given_multiplanetary) / (
#                                            1 - (survival_given_perils * probability_of_survival_to_perils_directly
#                                                 + preindustrial_given_perils * probability_of_preindustrial_to_perils_directly
#                                                 + industrial_given_perils * probability_of_preindustrial_to_perils_directly
#                                                 + multiplanetary_given_perils * (survival_given_multiplanetary * probability_of_survival_to_perils_directly
#                                                                                    + preindustrial_given_multiplanetary * probability_of_preindustrial_to_perils_directly
#                                                                                    + industrial_given_multiplanetary * probability_of_industrial_to_perils_directly
#                                                                                    + perils_given_multiplanetary)))
# probability_of_interstellar_from_survival = probability_of_survival_to_perils_directly * probability_of_interstellar_from_perils
# probability_of_interstellar_from_industrial = probability_of_industrial_to_perils_directly * probability_of_interstellar_from_perils
# probability_of_interstellar_from_preindustrial = probability_of_preindustrial_to_perils_directly * probability_of_interstellar_from_perils
# probability_of_interstellar_from_multiplanetary = (survival_given_multiplanetary * probability_of_interstellar_from_survival
#                                                    + preindustrial_given_multiplanetary * probability_of_interstellar_from_preindustrial
#                                                    + industrial_given_multiplanetary * probability_of_interstellar_from_industrial
#                                                    + perils_given_multiplanetary * probability_of_interstellar_from_perils
#                                                    + interstellar_given_multiplanetary)

# TODO find out why these produce different values

print(f"""
Probability of becoming interstellar from extinction = {probability_of_interstellar_from_extinction}, {mc.hitting_probabilities([6])[0]}
Probability of becoming interstellar from survival = {probability_of_interstellar_from_survival}, {mc.hitting_probabilities([6])[1]}
Probability of becoming interstellar from preindustrial = {probability_of_interstellar_from_preindustrial}, {mc.hitting_probabilities([6])[2]}
Probability of becoming interstellar from industrial = {probability_of_interstellar_from_industrial}, {mc.hitting_probabilities([6])[3]}
Probability of becoming interstellar from perils = {probability_of_interstellar_from_perils}, {mc.hitting_probabilities([6])[4]}
Probability of becoming interstellar from multiplanetary = {probability_of_interstellar_from_multiplanetary}, {mc.hitting_probabilities([6])[5]}
Probability of becoming interstellar from interstellar = {probability_of_interstellar_from_interstellar}, {mc.hitting_probabilities([6])[6]}

Differences in probability from perils...
... for survival = {probability_of_interstellar_from_perils - probability_of_interstellar_from_survival}
... for preindustrial = {probability_of_interstellar_from_perils - probability_of_interstellar_from_preindustrial}
... for industrial = {probability_of_interstellar_from_perils - probability_of_interstellar_from_industrial}
""")

# print(f"""
# Probability of becoming interstellar from extinction = {mc.hitting_probabilities([6])[0]}
# Probability of becoming interstellar from survival = {mc.hitting_probabilities([6])[1]}
# Probability of becoming interstellar from preindustrial = {mc.hitting_probabilities([6])[2]}
# Probability of becoming interstellar from industrial = {mc.hitting_probabilities([6])[3]}
# Probability of becoming interstellar from perils = {mc.hitting_probabilities([6])[4]}
# Probability of becoming interstellar from multiplanetary = {mc.hitting_probabilities([6])[5]}
# Probability of becoming interstellar from interstellar = {mc.hitting_probabilities([6])[6]}

# Differences in probability from perils...
# ... for survival = { mc.hitting_probabilities([6])[4] - mc.hitting_probabilities([6])[1]}
# ... for preindustrial = {mc.hitting_probabilities([6])[4] - mc.hitting_probabilities([6])[2]}
# ... for industrial = {mc.hitting_probabilities([6])[4] - mc.hitting_probabilities([6])[3]}
# ... for multiplanetary = {mc.hitting_probabilities([6])[5] - mc.hitting_probabilities([6])[4]}
# """)
