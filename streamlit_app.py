# pylint: disable=line-too-long

import streamlit as st
import plotly.express as px
import numpy as np
import pandas as pd
from calculators.simple_calc.simple_calc import SimpleCalc
st.set_page_config(
        page_title="L-risk calculator",
)

all_transitions = {
    'from preindustrial': [
        'Extinction',
        'Industrial'
    ],
    'from industrial': [
        'Extinction',
        'Future time of perils'
    ],
    'from present perils': [
        'Extinction',
        'Preindustrial',
        'Industrial',
        "A 'minor' technological regression†",
        'Multiplanetary††',
        'Interstellar/existential security'
    ],
    'from future perils': [
        'Extinction',
        'Preindustrial',
        'Industrial',
        'Multiplanetary††',
        'Interstellar/existential security'
    ],
    'from multiplanetary': [
        'Extinction',
        'Preindustrial',
        'Industrial',
        'Future perils',
        'Interstellar/existential security'
    ],
    'from abstract state': [
        'Extinction',
        'Preindustrial',
        'Industrial',
        "A 'minor' technological regression†",
        'Multiplanetary††',
        'Interstellar/existential security'
    ]
}

obelus_string = """† An event that technologically regressed us the equivalent of about about 50-100 years, but left us with nuclear arsenals or other comparatively destructive weaponry.

†† Civilisation has established self-sustaining settlements on more than one planet."""

last_listed_transitions = [transitions[-1] + " " + origin_state for origin_state, transitions in all_transitions.items()]

# Get a flattened list of all transitions
target_states = [target_state + " " + origin_state for origin_state, target_state_list in all_transitions.items()
                 for target_state in target_state_list]

common_form_values = {
    'min_value': 0.0,
    'max_value': 1.0,
    'step': 0.01,
    'format': "%.2f",
}

def update_transitions(transition_name, current_state):
    other_transitions = [transition for transition in all_transitions[current_state]
                         if transition != transition_name][::-1]
    st.session_state[transition_name + " " + current_state] = st.session_state[
        transition_name + " " + current_state + '_from_input']

    # Given the change, determine how much we need to adjust other transitional probabilities to
    # ensure they sum to 1
    excess_probability = sum([st.session_state[transition + " " + current_state] for transition in all_transitions[current_state]]) - 1

    for transition in other_transitions:
        # If excess_probability is positive that means we've lowered the value of the transition
        # we're updating, and need to raise another
        if excess_probability > 0 and excess_probability <= st.session_state[transition  + " " + current_state]:
            # The difference is low enough to be absorbed by this transition, so we're done
            # adjusting sliders
            st.session_state[transition + " " + current_state] += -excess_probability
            break
        elif excess_probability > 0:
            # Reduce this transition to 0 and continue to the next
            excess_probability -= st.session_state[transition + " " + current_state]
            st.session_state[transition + " " + current_state] = .0
    # If excess_probability is negative or 0, we add the difference it to extinction unless it's
    # extinction we modified, then we add it to the next-most regressed state)
    if excess_probability < 0 and transition_name + " " + current_state in last_listed_transitions:
        st.session_state[all_transitions[current_state][-2] + " " + current_state] -= excess_probability
    elif excess_probability < 0:
        st.session_state[all_transitions[current_state][-1] + " " + current_state] -= excess_probability

def get_remainder_value(remainder_function):
    return max(remainder_function(), .0)

for session_value in target_states:
    if session_value not in st.session_state and session_value in last_listed_transitions:

        st.session_state[session_value] = 1.0
    elif session_value not in st.session_state:
        st.session_state[session_value] = .0



# Make values percentages

# TODO Reword headers as questions. What is the probability of getting to preindustrial from
# prequilibrium? Eg. what is the probability of getting to industrial from preindustrial?

# TODO Decide how to select starting values? Is the value of making it look intuitive worth the cost
# of priming?

st.write("#### Adjust the values to see how the probability of human descendants becoming interstellar"\
         "changes based on your credences.")

col1, col2 = st.columns(2, gap="large")


# First Section: Industrial given Preindustrial

