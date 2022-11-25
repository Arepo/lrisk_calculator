import pdb

# wibble

# Transition probabilities

class InvalidTransitionProbabilities(Exception):
  pass


def survival_to_extinction():
  return 0.5

def survival_to_preindustrial():
  return 0.5

if not survival_to_extinction() + survival_to_preindustrial() == 1:
  raise InvalidTransitionProbabilities("Transition probabilities from survival must == 1")



def preindustrial_to_extinction():
  return 0.01

def preindustrial_to_industrial():
  return 0.99

if not preindustrial_to_extinction() + preindustrial_to_industrial() == 1:
  raise InvalidTransitionProbabilities("Transition probabilities from preindustrial must == 1")



def industrial_to_extinction():
  return 0.01

def industrial_to_perils():
  return 0.99

if not industrial_to_extinction() + industrial_to_perils() == 1:
  raise InvalidTransitionProbabilities("Transition probabilities from industrial must == 1")



def perils_to_extinction():
  return 0.1

def perils_to_survival():
  return 0.1

def perils_to_preindustrial():
  return 0.1

def perils_to_industrial():
  return 0.1

def perils_to_multiplanetary():
  return 0.5

def perils_to_interstellar():
  return 0.1

if not perils_to_extinction() + perils_to_survival() + perils_to_preindustrial() + perils_to_industrial() + perils_to_multiplanetary() + perils_to_interstellar() == 1:
  raise InvalidTransitionProbabilities("Transition probabilities from perils must == 1")



def multiplanetary_to_extinction():
  return 0.1

def multiplanetary_to_survival():
  return 0.1

def multiplanetary_to_preindustrial():
  return 0.1

def multiplanetary_to_industrial():
  return 0.1

def multiplanetary_to_perils():
  return 0.1

def multiplanetary_to_interstellar():
  return 0.5

if not multiplanetary_to_extinction() + multiplanetary_to_survival() + multiplanetary_to_preindustrial() + multiplanetary_to_industrial() + multiplanetary_to_perils() + multiplanetary_to_interstellar() == 1:
  raise InvalidTransitionProbabilities("Transition probabilities from multiplanetary must == 1")



# Simplifying

preindustrial_to_perils = preindustrial_to_industrial() * industrial_to_perils()
survival_to_perils = survival_to_preindustrial() * preindustrial_to_perils

# pdb.set_trace()
print((perils_to_survival() * survival_to_perils
                                                                 + perils_to_preindustrial() * preindustrial_to_perils
                                                                 + perils_to_industrial() * industrial_to_perils()
                                                                 + perils_to_multiplanetary() * multiplanetary_to_survival() * survival_to_perils
                                                                 + perils_to_multiplanetary() * multiplanetary_to_preindustrial() * preindustrial_to_perils
                                                                 + perils_to_multiplanetary() * multiplanetary_to_industrial() * industrial_to_perils()
                                                                 + perils_to_multiplanetary() * multiplanetary_to_perils()
                                                                 + perils_to_multiplanetary() * multiplanetary_to_interstellar()))

probability_of_interstellar_from_perils = perils_to_interstellar() / (1 - (perils_to_survival() * survival_to_perils
                                                                 + perils_to_preindustrial() * preindustrial_to_perils
                                                                 + perils_to_industrial() * industrial_to_perils()
                                                                 + perils_to_multiplanetary() * multiplanetary_to_survival() * survival_to_perils
                                                                 + perils_to_multiplanetary() * multiplanetary_to_preindustrial() * preindustrial_to_perils
                                                                 + perils_to_multiplanetary() * multiplanetary_to_industrial() * industrial_to_perils()
                                                                 + perils_to_multiplanetary() * multiplanetary_to_perils()
                                                                 + perils_to_multiplanetary() * multiplanetary_to_interstellar()))

probability_of_interstellar_from_extinction = 0
probability_of_interstellar_from_survival = survival_to_perils * probability_of_interstellar_from_perils
probability_of_interstellar_from_preindustrial = preindustrial_to_perils * probability_of_interstellar_from_perils
probability_success_from_industrial = industrial_to_perils() * probability_of_interstellar_from_perils
probability_of_interstellar_from_multiplanetary = (multiplanetary_to_interstellar()
                                                   + probability_of_interstellar_from_perils * (multiplanetary_to_survival() * survival_to_perils
                                                                                                + multiplanetary_to_preindustrial() * preindustrial_to_perils
                                                                                                + multiplanetary_to_industrial() * industrial_to_perils()
                                                                                                + multiplanetary_to_perils()))
probability_of_interstellar_from_interstellar = 1


