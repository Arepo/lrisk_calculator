import streamlit as st
import plotly.express as px
import numpy as np
import pandas as pd
from calculators.simple_calc.simple_calc import SimpleCalc
st.set_page_config(
        page_title="My Page Title",
)


all_transitions = {
    'from_preindustrial': [
        'Extinction given preindustrial',
        'Industrial given preindustrial'
    ],
    'from_industrial': [
        'Extinction given industrial',
        'Future perils given industrial'
    ],
    'from_present_perils': [
        'Extinction given present perils',
        'Preindustrial given present perils',
        'Industrial given present perils',
        'Future perils given present perils',
        'Multiplanetary given present perils',
        'Interstellar given present perils'
    ],
    'from_future_perils': [
        'Extinction given future perils',
        'Preindustrial given future perils',
        'Industrial given future perils',
        'Multiplanetary given future perils',
        'Interstellar given future perils'
    ],
    'from_multiplanetary': [
        'Extinction given multiplanetary',
        'Preindustrial given multiplanetary',
        'Industrial given multiplanetary',
        'Future perils given multiplanetary',
        'Interstellar given multiplanetary'
    ],
    'from_abstract_state': [
        'Extinction',
        'Preindustrial',
        'Industrial',
        'Remaining in present perils',
        'Future perils',
        'Multiplanetary',
        'Interstellar'
    ]
}

last_listed_transitions = [transitions[-1] for transitions in all_transitions.values()]

# Get a flattened list of all transitions
target_states = [target_state for target_state_list in all_transitions.values() for target_state in target_state_list]

common_form_values = {
    'min_value': 0.0,
    'max_value': 1.0,
    'step': 0.01,
    'format': "%.2f",
}

def update_transitions(transition_name, current_state):
    other_transitions = [transition for transition in all_transitions[current_state] if transition != transition_name][::-1]
    st.session_state[transition_name] = st.session_state[transition_name + '_value']

    # Given the change, determine how much we need to adjust other transitional probabilities to ensure they sum to 1
    excess_probability = sum([st.session_state[transition] for transition in all_transitions[current_state]]) - 1

    for transition in other_transitions:
        # If excess_probability is positive that means we've lowered the value of the transition we're updating, and need to raise another
        if excess_probability > 0 and excess_probability <= st.session_state[transition]:
            # The difference is low enough to be absorbed by this transition, so we're done adjusting sliders
            st.session_state[transition] += -excess_probability
            break
        elif excess_probability > 0:
            # Reduce this transition to 0 and continue to the next
            excess_probability -= st.session_state[transition]
            st.session_state[transition] = .0
    # If excess_probability is negative or 0, we add the difference it to extinction unless it's extinction we modified, then we add it to the next-most regressed state)
    if excess_probability < 0 and transition_name in last_listed_transitions:
        st.session_state[all_transitions[current_state][-2]] -= excess_probability
    elif excess_probability < 0:
        st.session_state[all_transitions[current_state][-1]] -= excess_probability

def get_remainder_value(remainder_function):
    return max(remainder_function(), .0)

for session_value in (target_states):
    if session_value not in st.session_state and session_value in last_listed_transitions:

        st.session_state[session_value] = 1.0
    elif session_value not in st.session_state:
        st.session_state[session_value] = .0



# Make values percentages

# TODO Reword headers as questions. What is the probability of getting to preindustrial from prequilibrium? Eg. what is the probability of getting to industrial from preindustrial?

# TODO Decide how to select starting values? Is the value of making it look intuitive worth the cost of priming?

st.write("""**Adjust the values to see how the probability of human descendants becoming interstellar changes based on your credences.**
         """)

col1, col2 = st.columns(2, gap="large")


# First Section: Industrial given Preindustrial

