from functools import cache
from pydtmc import MarkovChain


# This script prints out a series of probabilities for transition becoming interstellar based on
# estimates of the transition probabilities of various(values are currently hardcoded placeholders)
# states, as in a Markov chain. The states are extinction, pre_equilibrium, preindustrial, industrial, time
# of perils, multiplanetary, and interstellar.
#
# A full description/explanation of the model is in the section titled The Cyclical Model in this
# post:
# https://forum.effectivealtruism.org/posts/YnBwoNNqe6knBJH8p/modelling-civilisation-after-a-catastrophe#The_cyclical_model
#
# These values are all placeholders. Add your own, and see what happens.

# TODO Might want this model to still have two ToP-states - the current one, and all future ones

# Transition probabilities

def rounded(func):
  # Ensure that probabilities are between 0 and 1 (to deal with floating point errors)
  def inner(val):
    val = func(val)
    if val < 0:
        return 0
    elif val > 1:
        return 1
    return val
  return inner

class SimpleCalc:
  def __init__(self, extinction_given_pre_equilibrium=0, extinction_given_preindustrial=0,
               extinction_given_industrial=0, extinction_given_present_perils=0,
               pre_equilibrium_given_present_perils=0, preindustrial_given_present_perils=0,
               industrial_given_present_perils=0, future_perils_given_present_perils=0,
               interstellar_given_present_perils=0, multiplanetary_given_present_perils=0,
               extinction_given_future_perils=0, pre_equilibrium_given_future_perils=0,
               preindustrial_given_future_perils=0, industrial_given_future_perils=0,
               interstellar_given_future_perils=0, extinction_given_multiplanetary=0,
               pre_equilibrium_given_multiplanetary=0, preindustrial_given_multiplanetary=0,
               industrial_given_multiplanetary=0, future_perils_given_multiplanetary=0):

    # Premodern transition probabilities
    self.ext_g_pe = extinction_given_pre_equilibrium
    self.ext_g_pi = extinction_given_preindustrial
    self.ext_g_i = extinction_given_industrial

    # Present perils transition probabilities
    self.ext_g_pp = extinction_given_present_perils
    self.pe_g_pp = pre_equilibrium_given_present_perils
    self.pi_g_pp = preindustrial_given_present_perils
    self.i_g_pp = industrial_given_present_perils
    self.fp_g_pp = future_perils_given_present_perils
    self.int_g_pp = interstellar_given_present_perils

    # Future perils transition probabilities
    self.ext_g_fp = extinction_given_future_perils
    self.pe_g_fp = pre_equilibrium_given_future_perils
    self.pi_g_fp = preindustrial_given_future_perils
    self.i_g_fp = industrial_given_future_perils
    self.int_g_fp = interstellar_given_future_perils

    # Multiplanetary transition probabilities
    self.ext_g_mp = extinction_given_multiplanetary
    self.pe_g_mp = pre_equilibrium_given_multiplanetary
    self.pi_g_mp = preindustrial_given_multiplanetary
    self.i_g_mp = industrial_given_multiplanetary
    self.fp_g_mp = future_perils_given_multiplanetary

  # From pre-equilibrium


  @rounded
  def extinction_given_pre_equilibrium(self):
    return self.ext_g_pe

  @rounded
  def preindustrial_given_pre_equilibrium(self):
    return 1 - self.extinction_given_pre_equilibrium()


  # From preindustrial
  @rounded
  def extinction_given_preindustrial(self):
    return self.ext_g_pi

  @rounded
  def industrial_given_preindustrial(self):
    return 1 - self.extinction_given_preindustrial()


  # From industrial
  @rounded
  def extinction_given_industrial(self):
    return self.ext_g_i

  @rounded
  def future_perils_given_industrial(self):
    return 1 - self.extinction_given_industrial()


  # From present perils
  @rounded
  def extinction_given_present_perils(self):
    return self.ext_g_pp

  @rounded
  def pre_equilibrium_given_present_perils(self):
    return self.pe_g_pp

  @rounded
  def preindustrial_given_present_perils(self):
    return self.pi_g_pp

  @rounded
  def industrial_given_present_perils(self):
    return self.i_g_pp

  @rounded
  def future_perils_given_present_perils(self):
    return self.fp_g_pp

  @rounded
  def interstellar_given_present_perils(self):
    return self.int_g_pp

  @rounded
  def multiplanetary_given_present_perils(self):
    return 1 - (self.extinction_given_present_perils()
                + self.pre_equilibrium_given_present_perils()
                + self.preindustrial_given_present_perils()
                + self.industrial_given_present_perils()
                + self.future_perils_given_present_perils()
                + self.interstellar_given_present_perils())


  # From future perils
  @rounded
  def extinction_given_future_perils(self):
    return self.ext_g_fp

  @rounded
  def pre_equilibrium_given_future_perils(self):
    return self.pe_g_fp

  @rounded
  def preindustrial_given_future_perils(self):
    return self.pi_g_fp

  @rounded
  def industrial_given_future_perils(self):
    return self.i_g_fp

  @rounded
  def interstellar_given_future_perils(self):
    return self.int_g_fp

  @rounded
  def multiplanetary_given_future_perils(self):
    return 1 - (self.extinction_given_future_perils()
                + self.pre_equilibrium_given_future_perils()
                + self.preindustrial_given_future_perils()
                + self.industrial_given_future_perils()
                + self.interstellar_given_future_perils())


  # From mutiplanetary
  @rounded
  def extinction_given_multiplanetary(self):
    return self.ext_g_mp

  @rounded
  def pre_equilibrium_given_multiplanetary(self):
    return self.pe_g_mp

  @rounded
  def preindustrial_given_multiplanetary(self):
    return self.pi_g_mp

  @rounded
  def industrial_given_multiplanetary(self):
    return self.i_g_mp

  @rounded
  def future_perils_given_multiplanetary(self):
    return self.fp_g_mp

  @rounded
  def interstellar_given_multiplanetary(self):
    return 1 - (self.extinction_given_multiplanetary()
                + self.pre_equilibrium_given_multiplanetary()
                + self.preindustrial_given_multiplanetary()
                + self.industrial_given_multiplanetary()
                + self.future_perils_given_multiplanetary())

  @cache
  def markov_chain(self):
    extinction_transition_probabilities =     [1, 0, 0, 0, 0, 0, 0, 0]
    pre_equilibrium_transition_probabilities =  [self.extinction_given_pre_equilibrium(),
                                                0,
                                                self.preindustrial_given_pre_equilibrium(),
                                                0,
                                                0,
                                                0,
                                                0,
                                                0]
    preindustrial_transition_probabilities =  [self.extinction_given_preindustrial(),
                                               0,
                                               0,
                                               self.industrial_given_preindustrial(),
                                               0,
                                               0,
                                               0,
                                               0]
    industrial_transition_probabilities =     [self.extinction_given_industrial(),
                                               0,
                                               0,
                                               0,
                                               0,
                                               self.future_perils_given_industrial(),
                                               0,
                                               0]
    present_perils_transition_probabilities = [self.extinction_given_present_perils(),
                                               self.pre_equilibrium_given_present_perils(),
                                               self.preindustrial_given_present_perils(),
                                               self.industrial_given_present_perils(),
                                               0,
                                               self.future_perils_given_present_perils(),
                                               self.multiplanetary_given_present_perils(),
                                               self.interstellar_given_present_perils()]
    future_perils_transition_probabilities =   [self.extinction_given_future_perils(),
                                               self.pre_equilibrium_given_future_perils(),
                                               self.preindustrial_given_future_perils(),
                                               self.industrial_given_future_perils(),
                                               0,
                                               0,
                                               self.multiplanetary_given_future_perils(),
                                               self.interstellar_given_future_perils()]
    multiplanetary_transition_probabilities = [self.extinction_given_multiplanetary(),
                                               self.pre_equilibrium_given_multiplanetary(),
                                               self.preindustrial_given_multiplanetary(),
                                               self.industrial_given_multiplanetary(),
                                               0,
                                               self.future_perils_given_multiplanetary(),
                                               0,
                                               self.interstellar_given_multiplanetary()]
    interstellar_transition_probabilities =   [0, 0, 0, 0, 0, 0, 0, 1]

    transition_probability_matrix = [extinction_transition_probabilities,
                                     pre_equilibrium_transition_probabilities,
                                     preindustrial_transition_probabilities,
                                     industrial_transition_probabilities,
                                     present_perils_transition_probabilities,
                                     future_perils_transition_probabilities,
                                     multiplanetary_transition_probabilities,
                                     interstellar_transition_probabilities]

    # mini = [[0.2, 0.7, 0.0, 0.1], [0.0, 0.6, 0.3, 0.1], [0.0, 0.0, 1.0, 0.0], [0.5, 0.0, 0.5, 0.0]]
    # mc = MarkovChain(mini, ['A', 'B', 'C', 'D'])

    return MarkovChain(transition_probability_matrix, ['Extinction',
                                                       'Pre-equilibrium',
                                                       'Preindustrial',
                                                       'Industrial',
                                                       'Present perils',
                                                       'Future perils',
                                                       'Multiplanetary',
                                                       'Interstellar'])

    # Shortcuts for the probability of direct-path transitions

  def probability_of_preindustrial_to_perils_directly(self):
    return self.industrial_given_preindustrial() * self.future_perils_given_industrial()

  def probability_of_pre_equilibrium_to_perils_directly(self):
    return self.preindustrial_given_pre_equilibrium() * self.probability_of_preindustrial_to_perils_directly()

  def net_interstellar_from_pre_equilibrium(self):
    return self.markov_chain().absorption_probabilities()[1][0]

  def net_interstellar_from_preindustrial(self):
    return self.markov_chain().absorption_probabilities()[1][1]

  def net_interstellar_from_industrial(self):
    return self.markov_chain().absorption_probabilities()[1][2]

  def net_interstellar_from_present_perils(self):
    return self.markov_chain().absorption_probabilities()[1][3]

  def net_interstellar_from_future_perils(self):
    return self.markov_chain().absorption_probabilities()[1][4]

  def net_interstellar_from_multiplanetary(self):
    return self.markov_chain().absorption_probabilities()[1][5]

  def total_probability_of_non_extinction_milestone_regression_from_perils(self):
    return self.pre_equilibrium_given_perils() + self.preindustrial_given_perils() + self.industrial_given_perils()

  # def weighted_net_interstellar_from_unspecified_regress(self):
  #   return ((self.net_interstellar_from_pre_equilibrium() * self.pre_equilibrium_given_perils())
  #            + (self.net_interstellar_from_preindustrial() * self.preindustrial_given_perils())
  #            + (self.net_interstellar_from_industrial() * self.industrial_given_perils())
  #               / self.total_probability_of_non_extinction_milestone_regression_from_perils())

  def pre_equilibrium_probability_reduction(self):
    return str((self.net_interstellar_from_present_perils() - self.net_interstellar_from_pre_equilibrium())
                / self.net_interstellar_from_present_perils() * 100) + '%'

  def preindustrial_probability_reduction(self):
    return str((self.net_interstellar_from_present_perils() - self.net_interstellar_from_preindustrial())
                / self.net_interstellar_from_present_perils() * 100) + '%'

  def industrial_probability_reduction(self):
    return str((self.net_interstellar_from_present_perils() - self.net_interstellar_from_industrial())
               / self.net_interstellar_from_present_perils() * 100) + '%'

  def future_perils_probability_reduction(self):
    return str((self.net_interstellar_from_present_perils() - self.net_interstellar_from_future_perils())
                / self.net_interstellar_from_present_perils() * 100) + '%'

  def multiplanetary_probability_increase(self):
    return str((self.net_interstellar_from_multiplanetary() - self.net_interstellar_from_present_perils())
                / self.net_interstellar_from_present_perils() * 100) + '%'