print(f"""
Probability of becoming interstellar from extinction = {probability_of_interstellar_from_extinction}
Probability of becoming interstellar from survival = {probability_of_interstellar_from_survival}
Probability of becoming interstellar from preindustrial = {probability_of_interstellar_from_preindustrial}
Probability of becoming interstellar from industrial = {probability_success_from_industrial}
Probability of becoming interstellar from perils = {probability_of_interstellar_from_perils}
Probability of becoming interstellar from multiplanetary = {probability_of_interstellar_from_multiplanetary}
Probability of becoming interstellar from interstellar = {probability_of_interstellar_from_interstellar}
""")


# class State:
#   def __init__(self, transition_probabilities: dict):
#     self.transition_probabilities = transition_probabilities
#     if transition_probabilities and not sum(transition_probabilities) == 1:
#       raise InconsistentProbabilityError("Transition probabilities must sum to 1")

#   def transition_probability(state: string) -> float:
#       if state in self.transition_probabilities:
#         return self.transition_probabilities[state]
#       else:
#         return 0

#   class InconsistentProbabilityError(Exception):
#     pass



# extinction = State({})
# survival = State({'extinction': survival_to_extinction(), 'preindustrial': survival_to_preindustrial()})
# preindustrial = State({'extinction': preindustrial_to_extinction(), 'industrial': preindustrial_to_industrial()})
# industrial = State({'extinction': industrial_to_extinction(), 'perils': industrial_to_perils()})
# perils = State({
#   'extinction': perils_to_extinction(),
#   'survival': perils_to_survival(),
#   'preindustrial':perils_to_preindustrial(),
#   'industrial': perils_to_industrial(),
#   'multiplanetary': perils_to_multiplanetary(),
#   'interstellar': perils_to_interstellar()})
# multiplanetary = State({
#   'extinction': multiplanetary_to_extinction(),
#   'survival': multiplanetary_to_survival(),
#   'preindustrial':multiplanetary_to_preindustrial(),
#   'industrial': multiplanetary_to_industrial(),
#   'perils': multiplanetary_to_perils(),
#   'interstellar': multiplanetary_to_interstellar()})
# interstellar = State({})

# Probabilities of absorbtion in interstellar

# a0 = 0
# a6 = survival_to_preindustrial() * preindustrial_to_industrial() * industrial_to_perils() * a3
# a1 = preindustrial_to_industrial() * industrial_to_perils() * a3
# a2 = industrial_to_perils() * a3
# a3 = perils_to_interstellar() / (1 - ( perils_to_survival() * survival_to_preindustrial() * preindustrial_to_industrial() * industrial_to_perils()
#    + perils_to_preindustrial() * preindustrial_to_industrial() * industrial_to_perils()
#    + perils_to_industrial() * industrial_to_perils()
#    + perils_to_multiplanetary() * multiplanetary_to_survival() * survival_to_preindustrial() * preindustrial_to_industrial() * industrial_to_perils()
#    + perils_to_multiplanetary() * multiplanetary_to_preindustrial() * preindustrial_to_industrial() * industrial_to_perils()
#    + perils_to_multiplanetary() * multiplanetary_to_industrial() * industrial_to_perils()
#    + perils_to_multiplanetary() * multiplanetary_to_perils()
#    + perils_to_multiplanetary() * multiplanetary_to_interstellar()))
# a4 = multiplanetary_to_interstellar() + (multiplanetary_to_survival() * survival_to_preindustrial() * preindustrial_to_industrial() * industrial_to_perils()
#                                          + multiplanetary_to_preindustrial() * preindustrial_to_industrial() * industrial_to_perils()
#                                          + multiplanetary_to_industrial() * industrial_to_perils()
#                                          + multiplanetary_to_perils()) * a3
# a5 = 1
# a6 = survival_to_preindustrial() * preindustrial_to_industrial() * industrial_to_perils() * a3


# A3 calculations
# a3 = perils_to_survival() * survival_to_preindustrial() * preindustrial_to_industrial() * industrial_to_perils() * a3
#    + perils_to_preindustrial() * preindustrial_to_industrial() * industrial_to_perils() * a3
#    + perils_to_industrial() * industrial_to_perils() * a3
#    + perils_to_multiplanetary() * multiplanetary_to_survival() * survival_to_preindustrial() * preindustrial_to_industrial() * industrial_to_perils() * a3
#    + perils_to_multiplanetary() * multiplanetary_to_preindustrial() * preindustrial_to_industrial() * industrial_to_perils() * a3
#    + perils_to_multiplanetary() * multiplanetary_to_industrial() * industrial_to_perils() * a3
#    + perils_to_multiplanetary() * multiplanetary_to_perils() * a3
#    + perils_to_multiplanetary() * multiplanetary_to_interstellar() * a3
#    + perils_to_interstellar()

