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


# Transition probabilities

class InvalidTransitionProbabilities(Exception):
  pass


extinction_given_survival = 0.001
preindustrial_given_survival = 1 - extinction_given_survival

if not extinction_given_survival + preindustrial_given_survival == 1:
  raise InvalidTransitionProbabilities("Transition probabilities from survival must == 1")


extinction_given_preindustrial = 0.3
industrial_given_preindustrial = 1 - extinction_given_preindustrial

if not extinction_given_preindustrial + industrial_given_preindustrial == 1:
  raise InvalidTransitionProbabilities("Transition probabilities from preindustrial must == 1")


extinction_given_industrial = 0.1
perils_given_industrial = 1 - extinction_given_industrial

if not extinction_given_industrial + perils_given_industrial == 1:
  raise InvalidTransitionProbabilities("Transition probabilities from industrial must == 1")


extinction_given_perils = 0.1
survival_given_perils = 0.01
preindustrial_given_perils = 0.1
industrial_given_perils = 0.15
multiplanetary_given_perils = 0.6
interstellar_given_perils = 1 - (extinction_given_perils
                                 + survival_given_perils
                                 + preindustrial_given_perils
                                 + industrial_given_perils
                                 + multiplanetary_given_perils)

if not (extinction_given_perils
        + survival_given_perils
        + preindustrial_given_perils
        + industrial_given_perils
        + multiplanetary_given_perils
        + interstellar_given_perils
        == 1):
  raise InvalidTransitionProbabilities("Transition probabilities from perils must == 1")


extinction_given_multiplanetary = 0.08
survival_given_multiplanetary = 0.0001
preindustrial_given_multiplanetary = 0.01
industrial_given_multiplanetary = 0.05
perils_given_multiplanetary = 0.4
interstellar_given_multiplanetary = 1 - (extinction_given_multiplanetary
                                         + survival_given_multiplanetary
                                         + preindustrial_given_multiplanetary
                                         + industrial_given_multiplanetary
                                         + perils_given_multiplanetary)

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

mc = MarkovChain(transition_probability_matrix, ['Extinction',
                                                 'Survival',
                                                 'Preindustrial',
                                                 'Industrial',
                                                 'Perils',
                                                 'Multiplanetary',
                                                 'Interstellar'])

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

# # TODO find out why these produce different values

total_probability_of_non_extinction_milestone_regression_from_perils = survival_given_perils + preindustrial_given_perils + industrial_given_perils

# print(f"""
# Probability of becoming interstellar from extinction = {probability_of_interstellar_from_extinction}, {mc.hitting_probabilities([6])[0]}
# Probability of becoming interstellar from survival = {probability_of_interstellar_from_survival}, {mc.hitting_probabilities([6])[1]}
# Probability of becoming interstellar from preindustrial = {probability_of_interstellar_from_preindustrial}, {mc.hitting_probabilities([6])[2]}
# Probability of becoming interstellar from industrial = {probability_of_interstellar_from_industrial}, {mc.hitting_probabilities([6])[3]}
# Probability of becoming interstellar from perils = {probability_of_interstellar_from_perils}, {mc.hitting_probabilities([6])[4]}
# Probability of becoming interstellar from multiplanetary = {probability_of_interstellar_from_multiplanetary}, {mc.hitting_probabilities([6])[5]}
# Probability of becoming interstellar from interstellar = {probability_of_interstellar_from_interstellar}, {mc.hitting_probabilities([6])[6]}
# """)




print(f"""On your assumptions...
Probability of becoming interstellar from extinction = {mc.hitting_probabilities([6])[0]}
Probability of becoming interstellar from survival = {mc.hitting_probabilities([6])[1]}
Probability of becoming interstellar from preindustrial = {mc.hitting_probabilities([6])[2]}
Probability of becoming interstellar from industrial = {mc.hitting_probabilities([6])[3]}
Probability of becoming interstellar from perils = {mc.hitting_probabilities([6])[4]}
Probability of becoming interstellar from multiplanetary = {mc.hitting_probabilities([6])[5]}
Probability of becoming interstellar from interstellar = {mc.hitting_probabilities([6])[6]}

*****

Therefore, if we assume that becoming interstellar is the only concern...
a castatrophe that put us into a survival state would be {mc.hitting_probabilities([6])[4] - mc.hitting_probabilities([6])[1]} * as bad as extinction
a castatrophe that put us into a preindustrial state would be {mc.hitting_probabilities([6])[4] - mc.hitting_probabilities([6])[2]} * as bad as extinction
a castatrophe that put us into an industrial state would be {mc.hitting_probabilities([6])[4] - mc.hitting_probabilities([6])[3]} * as bad as extinction
a castatrophe that caused a milestone regression to one of the above states, weighted by the probability you've put on each, would be {mc.hitting_probabilities([6])[4]
                                              - mc.hitting_probabilities([6])[1] * survival_given_perils / total_probability_of_non_extinction_milestone_regression_from_perils
                                              - mc.hitting_probabilities([6])[2] * preindustrial_given_perils / total_probability_of_non_extinction_milestone_regression_from_perils
                                              - mc.hitting_probabilities([6])[3] * industrial_given_perils / total_probability_of_non_extinction_milestone_regression_from_perils} * as bad as extinction
and if we reached a multiplanetary state, the probability of extinction before becoming interstellar would decrease by {(mc.hitting_probabilities([6])[5] - mc.hitting_probabilities([6])[4])}%
""")


pdb.set_trace()
