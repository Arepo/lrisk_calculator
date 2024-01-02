# pylint: disable=line-too-long, fixme, too-many-locals, forgotten-debug-statement

"""Module containing the full Markov chain, and code to run it (ending in a breakpoint)."""

from functools import cache
import datetime
import csv
import os

from pydtmc import MarkovChain

import calculators.full_calc.runtime_constants as constant
from calculators.full_calc import preperils
from calculators.full_calc import sub_markov_chains
from calculators.full_calc.params import Params

def full_markov_chain():
    """Wrapper for a pydtmc Markov chain that implements the full decay/perils-focused/multiplanetary
    model as described here: https://forum.effectivealtruism.org/s/gWsTMm5Nbgdxedyns/p/YnBwoNNqe6knBJH8p"""
    def _zero_probabilities():
        """Represents a set of zero-probability transitions, eg all the preindustrial states'
        transitional probabilities from an industrial state. For perils and multiplanetary rows,
        we'll need to add an extra value, since they potentially include the current civilisation"""
        return [0] * (constant.MAX_CIVILISATIONS - 1)

    transient_states_count = 4 * constant.MAX_CIVILISATIONS - 2 # 4 classes of transient state,
    # (preindustrial, industrial, perils, multiplanetary) * max civilisations, minus the two
    # preperils states in our current civilisation)
    extinction_row   = [0] * transient_states_count + [1, 0]
    interstellar_row = [0] * transient_states_count + [0, 1]
    preperils_civilisation_range = range(1, constant.MAX_CIVILISATIONS)
    modern_civilisation_range = range(0, constant.MAX_CIVILISATIONS)

    preindustrial_rows = [
        _zero_probabilities()
        # ^Preindustrial states
        + [preperils.industrial_given_preindustrial(k,k1) for k1 in preperils_civilisation_range]
        # ^Industrial states
        + _zero_probabilities() + [0]
        # ^Perils states (which include the current civilisation)
        + _zero_probabilities() + [0]
        # ^Multiplanetary states (which potentially include the current civilisation)
        + [preperils.extinction_given_preindustrial(k)] + [0]
        # ^Extinction and Interstellar respectively
        for k in preperils_civilisation_range]

    industrial_rows =   [
        _zero_probabilities()
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
        # Create and cache a time of perils sub-chain for civilisation k
        return sub_markov_chains.IntraPerilsMCWrapper(k)

    # TODO: allow transition to perils k+1
    perils_rows = [[perils_chain(k).preindustrial_given_perils(k1)
                   for k1 in range(1, constant.MAX_CIVILISATIONS)]
                # ^Transition probabilities to future preindustrial states
                + [perils_chain(k).industrial_given_perils(k1)
                   for k1 in range(1, constant.MAX_CIVILISATIONS)]
                # ^Transition probabilities to future industrial states
                + _zero_probabilities() + [0]
                # ^Transition probabilities to perils states (which include our current civilisation)
                + [perils_chain(k).multiplanetary_given_perils(k1)
                   for k1 in range(0, constant.MAX_CIVILISATIONS)]
                # ^Transition probabilities to multiplanetary states (which potentially include our
                #  current civilisation)
                + [perils_chain(k).extinction_given_perils()]
                # ^Transition probability to the Extinction state (single-element list)
                + [perils_chain(k).interstellar_given_perils()]
                # ^Transition probabilities to the Interstellar state (single-element list)
                for k in range(0, constant.MAX_CIVILISATIONS)]

    @cache
    def multiplanetary_chain(k):
        # Create and cache a multiplanetary sub-chain for civilisation k
        return sub_markov_chains.IntraMultiplanetaryMCWrapper(k)

    print('Creating multiplanetary subchain')

    multiplanetary_rows = []
    for k in range(0, constant.MAX_CIVILISATIONS):
        preindustrial_transitions = [multiplanetary_chain(k).preindustrial_given_multiplanetary(k1)
                               for k1 in range(1, constant.MAX_CIVILISATIONS)]
        # ^Probabilities of transitioning from the multiplanetary state in the
        # kth civilisation to the predindustrial state in the k1th civilisation
        industrial_transitions = [multiplanetary_chain(k).industrial_given_multiplanetary(k1)
                               for k1 in range(1, constant.MAX_CIVILISATIONS)]
        # ^Probabilities of transitioning from the multiplanetary state in the
        # kth civilisation to the industrial state in the k1th civilisation
        perils_transitions = [multiplanetary_chain(k).perils_given_multiplanetary(k1)
                               for k1 in range(0, constant.MAX_CIVILISATIONS)]
        # ^Probabilities of transitioning from the multiplanetary state in the
        # kth civilisation to the perils state in the k1th civilisation
        multiplanetary_transitions = _zero_probabilities() + [0]
        # ^Probabilities of transitioning from the multiplanetary state in the
        # kth civilisation to the multiplanetary state in the k1th civilisation
        extinction_transition = [multiplanetary_chain(k).extinction_given_multiplanetary()]
        # ^Probabilities of transitioning from the multiplanetary state in the
        # kth civilisation to the (only) Extinction state
        interstellar_transition =[multiplanetary_chain(k).interstellar_given_multiplanetary()]
        # ^Probabilities of transitioning from the multiplanetary state in the
        # kth civilisation to the (only) Interstellar state
        transition_probabilities = (preindustrial_transitions + industrial_transitions
            + perils_transitions + multiplanetary_transitions + extinction_transition
            + interstellar_transition)

        multiplanetary_rows.append(transition_probabilities)

    probability_matrix = (preindustrial_rows
                          + industrial_rows
                          + perils_rows
                          + multiplanetary_rows
                          + [extinction_row]
                          + [interstellar_row])

    preindustrial_names = ['preindustrial-' + str(index[0] + 1)
                           for index in enumerate(preindustrial_rows)]
    industrial_names = ['industrial-' + str(index[0] + 1)
                        for index in enumerate(industrial_rows)]
    perils_names = ['perils-' + str(index[0])
                    for index in enumerate(perils_rows)]
    multiplanetary_names = ['multiplanetary-' + str(index[0])
                            for index in enumerate(multiplanetary_rows)]
    print('Creating full Markov chain')
    return MarkovChain(probability_matrix, preindustrial_names
                                           + industrial_names
                                           + perils_names
                                           + multiplanetary_names
                                           + ['Extinction']
                                           + ['Interstellar'])


print('Runtime constants:')
print('Max planets: ' + str(constant.MAX_PLANETS))
print('Max civilisations: ' + str(constant.MAX_CIVILISATIONS))
print('Max progress years: ' + str(constant.MAX_PROGRESS_YEARS))
print('With params as follows:')
print(Params().describe())
print("Read about what these params mean in the calculators/full_calc/params.yml file\n")
start = datetime.datetime.now()
mc = full_markov_chain()
runtime = (datetime.datetime.now() - start).seconds
current_perils_index = mc.states.index('perils-0')
first_preindustrial_index = mc.states.index('preindustrial-1')
first_industrial_index = mc.states.index('industrial-1')
# print(f"""From this breakpoint, you can query the MarkovChain (variable name mc) object as
#     described at https://github.com/TommasoBelluzzo/PyDTMC, and in this repo's README.md

#     Example values of interest:
#     From our current time of perils, your parameters imply that our chance of ultimately becoming
#     interstellar is
#     ~{round(mc.absorption_probabilities()[1][current_perils_index] * 100)}%.

#     If we we to regress once to a preindustrial state, our chance of becoming interstellar would be
#     ~{round(mc.absorption_probabilities()[1][first_preindustrial_index] * 100)}%.

#     If we we to regress once to an industrial state, our chance of becoming interstellar would be
#     ~{round(mc.absorption_probabilities()[1][first_industrial_index] * 100)}%.

#     (the runtime with these parameters was {runtime} seconds)""")
# # Intentionally checked in breakpoint - this is where you can manually query the results

print('Total runtime: ' + str(runtime) + ' seconds\n')
print('Probability of becoming interstellar from perils-0:')
print(mc.absorption_probabilities()[1][mc.states.index('perils-0')])
print('Probability of becoming interstellar from multiplanetary-0:')
print(mc.absorption_probabilities()[1][mc.states.index('multiplanetary-0')])
print('*' * 20)
for i in range(1, constant.MAX_CIVILISATIONS):
    print('Probability of becoming interstellar from preindustrial-' + str(i) + ':')
    print(mc.absorption_probabilities()[1][mc.states.index(f'preindustrial-{i}')])
    print('Probability of becoming interstellar from industrial-' + str(i) + ':')
    print(mc.absorption_probabilities()[1][mc.states.index(f'industrial-{i}')])
    print('Probability of becoming interstellar from perils-' + str(i) + ':')
    print(mc.absorption_probabilities()[1][mc.states.index(f'perils-{i}')])
    print('Probability of becoming interstellar from multiplanetary-' + str(i) + ':')
    print(mc.absorption_probabilities()[1][mc.states.index(f'multiplanetary-{i}')])
    print('*' * 20)


import os
file_name = 'results.csv'

states = []
for i in range(1, constant.MAX_CIVILISATIONS):
    for state in (f'preindustrial-{i}', f'industrial-{i}', f'perils-{i}', f'multiplanetary-{i}'):
        states.append(state)

success_probabilities = []
numbered_states = []
for i in range(1, 10): # ideally this would go up to constant.MAX_CIVILISATIONS, but that messes up
                       # the CSV columns; if you want to save the results beyond civ-10, you'll
                       # store them manually from the printed output

    for state in (f'preindustrial-{i}', f'industrial-{i}', f'perils-{i}', f'multiplanetary-{i}'):
        numbered_states.append(state)
        probability = mc.absorption_probabilities()[1][mc.states.index(state)]
        success_probabilities.append(probability)

# Check if the file is empty or doesn't exist
file_exists = os.path.exists(file_name) and os.path.getsize(file_name) > 0

with open(file_name, 'a', newline='') as csvfile:
    writer = csv.writer(csvfile)

    civ_0_states = ['perils-0', 'multiplanetary-0']
    all_numbered_states = civ_0_states + numbered_states

    civ_0_probabilities = [mc.absorption_probabilities()[1][mc.states.index('perils-0')],
                           mc.absorption_probabilities()[1][mc.states.index('multiplanetary-0')]]
    all_success_probabilities = civ_0_probabilities + success_probabilities
    preindustrial_in_terms_of_astronomical_value = civ_0_probabilities[0] - success_probabilities[0]
    preindustrial_as_extinction_proportion = (preindustrial_in_terms_of_astronomical_value) / civ_0_probabilities[0]
    industrial_in_terms_of_astronomical_value = civ_0_probabilities[0] - success_probabilities[1]
    industrial_as_extinction_proportion = (industrial_in_terms_of_astronomical_value) / civ_0_probabilities[0]
    industrial_as_preindustrial_proportion = industrial_in_terms_of_astronomical_value / preindustrial_in_terms_of_astronomical_value

    if not file_exists:
        # Write header only if file is empty or doesn't exist
        writer.writerow(
            [' ', 'Notes', 'Industrial-1 as proportion of Preindustrial-1', 'X(preindustrial)', 'X(industrial)', 'V(preindustrial)', 'V(industrial)']
            # Leave first two columns for people to enter their
            # names/descriptions of their params etc, and next four to show costs of a regression to
            # preindustrial/industrial relative to extinction to to astronomical value
            + all_numbered_states
            + ['MAX_PLANETS', 'MAX_CIVILISATIONS', 'MAX_PROGRESS_YEARS']
            + Params().get_param_keys())
    writer.writerow(
        [' ', ' ', industrial_as_preindustrial_proportion]
        + [preindustrial_as_extinction_proportion, industrial_as_extinction_proportion]
        + [preindustrial_in_terms_of_astronomical_value, industrial_in_terms_of_astronomical_value]
        + all_success_probabilities
        + [constant.MAX_PLANETS, constant.MAX_CIVILISATIONS, constant.MAX_PROGRESS_YEARS]
        + Params().get_param_values())

os.system('echo -n "\a"') # Make a beep noise to indicate the program has finished
