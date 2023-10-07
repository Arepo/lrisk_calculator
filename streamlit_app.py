import streamlit as st
import plotly.express as px
import numpy as np
import pandas as pd
from calculators.simple_calc.simple_calc import SimpleCalc

# calc = SimpleCalc()


# Make values percentages

# TODO Line up bar chart columns

# TODO Reword headers as questions. What is the probability of getting to preindustrial from prequilibrium? Eg. what is the probability of getting to industrial from preindustrial?

# TODO Decide how to select starting values? Is the value of making it look intuitive worth the cost of priming?

st.write("""**Adjust the values to see how the probability of human descendants becoming interstellar changes based on your credences.**
         """)

col1, col2 = st.columns(2, gap="large")


# First Section: Industrial given Preindus  trial

with col1:

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

# Second Section: Future perils given preindustrial

with col2:

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


# # Section 3: Transitions from present perils

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




# Section 4 - Transitional probabilities from future perils states

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


# Section 5 Transitional probabilities from multiplanetary states

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
    'extinction_given_preindustrial': 1 - st.session_state.industrial_given_preindustrial,
    'extinction_given_industrial': 1 - st.session_state.future_perils_given_industrial,

    'extinction_given_present_perils': st.session_state['Extinction given present perils'],
    'preindustrial_given_present_perils': st.session_state['Preindustrial given present perils'],
    'industrial_given_present_perils': st.session_state['Industrial given present perils'],
    'future_perils_given_present_perils': st.session_state['Future perils given present perils'],
    'interstellar_given_present_perils': st.session_state['Interstellar given present perils'],

    'extinction_given_future_perils': st.session_state['Extinction given future perils'],
    'preindustrial_given_future_perils': st.session_state['Preindustrial given future perils'],
    'industrial_given_future_perils': st.session_state['Industrial given future perils'],
    'interstellar_given_future_perils': st.session_state['Interstellar given future perils'],

    'extinction_given_multiplanetary': st.session_state['Extinction given multiplanetary'],
    'preindustrial_given_multiplanetary': st.session_state['Preindustrial given multiplanetary'],
    'industrial_given_multiplanetary': st.session_state['Industrial given multiplanetary'],
    'future_perils_given_multiplanetary': st.session_state['Future perils given multiplanetary'],
}

calc = SimpleCalc(**all_transition_probabilities)
mc = calc.markov_chain()
success_probabilities = mc.absorption_probabilities()[1]
data = dict(zip(mc.transient_states, success_probabilities))
probabilities_df = pd.DataFrame(data.items(), columns=['Civilisation state', 'Probability of becoming interstellar'])

# st.bar_chart(data)
probabilties_fig = px.bar(probabilities_df, x='Civilisation state', y='Probability of becoming interstellar')
st.plotly_chart(probabilties_fig, use_container_width=True)

# st.markdown("""
# Let $V$ be the value we imagine of humans colonising the stars. Assume that by the time we become interstellar, we're effectively safe.

# Let $T_{state}$ be some event that transitions us to some other state than 'present perils', for example 'nuclear war that destroys all industry', such that $P(V | T_{state})$ = the probability of becoming interstellar from the state $T_{state}$ would transition us to, and such that $P(V | !T_{state})$ is the probability of becoming interstellar from our current state, given that $T_{state}$ doesn't occur.

# We can then express the expected value of $T_{state}$ in terms of $V$, as $$V \cdot (P[V | T_{state}] - P[V | \neg T_{state}])$$""", unsafe_allow_html=True)

st.markdown("""
Let $V$ be the value we imagine of humans becoming interstellar, assume that by the time we reach that point we're highly likely to expand to multiple stars if we have any chance of doing so (see [post]() for rationale for this).

Let $T_{\\text{state}}$ be some event that transitions us to some other state than 'present perils', for example, 'nuclear war that destroys all industry'. Thus, we define:
- $P(V | T_{\\text{state}})$ as the probability of becoming interstellar from the state $T_{\\text{state}}$ would transition us to,
- $P(V | \\neg T_{\\text{state}})$ as the probability of becoming interstellar from our current state, given that $T_{\\text{state}}$ doesn't occur.

We can then express the expected value of $T_{\\text{state}}$ in terms of $V$, as
""", unsafe_allow_html=True)
st.latex(r'''
\mathbb{E}[T_{\text{state}}] = V \cdot \left( P[V | T_{\text{state}}] - P[V | \neg T_{\text{state}}] \right)
         '''
)