# total_probability_of_non_extinction_milestone_regression_from_present_perils = pre_equilibrium_given_present_perils() + preindustrial_given_present_perils() + industrial_given_present_perils()
# weighted_net_interstellar_from_unspecified_regress = ((net_interstellar_from_pre_equilibrium() * pre_equilibrium_given_present_perils())
#                                                      + (net_interstellar_from_preindustrial() * preindustrial_given_present_perils())
#                                                      + (net_interstellar_from_industrial() * industrial_given_present_perils())
#                                                    / total_probability_of_non_extinction_milestone_regression_from_present_perils)
# # TODO check below half of this when more awake - output looks suspicious
# reduced_chance_of_success = (net_interstellar_from_present_perils() - weighted_net_interstellar_from_unspecified_regress) / net_interstellar_from_present_perils()


# conclusions = {
#   'net_interstellar_from_pre_equilibrium': net_interstellar_from_pre_equilibrium(),
#   'net_interstellar_from_preindustrial': net_interstellar_from_preindustrial(),
#   'net_interstellar_from_industrial': net_interstellar_from_industrial(),
#   'net_interstellar_from_present_perils': net_interstellar_from_present_perils(),
#   'net_interstellar_from_multiplanetary': net_interstellar_from_multiplanetary()
# }


# # print(f"""
# # Therefore, if we assume that becoming interstellar is the only concern...
# # a castatrophe that put us into a survival state would reduce our chance of becoming interstellar by {(net_interstellar_from_present_perils() - net_interstellar_from_pre_equilibrium()) / net_interstellar_from_present_perils() * 100}%
# # a castatrophe that put us into a preindustrial state would reduce our chance of becoming interstellar by {(net_interstellar_from_present_perils() - net_interstellar_from_preindustrial()) / net_interstellar_from_present_perils() * 100}%
# # a castatrophe that put us into an industrial state would reduce our chance of becoming interstellar by {(net_interstellar_from_present_perils() - net_interstellar_from_industrial()) / net_interstellar_from_present_perils() * 100}%
# # and if we reached a multiplanetary state, it would increase our chance of becoming interstellar by {(net_interstellar_from_multiplanetary() - net_interstellar_from_present_perils()) / net_interstellar_from_present_perils() * 100}%
# # """)