with col1:
    st.write("""**What is the probability any time civilisation reverts to a preindustrial state,
             that it directly transitions to either of the following states (assuming those are the
             only possible outcomes)?**""")

    def make_on_change_preindustrial_callback(transition_name):
        # Create a function to allow us to pass the transition name to the callback
        def callback():
            update_transitions(transition_name, 'from preindustrial')
        return callback

    for transition in all_transitions['from preindustrial']:
        st.slider(
            label=transition,
            value=st.session_state[transition + " " +  'from preindustrial'],
            on_change=make_on_change_preindustrial_callback(transition),
            key=transition + " " + 'from preindustrial' + "_from_input",
            **common_form_values)

    # def update_preindustrial_from_slider():
    #     st.session_state['Industrial given preindustrial'] = st.session_state['preindustrial_slider_value']

    # def update_preindustrial_from_number():
    #     st.session_state['Industrial given preindustrial'] = st.session_state['preindustrial_num_input_value']

    # st.slider(label='Extinction (slider) given Preindustrial',
    #     value=1 - st.session_state['Industrial given preindustrial'],
    #     **common_form_values)

    # st.slider(
    #     label='Industrial (Slider) given Preindustrial',
    #     value=st.session_state['Industrial given preindustrial'],
    #     on_change=update_preindustrial_from_slider,
    #     key='preindustrial_slider_value' + "_from_input",
    #     **common_form_values)

    # st.number_input(label='Industrial (Number) given Preindustrial',
    #                 value=st.session_state['Industrial given preindustrial'],
    #                 on_change=update_preindustrial_from_number,
    #                 key='preindustrial_input_value' + "_from_input",
    #                 **common_form_values)

    # st.number_input(label='Extinction (number) given Preindustrial',
    #             value=round(1 - st.session_state['Industrial given preindustrial'], 5),
    #             disabled=True,
    #             **common_form_values)





    # def update_preindustrial():
    #     st.session_state['Industrial given preindustrial'] = round(st.session_state['preindustrial_input_value'], 5)








# Second Section: Future perils given preindustrial

with col2:
    st.write("""**What is the probability any time civilisation either enters an industrial
             state that it directly transitions to
             either of the following states (assuming those are the only possible outcomes)?**""")

    def make_on_change_industrial_callback(transition_name):
        # Create a function to allow us to pass the transition name to the callback
        def callback():
            update_transitions(transition_name, 'from industrial')
        return callback

    for transition in all_transitions['from industrial']:
        st.slider(
            label=transition,
            value=st.session_state[transition + " " + 'from industrial'],
            on_change=make_on_change_industrial_callback(transition),
            key=transition + " " + 'from industrial' + "_from_input",
            **common_form_values)

    # st.number_input(
    #     label='Future perils (number) given Industrial',
    #     value=st.session_state['Future perils given industrial'],
    #     on_change=update_perils_from_number,
    #     key='future_perils_num_input_value' + "_from_input",
    #     **common_form_values)

    # st.number_input(
    #     label='Extinction (number) given Industrial',
    #     value=round(1 - st.session_state['Future perils given industrial'], 5),
    #     disabled=True,
    #     **common_form_values)


# # Section 3: Transitions from present perils

'---'

st.markdown("""## Transitional probabilities from the current 'time of perils'
""")

st.write("""**From our current state (postindustrial, dependent on a single planet, high-tech weaponry available),
         what is the probability that civilisation transitions directly to the following states?
         (assuming those are the only possible outcomes)?**""")

def make_on_change_present_perils_callback(transition_name):
    # Create a function to allow us to pass the transition name to the callback
    def callback():
        update_transitions(transition_name, 'from present perils')
        for state in all_transitions['from present perils']:
            st.session_state[state + " " + 'from abstract state'] = st.session_state[state + " " + 'from present perils']
    return callback

# for transition in transitions['from present perils']:
#     st.number_input(
#         label=transition,
#         value=st.session_state[transition],
#         on_change=make_on_change_present_perils_callback(transition),
#         key=transition + '_value' + "_from_input",
#         **common_form_values)

# st.number_input(label=f'Multiplanetary given present perils',
#         value=get_remainder_value(present_perils_remainder),
#         disabled = True,
#         **common_form_values)

for transition in all_transitions['from present perils']:
    st.slider(
        label=transition,
        value=st.session_state[transition + " " + 'from present perils'],
        on_change=make_on_change_present_perils_callback(transition),
        key=transition + " " + 'from present perils' + "_from_input",
        **common_form_values)

st.write(obelus_string)

# Section 4 - Transitional probabilities from future perils states

'---'

st.markdown("""## Transitional probabilities from any future 'times of perils'
""")

st.write("""**If future civilisations ever regain technology resembling our current level
         (postindustrial, dependent on a single planet, high-tech weaponry available), what is the probability
         that they will transitions directly to the following states?
         (assuming those are the only possible outcomes)?**""")

def make_on_change_future_perils_callback(transition_name):
    # Create a function to allow us to pass the transition name to the callback
    def callback():
        update_transitions(transition_name, 'from future perils')
    return callback