difference_df = pd.DataFrame(calc.probability_differences().items(), columns=['State', 'Value of transitioning to state (as a multiple of V)'])
difference_fig = px.bar(difference_df, x='State', y='Value of transitioning to state (as a multiple of V)')
st.plotly_chart(difference_fig, use_container_width=True)

# TODO This example seems priming
st.markdown("""
We might also represent $T_{\\text{state}}$ as having some fraction of the cost of an extinction event $T_{\\text{extinction}}$. For example, if you think we have a 60% chance of becoming interstellar from our current state, and a 50% chance that we have to restart the time of perils would transition us to, the loss from $X$ would be $0.6V$, and the loss of transitioning to as a percentage of the loss of value from $T_{\\text{extinction}}$ would be $100\\frac{(0.6 - 0.5)}{0.6} \\approx 17\\%$.

Negative values are how *good* the transition is, relative to the badness of extinction (note that since in this model we assume extinction is the worst outcome, positive percentages are max 100% - the badness of extinction - but negative values can theoretically be higher if the current chance of success is less than 50%).
""", unsafe_allow_html=True)

proportion_df = pd.DataFrame(calc.probability_proportion_differences().items(), columns=['State', 'Cost of transitioning to state as a percentage of the cost of extinction'])
proportion_fig = px.bar(proportion_df, x='State', y='Cost of transitioning to state as a percentage of the cost of extinction')
st.plotly_chart(proportion_fig, use_container_width=True)

st.markdown("""If you find it more convenient to think of a specific event rather than a specific transition, you can enter your credences for that event transitioning us to each state below given its realisation, to see the expected value of that event in terms of $V$.""")

states = [
    'Extinction',
    'Preindustrial',
    'Industrial',
    'Future perils',
    'Multiplanetary',
    'Interstellar'
]

for state in states:
    if state not in st.session_state:
        st.session_state[state] = 0.1

def no_transition_given_event():
    if abstract_event_remainder() >= 0:
        return abstract_event_remainder()
    return .0

def abstract_event_remainder():
    return round(1 - sum([st.session_state[state] for state in states]),
                 5)

def update_abstract_transitions(state_name):
    other_states = [state for state in states if state != state_name]
    st.session_state[state_name] = round(st.session_state[state_name + '_value'], 5)
    # Reduce the values of the other states as much as need be to ensure that the sum of all states is 1
    excess_probability = round(-abstract_event_remainder(), 5)
    for state in reversed(other_states):
        if excess_probability > 0 and excess_probability <= st.session_state[state]:
            # The difference is low enough to be absorbed by this state, so we're done adjusting sliders
            st.session_state[state] += round(abstract_event_remainder(), 5)
            break
        elif excess_probability > 0:
            # Reduce this state to 0 and continue to the next
            excess_probability -= round(st.session_state[state], 5)
            st.session_state[state] = .0
        # If excess_probability is negative or 0, it will be added to the multiplanetary state probability


def make_on_change_abstract_transition_callback(state):
    # Create a function to allow us to pass the state name to the callback
    def callback():
        update_abstract_transitions(state)
    return callback

col1, col2, col3 = st.columns(3, gap="small")

for state, col in zip(states[:3], (col1, col2, col3)):
    with col:
        st.number_input(
            label=state,
            value=st.session_state[state],
            min_value=0.0,
            max_value=1.0,
            step=0.05,
            format="%.3f",
            on_change=make_on_change_abstract_transition_callback(state),
            key=state + '_value'
            )

for state, col in zip(states[3:], (col1, col2, col3)):
    with col:
        st.number_input(
            label=state,
            value=st.session_state[state],
            min_value=0.0,
            max_value=1.0,
            step=0.05,
            format="%.3f",
            on_change=make_on_change_abstract_transition_callback(state),
            key=state + '_value'
            )

st.number_input(label=f'Probability of remaining in current state given event',
        value=no_transition_given_event(),
        min_value=0.0,
        max_value=1.0,
        format="%.3f",
        disabled = True
        )

array1 = np.array(list(calc.probability_differences().values()))
array2 = np.array([st.session_state[state] for state in states])
result = np.round(np.dot(array1, array2), 3)
# result2 = str(np.round(calc.net_interstellar_from_present_perils() - result) / calc.net_interstellar_from_present_perils(), 3) + '%'
result2 = - np.round(result / calc.net_interstellar_from_present_perils(), 3)


st.markdown("""The expected value of the event in terms of $V$ is ${0}V$, or {1}x as bad as extinction""".format(result, result2))
