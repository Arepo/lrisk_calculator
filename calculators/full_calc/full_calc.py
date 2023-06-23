from functools import cache
import yaml
import datetime
import pdb

from pydtmc import MarkovChain

import runtime_constants as constant
import multiplanetary
import perils
import preperils
import sub_markov_chains

def full_markov_chain():
  def _zero_probabilities():
    """Represents a set of zero-probability transitions, eg all the preindustrial states'
    transitional probabilities from an industrial state. For perils and multiplanetary rows, we'll
    need to add an extra value, since they potentially include the current civilisation"""
    return [0] * (constant.MAX_CIVILISATIONS - 1)



  states_count = 5 * constant.MAX_CIVILISATIONS - 3 # 5 classes of states
  # (pre_equilibrium, preindustrial, industrial, perils, multiplanetary) * max civilisations, minus the three
  # preperils states in our current civilisation)
  extinction_row   = [0] * states_count + [1, 0]
  interstellar_row = [0] * states_count + [0, 1]
  preperils_civilisation_range = range(1, constant.MAX_CIVILISATIONS)
  modern_civilisation_range = range(0, constant.MAX_CIVILISATIONS)

  pre_equilibrium_rows = [_zero_probabilities()
                   # ^Other pre_equilibrium states
                   + [preperils.preindustrial_given_pre_equilibrium(k,k1) for k1 in preperils_civilisation_range]
                   # ^Preindustrial states, of which 1 is nonzero
                   + _zero_probabilities()
                   # ^Industrial states
                   + _zero_probabilities() + [0]
                   # ^Perils states (which include the current civilisation)
                   + _zero_probabilities() + [0]
                   # ^Multiplanetary states (which potentially include the current civilisation)
                   + [preperils.extinction_given_pre_equilibrium(k)] + [0]
                   # ^Extinction and Interstellar respectively
                   for k in preperils_civilisation_range]

  preindustrial_rows = [_zero_probabilities()
                         # ^pre_equilibrium states
                         + _zero_probabilities()
                         # ^Other preindustrial states
                         + [preperils.industrial_given_preindustrial(k,k1) for k1 in preperils_civilisation_range]
                         # ^Industrial states
                         + _zero_probabilities() + [0]
                         # ^Perils states (which include the current civilisation)
                         + _zero_probabilities() + [0]
                         # ^Multiplanetary states (which potentially include the current civilisation)
                         + [preperils.extinction_given_preindustrial(k)] + [0]
                         # ^Extinction and Interstellar respectively
                         for k in preperils_civilisation_range]

  industrial_rows =   [_zero_probabilities()
                       # ^pre_equilibrium states
                       + _zero_probabilities()
                       # ^Preindustrial states
                       + _zero_probabilities()
                       # ^Other industrial states
                       + [preperils.perils_given_industrial(k,k1) for k1 in modern_civilisation_range]
                       # ^Perils states (which include the current civilisation)
                       + _zero_probabilities() + [0]
                       # ^Multiplanetary states (which potentially include the current civilisation)
                       + [preperils.extinction_given_industrial(k)] + [0]
                       # ^Extinction and Interstellar respectively
                       for k in preperils_civilisation_range]

  @cache
  def perils_chain(k):
    return sub_markov_chains.IntraPerilsMCWrapper(k)

  # TODO: allow transition to perils k+1
  perils_rows = [[perils_chain(k).pre_equilibrium_given_perils(k1) for k1 in range(1, constant.MAX_CIVILISATIONS)]
               # ^Transition probabilities to future pre_equilibrium states
               + [perils_chain(k).preindustrial_given_perils(k1) for k1 in range(1, constant.MAX_CIVILISATIONS)]
               # ^Transition probabilities to future preindustrial states
               + [perils_chain(k).industrial_given_perils(k1) for k1 in range(1, constant.MAX_CIVILISATIONS)]
               # ^Transition probabilities to future industrial states
               + _zero_probabilities() + [0]
               # ^Transition probabilities to perils states (which include our current civilisation)
               + [perils_chain(k).multiplanetary_given_perils(k1) for k1 in range(0, constant.MAX_CIVILISATIONS)]
               # ^Transition probabilities to multiplanetary states (which potentially include our current civilisation)
               + [perils_chain(k).extinction_given_perils()]
               # ^Transition probability to the Extinction state (single-element list)
               + [perils_chain(k).interstellar_given_perils()]
               # ^Transition probabilities to the Interstellar state (single-element list)
               for k in range(0, constant.MAX_CIVILISATIONS)]

  @cache
  def multiplanetary_chain(k):
    return sub_markov_chains.IntraMultiplanetaryMCWrapper(k)

  multiplanetary_rows = [[multiplanetary_chain(k).pre_equilibrium_given_multiplanetary(k1) for k1 in range(1, constant.MAX_CIVILISATIONS)]
                         # ^pre_equilibrium states
                         + [multiplanetary_chain(k).preindustrial_given_multiplanetary(k1) for k1 in range(1, constant.MAX_CIVILISATIONS)]
                         # ^Preindustrial states
                         + [multiplanetary_chain(k).industrial_given_multiplanetary(k1) for k1 in range(1, constant.MAX_CIVILISATIONS)]
                         # ^Industrial states
                         + [multiplanetary_chain(k).perils_given_multiplanetary(k1) for k1 in range(0, constant.MAX_CIVILISATIONS)]
                         # ^Perils states (which include the current civilisation)
                         + _zero_probabilities() + [0]
                         # ^Multiplanetary states (which potentially include the current civilisation)
                         + [multiplanetary_chain(k).extinction_given_multiplanetary()]
                         # ^Only one Extinction state
                         + [multiplanetary_chain(k).interstellar_given_multiplanetary()]
                         # ^Only one Interstellar state
                         for k in range(0, constant.MAX_CIVILISATIONS)]

  probability_matrix = (pre_equilibrium_rows
                        + preindustrial_rows
                        + industrial_rows
                        + perils_rows
                        + multiplanetary_rows
                        + [extinction_row, interstellar_row])

  pre_equilibrium_names = ['pre_equilibrium-' + str(index[0] + 1) for index in enumerate(pre_equilibrium_rows)]
  preindustrial_names = ['preindustrial-' + str(index[0] + 1) for index in enumerate(preindustrial_rows)]
  industrial_names = ['industrial-' + str(index[0] + 1) for index in enumerate(industrial_rows)]
  perils_names = ['perils-' + str(index[0]) for index in enumerate(perils_rows)]
  multiplanetary_names = ['multiplanetary-' + str(index[0]) for index in enumerate(multiplanetary_rows)]

  # pdb.set_trace()
  return MarkovChain(probability_matrix, pre_equilibrium_names
                                         + preindustrial_names
                                         + industrial_names
                                         + perils_names
                                         + multiplanetary_names
                                         + ['Extinction', 'Interstellar'])


start = datetime.datetime.now()
mc = full_markov_chain()
runtime = (datetime.datetime.now() - start).seconds
print(f"""  From this breakpoint, you can query the MarkovChain (variable name mc) object as described
  at https://github.com/TommasoBelluzzo/PyDTMC, and in this repo's README.md

  Example values of interest:
  From our current time of perils, your parameters imply that our chance of ultimately becoming interstellar
  is ~{round(mc.absorption_probabilities()[1][(constant.MAX_CIVILISATIONS - 1) * 3] * 100)}%.

  If we we to regress once to a preindustrial state, our chance of becoming interstellar would be
  ~{round(mc.absorption_probabilities()[1][(constant.MAX_CIVILISATIONS - 1)] * 100)}%.

  In other words, assuming 'interstellar' and 'eventual extinction before becoming interstellar'
  were the only two outcomes of interest, such a 'non-existential' catastrophe would equate to
  ~{round(mc.absorption_probabilities()[1][(constant.MAX_CIVILISATIONS - 1) * 3] * 100 - mc.absorption_probabilities()[1][(constant.MAX_CIVILISATIONS - 1)] * 100)}%
  of the expected loss of value of immediate extinction.

  (the runtime with these parameters was {runtime} seconds)""")
pdb.set_trace()