# for transition in transitions['from future perils']:
#     st.number_input(
#         label=transition,
#         value=st.session_state[transition],
#         on_change=make_on_change_future_perils_callback(transition),
#         key=transition + '_value' + "_from_input",
#         **common_form_values)

# st.number_input(label=f'Multiplanetary given future perils',
#         value=get_remainder_value(future_perils_remainder),
#         disabled = True,
#         **common_form_values)

for transition in all_transitions['from future perils']:
    st.slider(
    label=transition,
    value=st.session_state[transition + " " + 'from future perils'],
    on_change=make_on_change_future_perils_callback(transition),
    key=transition + " " + 'from future perils' + "_from_input",
    **common_form_values)



# Section 5 Transitional probabilities from multiplanetary states

'---'

st.markdown("""## Transitional probabilities from multiplanetary states""")

st.write("""**If civilisation ever develops self-sustaining settlements on more than one planets),
         what is the probability that they will transitions directly to the following states?
         (assuming those are the only possible outcomes)?**""")

def make_on_change_multiplanetary_callback(transition_name):
    # Create a function to allow us to pass the transition name to the callback
    def callback():
        update_transitions(transition_name, 'from multiplanetary')
    return callback

# for transition in transitions['from multiplanetary']:
#     st.number_input(
#         label=transition,
#         value=st.session_state[transition],
#         on_change=make_on_change_multiplanetary_callback(transition),
#         key=transition + '_value' + "_from_input",
#         **common_form_values)

# st.number_input(label=f'Interstellar given multiplanetary',
#         value=get_remainder_value(multiplanetary_remainder),
#         disabled = True,
#         **common_form_values)

for transition in all_transitions['from multiplanetary']:
    st.slider(
    label=transition,
    value=st.session_state[transition + " " + 'from multiplanetary'],
    on_change=make_on_change_multiplanetary_callback(transition),
    key=transition + " " + 'from multiplanetary' + "_from_input",
    **common_form_values)

# st.slider(
#     label='Interstellar given multiplanetary',
#     value=get_remainder_value(multiplanetary_remainder),
#     disabled=True,
#     **common_form_values)

'---'

st.markdown("""## Comparing the value of outcomes""")

all_transition_probabilities = {
    'extinction_given_preindustrial': st.session_state['Extinction from preindustrial'],
    'extinction_given_industrial': st.session_state['Extinction from industrial'],

    'extinction_given_present_perils': st.session_state['Extinction from present perils'],
    'preindustrial_given_present_perils': st.session_state['Preindustrial from present perils'],
    'industrial_given_present_perils': st.session_state['Industrial from present perils'],
    'future_perils_given_present_perils': st.session_state["A 'minor' technological regression† from present perils"],
    'interstellar_given_present_perils': st.session_state['Interstellar/existential security from present perils'],

    'extinction_given_future_perils': st.session_state['Extinction from future perils'],
    'preindustrial_given_future_perils': st.session_state['Preindustrial from future perils'],
    'industrial_given_future_perils': st.session_state['Industrial from future perils'],
    'interstellar_given_future_perils': st.session_state['Interstellar/existential security from future perils'],

    'extinction_given_multiplanetary': st.session_state['Extinction from multiplanetary'],
    'preindustrial_given_multiplanetary': st.session_state['Preindustrial from multiplanetary'],
    'industrial_given_multiplanetary': st.session_state['Industrial from multiplanetary'],
    'future_perils_given_multiplanetary': st.session_state['Future perils from multiplanetary'],
}

calc = SimpleCalc(**all_transition_probabilities)
mc = calc.markov_chain()
success_probabilities = mc.absorption_probabilities()[1]
data = dict(zip(mc.transient_states, success_probabilities))
probabilities_df = pd.DataFrame(
    data.items(),
    columns=['Civilisation state', 'Probability of becoming interstellar'])

probabilties_fig = px.bar(probabilities_df,
                          x='Civilisation state',
                          y='Probability of becoming interstellar')
st.plotly_chart(probabilties_fig, use_container_width=True)

st.markdown("""
Let $V$ be the value we imagine of humans becoming interstellar, assume that by
the time we reach that point we're highly likely to expand to multiple stars if
we have any chance of doing so (see [post]() for rationale for this).

Let $T_{\\text{state}}$ be some event that transitions us to some other state
than 'present perils', for example, 'nuclear war that destroys all industry in
next 10 years' or 'humans develop self-sustaining offworld settlement before
2070'.
Thus, we define:
- $P(V | T_{\\text{state}})$ as the probability of becoming interstellar from
the state $T_{\\text{state}}$ would transition us to,
- $P(V | \\neg T_{\\text{state}})$ as the probability of becoming interstellar
from our current state, given that $T_{\\text{state}}$ doesn't occur.

We can then express the expected value of $T_{\\text{state}}$ in terms of $V$, as
""", unsafe_allow_html=True)
st.latex(r'''
\mathbb{E}[T_{\text{state}}] = V \cdot \left( P[V | T_{\text{state}}] - P[V | \neg T_{\text{state}}] \right)
''')

