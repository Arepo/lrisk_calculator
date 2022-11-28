import pdb

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



# Simplifying

probability_of_industrial_to_perils_directly = perils_given_industrial()
probability_of_preindustrial_to_perils_directly = industrial_given_preindustrial() * probability_of_industrial_to_perils_directly
probability_of_survival_to_perils_directly = preindustrial_given_survival() * probability_of_preindustrial_to_perils_directly


# =>

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



# pdb.set_trace()

print(f"""
Probability of becoming interstellar from extinction = {probability_of_interstellar_from_extinction}
Probability of becoming interstellar from survival = {probability_of_interstellar_from_survival}
Probability of becoming interstellar from preindustrial = {probability_of_interstellar_from_preindustrial}
Probability of becoming interstellar from industrial = {probability_of_interstellar_from_industrial}
Probability of becoming interstellar from perils = {probability_of_interstellar_from_perils}
Probability of becoming interstellar from multiplanetary = {probability_of_interstellar_from_multiplanetary}
Probability of becoming interstellar from interstellar = {probability_of_interstellar_from_interstellar}
""")


# Calculations:

# Absorbtion probabilities

# E = extinction
# S = survival
# P = preindustrial
# I = industrial
# M = modern, ie perils
# C = colonies, ie multiplanetary
# V = Virgo supercluster, ie interstellar

# a0 = prob(absorbed in V | X0 = E) = 0
# a1 = prob(absorbed in V | X0 = S)
# a2 = prob(absorbed in V | X0 = P)
# a3 = prob(absorbed in V | X0 = I)
# a4 = prob(absorbed in V | X0 = M)
# a5 = prob(absorbed in V | X0 = C)
# a6 = prob(absorbed in V | X0 = V) = 1

# a1 # = prob(E | S) * a0 + prob(P | S) * a2
#    # = prob(P | S) * a2
#    # = prob(P | S) * prob(I | P) * a3
#    = prob(P | S) * prob(I | P) * prob(M | I) * a4

# a2 # = prob(E | P) * a0 + prob(I | P) * a3
#    # = prob(I | P) * a3
#    = prob(I | P) * prob(M | I) * a4

# a3 # = prob(E | I) * a0 + prob(M | I) * a4
#    = prob(M | I) * a4

# a4 # = prob(E | M) * a0 + prob(S | M) * a1 + prob(P | M) * a2 + prob(I | M) * a3 + prob(C | M) * a5 + prob(V | M) * a6
#    # = prob(S | M) * a1
#    #   + prob(P | M) * a2
#    #   + prob(I | M) * a3
#    #   + prob(C | M) * a5
#    #   + prob(V | M)
#    = prob(S | M) * prob(P | S) * prob(I | P) * prob(M | I) * a4
#      + prob(P | M) * prob(I | P) * prob(M | I) * a4
#      + prob(I | M) * prob(M | I) * a4
#      + prob(C | M) * a5
#      + prob(V | M)

# a5 # = prob(E | C) * a0 + prob(S | C) * a1 + prob(P | C) * a2 + prob(I | C) * a3 + prob(M | C) * a4 + prob(V | C) * a6
#    # = prob(S | C) * a1
#    #   + prob(P | C) * a2
#    #   + prob(I | C) * a3
#    #   + prob(M | C) * a4
#    #   + prob(V | C)
#    = prob(S | C) * prob(P | S) * prob(I | P) * prob(M | I) * a4
#     + prob(P | C) * prob(I | P) * prob(M | I) * a4
#     + prob(I | C) * prob(M | I) * a4
#     + prob(M | C) * a4
#     + prob(V | C)

# # =>
# a4 = prob(V | M)
#      + prob(S | M) * prob(P | S) * prob(I | P) * prob(M | I) * a4
#      + prob(P | M) * prob(I | P) * prob(M | I) * a4
#      + prob(I | M) * prob(M | I) * a4
#      + prob(C | M) * [prob(S | C) * prob(P | S) * prob(I | P) * prob(M | I) * a4
#                       + prob(P | C) * = prob(I | P) * prob(M | I) * a4
#                       + prob(I | C) * prob(M | I) * a4
#                       + prob(M | C) * a4
#                       + prob(V | C)]

#    = prob(V | M) + prob(C | M) * prob(V | C)
#      + prob(S | M) * prob(P | S) * prob(I | P) * prob(M | I) * a4
#      + prob(P | M) * prob(I | P) * prob(M | I) * a4
#      + prob(I | M) * prob(M | I) * a4
#      + prob(C | M) * [prob(S | C) * prob(P | S) * prob(I | P) * prob(M | I) * a4
#                       + prob(P | C) * = prob(I | P) * prob(M | I) * a4
#                       + prob(I | C) * prob(M | I) * a4
#                       + prob(M | C) * a4]