with col1:
    def make_on_change_preindustrial_callback(transition_name):
        # Create a function to allow us to pass the transition name to the callback
        def callback():
            update_transitions(transition_name, 'from_preindustrial')
        return callback

    for transition in all_transitions['from_preindustrial']:
        st.slider(
            label=transition,
            value=st.session_state[transition],
            on_change=make_on_change_preindustrial_callback(transition),
            key=transition + '_value',
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
    #     key='preindustrial_slider_value',
    #     **common_form_values)

    # st.number_input(label='Industrial (Number) given Preindustrial',
    #                 value=st.session_state['Industrial given preindustrial'],
    #                 on_change=update_preindustrial_from_number,
    #                 key='preindustrial_input_value',
    #                 **common_form_values)

    # st.number_input(label='Extinction (number) given Preindustrial',
    #             value=round(1 - st.session_state['Industrial given preindustrial'], 5),
    #             disabled=True,
    #             **common_form_values)





    # def update_preindustrial():
    #     st.session_state['Industrial given preindustrial'] = round(st.session_state['preindustrial_input_value'], 5)








# Second Section: Future perils given preindustrial

with col2:
    def make_on_change_industrial_callback(transition_name):
        # Create a function to allow us to pass the transition name to the callback
        def callback():
            update_transitions(transition_name, 'from_industrial')
        return callback

    for transition in all_transitions['from_industrial']:
        st.slider(
            label=transition,
            value=st.session_state[transition],
            on_change=make_on_change_industrial_callback(transition),
            key=transition + '_value',
            **common_form_values)

    # st.number_input(
    #     label='Future perils (number) given Industrial',
    #     value=st.session_state['Future perils given industrial'],
    #     on_change=update_perils_from_number,
    #     key='future_perils_num_input_value',
    #     **common_form_values)

    # st.number_input(
    #     label='Extinction (number) given Industrial',
    #     value=round(1 - st.session_state['Future perils given industrial'], 5),
    #     disabled=True,
    #     **common_form_values)


# # Section 3: Transitions from present perils

'---'

st.markdown("""## Transitional probabilities from present perils states
""")

def make_on_change_present_perils_callback(transition_name):
    # Create a function to allow us to pass the transition name to the callback
    def callback():
        update_transitions(transition_name, 'from_present_perils')
    return callback

# for transition in transitions['from_present_perils']:
#     st.number_input(
#         label=transition,
#         value=st.session_state[transition],
#         on_change=make_on_change_present_perils_callback(transition),
#         key=transition + '_value',
#         **common_form_values)

# st.number_input(label=f'Multiplanetary given present perils',
#         value=get_remainder_value(present_perils_remainder),
#         disabled = True,
#         **common_form_values)

for transition in all_transitions['from_present_perils']:
    st.slider(
        label=transition,
        value=st.session_state[transition],
        on_change=make_on_change_present_perils_callback(transition),
        key=transition + '_value',
        **common_form_values)


# Section 4 - Transitional probabilities from future perils states

'---'

st.markdown("""## Transitional probabilities from future perils states
""")

def make_on_change_future_perils_callback(transition_name):
    # Create a function to allow us to pass the transition name to the callback
    def callback():
        update_transitions(transition_name, 'from_future_perils')
    return callback

# for transition in transitions['from_future_perils']:
#     st.number_input(
#         label=transition,
#         value=st.session_state[transition],
#         on_change=make_on_change_future_perils_callback(transition),
#         key=transition + '_value',
#         **common_form_values)

# st.number_input(label=f'Multiplanetary given future perils',
#         value=get_remainder_value(future_perils_remainder),
#         disabled = True,
#         **common_form_values)

for transition in all_transitions['from_future_perils']:
    st.slider(
    label=transition,
    value=st.session_state[transition],
    on_change=make_on_change_future_perils_callback(transition),
    key=transition + '_value',
    **common_form_values)



# Section 5 Transitional probabilities from multiplanetary states

'---'

st.markdown("""## Transitional probabilities from multiplanetary states
""")

def make_on_change_multiplanetary_callback(transition_name):
    # Create a function to allow us to pass the transition name to the callback
    def callback():
        update_transitions(transition_name, 'from_multiplanetary')
    return callback

# for transition in transitions['from_multiplanetary']:
#     st.number_input(
#         label=transition,
#         value=st.session_state[transition],
#         on_change=make_on_change_multiplanetary_callback(transition),
#         key=transition + '_value',
#         **common_form_values)

# st.number_input(label=f'Interstellar given multiplanetary',
#         value=get_remainder_value(multiplanetary_remainder),
#         disabled = True,
#         **common_form_values)

for transition in all_transitions['from_multiplanetary']:
    st.slider(
    label=transition,
    value=st.session_state[transition],
    on_change=make_on_change_multiplanetary_callback(transition),
    key=transition + '_value',
    **common_form_values)

# st.slider(
#     label='Interstellar given multiplanetary',
#     value=get_remainder_value(multiplanetary_remainder),
#     disabled=True,
#     **common_form_values)



all_transition_probabilities = {
    'extinction_given_preindustrial': 1 - st.session_state['Industrial given preindustrial'],
    'extinction_given_industrial': 1 - st.session_state['Future perils given industrial'],

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

probabilties_fig = px.bar(probabilities_df, x='Civilisation state', y='Probability of becoming interstellar')
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
         '''
)

difference_df = pd.DataFrame(calc.probability_differences().items(), columns=['State', 'Value of transitioning to state (as a multiple of V)'])
difference_fig = px.bar(difference_df, x='State', y='Value of transitioning to state (as a multiple of V)')
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

st.markdown("""If you find it more convenient to think of a specific event
rather than a specific transition, you can enter your credences for that event
transitioning us to each state below given its realisation, to see the overall
expected value of that event.""")


# Section 6 - Transitional probabilities from abstract events

def make_on_change_abstract_transition_callback(state_name):
    # Create a function to allow us to pass the state name to the callback
    def callback():
        update_transitions(state_name, 'from_abstract_state')
    return callback

col1, col2, col3 = st.columns(3, gap="small")

for state, col in zip(all_transitions['from_abstract_state'][:3], (col1, col2, col3)):
    with col:
        st.slider(
            label=state,
            value=st.session_state[state],
            on_change=make_on_change_abstract_transition_callback(state),
            key=state + '_value',
            **common_form_values)

        # st.number_input(
        #     label=state,
        #     value=st.session_state[state],
        #     on_change=make_on_change_abstract_transition_callback(state),
        #     key=state + '_value',
        #     **common_form_values)

for state, col in zip(all_transitions['from_abstract_state'][3:], (col1, col2, col3)):
    with col:
        st.slider(
            label=state,
            value=st.session_state[state],
            on_change=make_on_change_abstract_transition_callback(state),
            key=state + '_value',
            **common_form_values)

st.slider(
    label='Interstellar',
    value=st.session_state['Interstellar'],
    on_change=make_on_change_abstract_transition_callback('Interstellar'),
    key='Interstellar' + '_value',
    **common_form_values)

        # st.number_input(
        #     label=state,
        #     value=st.session_state[state],
        #     on_change=make_on_change_abstract_transition_callback(state),
        #     key=state + '_value',
        #     **common_form_values)

# st.number_input(label=f'Probability of remaining in current state given event',
#         value=get_remainder_value(abstract_event_remainder),
#         disabled = True,
#         **common_form_values)


array1 = np.array(list(calc.probability_differences().values()))
array2 = np.array([st.session_state[state] for state in all_transitions['from_abstract_state']])
result = np.round(np.dot(array1, array2), 3)

if calc.net_interstellar_from_present_perils():
    result2 = "${0}$ x".format(- np.round(result / calc.net_interstellar_from_present_perils(), 3))
    st.markdown("The expected value of the event is ${0}V$, or {1} "\
            "as bad as extinction".format(result, result2))
else:
    st.markdown("The expected value of the event is ${0}V$".format(result))