difference_df = pd.DataFrame(
    calc.probability_differences().items(),
    columns=['State', 'Value of transitioning to state (as a multiple of V)'])
difference_fig = px.bar(
    difference_df,
    x='State',
    y='Value of transitioning to state (as a multiple of V)')
st.plotly_chart(difference_fig, use_container_width=True)

# TODO This example seems priming
st.markdown("""
We might also represent $T_{\\text{state}}$ as having some fraction of the cost
of an extinction event $T_{\\text{extinction}}$. For example, if you think we
have a 60% chance of becoming interstellar from our current state, and a 50%
chance that we have to restart the time of perils would transition us to, the
loss from $X$ would be $0.6V$, and the loss of transitioning to as a percentage
of the loss of value from $T_{\\text{extinction}}$ would be $100\\frac{(0.6 - 0.5)}{0.6} \\approx 17\\%$.

Negative values are how *good* the transition is, relative to the badness of
extinction (note that since in this model we assume extinction is the worst
outcome, positive percentages are max 100% - the badness of extinction - but
negative values can theoretically be lower than -100% if the current chance of
success is less than 50%).
""", unsafe_allow_html=True)

proportion_df = pd.DataFrame(
    calc.probability_proportion_differences().items(),
    columns=['State', 'Cost of transitioning to state as a percentage of the cost of extinction'])
proportion_fig = px.bar(
    proportion_df,
    x='State',
    y='Cost of transitioning to state as a percentage of the cost of extinction')
st.plotly_chart(proportion_fig, use_container_width=True)

st.markdown("""An alternative way to think about a specific event, rather than being a transition,
is to reimagine your credences of the transitions from our current time of perils conditional on the
event happening, to compare the difference it makes to our prospects. You can do this for some event
you might imagine counterfactually effecting or preventing below""")


# Section 6 - Transitional probabilities from abstract events

def make_on_change_abstract_transition_callback(state_name):
    # Create a function to allow us to pass the state name to the callback
    def callback():
        update_transitions(state_name, 'from abstract state')
    return callback

col1, col2, col3 = st.columns(3, gap="small")

for state, col in zip(all_transitions['from abstract state'][:3], (col1, col2, col3)):
    with col:
        st.slider(
            label=state,
            value=st.session_state[state + " " + 'from abstract state'],
            on_change=make_on_change_abstract_transition_callback(state),
            key=state + " " + 'from abstract state' + "_from_input",
            **common_form_values)

        # st.number_input(
        #     label=state,
        #     value=st.session_state[state],
        #     on_change=make_on_change_abstract_transition_callback(state),
        #     key=state + '_value' + "_from_input",
        #     **common_form_values)

for state, col in zip(all_transitions['from abstract state'][3:], (col1, col2, col3)):
    with col:
        st.slider(
            label=state,
            value=st.session_state[state + " " + 'from abstract state'],
            on_change=make_on_change_abstract_transition_callback(state),
            key=state + " " + 'from abstract state' + "_from_input",
            **common_form_values)

st.write(obelus_string)
# st.slider(
#     label='Interstellar',
#     value=st.session_state['Interstellar/existential security from abstract state'],
#     on_change=make_on_change_abstract_transition_callback('Interstellar/existential security'),
#     key='Interstellar/existential security from abstract state_from_input',
#     **common_form_values)

        # st.number_input(
        #     label=state,
        #     value=st.session_state[state],
        #     on_change=make_on_change_abstract_transition_callback(state),
        #     key=state + '_value' + "_from_input",
        #     **common_form_values)

# st.number_input(label=f'Probability of remaining in current state given event',
#         value=get_remainder_value(abstract_event_remainder),
#         disabled = True,
#         **common_form_values)


array1 = np.array(list(calc.probability_differences().values()))
array2 = np.array([st.session_state[state + " " + 'from abstract state']
                   for state in all_transitions['from abstract state']])
result = np.round(np.dot(array1, array2), 3)

if calc.net_interstellar_from_present_perils():
    result2 = "${0}$ x".format(- np.round(result / calc.net_interstellar_from_present_perils(), 3))
    st.markdown("The expected value of the event is ${0}V$, or {1} "\
            "as bad as extinction".format(result, result2))
else:
    st.markdown("The expected value of the event is ${0}V$".format(result))