#    = prob(V | M) + prob(C | M) * prob(V | C)
#      + a4 * [prob(S | M) * prob(P | S) * prob(I | P) * prob(M | I)
#              + prob(P | M) * prob(I | P) * prob(M | I)
#              + prob(I | M) * prob(M | I)
#              + prob(C | M) * [prob(S | C) * prob(P | S) * prob(I | P) * prob(M | I)
#                               + prob(P | C) * = prob(I | P) * prob(M | I)
#                               + prob(I | C) * prob(M | I)
#                               + prob(M | C)]

# # =>
# prob(V | M) + prob(C | M) * prob(V | C) =
#   a4 - a4 * [prob(S | M) * prob(P | S) * prob(I | P) * prob(M | I)
#              + prob(P | M) * prob(I | P) * prob(M | I)
#              + prob(I | M) * prob(M | I)
#              + prob(C | M) * [prob(S | C) * prob(P | S) * prob(I | P) * prob(M | I)
#                               + prob(P | C) * = prob(I | P) * prob(M | I)
#                               + prob(I | C) * prob(M | I)
#                               + prob(M | C)]

#  = a4(1 - [prob(S | M) * prob(P | S) * prob(I | P) * prob(M | I)
#            + prob(P | M) * prob(I | P) * prob(M | I)
#            + prob(I | M) * prob(M | I)
#            + prob(C | M) * [prob(S | C) * prob(P | S) * prob(I | P) * prob(M | I)
#                             + prob(P | C) * = prob(I | P) * prob(M | I)
#                             + prob(I | C) * prob(M | I)
#                             + prob(M | C)])

# # =>
# a4 = [prob(V | M) + prob(C | M) * prob(V | C)] / (1 - [prob(S | M) * prob(P | S) * prob(I | P) * prob(M | I)
#                                                      + prob(P | M) * prob(I | P) * prob(M | I)
#                                                      + prob(I | M) * prob(M | I)
#                                                      + prob(C | M) * [prob(S | C) * prob(P | S) * prob(I | P) * prob(M | I)
#                                                                       + prob(P | C) * = prob(I | P) * prob(M | I)
#                                                                       + prob(I | C) * prob(M | I)
#                                                                       + prob(M | C)])

# probability_of_preindustrial_to_perils_directly = prob(I | P) * prob(M | I)
# probability_of_survival_to_perils_directly = prob(P | S) * probability_of_preindustrial_to_perils_directly

# # =>
# a4 = [prob(V | M) + prob(C | M) * prob(V | C)] / (1 - [prob(S | M) * probability_of_survival_to_perils_directly
#                                                      + prob(P | M) * probability_of_preindustrial_to_perils_directly
#                                                      + prob(I | M) * prob(M | I)
#                                                      + prob(C | M) * [prob(S | C) * probability_of_survival_to_perils_directly
#                                                                       + prob(P | C) * prob(I | P) * prob(M | I)
#                                                                       + prob(I | C) * prob(M | I)
#                                                                       + prob(M | C)])

# probability_of_interstellar_from_perils = a4 = [interstellar_given_perils() + multiplanetary_given_perils() * interstellar_given_multiplanetary()] /
#                                                (1 - [survival_given_perils() * probability_of_survival_to_perils_directly
#                                                      + preindustrial_given_perils() * probability_of_preindustrial_to_perils_directly
#                                                      + industrial_given_perils() * perils_given_industrial()
#                                                      + multiplanetary_given_perils() * [survival_given_multiplanetary() * probability_of_survival_to_perils_directly
#                                                                                         + preindustrial_given_multiplanetary() * industrial_given_preindustrial() * perils_given_industrial()
#                                                                                         + industrial_given_multiplanetary() * perils_given_industrial()
#                                                                                         + perils_given_multiplanetary()]])

# probability_of_interstellar_from_multiplanetary = a5 = survival_given_multiplanetary() * preindustrial_given_survival() * industrial_given_preindustrial() * perils_given_industrial() * probability_of_interstellar_from_perils
#                                                        + preindustrial_given_multiplanetary() * industrial_given_preindustrial() * perils_given_industrial() * probability_of_interstellar_from_perils
#                                                        + industrial_given_multiplanetary() * perils_given_industrial() * probability_of_interstellar_from_perils
#                                                        + perils_given_multiplanetary() * probability_of_interstellar_from_perils
#                                                        + interstellar_given_multiplanetary()

