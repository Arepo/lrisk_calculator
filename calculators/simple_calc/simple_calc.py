from functools import cache
from pydtmc import MarkovChain
from collections import OrderedDict
import numpy as np

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
  def __init__(self, extinction_given_preindustrial=0, extinction_given_industrial=0,
               extinction_given_present_perils=0, preindustrial_given_present_perils=0,
               industrial_given_present_perils=0, future_perils_given_present_perils=0,
               interstellar_given_present_perils=0, extinction_given_future_perils=0,
               preindustrial_given_future_perils=0, industrial_given_future_perils=0,
               interstellar_given_future_perils=0, extinction_given_multiplanetary=0,
               preindustrial_given_multiplanetary=0, industrial_given_multiplanetary=0,
               future_perils_given_multiplanetary=0):

    # Premodern transition probabilities
    self.ext_g_pi = extinction_given_preindustrial
    self.ext_g_i = extinction_given_industrial

    # Present perils transition probabilities
    self.ext_g_pp = extinction_given_present_perils
    self.pi_g_pp = preindustrial_given_present_perils
    self.i_g_pp = industrial_given_present_perils
    self.fp_g_pp = future_perils_given_present_perils
    self.int_g_pp = interstellar_given_present_perils

    # Future perils transition probabilities
    self.ext_g_fp = extinction_given_future_perils
    self.pi_g_fp = preindustrial_given_future_perils
    self.i_g_fp = industrial_given_future_perils
    self.int_g_fp = interstellar_given_future_perils

    # Multiplanetary transition probabilities
    self.ext_g_mp = extinction_given_multiplanetary
    self.pi_g_mp = preindustrial_given_multiplanetary
    self.i_g_mp = industrial_given_multiplanetary
    self.fp_g_mp = future_perils_given_multiplanetary

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
                + self.preindustrial_given_present_perils()
                + self.industrial_given_present_perils()
                + self.future_perils_given_present_perils()
                + self.interstellar_given_present_perils())


  # From future perils
  @rounded
  def extinction_given_future_perils(self):
    return self.ext_g_fp

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
                + self.preindustrial_given_future_perils()
                + self.industrial_given_future_perils()
                + self.interstellar_given_future_perils())


  # From mutiplanetary
  @rounded
  def extinction_given_multiplanetary(self):
    return self.ext_g_mp

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
                + self.preindustrial_given_multiplanetary()
                + self.industrial_given_multiplanetary()
                + self.future_perils_given_multiplanetary())

  @cache
  def markov_chain(self):
    extinction_transition_probabilities =     [1, 0, 0, 0, 0, 0, 0]
    preindustrial_transition_probabilities =  [self.extinction_given_preindustrial(),
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
                                               self.future_perils_given_industrial(),
                                               0,
                                               0]
    present_perils_transition_probabilities = [self.extinction_given_present_perils(),
                                               self.preindustrial_given_present_perils(),
                                               self.industrial_given_present_perils(),
                                               0,
                                               self.future_perils_given_present_perils(),
                                               self.multiplanetary_given_present_perils(),
                                               self.interstellar_given_present_perils()]
    future_perils_transition_probabilities =   [self.extinction_given_future_perils(),
                                               self.preindustrial_given_future_perils(),
                                               self.industrial_given_future_perils(),
                                               0,
                                               0,
                                               self.multiplanetary_given_future_perils(),
                                               self.interstellar_given_future_perils()]
    multiplanetary_transition_probabilities = [self.extinction_given_multiplanetary(),
                                               self.preindustrial_given_multiplanetary(),
                                               self.industrial_given_multiplanetary(),
                                               0,
                                               self.future_perils_given_multiplanetary(),
                                               0,
                                               self.interstellar_given_multiplanetary()]
    interstellar_transition_probabilities =   [0, 0, 0, 0, 0, 0, 1]

    transition_probability_matrix = [extinction_transition_probabilities,
                                     preindustrial_transition_probabilities,
                                     industrial_transition_probabilities,
                                     present_perils_transition_probabilities,
                                     future_perils_transition_probabilities,
                                     multiplanetary_transition_probabilities,
                                     interstellar_transition_probabilities]

    # mini = [[0.2, 0.7, 0.0, 0.1], [0.0, 0.6, 0.3, 0.1], [0.0, 0.0, 1.0, 0.0], [0.5, 0.0, 0.5, 0.0]]
    # mc = MarkovChain(mini, ['A', 'B', 'C', 'D'])

    return MarkovChain(transition_probability_matrix, ['Extinction',
                                                       'Preindustrial',
                                                       'Industrial',
                                                       'Present perils',
                                                       'Future perils',
                                                       'Multiplanetary',
                                                       'Interstellar'])

    # Shortcuts for the probability of direct-path transitions

  def probability_of_preindustrial_to_perils_directly(self):
    return self.industrial_given_preindustrial() * self.future_perils_given_industrial()

  def net_interstellar_from_preindustrial(self):
    return self.markov_chain().absorption_probabilities()[1][0]

  def net_interstellar_from_industrial(self):
    return self.markov_chain().absorption_probabilities()[1][1]

  def net_interstellar_from_present_perils(self):
    return self.markov_chain().absorption_probabilities()[1][2]

  def net_interstellar_from_future_perils(self):
    return self.markov_chain().absorption_probabilities()[1][3]

  def net_interstellar_from_multiplanetary(self):
    return self.markov_chain().absorption_probabilities()[1][4]

  def total_probability_of_non_extinction_milestone_regression_from_perils(self):
    return self.preindustrial_given_perils() + self.industrial_given_perils()

  # def weighted_net_interstellar_from_unspecified_regress(self):
  #   return ((self.net_interstellar_from_preindustrial() * self.preindustrial_given_perils())
  #            + (self.net_interstellar_from_industrial() * self.industrial_given_perils())
  #               / self.total_probability_of_non_extinction_milestone_regression_from_perils())


  def extinction_probability_difference(self):
    return -self.net_interstellar_from_present_perils()

  def preindustrial_probability_difference(self):
    return self.net_interstellar_from_preindustrial() - self.net_interstellar_from_present_perils()

  def industrial_probability_difference(self):
    return self.net_interstellar_from_industrial() - self.net_interstellar_from_present_perils()

  def present_perils_probability_difference(self):
    return 0

  def future_perils_probability_difference(self):
    return self.net_interstellar_from_future_perils() - self.net_interstellar_from_present_perils()

  def multiplanetary_probability_difference(self):
    return self.net_interstellar_from_multiplanetary() - self.net_interstellar_from_present_perils()

  def interstellar_probability_difference(self):
    return 1 - self.net_interstellar_from_present_perils()

  def probability_differences(self):
    return OrderedDict([
      ('Extinction', self.extinction_probability_difference()),
      ('Preindustrial', self.preindustrial_probability_difference()),
      ('Industrial', self.industrial_probability_difference()),
      ('Present perils', self.present_perils_probability_difference()),
      ('Future perils', self.future_perils_probability_difference()),
      ('Multiplanetary', self.multiplanetary_probability_difference()),
      ('Interstellar', self.interstellar_probability_difference())
    ])

  def extinction_probability_proportion(self):
    return '100%'

  def preindustrial_probability_proportion(self):
    return str((self.net_interstellar_from_present_perils() - self.net_interstellar_from_preindustrial())
                / self.net_interstellar_from_present_perils() * 100) + '%'

  def industrial_probability_proportion(self):
    return str((self.net_interstellar_from_present_perils() - self.net_interstellar_from_industrial())
               / self.net_interstellar_from_present_perils() * 100) + '%'

  def future_perils_probability_proportion(self):
    return str((self.net_interstellar_from_present_perils() - self.net_interstellar_from_future_perils())
                / self.net_interstellar_from_present_perils() * 100) + '%'

  def multiplanetary_probability_proportion(self):
    return str((self.net_interstellar_from_present_perils() - self.net_interstellar_from_multiplanetary())
                / self.net_interstellar_from_present_perils() * 100) + '%'

  def interstellar_probability_proportion(self):
    return str((self.net_interstellar_from_present_perils() - 1)
                / self.net_interstellar_from_present_perils() * 100) + '%'

  def probability_proportion_differences(self):
    if self.net_interstellar_from_present_perils():
      return OrderedDict([
        ('Extinction', self.extinction_probability_proportion()),
        ('Preindustrial', self.preindustrial_probability_proportion()),
        ('Industrial', self.industrial_probability_proportion()),
        ('Future perils', self.future_perils_probability_proportion()),
        ('Multiplanetary', self.multiplanetary_probability_proportion()),
        ('Interstellar', self.interstellar_probability_proportion())
      ])
    else:
      return OrderedDict([
        ('Extinction', np.nan),
        ('Preindustrial', np.nan),
        ('Industrial', np.nan),
        ('Future perils', np.nan),
        ('Multiplanetary', np.nan),
        ('Interstellar', np.nan)
      ])
