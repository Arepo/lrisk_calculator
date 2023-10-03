import streamlit as st
import pandas as pd
import numpy as np
from calculators.simple_calc.simple_calc import SimpleCalc

# calc = SimpleCalc()


# Make values percentages

# TODO Reword headers as questions. What is the probability of getting to preindustrial from prequilibrium? Eg. what is the probability of getting to industrial from preindustrial?

# TODO Decide how to select starting values? Is the value of making it look intuitive worth the cost of priming?

st.write("""**Adjust the values to see how the probability of human descendants becoming interstellar changes based on your credences.**
         """)

col1, col2, col3 = st.columns(3)

with col1:
    # First Section: Preindustrial given Pre-Equilibrium

    if 'preindustrial_given_pre_equilibrium' not in st.session_state:
        st.session_state.preindustrial_given_pre_equilibrium = 0.5

    def update_preindustrial():
        st.session_state.preindustrial_given_pre_equilibrium = round(st.session_state['pre_equilibrium_input_value'], 5)

    st.number_input(label='What is the probability of getting to preindustrial from prequilibrium?',
                    value=st.session_state.preindustrial_given_pre_equilibrium,
                    min_value=0.0,
                    max_value=1.0,
                    step=0.05,
                    format="%.3f",
                    on_change=update_preindustrial,
                    key='pre_equilibrium_input_value')

    st.number_input(label='Extinction given Pre-Equilibrium',
                    min_value=0.0,
                    max_value=1.0,
                    value=round(1 - st.session_state.preindustrial_given_pre_equilibrium, 5),
                    disabled=True, format="%f")


# Second Section: Industrial given Preindustrial

with col2:

    if 'industrial_given_preindustrial' not in st.session_state:
        st.session_state.industrial_given_preindustrial = 0.5

    def update_preindustrial():
        st.session_state.industrial_given_preindustrial = round(st.session_state['preindustrial_input_value'], 5)

    st.number_input(label='Industrial given Preindustrial',
                    value=st.session_state.industrial_given_preindustrial,
                    min_value=0.0,
                    max_value=1.0,
                    step=0.05,
                    format="%.3f",
                    on_change=update_preindustrial,
                    key='preindustrial_input_value')

    st.number_input(label='Extinction given Preindustrial',
                    min_value=0.0,
                    max_value=1.0,
                    value=round(1 - st.session_state.industrial_given_preindustrial, 5),
                    disabled=True,
                    format="%.3f")

# Third Section: Future perils given preindustrial

with col3:

    if 'future_perils_given_industrial' not in st.session_state:
        st.session_state.future_perils_given_industrial = 0.5

    def update_perils_from_number():
        st.session_state.future_perils_given_industrial = round(st.session_state['future_perils_num_input_value'], 5)

    st.number_input(label='Future perils given Industrial',
                    value=st.session_state.future_perils_given_industrial,
                    min_value=0.0,
                    max_value=1.0,
                    step=0.05,
                    format="%.3f",
                    on_change=update_perils_from_number,
                    key='future_perils_num_input_value')

    st.number_input(label='Extinction given Industrial',
                    min_value=0.0,
                    max_value=1.0,
                    value=round(1 - st.session_state.future_perils_given_industrial, 5),
                    disabled=True,
                    format="%.3f")


# # Section 4: Transitions from present perils

'---'

st.markdown("""## Transitional probabilities from present perils states
""")

def multiplanetary_given_present_perils():
    if present_perils_remainder() >= 0:
        return present_perils_remainder()
    return .0

def present_perils_remainder():
    return round(1 - sum([st.session_state[transition] for transition in specifiable_transitions_from_present_perils]),
                 5)

specifiable_transitions_from_present_perils = [
    'Extinction given present perils',
    'Pre_equilibrium given present perils',
    'Preindustrial given present perils',
    'Industrial given present perils',
    'Future perils given present perils',
    'Interstellar given present perils'
]

for transition in specifiable_transitions_from_present_perils:
    if transition not in st.session_state:
        st.session_state[transition] = 0.1

def update_transitions_given_present_perils(transition_name):
    other_transitions = [transition for transition in specifiable_transitions_from_present_perils if transition != transition_name]
    st.session_state[transition_name] = round(st.session_state[transition_name + '_value'], 5)
    # Reduce the values of the other transitions as much as need be to ensure that the sum of all transitions is 1
    excess_probability = -present_perils_remainder()
    for transition in reversed(other_transitions):
        if excess_probability > 0 and excess_probability <= st.session_state[transition]:
            # The difference is low enough to be absorbed by this transition, so we're done adjusting sliders
            st.session_state[transition] += round(present_perils_remainder(), 5)
            break
        elif excess_probability > 0:
            # Reduce this transition to 0 and continue to the next
            excess_probability -= round(st.session_state[transition], 5)
            st.session_state[transition] = .0
        # If excess_probability is negative or 0, it will be added to the multiplanetary transition probability