# a3 = a3 * ( perils_to_survival() * survival_to_preindustrial() * preindustrial_to_industrial() * industrial_to_perils()
#    + perils_to_preindustrial() * preindustrial_to_industrial() * industrial_to_perils()
#    + perils_to_industrial() * industrial_to_perils()
#    + perils_to_multiplanetary() * multiplanetary_to_survival() * survival_to_preindustrial() * preindustrial_to_industrial() * industrial_to_perils()
#    + perils_to_multiplanetary() * multiplanetary_to_preindustrial() * preindustrial_to_industrial() * industrial_to_perils()
#    + perils_to_multiplanetary() * multiplanetary_to_industrial() * industrial_to_perils()
#    + perils_to_multiplanetary() * multiplanetary_to_perils()
#    + perils_to_multiplanetary() * multiplanetary_to_interstellar())
#    + perils_to_interstellar()


# a3 - a3 * ( perils_to_survival() * survival_to_preindustrial() * preindustrial_to_industrial() * industrial_to_perils()
#    + perils_to_preindustrial() * preindustrial_to_industrial() * industrial_to_perils()
#    + perils_to_industrial() * industrial_to_perils()
#    + perils_to_multiplanetary() * multiplanetary_to_survival() * survival_to_preindustrial() * preindustrial_to_industrial() * industrial_to_perils()
#    + perils_to_multiplanetary() * multiplanetary_to_preindustrial() * preindustrial_to_industrial() * industrial_to_perils()
#    + perils_to_multiplanetary() * multiplanetary_to_industrial() * industrial_to_perils()
#    + perils_to_multiplanetary() * multiplanetary_to_perils()
#    + perils_to_multiplanetary() * multiplanetary_to_interstellar())
#    = perils_to_interstellar()

# a3 * (1 - ( perils_to_survival() * survival_to_preindustrial() * preindustrial_to_industrial() * industrial_to_perils()
#    + perils_to_preindustrial() * preindustrial_to_industrial() * industrial_to_perils()
#    + perils_to_industrial() * industrial_to_perils()
#    + perils_to_multiplanetary() * multiplanetary_to_survival() * survival_to_preindustrial() * preindustrial_to_industrial() * industrial_to_perils()
#    + perils_to_multiplanetary() * multiplanetary_to_preindustrial() * preindustrial_to_industrial() * industrial_to_perils()
#    + perils_to_multiplanetary() * multiplanetary_to_industrial() * industrial_to_perils()
#    + perils_to_multiplanetary() * multiplanetary_to_perils()
#    + perils_to_multiplanetary() * multiplanetary_to_interstellar()))
#    = perils_to_interstellar()

# actual_a3 = perils_to_interstellar() / (1 - ( perils_to_survival() * survival_to_preindustrial() * preindustrial_to_industrial() * industrial_to_perils()
#    + perils_to_preindustrial() * preindustrial_to_industrial() * industrial_to_perils()
#    + perils_to_industrial() * industrial_to_perils()
#    + perils_to_multiplanetary() * multiplanetary_to_survival() * survival_to_preindustrial() * preindustrial_to_industrial() * industrial_to_perils()
#    + perils_to_multiplanetary() * multiplanetary_to_preindustrial() * preindustrial_to_industrial() * industrial_to_perils()
#    + perils_to_multiplanetary() * multiplanetary_to_industrial() * industrial_to_perils()
#    + perils_to_multiplanetary() * multiplanetary_to_perils()
#    + perils_to_multiplanetary() * multiplanetary_to_interstellar()))


# perils_to_multiplanetary() * a4 =
# perils_to_multiplanetary() * (multiplanetary_to_survival() * survival_to_preindustrial() * preindustrial_to_industrial() * industrial_to_perils() * a3
#    + multiplanetary_to_preindustrial() * preindustrial_to_industrial() * industrial_to_perils() * a3
#    + multiplanetary_to_industrial() * industrial_to_perils() * a3
#    + multiplanetary_to_perils() * a3
#    + multiplanetary_to_interstellar() * a3)

# # =
#    + perils_to_multiplanetary() * multiplanetary_to_survival() * survival_to_preindustrial() * preindustrial_to_industrial() * industrial_to_perils() * a3
#    + perils_to_multiplanetary() * multiplanetary_to_preindustrial() * preindustrial_to_industrial() * industrial_to_perils() * a3
#    + perils_to_multiplanetary() * multiplanetary_to_industrial() * industrial_to_perils() * a3
#    + perils_to_multiplanetary() * multiplanetary_to_perils() * a3
#    + perils_to_multiplanetary() * multiplanetary_to_interstellar() * a3