def make_on_change_present_perils_callback(transition_name):
    # Create a function to allow us to pass the transition name to the callback
    def callback():
        update_transitions_given_present_perils(transition_name)
    return callback

if 'present_perils_remainder' not in st.session_state:
    st.session_state.present_perils_remainder = present_perils_remainder()

for transition in specifiable_transitions_from_present_perils:
    st.number_input(
        label=transition,
        value=st.session_state[transition],
        min_value=0.0,
        max_value=1.0,
        step=0.05,
        format="%.3f",
        on_change=make_on_change_present_perils_callback(transition),
        key=transition + '_value'
        )

st.number_input(label=f'Multiplanetary given present perils',
        value=multiplanetary_given_present_perils(),
        min_value=0.0,
        max_value=1.0,
        format="%.3f",
        disabled = True
        )




# Section 5 - Transitional probabilities from future perils states

'---'

st.markdown("""## Transitional probabilities from future perils states
""")

def multiplanetary_given_future_perils():
    if future_perils_remainder() >= 0:
        return future_perils_remainder()
    return .0

def future_perils_remainder():
    return round(1 - sum([st.session_state[transition] for transition in specifiable_transitions_from_future_perils]),
                 5)

specifiable_transitions_from_future_perils = [
    'Extinction given future perils',
    'Pre_equilibrium given future perils',
    'Preindustrial given future perils',
    'Industrial given future perils',
    'Interstellar given future perils'
]

for transition in specifiable_transitions_from_future_perils:
    if transition not in st.session_state:
        st.session_state[transition] = 0.1

def update_transitions_given_future_perils(transition_name):
    other_transitions = [transition for transition in specifiable_transitions_from_future_perils if transition != transition_name]
    st.session_state[transition_name] = round(st.session_state[transition_name + '_value'], 5)
    # Reduce the values of the other transitions as much as need be to ensure that the sum of all transitions is 1
    excess_probability = -future_perils_remainder()
    for transition in reversed(other_transitions):
        if excess_probability > 0 and excess_probability <= st.session_state[transition]:
            # The difference is low enough to be absorbed by this transition, so we're done adjusting sliders
            st.session_state[transition] += round(future_perils_remainder(), 5)
            break
        elif excess_probability > 0:
            # Reduce this transition to 0 and continue to the next
            excess_probability -= round(st.session_state[transition], 5)
            st.session_state[transition] = .0
        # If excess_probability is negative or 0, it will be added to the multiplanetary transition probability

def make_on_change_future_perils_callback(transition_name):
    # Create a function to allow us to pass the transition name to the callback
    def callback():
        update_transitions_given_future_perils(transition_name)
    return callback

if 'future_perils_remainder' not in st.session_state:
    st.session_state.future_perils_remainder = future_perils_remainder()

for transition in specifiable_transitions_from_future_perils:
    st.number_input(
        label=transition,
        value=st.session_state[transition],
        min_value=0.0,
        max_value=1.0,
        step=0.05,
        format="%.3f",
        on_change=make_on_change_future_perils_callback(transition),
        key=transition + '_value'
        )

st.number_input(label=f'Multiplanetary given future perils',
        value=multiplanetary_given_future_perils(),
        min_value=0.0,
        max_value=1.0,
        format="%.3f",
        disabled = True
        )


# Section 6 Transitional probabilities from multiplanetary states

'---'

st.markdown("""## Transitional probabilities from multiplanetary states
""")

def interstellar_given_multiplanetary():
    if multiplanetary_remainder() >= 0:
        return multiplanetary_remainder()
    return .0

def multiplanetary_remainder():
    return round(1 - sum([st.session_state[transition] for transition in specifiable_transitions_from_multiplanetary]),
                 5)

specifiable_transitions_from_multiplanetary = [
    'Extinction given multiplanetary',
    'Pre_equilibrium given multiplanetary',
    'Preindustrial given multiplanetary',
    'Industrial given multiplanetary',
    'Future perils given multiplanetary',
]

for transition in specifiable_transitions_from_multiplanetary:
    if transition not in st.session_state:
        st.session_state[transition] = 0.1

def update_multiplanetary_transitions(transition_name):
    other_transitions = [transition for transition in specifiable_transitions_from_multiplanetary if transition != transition_name]
    st.session_state[transition_name] = round(st.session_state[transition_name + '_value'], 5)
    # Reduce the values of the other transitions as much as need be to ensure that the sum of all transitions is 1
    excess_probability = round(-multiplanetary_remainder(), 5)
    for transition in reversed(other_transitions):
        if excess_probability > 0 and excess_probability <= st.session_state[transition]:
            # The difference is low enough to be absorbed by this transition, so we're done adjusting sliders
            st.session_state[transition] += round(multiplanetary_remainder(), 5)
            break
        elif excess_probability > 0:
            # Reduce this transition to 0 and continue to the next
            excess_probability -= round(st.session_state[transition], 5)
            st.session_state[transition] = .0
        # If excess_probability is negative or 0, it will be added to the multiplanetary transition probability

def make_on_change_multiplanetary_callback(transition_name):
    # Create a function to allow us to pass the transition name to the callback
    def callback():
        update_multiplanetary_transitions(transition_name)
    return callback

if 'multiplanetary_remainder' not in st.session_state:
    st.session_state.multiplanetary_remainder = multiplanetary_remainder()

for transition in specifiable_transitions_from_multiplanetary:
    st.number_input(
        label=transition,
        value=st.session_state[transition],
        min_value=0.0,
        max_value=1.0,
        step=0.05,
        format="%.3f",
        on_change=make_on_change_multiplanetary_callback(transition),
        key=transition + '_value'
        )

st.number_input(label=f'Interstellar given multiplanetary',
        value=interstellar_given_multiplanetary(),
        min_value=0.0,
        max_value=1.0,
        format="%.3f",
        disabled = True
        )











all_transition_probabilities = {
    'extinction_given_pre_equilibrium': 1 - st.session_state.preindustrial_given_pre_equilibrium,
    'extinction_given_preindustrial': 1 - st.session_state.industrial_given_preindustrial,
    'extinction_given_industrial': 1 - st.session_state.future_perils_given_industrial,

    'extinction_given_present_perils': st.session_state['Extinction given present perils'],
    'pre_equilibrium_given_present_perils': st.session_state['Pre_equilibrium given present perils'],
    'preindustrial_given_present_perils': st.session_state['Preindustrial given present perils'],
    'industrial_given_present_perils': st.session_state['Industrial given present perils'],
    'future_perils_given_present_perils': st.session_state['Future perils given present perils'],
    'interstellar_given_present_perils': st.session_state['Interstellar given present perils'],

    'extinction_given_future_perils': st.session_state['Extinction given future perils'],
    'pre_equilibrium_given_future_perils': st.session_state['Pre_equilibrium given future perils'],
    'preindustrial_given_future_perils': st.session_state['Preindustrial given future perils'],
    'industrial_given_future_perils': st.session_state['Industrial given future perils'],
    'interstellar_given_future_perils': st.session_state['Interstellar given future perils'],

    'extinction_given_multiplanetary': st.session_state['Extinction given multiplanetary'],
    'pre_equilibrium_given_multiplanetary': st.session_state['Pre_equilibrium given multiplanetary'],
    'preindustrial_given_multiplanetary': st.session_state['Preindustrial given multiplanetary'],
    'industrial_given_multiplanetary': st.session_state['Industrial given multiplanetary'],
    'future_perils_given_multiplanetary': st.session_state['Future perils given multiplanetary'],
}

calc = SimpleCalc(**all_transition_probabilities)
mc = calc.markov_chain()
success_probabilities = mc.absorption_probabilities()[1]
data = dict(zip(mc.transient_states, success_probabilities))
# breakpoint()
st.bar_chart(data)

# string = f"""
#     On your assumptions...
#     The probability of becoming interstellar from a pre_equilibrium state = { calc.net_interstellar_from_pre_equilibrium() }
#     The probability of becoming interstellar from a preindustrial state = { calc.net_interstellar_from_preindustrial() }
#     The probability of becoming interstellar from an industrial state = { calc.net_interstellar_from_industrial() }
#     The probability of becoming interstellar from a time of perils state = { calc.net_interstellar_from_perils() }</p>
#     The probability of becoming interstellar from a multiplanetary state = { calc.net_interstellar_from_multiplanetary() }</p>

#     *****

#     Therefore, if we consider eventual extinction and interstellar colonisation the only two outcomes...
#     a castatrophe that put us into a pre-equilibrium state would be { calc.pre_equilibrium_probability_reduction() } as bad as an extinction event
#     a castatrophe that put us into a preindustrial state would be { calc.preindustrial_probability_reduction() } as bad as an extinction event
#     a castatrophe that put us into an industrial state would be { calc.industrial_probability_reduction() } as bad as an extinction event
#     and if we reached a multiplanetary state, it would increase our chance of becoming interstellar by { calc.multiplanetary_probability_increase() }
# """

# breakpoint()

st.write(f"""
    On your assumptions...

    *****

    Therefore, if we consider eventual extinction and interstellar colonisation the only two outcomes...
    a castatrophe that put us into a pre-equilibrium state would be { calc.pre_equilibrium_probability_reduction() } as bad as an extinction event
    a castatrophe that put us into a preindustrial state would be { calc.preindustrial_probability_reduction() } as bad as an extinction event
    a castatrophe that put us into an industrial state would be { calc.industrial_probability_reduction() } as bad as an extinction event
    and if we reached a multiplanetary state, it would increase our chance of becoming interstellar by { calc.multiplanetary_probability_increase() }
""")
